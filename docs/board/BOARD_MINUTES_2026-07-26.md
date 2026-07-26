# Board Minutes — JHI Research & Analytics Firm, Inc.

**Meeting date:** 2026-07-26 · **Type:** Founder working session (platform build) · **Recorder:** Cy Henry (VP, Software Engineering — AI teammate)
**Present:** Founder (Galen Marcellus Miller).

> NOT legal/tax/accounting advice. Prior session: `docs/board/BOARD_MINUTES_2026-07-23.md`.
> Signature of record: `69M2705M`. Ethos: *How we do anything is how we do everything.*

---

## 1. 🔴 PRIORITY — Set up the JHI business bank account (RECORDED)
- **Founder directive:** stand up a **business bank account for JHI Research & Analytics Firm, Inc.** as a top priority.
- **Why it's on the critical path:** the bank account underpins **billing/revenue** (Stripe payouts for subscriptions), **payroll/AP** (paying vendors incl. AWS/NASDAQ), and clean **corporate books** (the in-house Chart of Accounts). No account = no way to collect subscription revenue at launch.
- **Suggested essentials (Founder + counsel/accountant to execute):** EIN + formation docs in the entity's exact legal name; a business checking account; connect it to **Stripe** (payouts) and the accounting system; keep it strictly separate from personal funds. *(Not legal/tax advice — confirm with the firm's accountant/attorney.)*

## 2. Platform merges completed (RECORDED)
Merged to `main` this session: **#122** (institutional newsletter PDF — headless render), **#120** (Editorial E2 grounded LLM, flag-off), **#121** (domain wiring `johnhenrycapital.com`), **#119** (board minutes 07-23), **#118** (CVP editorial budget), **#117** (E2 model evaluation), and **#111** closed/merged as a no-op (Newsletter link already on `main`). **Verification green:** ruff clean, 195 backend tests pass (10 known pre-existing accounting/auth failures from #104 staff-gating — a scheduled test-only fix), eslint clean, `next build` green; stack rebuilt from `main` and healthy (newsletter PDF renders institutional; domain metadata baked).

## 3. AWS Bedrock in editorial — status (RECORDED)
- **Integrated, merged (#120), and verified working** live: **Amazon Bedrock + Claude Sonnet 4.5** elevated a real edition, figures preserved, fact-lock passed, ~**$0.0095/edition**. Provider auto-selects Bedrock from `AWS_BEARER_TOKEN_BEDROCK`.
- **Not yet ACTIVE in reader-facing output**, because: (1) `ENABLE_LLM_EDITORIAL` is **off** by default; and (2) post-#122 the primary edition (on-screen + the PDF that mirrors it) is **deterministic** — E2 currently elevates only the reportlab **fallback** path.
- **To activate:** wire E2 into the **on-screen edition** (so the page and its PDF show the AI-elevated prose) + set `ENABLE_LLM_EDITORIAL=1`. Account has access to **Sonnet 4.5 / Haiku 4.5 / Opus 4.5**; **Sonnet 5 needs a Model-access request** in Bedrock (us-east-2). Pending Founder go-ahead + budget-cap selection.

## Decisions locked
Bank account = top launch priority; AWS Bedrock is the editorial LLM provider (data-in-account); E2 stays **off** until wired into the on-screen edition and explicitly enabled; fact-lock is non-negotiable.

---

## Action items (owner · priority)
| # | Action | Owner | Priority |
| --- | --- | --- | --- |
| 1 | **Open the JHI business bank account** (entity legal name; connect to Stripe + accounting) | Founder (+ accountant/attorney) | 🔴 |
| 2 | Authorize wiring **E2 into the on-screen edition** + pick the budget cap ($100/$250/$500), then set `ENABLE_LLM_EDITORIAL=1` | Founder → Cy | 🟡 |
| 3 | (Optional) request **Claude Sonnet 5** Model access in Bedrock (us-east-2); Sonnet 4.5 works today | Founder | 🟢 |
| 4 | Carry-over: **Stripe** live keys + price IDs; **NASDAQ 5H** + Order Form; **DNS** point domain at deploy target + **SES**/Workspace for newsletter email; **storefront copy** rewrite | Founder | 🟡 |
| 5 | Fix the 10 pre-existing accounting tests (staff-auth) for fully-green CI | Cy | 🟢 |

**Next review:** next working session.
**Recorded by:** Cy Henry · signature of record `69M2705M`.
