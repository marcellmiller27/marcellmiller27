# Operational Due-Diligence Audit — Top to Bottom (2026-07-03)

> A blunt, no-stone-unturned review of JHI's systems, processes, procedures, policies, and
> business structure — front-end to back-end — with gaps/leakage flagged by severity and a
> clear action for each. Honest outlook at the end.
>
> **Severity:** 🔴 P0 (fix before real paying users / signing money) · 🟡 P1 (before scale) ·
> 🟢 P2 (polish). **NOT legal/tax/accounting advice** — confirm regulated items with counsel/CPA.

---

## 0. Validation performed (evidence this audit is grounded)
- ✅ Backend (base `unified-platform`): **98 tests pass**, `ruff` clean, app boots (21 routes).
- ✅ Frontend (base): `eslint` clean, `next build` passes (18 routes).
- ✅ Feature branches each passed their own suites when created (integrations 103, security-P0 121, module-pages via UI + video review).
- ⚠️ **Repo state: 33 open PRs, only 1 merged.** Nothing consolidated to `main`. (See §1.)

---

## 1. Engineering, release & coordination
| Item | Status | Gap / leakage | Sev | Action |
| --- | --- | --- | --- | --- |
| Codebase quality | ✅ tests/lint/build green on base + branches | Coverage is decent but not enforced | 🟡 | Add CI to enforce |
| **Release coordination** | ⚠️ **33 open PRs, 1 merged** | **Nothing consolidated to `main`; deep stacked branches → merge-conflict & "which version is prod" risk; signatures/entity spread across branches** | 🔴 | **Merge sequence:** land `unified-platform` → main, then merge feature PRs in order; then one consolidated signature/entity pass |
| CI/CD | ❌ none | No automated pytest/ruff/lint/build on push; manual only | 🔴 | GitHub Actions pipeline |
| Observability | ❌ none | No error tracking (Sentry), structured logs, metrics, uptime/alerting → blind in prod | 🔴 | Sentry + JSON logs + uptime monitor |
| Migrations | ❌ none | `create_all` only (no Alembic); schema changes (e.g., `sign_count`) not migratable in prod Postgres | 🔴 | Add Alembic before prod data |
| Backups / DR | ❌ none | No backup/restore drill; ransomware/loss recovery unproven | 🟡 | Managed Postgres backups + restore test |
| IaC | ❌ none | Infra not reproducible | 🟢 | Terraform/CDK later |

