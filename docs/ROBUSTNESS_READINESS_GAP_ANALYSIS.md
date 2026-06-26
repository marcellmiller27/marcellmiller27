# Robustness & Top‑Tier Readiness — Gap Analysis (current status)

Honest assessment of what's missing to make John Henry Investments a robust, top‑tier
asset, plus the Docker production hardening needed to run it "without anomalies."
Grounded in the current codebase.

## Progress update (2026-06-26 hardening pass)

Completed in the production-hardening pass:
- ✅ **Config/secret validation** — `app/config.py` fails fast in production on a default
  `AUTH_JWT_SECRET` or SQLite DB (`get_settings().validate()` at startup).
- ✅ **Readiness probe** `GET /ready` (verifies DB connectivity).
- ✅ **Rate limiting** — env-gated in-process middleware (`RATE_LIMIT_PER_MINUTE`, off by default).
- ✅ **Postgres support** — `psycopg[binary]` dependency; Compose now runs Postgres with
  durable persistence for the SQLAlchemy modules (auth, billing, security, leads, tickets).
- ✅ **Docker hardening** — non-root users, `HEALTHCHECK`s, multi-worker backend, Postgres
  service in Compose with healthcheck/depends-on.
- ✅ **Sharadar SF1 adapter pre-wired (gated)** — activates on `NASDAQ_DATA_LINK_API_KEY`;
  `fundamentals-status` and `/market/providers` reflect it.

- ✅ **CRM migrated to durable Postgres/SQLAlchemy** (seeded; survives restart; 86 tests).

Still open (next): migrate the remaining in-memory modules (accounting/reports/dashboards/integrations) to Postgres,
wire the static module pages to live data, live Stripe, WebAuthn signature verification,
observability (Sentry/metrics), CI/CD, SES email + password reset, and H5 validation.

## Where we are (strong foundation)

Functional today: auth (password/2FA/biometric), live market data (CoinGecko/Yahoo/BLS
+ FX/curve/bonds), live dashboard, research harness, modeled valuations, AI support +
5‑agent team with founder escalation, waitlist lead capture, mobile app, brand/mission,
Docker config, 73 backend tests, lint/build green.

## Gaps to "robust top‑tier" — prioritized

### P0 — must fix before real paying users
1. **Core module pages are static prototypes.** Opportunities, portfolio, reports,
   due‑diligence, assistant, account render static content — not wired to live data or
   actions. *Top‑tier requires every module to produce real results.*
2. **Non‑durable persistence.** accounting, crm, reports, dashboards, integrations use
   an **in‑memory store → data is lost on restart** (confirmed). Move these to
   SQLAlchemy/Postgres.
3. **Billing isn't live.** Checkout is a contract/mock — **no Stripe SDK** and no
   webhook signature verification. Wire real Stripe before charging.
4. **Security hardening:** default dev token secret (`AUTH_JWT_SECRET`), **biometric
   assertion not cryptographically verified** (WebAuthn), 2FA window widened, **no rate
   limiting**, public endpoints, limited RBAC. Required for a fintech handling money/PII.
5. **Database/prod parity:** SQLite default, **no Alembic migrations** (schema via
   `create_all`). Add Postgres + migrations.

### P1 — needed for "exceptional, anomaly‑free" operation
6. **Observability:** no error tracking (Sentry), structured logging, metrics, alerting,
   tracing, or uptime monitoring. You can't ensure "no anomalies" without it.
7. **CI/CD:** no pipeline. Add automated tests + lint + build + deploy on push.
8. **Testing depth:** strong backend unit tests, but **no frontend tests and no E2E**
   (Playwright) or load/performance tests.
9. **Docker production hardening** (see checklist below).
10. **Email delivery (SES):** lead/escalation notifications, **password reset** (no
    reset endpoint exists), and transactional email are not wired.
11. **Score validity (H5):** unproven; needs licensed point‑in‑time fundamentals
    (Sharadar) to validate before marketing the Opportunity Score as predictive.

### P2 — top‑tier polish
12. **Compliance/legal (finance):** Terms/Privacy/disclaimers, GDPR/CCPA data handling,
    advice/RIA positioning, KYC/AML if custody/payments expand, SOC 2 path.
13. **Resilience/DR:** backups + restore drills, autoscaling policy, IaC (Terraform/CDK).
14. **Performance/UX:** caching strategy, perf budgets, accessibility (a11y), SEO.
15. **Branch consolidation:** unify to one `main` (PR #13) so there's a single source of truth.

## Docker production hardening checklist (you flagged this)

Current images run a single `uvicorn` as **root with no healthcheck**. For
"exceptional performance without anomalies," add:

- **Healthchecks** (`HEALTHCHECK` / compose `healthcheck`) on `/health`, plus
  readiness/liveness for orchestrators.
- **Non‑root user** in both Dockerfiles (security).
- **Production server config:** run uvicorn with multiple workers (or gunicorn +
  uvicorn workers) sized to CPU; graceful shutdown/timeouts.
- **Next.js standalone output** for a smaller, faster frontend image.
- **Postgres service in compose** (not SQLite) for prod parity + a volume for data.
- **Resource limits** (cpu/memory) and restart policies (already `unless-stopped`).
- **Env validation + secrets** (fail fast if `AUTH_JWT_SECRET` is default; set
  `APP_ENV=production` to disable dev‑only endpoints).
- **Log to stdout in JSON**, shipped to your observability stack.
- **Multi‑stage builds** (frontend already multi‑stage; keep images lean) + `.dockerignore` (present).

## Recommended sequence

1. **Consolidate to `main`** (merge PR #13).
2. **P0:** wire core modules to live data; move in‑memory modules to Postgres + Alembic;
   live Stripe; security hardening (real `AUTH_JWT_SECRET`, rate limiting, WebAuthn
   verification, RBAC).
3. **P1:** Docker hardening (checklist above) → observability (Sentry + metrics + uptime)
   → CI/CD → E2E tests → SES email + password reset.
4. **Validate H5** with licensed fundamentals before predictive claims.
5. **P2:** compliance/legal, DR/IaC, performance/a11y/SEO.

## Bottom line

The platform is a **strong, broad MVP scaffold** with several genuinely functional,
tested subsystems — but it is **not yet robust/top‑tier** because: core modules are
static, key data isn't durably persisted, billing/security aren't production‑grade,
and there's no observability/CI/Docker hardening. Close the **P0 + Docker hardening**
items first; that's the shortest path to a platform that deploys in Docker and
"performs exceptionally without anomalies."
