# Strategic Roadmap — living life-cycle plan

> JHI-SIG: 69M2705M · **Living document.** JHI's continuous, never-ending life-cycle plan.
> Add/adjust items here as the firm evolves. Status: ✅ done · 🟡 in progress · ⬜ planned.
> Priority: 🔴 P0 (launch-blocking) · 🟠 P1 (before public launch) · 🟡 P2 (scale/maturity).
> Companions: `docs/SOFTWARE_PLATFORM_AUDIT.md` (gates), `docs/SYSTEM_ADMINISTRATOR_MODULE.md`.

## Guiding posture
Software publisher (NAICS 513210); never manages outside money; private & bootstrapped (no outside
investors by default, optionality retained). Product = research / analytics / decision-support / education
(**not** investment advice). Serve **Derived Data only** externally, within the NASDAQ addendum.

---

## A. Access & identity (the gatekeeper)
| Item | Status | Pri | Notes |
|---|---|---|---|
| Security hardening (encrypted TOTP, PyJWT, Stripe webhook verify, WebAuthn) | ✅ | 🔴 | PR #64 |
| Gatekeeper P0 (RBAC, `require_permission`, `ENFORCE_AUTH`, admin console, audit) | ✅ | 🔴 | PR #65 |
| **Functional/module-based roles** (Viewer · Analyst · Contributor · Billing Mgr · Org Admin · Super Admin) with an editable role↔permission matrix; keep **persona** (cpa/attorney/searcher…) as a *profile/segment tag*, not access | ⬜ | 🟠 | Founder request 2026-07-13. Decouple access from job title. |
| Front-end login flow (attach Bearer token to all API calls) → enables flipping `ENFORCE_AUTH=true` cleanly | ⬜ | 🔴 | Prereq before enabling enforcement in prod |
| Org-admin tier, invitations/approvals (four-eyes), refresh tokens + instant revocation, impersonation, AI-agent-admin autonomy | ⬜ | 🟠/🟡 | Admin P1 (see admin design doc) |

## B. Data sourcing & feeds
| Item | Status | Pri | Notes |
|---|---|---|---|
| Market data (crypto, indices, commodities, treasuries, FX, bond/PE/SMB proxies) | ✅ | — | Yahoo/CoinGecko |
| Macro (CPI, GDP, unemployment, M2, treasury yields) | ✅ | — | BLS + FRED + Yahoo |
| **Federal macro expansion** (Fed Funds, consumer credit, revolving credit, household debt/GDP, credit-card & loan & mortgage delinquency, retail sales, consumer sentiment, industrial production) | ✅ | 🟠 | Added via FRED (this pass). **Needs free `FRED_API_KEY` in Secrets** to poll live. Public data — no license constraints. |
| Treasury Fiscal Data (federal debt/deficit) | ⬜ | 🟡 | `fiscaldata.treasury.gov` API (public, free) |
| SF1 fundamentals (Sharadar/NASDAQ) | 🟡 | 🔴 | Code ready; **gated on the signed NASDAQ addendum** + `FRED`/`NASDAQ` keys; derived-data only externally |
| **Search-fund deal-flow data** (BizBuySell, brokerages, Axial/BizQuest/DealStream, IBBA) | ⬜ | 🟠 | **License / partnership — do NOT scrape (ToS/legal risk).** Broker partnerships double as a distribution channel. BD initiative. |

## C. Product & content
| Item | Status | Pri | Notes |
|---|---|---|---|
| Deal X-Ray (CIM analysis, DCF/valuation, scorecard) | ✅ | — | On `main` |
| Quality of Earnings / Financial Diligence Suite (partner-CPA) | ✅ | — | On `main` |
| Deal Pipeline + Documents/downloads + full Chart of Accounts | ✅ | — | Merged |
| **Newsletters** (daily market brief · weekly deal digest · monthly research · annual outlook) from datasets + interfaced sources | ⬜ | 🟠 | Content flywheel. Needs a content pipeline + scheduler + **transactional email** (SES/Postmark) + subscriber entitlement + disclaimers. Uses **Derived Data** (within NASDAQ addendum). |
| CIM upload → auto-extract (Deal X-Ray v2) | ⬜ | 🟡 | Attacks the "reading is the bottleneck" pain |
| Opportunity/Deal Score **validation (H5)** | 🟡 | 🔴 | No predictive claim until it clears the pre-registered bar |

## D. Compliance, legal & data license
| Item | Status | Pri | Notes |
|---|---|---|---|
| NASDAQ addendum (SaaS + external Derived-Data + Sharadar consent) | 🟡 | 🔴 | NASDAQ agreed; **awaiting counter-signed addendum** (email not binding, §22). Hold client-facing use until returned. |
| Data-entitlement + purge controls (who accesses licensed-data output; delete/certify on termination §6.3; audit §8) | ⬜ | 🟠 | Admin P1, unblocked by the addendum |
| Formal legal instruments (ToS, Privacy, Cookie, DPA, Acceptable-Use, DR/retention) | ⬜ | 🔴 | Launch gate |
| Copyright/trademark registration + §351 IP assignment + stock ledger | 🟡 | 🔴 | Founder + counsel; checklist in `docs/legal/` |

## E. Operations & launch readiness (gates)
| Item | Status | Pri | Notes |
|---|---|---|---|
| CI/CD + branch protection + secret/dependency scanning | ⬜ | 🔴 | `.github/` absent today |
| Backups + tested restore (RTO/RPO); DR plan | ⬜ | 🔴 | Before real customer data |
| Observability (error tracking, logs, uptime/alerting) | ⬜ | 🔴 | — |
| Production cloud deploy (AWS) + secrets manager + prod hardening | ⬜ | 🔴 | Enable `ENFORCE_AUTH=true`, set `APP_ENCRYPTION_KEY`/`STRIPE_WEBHOOK_SECRET` |
| Billing ↔ access coupling (subscription status drives entitlement) | ⬜ | 🟠 | — |
| SOC 2 / ISO 27001 readiness; ADA/accessibility | ⬜ | 🟡 | Maturity |

---

## Immediate next candidates
1. **Front-end auth wiring** (unlocks turning on `ENFORCE_AUTH`).
2. **Functional-role model** (item A) — closest extension of the gatekeeper.
3. **Data-entitlement + purge** (D) — now unblocked by the addendum.
4. **Newsletter MVP** (C) — needs transactional email first.
5. **Deal-flow data partnerships** (B) — BD track.

*Maintenance: update statuses here each session; this is the firm's continuous life-cycle plan. Provenance `69M2705M`.*
