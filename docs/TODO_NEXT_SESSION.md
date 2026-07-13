# John Henry Investments — Next Session To‑Do

Start-of-day checklist. Prioritized; tackle top‑down. Context lives in
`docs/ROBUSTNESS_READINESS_GAP_ANALYSIS.md`.

## Where we left off (2026-07-13) — CLEAN START
**Merged to `main` today:** #48 (NAICS/posture), #49 (IP valuation — corrected: $0.0001 par → Common Stock $1,000 + APIC $399,000), #50 (commission ramp), #55 (System Admin design + 07-12 minutes), #56 (Cy Henry on Team), #57 (software audit + due-diligence binder), #58 (glossary/acronyms). Earlier: #51 (accounting), #52 (finance model + competitor), #59 (full Chart of Accounts + Documents page).

**Decisions locked:** IP-for-stock §351 (10M shares → Common Stock $1,000 + APIC $399,000); founder comp **$1/yr + discretionary benchmark bonuses** (founder discretion); software-publisher posture (never manages outside money; private/bootstrapped; no outside investors by default, optionality retained); NASDAQ addendum drafted (SaaS + external Derived-Data + Sharadar consent); `investor_package` → `internal_valuation_package`.

### 🔴 1. Merge the 3 still-open PRs first
- [ ] **#60** — LICENSE + governance docs (posture/security/org charts/copyright) + **durable Postgres integrations (#33)** + **authoritative NASDAQ T&Cs + review**.
- [ ] **#61** — `investor_package` → `internal_valuation_package` (internal relabel; optionality retained).
- [ ] **#62** — 2026-07-13 board minutes (founder comp + resolutions).

### 🔴 2. Security rescue → close stale stack → Gatekeeper P0
1. [ ] **Rescue #17 security hardening** onto `main` (encrypted TOTP at rest, PyJWT, **Stripe webhook verification**, **real WebAuthn**) — confirmed NOT on `main`; do this **before** P0 so the gatekeeper sits on hardened auth.
2. [ ] Rescue remaining not-on-`main` code: **#34** (module live-data wiring), **#30/#27** (SF1 fundamentals + R&D validation); verify #20, #25, #29, #31.
3. [ ] **Close the entire stale #9–#41 stack** — only after the rescues above (content preserved).
4. [ ] **Build Gatekeeper P0** (System Admin): `require_permission` + RBAC seed (8 roles → permission sets) + enforce auth across all endpoints **behind an `ENFORCE_AUTH` flag** + user management (invite/deactivate/role/reset-MFA) + admin-MFA + full audit + `/admin` UI. Spec: `docs/SYSTEM_ADMINISTRATOR_MODULE.md`.
5. [ ] **P1 right after:** data-entitlement + purge (NASDAQ compliance), org-admin tier, refresh tokens + revocation.

### 🟠 3. Founder action items (external)
- [ ] **CPA:** confirm $1 salary/bonus payroll mechanics; execute §351 **IP assignment + stock ledger** + opening-cash JE at bank-account opening.
- [ ] **NASDAQ:** get the **addendum counter-signed** (SaaS + external Derived-Data + Sharadar consent) by an authorized signatory — email isn't binding (§22).
- [ ] Confirm debt clarification (equity: none ever; **debt/lending: allowed?**) so the posture doc is exact.

### 🟡 4. Launch-readiness gates (go/no-go — `docs/SOFTWARE_PLATFORM_AUDIT.md`)
authZ + admin · score validation (H5) · NASDAQ derived-data rights · prod security hardening · backups/DR · observability · legal (ToS/Privacy/DPA) · billing↔access coupling.

---

## Where we left off (2026‑07‑05)
- **Financial Diligence Suite shipped** (branch `cursor/financial-diligence-suite-0d47`): software-accelerated Quality-of-Earnings — proof-of-cash, EBITDA normalization, NWC peg, revenue quality, debt-like items, Financial Integrity Score, tiered pricing, and partner-CPA engagement quotes. Backend `financial_diligence` (engine/models/router at `/api/v1/financial-diligence/*`), web `/diligence-suite` page + nav, and a mobile "Run Financial Diligence" screen (all hitting the same endpoint). **CPA function is outsourced to a partner network — not an owned firm.** Ref: `docs/FINANCIAL_DILIGENCE_SUITE_CONCEPT.md`.
- **Deal X-Ray hardened** (PR #36): blended-earnings basis, curbed DCF, concentration/volatility ethics, asset-light capex — validated on the real Carrollton Design Build CIM.
- Board minutes: `docs/board/BOARD_MINUTES_2026-07-04.md`.

### Next up
- [ ] **Founder:** engage counsel for the Financial Diligence Suite (fee structure vs. AICPA 1.520, partner agreements, engagement letters); recruit/vet the partner-CPA network; validate the pricing table.
- [ ] Extend the Integrations module to feed QoE workpapers (accounting connectors / uploads / bank statements).
- [ ] Decide the Deal X-Ray segment-section title (Business Quality Assessment vs. Six-Pillar Business Assessment) → Cy ships the one-line copy change.
- [ ] Consider CIM PDF upload → auto-extract (Deal X-Ray v2) + printable one-page PDF reports.

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
