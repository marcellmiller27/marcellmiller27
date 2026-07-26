# Launch Readiness Map — JHI Research & Analytics Firm, Inc.

**Owner:** Cy Henry (VP, Software Engineering — AI) · **Signature of record:** `69M2705M`
**Purpose:** A clear map of where the platform stands — architecture → completed → deploy-ready —
so that once the **NASDAQ agreement commences and line-item 5H validates**, we can launch and
begin taking subscriptions with confidence. Living document; reconcile each release.

> Status legend: 🟢 Live (real data / wired) · 🟡 Partial (works, but static data or gaps) ·
> 🔴 Stub/placeholder (not wired) · ⏳ Pending merge (built, in an open PR).

---

## 1. Architecture at a glance (two planes)
- **Plane A — Storefront (public marketing):** `StorefrontShell` + marketing pages. Job: convert visitors → free newsletter → paid.
- **Plane B — Application (authenticated product):** `AppShell` + left menu drawer. Job: deliver research, records, diligence, and firm operations.
- **Backend:** FastAPI (`backend/app`) — 20+ routers, Postgres/SQLAlchemy, JWT auth, Stripe billing contract, reportlab PDF, market/economic data services.
- **Data spine:** live public feeds (FRED · BEA · BLS · market quotes) wired; entity graph currently **frontend seed** (`src/lib/entities.ts`) pending the Phase-3.1 backend schema; licensed vendor data (NASDAQ/Sharadar SF1) gated on 5H.

