#!/usr/bin/env python3
"""Generate the AI-agent operating-cost schedule (cost centers, NOT payroll).

Each agent is a cost center; the figures are the real run cost (LLM/API + compute +
tooling allocation), booked to account 5400 'AI Agents & Automation Expense'.
These are NOT salaries/wages. Pure standard library.
Run: python3 docs/ops/generate_agent_costs.py
"""

from __future__ import annotations

import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# Illustrative monthly run cost per agent at MVP volume (edit with real usage).
# Columns: agent, role, llm_api, compute_share, tooling_share  (USD/month)
AGENTS = [
    ("Ava (onboarding)", "Onboarding Concierge", 12, 5, 8),
    ("Max (billing)", "Subscriptions & Billing", 10, 5, 5),
    ("Sage (security)", "Account & Security", 8, 5, 5),
    ("Quinn (product)", "Product & Markets Guide", 14, 5, 6),
    ("Tess (technical)", "Technical Support & Triage", 18, 6, 6),
]
# Human fully-loaded equivalent (for savings context only) — see cost analysis.
HUMAN_LOADED_MONTHLY = 4800


def main() -> None:
    rows = []
    total = 0
    for agent, role, llm, compute, tooling in AGENTS:
        monthly = llm + compute + tooling
        total += monthly
        rows.append(
            {
                "agent": agent,
                "role": role,
                "llm_api_usd": llm,
                "compute_share_usd": compute,
                "tooling_share_usd": tooling,
                "monthly_operating_cost_usd": monthly,
                "annual_operating_cost_usd": monthly * 12,
                "human_loaded_equivalent_usd_mo": HUMAN_LOADED_MONTHLY,
                "monthly_savings_vs_human_usd": HUMAN_LOADED_MONTHLY - monthly,
            }
        )
    path = os.path.join(HERE, "agent_operating_costs.csv")
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(
        f"5 AI agents total operating cost ~${total}/mo (~${total*12}/yr). "
        f"Wrote {path}. NOTE: operating cost, not payroll."
    )


if __name__ == "__main__":
    main()
