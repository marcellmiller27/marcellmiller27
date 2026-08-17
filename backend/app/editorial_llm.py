# JHI-SIG: 69M2705M | Editorial E2 — grounded (fact-locked) LLM drafting | JHI Research & Analytics Firm, Inc. (proprietary)
"""E2 of the editorial roadmap: elevate the deterministic edition's *prose* with an LLM
(Claude via Anthropic; Bedrock later) while the deterministic engine remains the sole
source of every figure.

Guardrails (defense in depth):
- **Flag-gated:** off unless ENABLE_LLM_EDITORIAL is truthy.
- **Structural fact-lock:** only prose fields (intro, group blurbs, item bodies) are sent
  for rephrasing; numeric fields (`value`, tickers, tags) are NEVER sent and are rendered
  verbatim from the engine.
- **Numeric fact-lock:** any rephrased passage that introduces a number not present in the
  engine's output is rejected and that field falls back to the deterministic text.
- **Budget cap:** monthly USD cap (LLMUsageDB ledger); over cap → deterministic fallback.
- **Fail-safe:** any error/misconfig → deterministic edition unchanged.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import replace
from datetime import datetime, timezone
from typing import Callable

from app.newsletter_content import Edition, Group, Item

# Default model id is intentionally overridable — set EDITORIAL_LLM_MODEL to the exact
# Claude Sonnet id confirmed from `client.models.list()` (e.g. the Sonnet 5 id on your account).
DEFAULT_MODEL = os.getenv("EDITORIAL_LLM_MODEL", "claude-sonnet-4-5")
DEFAULT_MONTHLY_BUDGET_USD = float(os.getenv("EDITORIAL_LLM_MONTHLY_BUDGET_USD", "250"))
# Rough price per 1M tokens (USD); override per model/account at contract time.
PRICE_IN = float(os.getenv("EDITORIAL_LLM_PRICE_IN", "3.0"))
PRICE_OUT = float(os.getenv("EDITORIAL_LLM_PRICE_OUT", "15.0"))
MAX_OUTPUT_TOKENS = int(os.getenv("EDITORIAL_LLM_MAX_TOKENS", "1500"))

_SYSTEM = (
    "You are Ellery Vance, VP of Editorial (AI) for Aegira. You write the analytical "
    "research-essay voice of an institutional desk: a macro-to-micro narrative that does not "
    "merely state levels but EXPLAINS THE MECHANISM — how the cost of capital transmits through "
    "policy, rates, and inflation into cash flows, valuations, and positioning. Rewrite each "
    "provided passage into polished, measured, Ivy-league prose for allocators, acquirers, and "
    "advisors: connect cause to effect, name the transmission channel, and keep the through-line "
    "of an argument across passages. "
    "STRICT RULES (fact-lock — non-negotiable): (1) Do NOT add, remove, or change any number, "
    "percentage, ticker symbol, or date. (2) Introduce NO new facts, figures, forecasts, price "
    "targets, or named securities beyond what each passage already contains — only rephrase and "
    "sharpen the reasoning already present. (3) No investment advice; this is an independent "
    "professional read, not a recommendation. (4) Preserve each passage's meaning and keep it "
    "roughly the same length (essay cadence, not padding). Return ONLY a JSON object mapping each "
    "input id to its rewritten passage — no preamble, no code fence."
)

DraftFn = Callable[[dict[str, str]], tuple[dict[str, str], int, int]]
"""A drafting function: {id: text} -> ({id: rewritten}, input_tokens, output_tokens)."""

_NUM_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")


def llm_enabled() -> bool:
    return os.getenv("ENABLE_LLM_EDITORIAL", "0").strip().lower() in ("1", "true", "yes", "on")


def _valid_key() -> str | None:
    key = os.getenv("ANTHROPIC_API_KEY", "")
    # Reject an obviously malformed value (e.g. a pasted `export NAME=...` line).
    if not key or " " in key.strip() or not key.startswith("sk-ant-"):
        return None
    return key


def _bedrock_model() -> str:
    """A Bedrock model / inference-profile id. If EDITORIAL_LLM_MODEL isn't a Bedrock-style
    id (e.g. the Anthropic-direct default), fall back to an accessible Sonnet profile."""
    m = os.getenv("EDITORIAL_LLM_MODEL", "").strip()
    if m and any(m.startswith(p) for p in ("us.", "global.", "anthropic.")):
        return m
    return "us.anthropic.claude-sonnet-4-5-20250929-v1:0"


def _bedrock_creds() -> tuple[str, str] | None:
    """Amazon Bedrock long-term API key (bearer token) + region, if configured.

    AWS shows the value once at generation and hands you `AWS_BEARER_TOKEN_BEDROCK`.
    We call the Bedrock runtime endpoint directly with it (no boto3 / SigV4 needed)."""
    token = os.getenv("AWS_BEARER_TOKEN_BEDROCK", "").strip()
    if not token or " " in token:
        return None
    region = os.getenv("AWS_REGION", "").strip() or "us-east-2"
    return token, region


def _numbers(text: str | None) -> set[str]:
    if not text:
        return set()
    return {m.replace(",", "") for m in _NUM_RE.findall(text)}


def _allowed_numbers(edition: Edition) -> set[str]:
    """Every number the engine legitimately shows — the whitelist for rephrased prose."""
    allowed: set[str] = set()
    allowed |= _numbers(edition.intro)
    allowed |= _numbers(edition.dateline)
    for g in edition.groups:
        allowed |= _numbers(g.blurb)
        for it in g.items:
            allowed |= _numbers(it.label) | _numbers(it.value) | _numbers(it.body)
    # The editor's letter (lede) is assembled deterministically from the same engine data,
    # so its numbers are engine-produced and belong on the whitelist too.
    el = getattr(edition, "editor_letter", None)
    if el is not None:
        allowed |= _numbers(el.greeting) | _numbers(el.narrative) | _numbers(el.philosophy)
        for q in el.questions:
            allowed |= _numbers(q)
        for p in el.persona_paths:
            allowed |= _numbers(p.blurb)
    return allowed


def _collect_prose(edition: Edition) -> dict[str, str]:
    """Only prose fields are eligible for rephrasing — never numeric/value fields.

    Includes the editor's-letter prose (narrative, teaser questions, philosophy, persona
    blurbs) so the lede is elevated in Ellery's voice. Structural fields — the greeting, the
    persona labels/hrefs, and the CTA — are NEVER sent (they are fixed brand/navigation)."""
    prose: dict[str, str] = {}
    if edition.intro:
        prose["intro"] = edition.intro
    for gi, g in enumerate(edition.groups):
        if g.blurb:
            prose[f"g{gi}.blurb"] = g.blurb
        for ii, it in enumerate(g.items):
            if it.body:
                prose[f"g{gi}.i{ii}.body"] = it.body
    el = getattr(edition, "editor_letter", None)
    if el is not None:
        if el.narrative:
            prose["el.narrative"] = el.narrative
        if el.philosophy:
            prose["el.philosophy"] = el.philosophy
        for qi, q in enumerate(el.questions):
            if q:
                prose[f"el.q{qi}"] = q
        for pi, p in enumerate(el.persona_paths):
            if p.blurb:
                prose[f"el.p{pi}.blurb"] = p.blurb
    return prose


def _parse_json_object(text: str) -> dict[str, str]:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text[text.find("{") : text.rfind("}") + 1]
    return {str(k): str(v) for k, v in json.loads(text).items()}


def _anthropic_draft(payload: dict[str, str], model: str, key: str,
                     system: str = _SYSTEM) -> tuple[dict[str, str], int, int]:
    import anthropic

    client = anthropic.Anthropic(api_key=key)
    msg = client.messages.create(
        model=model,
        max_tokens=MAX_OUTPUT_TOKENS,
        system=system,
        messages=[{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
    )
    text = "".join(getattr(b, "text", "") for b in msg.content)
    usage = getattr(msg, "usage", None)
    in_tok = getattr(usage, "input_tokens", 0) or 0
    out_tok = getattr(usage, "output_tokens", 0) or 0
    return _parse_json_object(text), in_tok, out_tok


def _bedrock_draft(
    payload: dict[str, str], model: str, token: str, region: str, system: str = _SYSTEM
) -> tuple[dict[str, str], int, int]:
    """Call Claude on Amazon Bedrock via the runtime endpoint using the bearer API key.

    `model` is the Bedrock model / inference-profile id (e.g. us.anthropic.claude-...).
    """
    import httpx

    url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model}/invoke"
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": MAX_OUTPUT_TOKENS,
        "system": system,
        "messages": [{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
    }
    resp = httpx.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        json=body,
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    text = "".join(b.get("text", "") for b in data.get("content", []))
    usage = data.get("usage", {})
    return _parse_json_object(text), usage.get("input_tokens", 0), usage.get("output_tokens", 0)


def _apply(edition: Edition, elevated: dict[str, str], allowed: set[str]) -> tuple[Edition, int]:
    """Apply rephrased prose, reverting any field that introduces a disallowed number."""
    reverted = 0

    def keep(field_id: str, original: str) -> str:
        nonlocal reverted
        new = elevated.get(field_id)
        if not new:
            return original
        if _numbers(new) - allowed:  # a number not in the engine's whitelist
            reverted += 1
            return original
        return new

    new_intro = keep("intro", edition.intro) if edition.intro else edition.intro
    new_groups: list[Group] = []
    for gi, g in enumerate(edition.groups):
        new_blurb = keep(f"g{gi}.blurb", g.blurb) if g.blurb else g.blurb
        new_items: list[Item] = []
        for ii, it in enumerate(g.items):
            new_body = keep(f"g{gi}.i{ii}.body", it.body) if it.body else it.body
            new_items.append(replace(it, body=new_body))
        new_groups.append(replace(g, blurb=new_blurb, items=new_items))

    new_letter = edition.editor_letter
    if new_letter is not None:
        el = new_letter
        new_questions = [keep(f"el.q{qi}", q) if q else q for qi, q in enumerate(el.questions)]
        new_paths = [
            replace(p, blurb=keep(f"el.p{pi}.blurb", p.blurb) if p.blurb else p.blurb)
            for pi, p in enumerate(el.persona_paths)
        ]
        new_letter = replace(
            el,
            narrative=keep("el.narrative", el.narrative) if el.narrative else el.narrative,
            philosophy=keep("el.philosophy", el.philosophy) if el.philosophy else el.philosophy,
            questions=new_questions,
            persona_paths=new_paths,
        )
    return replace(edition, intro=new_intro, groups=new_groups,
                   editor_letter=new_letter), reverted


def _month_spend(db, period: str) -> float:
    from sqlalchemy import select

    from app.db_models import LLMUsageDB

    rows = db.scalars(select(LLMUsageDB.cost_usd).where(LLMUsageDB.period == period)).all()
    return float(sum(rows))


def _record(db, period: str, model: str, in_tok: int, out_tok: int, cost: float) -> None:
    from app.db_models import LLMUsageDB

    db.add(
        LLMUsageDB(
            period=period, feature="editorial", model=model,
            input_tokens=in_tok, output_tokens=out_tok, cost_usd=cost,
        )
    )
    db.commit()


def _rag_query(edition: Edition) -> str:
    """Build a compact retrieval query from the edition's title/intro/section headings.

    Prose only — no figures needed for semantic retrieval — so the query never leaks a
    licensed row and the retrieved context is used purely to sharpen reasoning."""
    parts = [edition.title, edition.eyebrow]
    if edition.intro:
        parts.append(edition.intro[:400])
    parts.extend(g.heading for g in edition.groups[:4])
    return " ".join(p for p in parts if p)


def _rag_grounding(edition: Edition) -> tuple[str | None, list[dict]]:
    """Retrieve cited grounding passages (flag-gated, graceful no-op).

    Returns (grounded_system_prompt_or_None, serializable_citations). When RAG is off
    or nothing is retrieved, returns (None, []) and the E2 path is unchanged."""
    from app import editorial_rag

    if not editorial_rag.rag_enabled():
        return None, []
    citations = editorial_rag.retrieve(_rag_query(edition))
    block = editorial_rag.grounding_block(citations)
    if not block:
        return None, []
    return f"{_SYSTEM}\n\n{block}", editorial_rag.citation_meta(citations)


def elevate_edition(edition: Edition, db=None, draft_fn: DraftFn | None = None) -> tuple[Edition, dict]:
    """Return (possibly-elevated edition, meta). Never raises; falls back to deterministic."""
    meta: dict = {"used_llm": False, "reason": "disabled", "model": None, "fields_reverted": 0}
    if not llm_enabled():
        return edition, meta

    model = DEFAULT_MODEL
    period = datetime.now(timezone.utc).strftime("%Y-%m")

    # Editorial RAG (flag-gated): retrieve cited grounding passages to ground the essay.
    # Graceful no-op until AWS is provisioned → E2/deterministic behavior is unchanged.
    grounded_system, rag_citations = _rag_grounding(edition)
    meta["rag"] = {"enabled": bool(grounded_system), "citations": rag_citations}
    system = grounded_system or _SYSTEM

    if draft_fn is None:
        bedrock = _bedrock_creds()
        if bedrock is not None:
            token, region = bedrock
            model = _bedrock_model()  # ensure a Bedrock model/inference-profile id
            meta["provider"] = "bedrock"
            draft_fn = lambda p: _bedrock_draft(p, model, token, region, system=system)  # noqa: E731
        else:
            key = _valid_key()
            if key is None:
                meta["reason"] = "invalid_or_missing_api_key"
                return edition, meta
            meta["provider"] = "anthropic"
            draft_fn = lambda p: _anthropic_draft(p, model, key, system=system)  # noqa: E731

    if db is not None and _month_spend(db, period) >= DEFAULT_MONTHLY_BUDGET_USD:
        meta["reason"] = "budget_exceeded"
        return edition, meta

    try:
        prose = _collect_prose(edition)
        if not prose:
            meta["reason"] = "nothing_to_elevate"
            return edition, meta
        elevated, in_tok, out_tok = draft_fn(prose)
        allowed = _allowed_numbers(edition)
        new_edition, reverted = _apply(edition, elevated, allowed)
        cost = in_tok / 1_000_000 * PRICE_IN + out_tok / 1_000_000 * PRICE_OUT
        if db is not None:
            _record(db, period, model, in_tok, out_tok, cost)
        meta.update(
            used_llm=True, reason="ok", model=model, fields_reverted=reverted,
            input_tokens=in_tok, output_tokens=out_tok, cost_usd=round(cost, 6),
        )
        return new_edition, meta
    except Exception as exc:  # fail-safe: never break the newsletter
        meta["reason"] = f"error:{type(exc).__name__}"
        return edition, meta