## 2. Product (built vs. prototype — honesty)
| Module | Status | Gap | Sev |
| --- | --- | --- | --- |
| Auth (password/2FA/biometric) | ✅ built (2FA encrypted at rest, real WebAuthn) — *unmerged (#17)* | RBAC not enforced on all routes | 🔴 |
| CRM / Accounting / Reports / Integrations | ✅ durable Postgres | — | — |
| Live market data | ✅ built (CoinGecko/Yahoo/BLS) | key-gated FRED/TwelveData inactive | 🟢 |
| Module pages | ✅ wired to live data — *unmerged (#34)* | — | — |
| **Opportunity Score** | 🟡 defined + live; **predictive validity UNPROVEN (H5)** | can't claim alpha until SF1 validation passes \|t\|≥2.0 | 🔴 (claims) |
| **Acquisition engine (CIM/EBITDA/DSCR/SBA)** | 🟡 engine logic; UX prototype | the CIM analyzer/screener (the niche wedge) needs building | 🟡 |
| Due-diligence center | ⬜ prototype | doc parsing/QoE not built | 🟡 |
| Billing / Stripe | 🟡 webhook verified (#17); checkout is mock | live checkout not wired | 🔴 (to charge) |

## 3. Data & licensing (NASDAQ SF1)
- **Status:** key authenticates but is the **free SAMPLE** (MRY-only, 30 tickers). Commercial Order Form (**$18k/yr, 5-day trial**) drafted, **not signed**.
- 🔴 **Gaps:** (a) Order Form must name the **separate WY entity** (not "dba"); (b) **SaaS + external distribution rights** must be written in; (c) **"1,000 subscribers" cap is email-only** — get it in the Order Form (merger clause); (d) must respect third-party **Sharadar terms**, delete-on-termination, audit rights.
- **Action:** sign only after amendments + counsel; validate H5 during the 5-day trial.

## 4. Security & data protection
- ✅ Strong for stage: PBKDF2, PyJWT, scoped tokens, TOTP **encrypted at rest**, real WebAuthn, parameterized ORM, rate-limit middleware, non-root containers, config fail-fast (all in #17, **unmerged**).
- 🔴 **Gaps:** RBAC not enforced everywhere; rate-limit off by default + per-instance (needs Redis); no secrets manager in prod; no pen test; TLS/HSTS/security headers + tightened CORS for prod; enforce strong `AUTH_JWT_SECRET`/`APP_ENCRYPTION_KEY`/`STRIPE_WEBHOOK_SECRET`.
- **Data minimization is a genuine strength** (no card/bank data → Stripe; no SSN/addresses/keys). See `docs/SECURITY_POSTURE_AND_DATA_PROTECTION.md`.

## 5. Legal & entity structure
- **Decided:** family office (**John Henry Investments, LLC**) + **separate WY corporation "JHI Research & Analytics Firm, Inc."** holding the platform/data/clients; bootstrapped, **no outside investors**; debt/LOC allowed.
- 🔴 **Gaps:** WY corp **not formed yet**; **IP not assigned** to it; **no LICENSE/copyright registration** filed; the NASDAQ contract must be signed by the (formed) research corp; **DBA wording** on the Order Form still wrong.
- **Action:** form WY corp → assign IP (founder → corp) → then sign NASDAQ; file copyright per `docs/legal/COPYRIGHT_REGISTRATION_CHECKLIST.md`.

## 6. Compliance & regulatory
- 🔴 **Advice vs. tools line:** must stay **research/education/decision-support**, not personalized advice-for-fee (adviser rules). No Terms/Privacy/disclaimers live yet.
- 🔴 **Business-broker line (search-fund product):** provide **analysis/tools only** — do **not** facilitate transactions for a fee (broker licensing). Disclose any lender/broker referral fees.
- 🟡 GDPR/CCPA (user PII), data-retention/deletion, SOC 2 path (B2B buyers will ask).
- **Action:** counsel to bless positioning + publish Terms/Privacy/disclaimers before client acquisition.

## 7. Finance & accounting
- ✅ Durable double-entry ledger, trial balance, IP/amortization + AI-agent cost accounting **designed**.
- 🔴 **Gaps:** no real bookkeeping/bank feeds, **no CPA engaged**, no separate business bank accounts per entity yet, no revenue recognition process, no budget/cash tracking against actuals.
- **Action:** open per-entity bank accounts (post-formation), engage CPA, wire Stripe Tax, keep clean intercompany books (no commingling).

## 8. Operations & support
- ✅ 5 AI agents (deterministic FAQ + founder escalation, durable tickets).
- 🟡 **Gaps:** no SLAs/response-time policy, no incident-response runbook, no status page, email notifications (SES) not wired (lead/escalation/password-reset).
- **Action:** define support SLA + incident runbook; wire SES.

## 9. Go-to-market / distribution (the real bottleneck)
- 🟡 Waitlist funnel built; marketing strategy + Phase-1 playbook documented.
- 🔴 **Gap:** **zero live subscribers, no live funnel running, no analytics/CRM/email stack stood up.** Distribution — not product or cash — is the #1 risk.
- **Action:** stand up the lean stack (PostHog + free CRM + Resend/SES); ship the search-fund lead magnet; begin founder-led niche outreach.

## 10. Governance / corporate
- 🔴 **Gaps:** no formed entity yet → no **operating agreement/bylaws**, **cap table**, **founder IP-assignment agreement**, **board/decision record** (until now), or **EIN/registered agent**.
- **Action:** on formation, adopt bylaws, issue founder equity, sign IP assignment, start a board-minutes cadence (this audit + `docs/board/BOARD_MINUTES_2026-07-03.md` begin it).

---

## Top-10 "no leakage" priority list
1. 🔴 **Consolidate the code** — merge `unified-platform` → main, then feature PRs (stop the 33-PR sprawl).
2. 🔴 **Form the WY corp + assign IP** — unblocks the NASDAQ signature, banking, and provenance rename.
3. 🔴 **Fix + sign the NASDAQ Order Form** (correct entity, SaaS/distribution rights, 1,000-sub cap in writing) — during the 5-day trial, **validate H5**.
4. 🔴 **CI/CD + Alembic + observability** — no prod without these.
5. 🔴 **Publish Terms/Privacy/disclaimers + confirm advice/broker positioning with counsel.**
6. 🔴 **Enforce RBAC + prod security env** (secrets, headers/TLS, rate-limit/Redis).
7. 🔴 **Live Stripe checkout** (to actually charge) + Stripe Tax.
8. 🟡 **Engage a CPA**, open per-entity bank accounts, clean intercompany books.
9. 🟡 **Stand up the GTM stack** + ship the search-fund wedge (CIM analyzer/screener).
10. 🟡 **Backups/DR + support SLA + incident runbook + SES notifications.**

---

## Honest outlook — where JHI stands
**A genuinely strong, broad prototype with an unusually clear strategy — but not yet an operating business.** Blunt truth:

**Strengths:** a real, tested, Docker-ready platform across ~14 backend subsystems with durable persistence; strong-for-stage security with real data minimization; a sharp, defensible strategy (bootstrapped, private, research/decision-support, **search-fund/SMB niche wedge**); honest research discipline (H5 not overclaimed); and clean financing posture (debt-not-equity).

**The gap between "prototype" and "company":** three things convert this from an impressive build into a real business, in order —
1. **Consolidate + productionize** (merge the code, CI/CD, migrations, observability, live Stripe, security enforcement).
2. **Formalize the entity + legal** (form the WY corp, assign IP, Terms/Privacy, counsel on positioning, sign NASDAQ correctly).
3. **Prove demand** (first 25 → 1,000 subscribers in the search-fund niche) — **this is the real risk; capital and product quality are not.**

**Valuation reality:** ~**$360K asset/cost floor today**; the hockey stick is earned in **ARR + retention + moat**, one rung at a time (≈$70K MRR ≈ ~235 niche subs).

**Bottom line:** We are **~80% "platform," ~20% "business."** The engineering is ahead of the operations, legal, and go-to-market. The next phase is **less about building features and more about consolidation, formalization, and distribution.** Do the Top-10 above and JHI becomes a lean, credible, sellable operating company — with a real shot at the niche.

> Cross-refs: `docs/ROBUSTNESS_READINESS_GAP_ANALYSIS.md`, `docs/SECURITY_POSTURE_AND_DATA_PROTECTION.md`, `docs/COMPANY_POSTURE_AND_COMPLIANCE.md`, `docs/PHASE1_ZERO_TO_1000_PLAYBOOK.md` (planned), `docs/TODO_NEXT_SESSION.md`.
