# AI Agent "Onboarding" & Cost Accounting (Operating Cost, NOT Payroll)

How we account for the cost of the five AI customer-service agents' jobs.

> **Disclosure / concern (important):** AI agents are **software, not employees.** We do
> **not** record salaries, wages, W‑2s, payroll taxes, benefits, or workers' comp for
> them — doing so would **misstate the books** and, if deducted on a tax return as
> wages, create a **compliance/fraud risk**. Instead we account for the agents'
> **real run cost** as an **AI/automation operating expense**, with each agent as a
> **cost center**. This accurately captures "the cost of employment for their specific
> jobs" while keeping the records correct and audit-safe. (Not tax advice — confirm
> with a CPA.)

## 1. Treatment

- **Classification:** Operating expense (technology/automation), **not** payroll.
- **Account:** `5400 – AI Agents & Automation Expense` (added to the chart of accounts).
  Underlying spend is LLM/API usage, a share of compute, and tooling.
- **Cost centers:** each of the five agents is tracked as a cost center so we know the
  cost of each automated function (the AI equivalent of a role's cost line).
- **No payroll accounts** (no wages payable, payroll tax liabilities, or benefits).

## 2. The five agents and their monthly operating cost

These are run costs, **not salaries**. Illustrative at MVP volume — replace with real
usage (`docs/ops/agent_operating_costs.csv`, regenerate via
`python3 docs/ops/generate_agent_costs.py`).

| Agent | Function (job) | LLM/API | Compute | Tooling | **Monthly cost** | Annual |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Ava | Onboarding Concierge | $12 | $5 | $8 | **$25** | $300 |
| Max | Subscriptions & Billing | $10 | $5 | $5 | **$20** | $240 |
| Sage | Account & Security | $8 | $5 | $5 | **$18** | $216 |
| Quinn | Product & Markets Guide | $14 | $5 | $6 | **$25** | $300 |
| Tess | Technical Support & Triage | $18 | $6 | $6 | **$30** | $360 |
| **Total** | | | | | **~$118/mo** | **~$1,416/yr** |

For context (not booked as payroll): a single fully‑loaded **human** support hire is
~$4,800/mo (see `docs/OPERATING_COST_LEAN_VS_STAFFED.md`) — so the five‑agent team runs
at a tiny fraction of one human salary.

## 3. Journal entry (monthly)

Book the agents' run cost as an operating expense (split by cost center if desired):
```
Dr 5400 AI Agents & Automation Expense   118.00
   Cr 1000 Cash (or 2000 Accounts Payable)    118.00
```
Posts cleanly through `POST /api/v1/accounting/journal-entries` and flows to the trial
balance / P&L. Tag the memo with the agent/cost-center for per-function reporting.

## 4. "Onboarding" an AI agent (the right checklist)

Instead of HR onboarding, each agent has a **deployment record**:
- Defined role, scope, and escalation path (already in `/api/v1/agents` + `docs/AI_AGENT_TEAM_PROFILES.md`).
- Cost center + monthly run-cost budget (this doc).
- Owner/accountability: founder (Tess escalates to founder).
- Data access & guardrails (least privilege; non-custodial).
- Monitoring: track usage/cost, escalation rate, CSAT.

## 5. What we will NOT do (and why)

- ❌ Set up payroll / pay "salaries" to AI agents — they aren't people; it misstates the
  books and risks tax fraud.
- ❌ Record wage/benefit/payroll-tax liabilities for them.
- ✅ Book their real run cost as `5400` operating expense, per cost center.

If/when you hire **real human** employees, that's a separate, proper payroll setup
(wages, payroll‑tax liabilities, benefits) — I'll implement that distinctly when needed.
