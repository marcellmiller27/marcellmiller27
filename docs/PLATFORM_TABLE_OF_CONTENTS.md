# Platform Table of Contents — by Component (Subsystem)

> A code-grounded index of the John Henry Investments (JHI) platform, organized by
> subsystem. Each entry maps the **actual files** (backend + frontend + tests) and the
> **API surface** for that component. Paths are relative to the repo root.
>
> **Legend:** ✅ durable/DB-backed · 🟡 partial/prototype · ⬜ key-gated/not wired.
> **Note:** the security-hardening modules `backend/app/billing_webhook.py` and
> `backend/app/webauthn.py` (+ their tests) land via PR #17 and are referenced where relevant.

---

## 0. Platform spine (entry, config, persistence)

| Concern | Files | Notes |
| --- | --- | --- |
| App entry / router registration | `backend/app/main.py` | FastAPI app, CORS, rate-limit middleware, `/health`, `/ready`, mounts all `/api/v1` routers |
| Runtime settings + prod validation | `backend/app/config.py` | `APP_ENV`, `AUTH_JWT_SECRET`, `DATABASE_URL`, fail-fast in prod |
| Rate limiting | `backend/app/rate_limit.py` | Env-gated per-IP middleware |
| Database / ORM bootstrap | `backend/app/database.py` | Engine, `SessionLocal`, `get_db`, `init_db` + seeding |
| ORM models (all tables) | `backend/app/db_models.py` | Orgs, users, memberships, subscriptions, security, device creds, CRM, accounting, leads, tickets, audit |
| Auth dependencies | `backend/app/dependencies.py` | `get_current_principal`, `require_admin` |
| Shared Pydantic models | `backend/app/models.py` | Accounting/CRM/integration request+response schemas |
| Legacy in-memory store | `backend/app/store.py`, `backend/app/services.py` | Prototype services; **only `IntegrationService` still wired** (others migrated to DB) |

---

## 1. Identity, Auth & Security

**Purpose:** registration/login, tokens, multi-factor (TOTP + biometric), tenancy.

