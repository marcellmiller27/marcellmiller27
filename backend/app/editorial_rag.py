# JHI-SIG: 69M2705M | Editorial RAG (Bedrock Knowledge Base retrieval) — flag-gated | JHI Research & Analytics Firm, Inc. (proprietary)
"""Editorial RAG scaffolding: ground Ellery's research-essay in cited historical /
context passages retrieved from an **Amazon Bedrock Knowledge Base**.

This is a *scaffold* — it is entirely flag-gated and is a **graceful no-op** until AWS
is provisioned, so it is safe to merge before any AWS setup exists:

- OFF unless ``ENABLE_EDITORIAL_RAG`` is truthy AND ``BEDROCK_KB_ID`` is set (+ a region
  from ``BEDROCK_KB_REGION`` / ``AWS_REGION``). Missing config → ``retrieve()`` returns
  ``[]`` and the E2/deterministic path is unchanged.
- When configured, it calls the Bedrock Agent Runtime ``Retrieve`` API (semantic search
  over the KB's vector index) and returns cited passages.

Fact-lock is preserved end to end: retrieved passages are injected only as *read-only
grounding context* in the prompt. The deterministic engine remains the sole source of
every figure, and ``editorial_llm._apply`` still reverts any output that introduces a
number outside the engine's whitelist. Retrieved passages are used to sharpen reasoning
and are surfaced to the reader **as citations**, never as new figures.

Activation runbook: ``docs/NEWSLETTER_RAG_ACTIVATION.md``.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any, Callable

logger = logging.getLogger(__name__)

DEFAULT_TOP_K = int(os.getenv("EDITORIAL_RAG_TOP_K", "4"))

# A retrieval function: (query, top_k) -> raw Bedrock ``retrievalResults`` list.
RetrieveFn = Callable[[str, int], list[dict[str, Any]]]


@dataclass
class Citation:
    """One retrieved, cited grounding passage (safe to surface to the reader)."""

    text: str
    source: str | None = None      # e.g. an S3 URI or document title
    score: float | None = None

    def short(self, limit: int = 280) -> str:
        t = " ".join(self.text.split())
        return t if len(t) <= limit else t[: limit - 1].rstrip() + "…"


def rag_enabled() -> bool:
    """True only when the RAG flag is on AND a Knowledge Base id is configured."""
    flag = os.getenv("ENABLE_EDITORIAL_RAG", "0").strip().lower() in ("1", "true", "yes", "on")
    return flag and bool(_kb_id())


def _kb_id() -> str | None:
    kb = os.getenv("BEDROCK_KB_ID", "").strip()
    return kb or None


def _region() -> str:
    return (os.getenv("BEDROCK_KB_REGION", "").strip()
            or os.getenv("AWS_REGION", "").strip()
            or "us-east-1")


def rag_config() -> tuple[str, str] | None:
    """(knowledge_base_id, region) when fully configured, else None."""
    kb = _kb_id()
    if not kb:
        return None
    return kb, _region()


def _default_retrieve(query: str, top_k: int) -> list[dict[str, Any]]:
    """Call the Bedrock Agent Runtime ``Retrieve`` API via boto3 (SigV4).

    Isolated so tests inject a mock and never touch AWS. Raises on any AWS/boto issue;
    the public ``retrieve`` wrapper catches and degrades to ``[]``."""
    import boto3  # local import: only needed when RAG is actually active

    cfg = rag_config()
    if cfg is None:
        return []
    kb_id, region = cfg
    client = boto3.client("bedrock-agent-runtime", region_name=region)
    resp = client.retrieve(
        knowledgeBaseId=kb_id,
        retrievalQuery={"text": query},
        retrievalConfiguration={
            "vectorSearchConfiguration": {"numberOfResults": top_k}
        },
    )
    return resp.get("retrievalResults", []) or []


def _parse_results(results: list[dict[str, Any]]) -> list[Citation]:
    """Map raw Bedrock ``retrievalResults`` into Citation objects (defensive)."""
    citations: list[Citation] = []
    for r in results:
        content = r.get("content") or {}
        text = (content.get("text") or "").strip()
        if not text:
            continue
        location = r.get("location") or {}
        source: str | None = None
        # Bedrock returns a typed location (s3Location / webLocation / ...).
        for key in ("s3Location", "webLocation", "confluenceLocation",
                    "salesforceLocation", "sharePointLocation"):
            loc = location.get(key)
            if isinstance(loc, dict):
                source = loc.get("uri") or loc.get("url")
                if source:
                    break
        score = r.get("score")
        citations.append(Citation(
            text=text,
            source=source,
            score=float(score) if isinstance(score, (int, float)) else None,
        ))
    return citations


def retrieve(query: str, top_k: int = DEFAULT_TOP_K,
             retrieve_fn: RetrieveFn | None = None) -> list[Citation]:
    """Retrieve grounding passages for ``query``. Graceful no-op when RAG is not active.

    Never raises: any misconfiguration or AWS error degrades to ``[]`` so the editorial
    path (E2 or deterministic) is entirely unaffected. Pass ``retrieve_fn`` in tests to
    avoid live AWS."""
    fn = retrieve_fn or _default_retrieve
    if retrieve_fn is None and not rag_enabled():
        return []
    if not query or not query.strip():
        return []
    try:
        raw = fn(query.strip(), max(1, top_k))
    except Exception as exc:  # noqa: BLE001 - RAG must never break the newsletter
        logger.info("editorial_rag: retrieval unavailable (%s); continuing without RAG", exc)
        return []
    return _parse_results(raw)


def grounding_block(citations: list[Citation]) -> str:
    """A read-only GROUNDING CONTEXT block for the LLM prompt (never a source of figures).

    Explicitly instructs the model to treat the passages as background only and to obey
    the fact-lock — reinforcing the guardrail defense-in-depth."""
    if not citations:
        return ""
    lines = [
        "GROUNDING CONTEXT (read-only, for reasoning and continuity only — do NOT copy any "
        "number, figure, or claim from it into the output; the engine remains the sole source "
        "of every figure):",
    ]
    for i, c in enumerate(citations, 1):
        tag = f" [source: {c.source}]" if c.source else ""
        lines.append(f"({i}) {c.short()}{tag}")
    return "\n".join(lines)


def citation_meta(citations: list[Citation]) -> list[dict[str, Any]]:
    """Serializable citation list for the edition/editorial meta (shown to the reader)."""
    return [
        {"text": c.short(), "source": c.source, "score": c.score}
        for c in citations
    ]
