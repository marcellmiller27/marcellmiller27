# Board Minutes — JHI Research & Analytics Firm, Inc.

**Meeting date:** 2026-07-11 · **Type:** Founder working session · **Recorder:** Cy (VP, Software Engineering — AI teammate)
**Present:** Founder.

> NOT legal/tax/accounting/investment advice. Prior session: `docs/board/BOARD_MINUTES_2026-07-10.md`.

---

## 1. Code consolidation (DONE)
- **PR #46 merged → `main`.** `main` is now the **single source of truth** for the full platform (backend + frontend + mobile + docs). Branch sprawl ended; future work branches off a clean `main`. Prior stacked PRs (#36–#45) are redundant (their commits are included via #46) and can be closed.

## 2. NAICS classification (RECORDED)
- Corporation classified under **NAICS 513210 — Software Publishers** (sector 51, Information). Recorded in `docs/COMPANY_POSTURE_AND_COMPLIANCE.md`. Reinforces the **software/data publisher, not investment adviser/broker** posture. R&D-credit and SaaS-sales-tax items flagged for CPA.

## 3. IP capitalization basis (RECORDED)
- Platform IP contributed for **10,000,000 shares at $0.04 par = $400,000** stated-capital basis, supported by an **IP Valuation Schedule** (completed + projected engineering/professional hours). Note: **par value ≠ fair value** — the official §351 basis is the CPA/appraiser's determination; the schedule is defensible support.

## 4. Session deliverables (this working session)
- **Accounting UI page** (`/accounting`) — surfaces the live general ledger (chart of accounts, trial balance, journal entries). PR #47.
- **IP Valuation Schedule** — interactive Excel + doc reconciling to $400K (separate PR).
- **Conservative-ramp scenario** — added to the sales commission + EBITDA model (separate PR).

---

## Action items (owner · priority)
| # | Action | Owner | Priority |
| --- | --- | --- | --- |
| 1 | Close redundant PRs #36–#45 (included in `main` via #46) | Founder | 🟡 |
| 2 | Review/merge the four new PRs (accounting, NAICS/posture, IP schedule, commission ramp) | Founder | 🟡 |
| 3 | Execute IP Assignment + share issuance (counsel/CPA); confirm §351 basis | Founder + counsel | 🔴 |
| 4 | Await NASDAQ addendum response; sign final amended Order by ~05-Aug-26 | Founder | 🔴 |

**Next review:** next working session.
**Recorded by:** Cy · signature of record `69M2705M`.
