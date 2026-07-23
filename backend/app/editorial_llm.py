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
    "You are Ellery Vance, VP of Editorial (AI) for JHI Research & Analytics Firm, Inc. "
    "Rewrite each provided passage into polished, measured, Ivy-league institutional prose for "
    "allocators, acquirers, and advisors. STRICT RULES: (1) Do NOT add, remove, or change any "
    "number, percentage, ticker symbol, or date. (2) Introduce NO new facts or figures — only "
    "rephrase what is given. (3) No investment advice; this is an independent professional read. "
    "(4) Keep each passage concise and roughly the same length. Return ONLY a JSON object mapping "
    "each input id to its rewritten passage — no preamble, no code fence."
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
    return allowed


def _collect_prose(edition: Edition) -> dict[str, str]:
    """Only prose fields are eligible for rephrasing — never numeric/value fields."""
    prose: dict[str, str] = {}
    if edition.intro:
        prose["intro"] = edition.intro
    for gi, g in enumerate(edition.groups):
        if g.blurb:
            prose[f"g{gi}.blurb"] = g.blurb
        for ii, it in enumerate(g.items):
            if it.body:
                prose[f"g{gi}.i{ii}.body"] = it.body
    return prose


def _real_draft(payload: dict[str, str], model: str, key: str) -> tuple[dict[str, str], int, int]:
    import anthropic

    client = anthropic.Anthropic(api_key=key)
    msg = client.messages.create(
        model=model,
        max_tokens=MAX_OUTPUT_TOKENS,
        system=_SYSTEM,
        messages=[{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
    )
    text = "".join(getattr(b, "text", "") for b in msg.content).strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text[text.find("{") : text.rfind("}") + 1]
    data = json.loads(text)
    usage = getattr(msg, "usage", None)
    in_tok = getattr(usage, "input_tokens", 0) or 0
    out_tok = getattr(usage, "output_tokens", 0) or 0
    return {str(k): str(v) for k, v in data.items()}, in_tok, out_tok


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
    return replace(edition, intro=new_intro, groups=new_groups), reverted


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


def elevate_edition(edition: Edition, db=None, draft_fn: DraftFn | None = None) -> tuple[Edition, dict]:
    """Return (possibly-elevated edition, meta). Never raises; falls back to deterministic."""
    meta: dict = {"used_llm": False, "reason": "disabled", "model": None, "fields_reverted": 0}
    if not llm_enabled():
        return edition, meta

    model = DEFAULT_MODEL
    period = datetime.now(timezone.utc).strftime("%Y-%m")

    if draft_fn is None:
        key = _valid_key()
        if key is None:
            meta["reason"] = "invalid_or_missing_api_key"
            return edition, meta
        draft_fn = lambda p: _real_draft(p, model, key)  # noqa: E731

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
