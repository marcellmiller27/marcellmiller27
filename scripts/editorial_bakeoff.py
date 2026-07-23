#!/usr/bin/env python
# JHI-SIG: 69M2705M | Editorial E2 bake-off / live test-run | JHI Research & Analytics Firm, Inc. (proprietary)
"""Live test-run + bake-off for the E2 grounded-LLM editorial layer.

Runs one edition through the deterministic engine, then elevates it with the
configured LLM (Claude via Anthropic), and prints a before/after with the
fact-lock result + token cost. Requires a VALID ANTHROPIC_API_KEY in the env
(starts with sk-ant-) and ENABLE_LLM_EDITORIAL=1.

Usage (from repo root, backend venv):
    ENABLE_LLM_EDITORIAL=1 EDITORIAL_LLM_MODEL=<sonnet-id> \
      .venv/bin/python scripts/editorial_bakeoff.py economic-brief
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.editorial_llm import elevate_edition, llm_enabled  # noqa: E402
from app.market_services import MarketDataService  # noqa: E402
from app.newsletter_content import NEWSLETTER_SYMBOLS, build_edition  # noqa: E402


def main() -> None:
    slug = sys.argv[1] if len(sys.argv) > 1 else "economic-brief"
    if not llm_enabled():
        print("ENABLE_LLM_EDITORIAL is off — set it to 1 to run the live elevation.")
    quotes = MarketDataService().quotes(NEWSLETTER_SYMBOLS).quotes
    ed = build_edition(slug, quotes, datetime.now(timezone.utc), full=True)
    elevated, meta = elevate_edition(ed)

    print(f"\n=== {ed.title} — {ed.dateline} ===")
    print(f"meta: {meta}\n")
    print("--- Executive read ---")
    print(f"[deterministic] {ed.intro}\n")
    print(f"[elevated]      {elevated.intro}\n")
    for g0, g1 in zip(ed.groups, elevated.groups):
        for i0, i1 in zip(g0.items, g1.items):
            if i0.body and i0.body != i1.body:
                print(f"• {i0.label} ({i0.value})")
                print(f"    det: {i0.body}")
                print(f"    llm: {i1.body}")
    if meta.get("fields_reverted"):
        print(f"\n⚠ {meta['fields_reverted']} field(s) reverted to deterministic (fact-lock).")


if __name__ == "__main__":
    main()
