# JHI-SIG: 69M2705M | Editorial RAG tests (mocked; no live AWS) | JHI Research & Analytics Firm, Inc. (proprietary)
"""Unit tests for the flag-gated Bedrock Knowledge Base retrieval layer.

All tests are network-free: the Bedrock ``Retrieve`` call is either injected as a mock
``retrieve_fn`` or exercised via a monkeypatched ``boto3.client``. They assert the
graceful no-op contract (safe to merge before AWS exists) and the fact-locked grounding
path in ``editorial_llm``.
"""

from __future__ import annotations

import sys
import types

from app import editorial_rag
from app.editorial_llm import elevate_edition
from app.editorial_rag import Citation, grounding_block, rag_enabled, retrieve
from app.newsletter_content import Edition, Group, Item

# A canned Bedrock ``retrievalResults`` payload (shape mirrors the real API).
_CANNED = [
    {
        "content": {"text": "In prior tightening cycles, positive real yields compressed "
                            "long-duration equity multiples."},
        "location": {"type": "S3", "s3Location": {"uri": "s3://aegira-research/real-rates.md"}},
        "score": 0.82,
    },
    {
        "content": {"text": "Gold has historically served as a fiscal-risk hedge even with "
                            "positive real rates."},
        "location": {"type": "S3", "s3Location": {"uri": "s3://aegira-research/gold.md"}},
        "score": 0.71,
    },
]


def _sample_edition() -> Edition:
    return Edition(
        slug="insider-briefs", title="Insider Brief — The Real Cost of Capital",
        eyebrow="Insider Briefs", dateline="Edition of Saturday, August 8, 2026",
        intro="Positive real rates reset the price of every asset.",
        groups=[Group(heading="Why it matters", blurb="The mechanism.",
                      items=[Item(label="Real 10Y", value="1.13%", body="The after-inflation hurdle.")])],
        footer="f", disclaimer="d", methodology="m",
    )


def test_rag_disabled_by_default(monkeypatch) -> None:
    monkeypatch.delenv("ENABLE_EDITORIAL_RAG", raising=False)
    monkeypatch.delenv("BEDROCK_KB_ID", raising=False)
    assert rag_enabled() is False
    # Graceful no-op: retrieve returns [] without touching AWS.
    assert retrieve("anything") == []


def test_rag_requires_both_flag_and_kb_id(monkeypatch) -> None:
    monkeypatch.setenv("ENABLE_EDITORIAL_RAG", "1")
    monkeypatch.delenv("BEDROCK_KB_ID", raising=False)
    assert rag_enabled() is False  # flag alone is not enough
    monkeypatch.setenv("BEDROCK_KB_ID", "KB123456")
    assert rag_enabled() is True
    monkeypatch.setenv("ENABLE_EDITORIAL_RAG", "0")
    assert rag_enabled() is False  # kb id alone is not enough


def test_retrieve_parses_results_from_injected_fn() -> None:
    cites = retrieve("real rates", retrieve_fn=lambda q, k: _CANNED)
    assert len(cites) == 2
    assert cites[0].source == "s3://aegira-research/real-rates.md"
    assert cites[0].score == 0.82
    assert "real yields" in cites[0].text


def test_retrieve_swallows_errors() -> None:
    def boom(_q, _k):
        raise RuntimeError("bedrock unavailable")

    # Never raises: a retrieval failure degrades to no grounding.
    assert retrieve("x", retrieve_fn=boom) == []


def test_retrieve_skips_empty_and_missing_content() -> None:
    messy = [
        {"content": {"text": ""}, "location": {}},
        {"content": {"text": "kept passage"}, "location": {"webLocation": {"url": "https://x/y"}},
         "score": 0.5},
    ]
    cites = retrieve("q", retrieve_fn=lambda q, k: messy)
    assert len(cites) == 1
    assert cites[0].source == "https://x/y"


def test_default_retrieve_uses_boto3(monkeypatch) -> None:
    # Exercise the boto3 path without live AWS by injecting a fake boto3 module.
    monkeypatch.setenv("ENABLE_EDITORIAL_RAG", "1")
    monkeypatch.setenv("BEDROCK_KB_ID", "KB999")
    monkeypatch.setenv("BEDROCK_KB_REGION", "us-east-1")

    calls: dict = {}

    class _FakeClient:
        def retrieve(self, **kwargs):
            calls.update(kwargs)
            return {"retrievalResults": _CANNED}

    fake_boto3 = types.ModuleType("boto3")
    fake_boto3.client = lambda service, region_name=None: _FakeClient()  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "boto3", fake_boto3)

    cites = editorial_rag._default_retrieve("real rates", 4)
    assert len(cites) == 2
    assert calls["knowledgeBaseId"] == "KB999"
    assert calls["retrievalQuery"] == {"text": "real rates"}
    assert calls["retrievalConfiguration"]["vectorSearchConfiguration"]["numberOfResults"] == 4


def test_grounding_block_shape() -> None:
    assert grounding_block([]) == ""
    block = grounding_block([Citation(text="a passage", source="s3://x")])
    assert "GROUNDING CONTEXT" in block
    assert "do NOT copy any number" in block
    assert "s3://x" in block


def test_elevate_edition_records_rag_off_when_disabled(monkeypatch) -> None:
    monkeypatch.setenv("ENABLE_LLM_EDITORIAL", "1")
    monkeypatch.delenv("ENABLE_EDITORIAL_RAG", raising=False)
    ed = _sample_edition()
    _out, meta = elevate_edition(ed, draft_fn=lambda p: (dict(p), 10, 5))
    assert meta["used_llm"] is True
    assert meta["rag"] == {"enabled": False, "citations": []}


def test_elevate_edition_grounds_when_rag_enabled(monkeypatch) -> None:
    monkeypatch.setenv("ENABLE_LLM_EDITORIAL", "1")
    monkeypatch.setenv("ENABLE_EDITORIAL_RAG", "1")
    monkeypatch.setenv("BEDROCK_KB_ID", "KB123")
    # Avoid live AWS: the default retriever is monkeypatched to the canned payload.
    monkeypatch.setattr(editorial_rag, "_default_retrieve", lambda q, k: _CANNED)

    def draft(payload):
        # A faithful echo (fact-lock safe); records nothing new.
        return dict(payload), 20, 10

    ed = _sample_edition()
    out, meta = elevate_edition(ed, draft_fn=draft)
    assert meta["used_llm"] is True
    assert meta["rag"]["enabled"] is True
    assert len(meta["rag"]["citations"]) == 2
    assert meta["rag"]["citations"][0]["source"] == "s3://aegira-research/real-rates.md"
    # Fact-lock unaffected: the deterministic figure is preserved.
    assert "1.13%" in out.groups[0].items[0].body