## 2. Backend routers (capabilities present)
`auth` · `mobile_auth` · `billing` · `accounting` · `crm` · `pipeline` · `dashboards` · `reports` ·
`market` · `public_macro` · `bea` · `research` · `valuations` · `deal_xray` · `financial_diligence` ·
`edgar` · `integrations` · `leads` · `support` · `agents` (+ `newsletters` ⏳ PR #109).
Security hardening (encrypted TOTP, PyJWT, Stripe webhook verify, real WebAuthn) exists in PR #17 (rescue pending).

## 3. Frontend surface — status by route

### Plane A — Storefront
| Route | Purpose | Status | Notes / gap |
|---|---|---|---|
| `/` Home | Positioning + Opportunity Score hero | 🟡 | **Copy not institutional-grade** (rewrite queued); legacy "John Henry Investments" mark to reconcile |
| `/pricing` | Plans | 🔴 | **No purchase control** — tiers not selectable/buyable (Phase A) |
| `/about`, `/team` | Firm + people | 🟢 | Static, acceptable |
| `/join` | Waitlist capture | 🟢 | Live leads API |
| `/login`, `/register` | Auth | 🟡 | Real auth + route enforcement in PR #104 (⏳) |
| `/support` | AI FAQ agent | 🟢 | Live agents API |
| `/mobile` | Mobile companion | 🟢 | Live auth (password/2FA/biometric) |

### Plane B — Application
| Route (menu label) | Status | Notes / gap |
|---|---|---|
| `/dashboard` | 🟡 | Live market rail + **static** launchpad/coverage/watchlist |
| `/macro` (Economics) | 🟢 | Live FRED/BEA/Treasury/market |
| `/opportunities` (Screener) | 🟡 | **Static** seed (`platform-data`), not a live screener |
| `/reports` (Reports) | 🔴 | **Static** + **dead "Generate report preview"** button |
| `/deal-xray` (Scope) | 🟢 | Live backend engine + Excel/PDF export |
| `/diligence-suite` (Earnings/QoE) | 🟢 | Live backend engine + export |
| `/due-diligence` (Document Review) | 🟡 | **Static** content |
| `/pipeline` | 🟢 | Live pipeline API (add/remove wired) |
| `/portfolio` | 🟡 | **Static** seed |
| `/assistant` (Ask JHI) | 🟡 | Verify live agents wiring on the page |
| `/newsletters` (+ 3 editions) | 🟢⏳ | Live generation; **PDF download** PR #109; **menu link** PR #111 |
| `/companies`, `/firms/*`, `/advisors/*` | 🟡 | Entity graph = **frontend seed**; Phase-3.1 backend pending |
| `/downloads` (Documents) | 🟢 | Static file list (baked) |
| `/account` (+ `/account/cancel`) | 🟢⏳ | Cancellation flow PR #108 |
| `/accounting` (Firm Operations) | 🟢⏳ | Live GL; staff-gated; PR #104 stack |

## 4. Inactive / unwired controls — audit (from a full `src` scan)
| # | Location | Control | State | Fix |
|---|---|---|---|---|
| 1 | `src/app/reports/page.tsx` | **"Generate report preview"** | 🔴 no `onClick` — does nothing | Wire to the #109 server-side PDF engine / matching edition (needs report→output mapping) |
| 2 | `src/app/pricing/page.tsx` | **Plan purchase** | 🔴 no control exists | Phase A: radio-select + Continue → checkout-session (mock now, Stripe later) |

**Everything else scanned is wired:** menu drawer, newsletter action (Print→Download in #109), `live-accounting` (post/add/remove JE), `deal-xray` & `financial-diligence` (Save to Pipeline / Excel / PDF / Request QoE), `entity-directory` filters, `company-record` tabs, `support` chips/ask, `pipeline-board` remove, `newsletter-subscribe` & `waitlist` forms, all `/mobile` flows. Home CTAs ("Start free", "Open the platform") are links (fine).

## 5. Deployment gates (must clear before public paid launch)
| Gate | Owner | Status |
|---|---|---|
| **NASDAQ line-item 5H validation** (5-day trial) + Order Form countersigned | Founder | ⏳ blocking data license; contingency in `docs/legal/nasdaq/NASDAQ_TRIAL_CONTINGENCY_5H.md` |
| **Auth + RBAC enforcement** on every premium route | Cy | ⏳ PR #104 (foundation) → Gatekeeper P0 |
| **Billing live** (Stripe keys + price IDs) — purchase + webhook → plan active | Founder + Cy | 🔴 Phase B (mock today) |
| **Per-plan feature/seat gating** | Cy | 🔴 Phase 6 (P0→P1→gates) |
| **Live data on static pages** (Screener, Reports, Portfolio, Due-Diligence, entity graph) | Cy | 🟡 Phases 3.1–5 |
| **Institutional copy rewrite** (storefront) + brand-mark reconcile | Founder + Cy | 🔴 queued |
| **Newsletter email send (Step B)** — SES creds | Founder | ⏳ gated |
| **Empty/error states**, mobile-parity decision | Cy | 🟡 Phase 6 |
| **Secrets:** `AUTH_JWT_SECRET` ✅ · `STRIPE_*` 🔴 · `SES` 🔴 · `TWELVEDATA/NASDAQ_DATA_LINK/FUNDAMENTALS` 🔴 | Founder | mixed |

## 6. Readiness verdict
- **Deploy-ready today (soft/private):** Economics, Deal X-Ray (Scope), Earnings/QoE, Pipeline, Support, Mobile auth, Accounting (staff). Auth/RBAC foundation is in-flight (#104).
- **Before taking subscriptions (revenue-critical):** (1) purchase flow + live Stripe, (2) per-plan gating, (3) NASDAQ 5H clear, (4) storefront copy rewrite, (5) graduate the static product pages to live.
- **Recommended launch sequence:** clear 5H → merge #104 → Gatekeeper P0 → purchase flow (Phase A→B) → per-plan gating → copy rewrite → live-data graduation (Phases 3.1–5) → Phase-6 launch gates → open subscriptions.

---
*Cross-refs:* `docs/PLATFORM_RESTRUCTURE_PLAN.md`, `docs/PRICING_BILLING_SCHEMA.md`, `docs/EDITORIAL_PROGRAM_ASSESSMENT.md`, `docs/GTM_LAUNCH_STRATEGY.md`, `docs/CONTRIBUTION_MARGIN_CVP.md`, `docs/TODO_NEXT_SESSION.md`.
