from app.editorial_llm import elevate_edition
from app.newsletter_content import Edition, Group, Item


def _sample() -> Edition:
    return Edition(
        slug="economic-brief",
        title="The Economic Brief",
        eyebrow="Economic Tracking",
        dateline="Edition of Thursday, July 23, 2026",
        intro="Policy remains restrictive with inflation at 3.53%, still above the 2% target.",
        groups=[
            Group(
                heading="Inflation",
                blurb="The pace of price growth relative to the 2% objective.",
                items=[Item(label="US CPI", value="3.53%", body="Running above the 2% target.")],
            )
        ],
        footer="Sourced from public data.",
        disclaimer="Not investment advice.",
        methodology="Deterministic from public feeds.",
    )


def test_flag_off_returns_deterministic(monkeypatch) -> None:
    monkeypatch.delenv("ENABLE_LLM_EDITORIAL", raising=False)
    ed = _sample()
    out, meta = elevate_edition(ed, draft_fn=lambda p: ({}, 0, 0))
    assert out is ed
    assert meta["used_llm"] is False and meta["reason"] == "disabled"


def test_clean_rephrase_is_applied(monkeypatch) -> None:
    monkeypatch.setenv("ENABLE_LLM_EDITORIAL", "1")
    ed = _sample()

    def draft(payload):
        # A faithful rephrase that preserves every figure (3.53%, 2%).
        out = {
            k: v.replace("Policy remains restrictive", "The policy stance stays restrictive")
                .replace("Running above", "It runs above")
            for k, v in payload.items()
        }
        return out, 100, 50

    out, meta = elevate_edition(ed, draft_fn=draft)
    assert meta["used_llm"] is True and meta["reason"] == "ok"
    assert meta["fields_reverted"] == 0
    assert "The policy stance stays restrictive" in out.intro
    # Figures preserved.
    assert "3.53%" in out.intro


def test_factlock_reverts_injected_number(monkeypatch) -> None:
    monkeypatch.setenv("ENABLE_LLM_EDITORIAL", "1")
    ed = _sample()

    def draft(payload):
        # Malicious/hallucinated: injects a number (99) not in the engine's output.
        return {k: v + " Our proprietary model targets 99 by year-end." for k, v in payload.items()}, 100, 60

    out, meta = elevate_edition(ed, draft_fn=draft)
    assert meta["used_llm"] is True
    assert meta["fields_reverted"] >= 1
    # The invented number must NOT appear — reverted to deterministic text.
    assert "99" not in out.intro
    assert out.intro == ed.intro  # this field fell back
