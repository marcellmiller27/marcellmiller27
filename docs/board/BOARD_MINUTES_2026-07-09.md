# Board Minutes — JHI Research & Analytics Firm, Inc.

**Meeting date:** 2026-07-09 · **Type:** Founder working session · **Recorder:** Cy (VP, Software Engineering — AI teammate)
**Present:** Marcellus Miller (Founder).

> NOT legal/tax/accounting/investment advice. Prior session: `docs/board/BOARD_MINUTES_2026-07-08.md`.

---

## 1. Corporate milestone (RESOLVED)
- ✅ **JHI Research & Analytics Firm, Inc. (Wyoming) formation is COMPLETE.** The research/analytics platform now has its operating C-corp. Next legal step: **assign platform IP → the corp**, then update copyright/entity attribution in code + `LICENSE`.

## 2. Code consolidation (DONE — awaiting founder merge)
- **Consolidation PR #42** opened: `cursor/consolidation-to-main-0d47` → **`main`**, landing the entire platform (89 commits) as the single source of truth. Verified (136 backend tests, ruff, eslint, next build, Docker smoke). **Not merged by the agent — founder to review & merge; then close stacked PRs #36–#41.**

## 3. NASDAQ SF1 Service Order 00151172 (REVIEWED — sign this month)
- Nasdaq **countersigned 7/8/2026**; founder to sign this month. Full review: `docs/legal/nasdaq/SERVICE_ORDER_00151172_REVIEW.md`.
- **Entity confirmed correct** — "JHI Research & Analytics Firm, Inc." is the binding Client; the DocuSign subject-line "LLC dba…" is non-binding metadata (**no action** — founder's position accepted).
- **Terms:** SF1 $13,800 + NDL Platform $4,200 = **$18,000/yr**; Internal **& External**; Initial 12 mo (11-Jul-26 → 10-Jul-27); **5-day cancellable trial**; **90-day** non-renewal notice.
- **Payment terms: Net 30** (invoiced; due 30 days — not on signature). Eases Phase-1 cash flow.
- **Additional Terms to secure before countersigning** (drafted in the review doc + side-letter email to Michael): (1) external distribution up to 1,000 subscribers in writing; (2) Derived-Data + SaaS delivery rights; (3) Derived Data survives termination (delete only raw SF1); (4) source attribution.
- **Signing method:** Adobe-sign + email is acceptable **provided** it's the final version with the Additional Terms (Nasdaq to re-issue the Order or accept the side letter) and Michael confirms he'll take an emailed signed PDF; end state = one fully-executed document. Otherwise complete DocuSign.

## 4. Key dates (calendared)
- **Sign-by (avoid reprice):** ~**05-Aug-26**.
- **Non-renewal notice deadline (90 days):** ~**11-Apr-27**.
- **Initial Term:** 11-Jul-26 → 10-Jul-27.

## 5. H5 validation during the 5-day trial (plan)
- **Pre-register the bar before day 1:** mean IC ≥ 0.03, |t| ≥ 2.0, hit rate ≥ 0.55.
- **Provision data on day 1** (SF1 adapter + PIT fundamentals engine pre-built). **Decide by day 4; send any cancellation early** (not day 5). **Ask Michael to extend the trial to ~10–14 days** to remove timing risk on the $18k/12-month decision.

---

## Action items (owner · priority)
| # | Action | Owner | Priority |
| --- | --- | --- | --- |
| 1 | Send side-letter email to Michael (Additional Terms + email-signature + trial extension) | Founder | 🔴 |
| 2 | On revised Order: sign (Adobe+email or DocuSign) by ~05-Aug-26 | Founder | 🔴 |
| 3 | Run SF1 H5 validation in the trial (pre-registered bar; decide by day 4) | Cy | 🔴 |
| 4 | Assign platform IP → corp; then update copyright attribution in code/LICENSE | Founder + counsel → Cy | 🔴 |
| 5 | Review & merge consolidation PR #42 → main; close #36–#41 | Founder | 🟡 |
| 6 | Calendar non-renewal notice deadline ~11-Apr-27 | Founder | 🟢 |

**Next review:** next working session or upon trial start.
**Recorded by:** Cy · signature of record `69M2705M`.
