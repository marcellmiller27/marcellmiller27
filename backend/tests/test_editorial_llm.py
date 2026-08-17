from app.editorial_llm import _bedrock_creds, _valid_key, elevate_edition
from app.newsletter_content import CTA, Edition, EditorLetter, Group, Item, PersonaPath


def test_bedrock_creds_detected(monkeypatch) -> None:
    monkeypatch.setenv("AWS_BEARER_TOKEN_BEDROCK", "ABSKtestvalue123")
    monkeypatch.setenv("AWS_REGION", "us-east-2")
    assert _bedrock_creds() == ("ABSKtestvalue123", "us-east-2")
    monkeypatch.delenv("AWS_BEARER_TOKEN_BEDROCK", raising=False)
    assert _bedrock_creds() is None


def test_anthropic_key_validation(monkeypatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "export ANTHROPIC_API_KEY=oops")  # malformed
    assert _valid_key() is None
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-api03-valid-looking-key")
    assert _valid_key() == "sk-ant-api03-valid-looking-key"


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


def _sample_with_letter() -> Edition:
    ed = _sample()
    ed.editor_letter = EditorLetter(
        greeting="Welcome to The Aegira Monthly.",
        narrative="Policy remains restrictive with inflation at 3.53%, still above the 2% target.",
        questions=["Is the market pricing the last mile of disinflation, or the cut it wants?"],
        philosophy="The edge is a repeatable process, not a prediction.",
        persona_paths=[
            PersonaPath(label="The Core Read", blurb="Stay with the standing macro read.",
                        href="#news-summary"),
            PersonaPath(label="Act on the Signals", blurb="Take the read into the scan.",
                        href="/opportunities", gated=True),
        ],
        cta=CTA(label="Explore Aegira Research", href="/reports"),
    )
    return ed


def test_editor_letter_prose_is_elevated(monkeypatch) -> None:
    monkeypatch.setenv("ENABLE_LLM_EDITORIAL", "1")
    ed = _sample_with_letter()

    def draft(payload):
        # A faithful rephrase (prefix marker) that preserves every figure.
        return {k: "[E] " + v for k, v in payload.items()}, 120, 60

    out, meta = elevate_edition(ed, draft_fn=draft)
    assert meta["used_llm"] is True and meta["fields_reverted"] == 0
    el = out.editor_letter
    # Prose fields are elevated ...
    assert el.narrative.startswith("[E] ")
    assert el.questions[0].startswith("[E] ")
    assert el.persona_paths[0].blurb.startswith("[E] ")
    assert el.philosophy.startswith("[E] ")
    # ... figures preserved, and structural brand/nav fields are NEVER sent/changed.
    assert "3.53%" in el.narrative
    assert el.greeting == "Welcome to The Aegira Monthly."
    assert el.persona_paths[0].label == "The Core Read"
    assert el.persona_paths[1].href == "/opportunities" and el.persona_paths[1].gated is True
    assert el.cta == ed.editor_letter.cta


def test_editor_letter_factlock_reverts_injected_number(monkeypatch) -> None:
    monkeypatch.setenv("ENABLE_LLM_EDITORIAL", "1")
    ed = _sample_with_letter()

    def draft(payload):
        return {k: v + " We target 99 by year-end." for k, v in payload.items()}, 100, 60

    out, meta = elevate_edition(ed, draft_fn=draft)
    assert meta["used_llm"] is True and meta["fields_reverted"] >= 1
    el = out.editor_letter
    assert "99" not in el.narrative
    assert el.narrative == ed.editor_letter.narrative  # fell back to deterministic
    assert "99" not in el.questions[0]


def test_editor_letter_flag_off_is_unchanged(monkeypatch) -> None:
    monkeypatch.delenv("ENABLE_LLM_EDITORIAL", raising=False)
    ed = _sample_with_letter()
    out, meta = elevate_edition(ed, draft_fn=lambda p: ({}, 0, 0))
    assert out is ed and meta["used_llm"] is False
    assert out.editor_letter is ed.editor_letter
