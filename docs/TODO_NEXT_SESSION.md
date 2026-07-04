# John Henry Investments — Next Session To‑Do

Start-of-day checklist. Prioritized; tackle top‑down. Context lives in
`docs/ROBUSTNESS_READINESS_GAP_ANALYSIS.md`.

## Where we left off (2026‑06‑26)
- Unified, Docker‑ready platform on branch `cursor/unified-platform-0d47` (PR #13 → main).
- Production hardening done: config/secret validation, `/ready` probe, env‑gated rate
  limiting, Postgres + Docker hardening (non‑root, healthchecks, workers), Sharadar
  SF1 adapter pre‑wired (gated). 81 backend tests pass; build clean.

## 0. Kick‑off (5 min)
- [ ] Merge PR #13 into `main` (single source of truth), or confirm we keep working on the branch.
- [ ] `docker compose up --build` in the sandbox; verify `/`, `/dashboard`, `/mobile`, `/support`, `/team`, `/join`, and `/api/v1/.../docs`.

## 1. P0 — durability & real functionality (biggest robustness wins)
- [x] **CRM migrated to Postgres/SQLAlchemy** (durable; survives restart; seeded). 2026‑06‑26.
- [x] **Accounting migrated to Postgres/SQLAlchemy** (chart of accounts, balanced journal entries, trial balance; durable; seeded). 2026‑06‑26.
- [x] **Reports & dashboards migrated to Postgres** (financial/audit reports + executive dashboard now compute from the durable ledger & CRM deals; 98 tests pass). 2026‑06‑26.
- [ ] Migrate remaining in‑memory module to Postgres: **integrations** (with tests).
- [ ] Wire the static module pages to live data/actions: **opportunities, portfolio, reports, due‑diligence, assistant, account** (so every button returns a real result).
- [ ] **Live Stripe**: real checkout session + webhook signature verification (replace the mock).

## 2. P0 — security hardening
- [ ] Enforce a real `AUTH_JWT_SECRET` everywhere; rotate dev default.
- [ ] **WebAuthn**: real biometric assertion (challenge + signature + counter) verification.
- [ ] Turn on `RATE_LIMIT_PER_MINUTE` in prod; add RBAC checks on protected routes.
- [ ] Tighten 2FA window back to ±30s now that the demo code refreshes.

## 3. P1 — operate "without anomalies"
- [ ] **Observability**: Sentry (errors) + structured JSON logs + basic metrics/alerts + uptime monitor.
- [ ] **CI/CD**: GitHub Actions to run `pytest`, `ruff`, `npm lint/typecheck/build` on push (+ deploy).
- [ ] **E2E tests** (Playwright) for the core flows: signup → dashboard → mobile 2FA → support → waitlist.
- [ ] **Email (SES)**: lead + escalation notifications, transactional email, and a real **password‑reset** flow.

## 4. Data / research (drop‑in when ready)
- [ ] When the **Sharadar SF1** key arrives → add `NASDAQ_DATA_LINK_API_KEY` to Secrets;
      integrate value/quality/growth factors; re‑run the equity OOS back‑test to **|t| ≥ 2.0** and report.
- [ ] Optionally add `FRED_API_KEY` (macro) and `TWELVEDATA_API_KEY` (licensed quotes) to go fully live.

## 5. P2 — top‑tier polish
- [ ] Compliance/legal: Terms, Privacy, disclaimers; GDPR/CCPA; advice/RIA positioning; SOC 2 path.
- [ ] DR: backups + restore drill; IaC (Terraform/CDK) for reproducible infra.
- [ ] Performance/a11y/SEO pass; founder "ticket inbox" UI for escalated agent tickets.

## Suggested first task tomorrow
**Migrate the CRM module to Postgres** (self‑contained, high‑value template) + wire the
`/account` and `/portfolio` pages to live data — then repeat the pattern for the other
modules. Pairs well with turning on observability so we can watch for anomalies.