| Layer | Files |
| --- | --- |
| Crypto primitives | `backend/app/security.py` (PBKDF2, JWT/scoped tokens, TOTP; at-rest encryption via PR #17) |
| Web auth API | `backend/app/routers/auth.py` → `POST /auth/register`, `POST /auth/login`, `GET /auth/me` |
| Auth/tenancy service | `backend/app/foundation_services.py` |
| Auth/tenancy models | `backend/app/foundation_models.py` (`Principal`, `UserRole`, plans/status) |
| Mobile multi-factor API | `backend/app/routers/mobile_auth.py` → 2FA + biometric + `GET /auth/security/status` |
| Mobile auth service | `backend/app/mobile_services.py` (TOTP; WebAuthn verify via PR #17 `webauthn.py`) |
| Mobile auth models | `backend/app/mobile_models.py` |
| Frontend | `src/app/login/page.tsx`, `src/app/register/page.tsx`, `src/app/mobile/page.tsx` |
| Tests | `backend/tests/test_foundation.py`, `backend/tests/test_mobile_auth.py` |

---

## 2. Billing & Subscriptions

**Purpose:** plans, checkout, webhook, entitlements, billing audit.

| Layer | Files |
| --- | --- |
| API | `backend/app/routers/billing.py` → `/billing/plans`, `/subscription`, `/checkout-session`, `/webhook`, `/audit-logs` |
| Service | `backend/app/foundation_services.py` (billing methods + audit) |
| Webhook verification | `backend/app/billing_webhook.py` (Stripe signature verify — PR #17) |
| Frontend | `src/app/pricing/page.tsx`, `src/app/account/page.tsx` |
| Tests | `backend/tests/test_foundation.py` (+ `test_billing_webhook.py` in PR #17) |

---

## 3. Accounting & Financial Reporting ✅

**Purpose:** chart of accounts, journal entries, trial balance, financial/audit reports, executive dashboard.

| Layer | Files |
| --- | --- |
| Accounting API | `backend/app/routers/accounting.py` → `/accounting/chart-of-accounts`, `/journal-entries`, `/trial-balance` |
| Accounting service (DB) | `backend/app/accounting_services.py` |
| Reports API | `backend/app/routers/reports.py` → `/reports/financial`, `/reports/audit` |
| Dashboards API | `backend/app/routers/dashboards.py` → `/dashboards/executive` |
| Reporting service (DB) | `backend/app/reporting_services.py` |
| Models | `backend/app/models.py` (accounting/report schemas) |
| Frontend | `src/app/reports/page.tsx` |
| Tests | `backend/tests/test_accounting_db.py`, `backend/tests/test_reports_db.py`, `backend/tests/test_api.py`, `backend/tests/test_services.py` |

---

## 4. CRM ✅

**Purpose:** contacts, deals, activities, pipeline summary.

| Layer | Files |
| --- | --- |
| API | `backend/app/routers/crm.py` → `/crm/contacts`, `/deals`, `/activities`, `/summary` |
| Service (DB) | `backend/app/crm_services.py` |
| Models | `backend/app/models.py` (CRM schemas) |
| Tests | `backend/tests/test_crm.py` |

---

## 5. Market Data ✅

**Purpose:** live multi-asset quotes, inflation, provider/symbol catalogs.

| Layer | Files |
| --- | --- |
| API | `backend/app/routers/market.py` → `/market/quotes`, `/inflation`, `/providers`, `/symbols` |
| Service + adapters | `backend/app/market_services.py` (CoinGecko/Yahoo/BLS live; FRED/Twelve Data ⬜; 60s TTL cache, failover) |
| Models | `backend/app/market_models.py` |
| Frontend | `src/components/live-market.tsx` (15s poll), `src/app/dashboard/page.tsx` |
| Tests | `backend/tests/test_market.py` |

---

## 6. Research & Opportunity Score 🟡

**Purpose:** cross-asset 0–100 score, backtests, adoption/acquisition validation, data coverage, fundamentals status.

| Layer | Files |
| --- | --- |
| API | `backend/app/routers/research.py` → `/research/score-backtest`, `/opportunity-scores`, `/equity-oos-backtest`, `/fundamentals-status`, `/acquisition-validation`, `/data-coverage`, `/adoption` |
| Service | `backend/app/research_services.py` |
| Scoring engine | `backend/app/opportunity_score.py` |
| Models | `backend/app/research_models.py` |
| Frontend | `src/app/opportunities/page.tsx`, `src/app/assistant/page.tsx` |
| Tests | `backend/tests/test_research.py` |

---

## 7. Valuations (illiquid assets) 🟡

**Purpose:** modeled real-time valuations for real estate / SMB / PE using live inputs.

| Layer | Files |
| --- | --- |
| API | `backend/app/routers/valuations.py` → `/valuations/estimate` |
| Service | `backend/app/valuation_services.py` (uses `MarketDataService`) |
| Models | `backend/app/valuation_models.py` |
| Frontend | `src/app/portfolio/page.tsx`, `src/app/due-diligence/page.tsx` |
| Tests | `backend/tests/test_valuations.py` |

---

## 8. Support & AI Agents ✅

**Purpose:** FAQ assistant + the five AI customer-service agents with routing and founder escalation.

| Layer | Files |
| --- | --- |
| Support API | `backend/app/routers/support.py` → `/support/faq`, `/support/ask` |
| Support service | `backend/app/support_services.py`, models `support_models.py` |
| Agents API | `backend/app/routers/agents.py` → `GET /agents`, `POST /agents/message`, `GET /agents/tickets` |
| Agents service (Ava/Max/Sage/Quinn/Tess) | `backend/app/agents_services.py`, models `agents_models.py` |
| Frontend | `src/app/support/page.tsx`, `src/app/team/page.tsx` |
| Tests | `backend/tests/test_support.py`, `backend/tests/test_agents.py` |

---

## 9. Growth / Leads (GTM) ✅

**Purpose:** waitlist lead capture + count.

| Layer | Files |
| --- | --- |
| API | `backend/app/routers/leads.py` → `POST /leads`, `GET /leads/count`, `GET /leads` |
| Models | `backend/app/lead_models.py` |
| Frontend | `src/components/waitlist-form.tsx`, `src/app/join/page.tsx`, `src/app/page.tsx` |
| Tests | `backend/tests/test_leads.py` |

---

## 10. External Integrations 🟡

**Purpose:** banking/vendor/Office connectors + sync jobs (prototype, in-memory).

| Layer | Files |
| --- | --- |
| API | `backend/app/routers/integrations.py` → `/integrations/connectors`, `/connections`, `/sync-jobs`, `/banking/transactions`, `/vendor/bills`, `/office/export-package` |
| Service (in-memory) | `backend/app/services.py` (`IntegrationService`) + `backend/app/store.py` |
| Models | `backend/app/models.py` (integration schemas) |
| Tests | `backend/tests/test_integrations.py` |

---

## 11. Frontend shell & marketing

**Purpose:** app navigation, branding, marketing/landing, mission.

| Concern | Files |
| --- | --- |
| Root layout / global styles / favicon | `src/app/layout.tsx`, `src/app/globals.css`, `src/app/icon.svg` |
| Shared shell / nav | `src/components/platform-shell.tsx`, `src/components/logo.tsx` |
| Marketing / landing | `src/app/page.tsx`, `src/app/pricing/page.tsx`, `src/app/join/page.tsx` |
| Static module pages | `src/app/{dashboard,opportunities,portfolio,reports,due-diligence,assistant,account}/page.tsx` |
| Shared client data | `src/lib/platform-data.ts` |

---

## 12. Build, deploy & ops

| Concern | Files |
| --- | --- |
| Frontend container | `Dockerfile` (Next.js, non-root, healthcheck) |
| Backend container | `backend/Dockerfile` (Uvicorn workers, non-root, healthcheck) |
| Orchestration | `docker-compose.yml` (frontend + backend + Postgres) |
| Build context ignore | `.dockerignore` |
| Frontend project | `package.json`, `next.config.mjs`, `tsconfig.json` |
| Backend project | `backend/pyproject.toml`, `backend/README.md` |
| Health/readiness | `backend/app/main.py` → `GET /health`, `GET /ready` |

---

## Subsystem → API prefix quick map

| Subsystem | API prefix | Frontend route(s) |
| --- | --- | --- |
| Identity/Auth | `/api/v1/auth` | `/login`, `/register`, `/mobile` |
| Billing | `/api/v1/billing` | `/pricing`, `/account` |
| Accounting/Reports/Dashboards | `/api/v1/accounting`, `/reports`, `/dashboards` | `/reports` |
| CRM | `/api/v1/crm` | — |
| Market data | `/api/v1/market` | `/dashboard` |
| Research/Score | `/api/v1/research` | `/opportunities`, `/assistant` |
| Valuations | `/api/v1/valuations` | `/portfolio`, `/due-diligence` |
| Support/Agents | `/api/v1/support`, `/agents` | `/support`, `/team` |
| Leads | `/api/v1/leads` | `/join`, `/` |
| Integrations | `/api/v1/integrations` | — |

---

## Cross-references
- Architecture & command flows: `docs/ORGANIZATION_CHARTS.md`
- Data-polling interfaces: `docs/DATA_POLLING_INTERFACES_FLOWCHART.md`
- Access control & deployment: `docs/ROLE_BASED_ACCESS_AND_DEPLOYMENT.md`
- Module objectives: `docs/CODE_OBJECTIVES.md`
- Security model: `docs/SECURITY_POSTURE_AND_DATA_PROTECTION.md`
