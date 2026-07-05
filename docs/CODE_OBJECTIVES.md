# Code Objectives — what each module performs

A concise map of the codebase: each module's **objective** and **what it does**.

## Backend — `backend/app/`

| Module | Objective | What it performs |
| --- | --- | --- |
| `main.py` | App entrypoint | Creates the FastAPI app, CORS, `init_db()`, and registers all routers under `/api/v1`. |
| `database.py` | Persistence wiring | SQLAlchemy engine/session; `init_db()` creates tables; `get_db()` dependency. |
| `db_models.py` | ORM schema | Organizations, users, memberships, subscriptions, audit logs, user-security (2FA), device credentials. |
| `security.py` | Crypto primitives | Password hashing (PBKDF2), signed access tokens, scoped challenge tokens, RFC-6238 TOTP. |
| `dependencies.py` | AuthN | `get_current_principal` / `require_admin` from bearer tokens. |
| `foundation_models.py` / `foundation_services.py` | Accounts/billing core | Register/login/me, plans, checkout, webhooks, audit logs. |
| `mobile_models.py` / `mobile_services.py` / `routers/mobile_auth.py` | Multi-factor sign-in | Password step, TOTP 2FA (+ dev code), WebAuthn-style biometric, security status. |
| `market_models.py` / `market_services.py` / `routers/market.py` | Live market data | Real-time quotes from CoinGecko/Yahoo/BLS + key-gated FRED + licensed-vendor (Twelve Data) with Yahoo fallback; symbol registry; provider status; caching + host failover + graceful degradation. |
| `opportunity_score.py` | **Defined scoring model** | The published 0-100 John Henry Opportunity Score: a fixed-weight cross-sectional z-blend of momentum / low-volatility / trend / reversal-guard factors. Pure functions, reused by the live scorer and the back-test. |
| `research_models.py` / `research_services.py` / `routers/research.py` | Validation harness (§8) | Score back-test with **pre-registered H5 criteria**, live opportunity-score snapshot, segment-adoption KPIs (real DB), acquisition-engine validation, and the data-coverage/deficiency matrix. |
| `valuation_models.py` / `valuation_services.py` / `routers/valuations.py` | **Modeled real-time estimates** | Request-time estimates for illiquid classes from live inputs: real estate (NOI ÷ live cap rate), SMB (live small-cap multiple), PE (listed-PE proxy NAV). Clearly labeled `modeled_estimate`. |
| `support_models.py` / `support_services.py` / `routers/support.py` | AI customer service | Retrieval FAQ assistant: scores a question against a knowledge base, returns answer + confidence + follow-ups, escalates when unsure. |
| `models.py` / `services.py` / `store.py` + `routers/{accounting,reports,dashboards,crm,integrations}.py` | Operating workflows | In-memory accounting/CRM/reporting/dashboard/integration prototypes. |

## Frontend — `src/`

| File | Objective | What it performs |
| --- | --- | --- |
| `app/page.tsx` | Marketing landing | Hero, mission section, plans, modules, score, vision. |
| `app/dashboard/page.tsx` + `components/live-market.tsx` | Live command center | Auto-refreshing live market widgets (markets, FX, fixed-income/curve) from `/market/quotes`. |
| `app/mobile/page.tsx` | Mobile companion app | Phone-framed dual-access flows: password, 2FA, biometric, security options. |
| `app/support/page.tsx` | Help center | FAQ + chat assistant calling `/support/ask`. |
| `components/platform-shell.tsx` / `components/logo.tsx` | Shared UI | App nav shell and brand emblem. |
| `app/{opportunities,due-diligence,portfolio,reports,assistant,account,pricing,login,register}/page.tsx` | Product surfaces | Module pages (mostly static prototypes). |
| `app/globals.css` | Design system | Behavioral-science color tokens + component styles. |
| `lib/platform-data.ts` | Static content | Plans, modules, score categories, sample data. |
