# John Henry Investments — Next Session To‑Do

Start-of-day checklist. Prioritized; tackle top‑down. Context lives in
`docs/ROBUSTNESS_READINESS_GAP_ANALYSIS.md`.

## Where we left off (2026‑06‑27)
- Unified, Docker‑ready platform on branch `cursor/unified-platform-0d47` (PR #13 → main).
- Production hardening done: config/secret validation, `/ready` probe, env‑gated rate
  limiting, Postgres + Docker hardening (non‑root, healthchecks, workers), Sharadar
  SF1 adapter pre‑wired (gated). Backend tests pass; build clean.
- **CRM, Accounting, and Reports/Dashboards** migrated to durable Postgres (seeded + tests).
- **IP/intangibles** capitalization + amortization accounting and **AI‑agent operating‑cost**
  treatment added to the ledger.
- Strategy/research docs added: honest **company valuation**, **services pricing‑fit**,
  **mutual + one‑way NDAs** (Delaware default), **Research Phase Two marketing strategy**
  (PR #14), and an **honest security posture & data‑protection assessment** (PR #15).

### Open PRs to triage first
- [ ] **PR #13** → merge `cursor/unified-platform-0d47` into `main` (single source of truth) or confirm we keep building on the branch.
- [ ] **PR #14** → `docs/MARKETING_STRATEGY_CAMPAIGN.md` (Research Phase Two) — review/merge.
- [ ] **PR #15** → `docs/SECURITY_POSTURE_AND_DATA_PROTECTION.md` — review/merge.

## 0. Kick‑off (5 min)
- [ ] Triage the open PRs above.
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

## Suggested first task for Saturday's session
**Start executing the security P0 list** — it directly protects clients' data and is the
highest‑trust work right now (`docs/SECURITY_POSTURE_AND_DATA_PROTECTION.md`):
1. Real **WebAuthn** biometric verification (challenge + signature + counter).
2. **Encrypt `totp_secret` at rest** (KMS) — stop storing the 2FA seed in plaintext.
3. **Swap the hand‑rolled JWT** for a vetted library (PyJWT/authlib), keep scoped tokens.
4. **Live Stripe** checkout + **webhook signature verification**.

Then resume the durability track: wire the static module pages (`/opportunities`,
`/portfolio`, `/reports`, `/due-diligence`, `/assistant`, `/account`) to live
data/actions, and migrate **integrations** to Postgres. Pair with **observability**
(Sentry + structured logs) so we can watch for anomalies as we harden.
