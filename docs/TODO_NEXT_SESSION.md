# John Henry Investments — Next Session To‑Do

Start-of-day checklist. Prioritized; tackle top‑down. Context lives in
`docs/ROBUSTNESS_READINESS_GAP_ANALYSIS.md`.

---

## 🔝 Current Work Group (2026-07-23) — prioritized

> Nomenclature is living (Founder). Standing rule: kindergarten/elementary terms → institutional-grade;
> two layers (institutional **display** names vs. stable **internal** ids); dictated headings use **Title Case**.

### ✅ Completed 2026-07-20 → 22 (merged to `main`)
Rule B monochrome (#91) · "Macro" → "Economics" + Title-Case heading (#92) · same-origin API fix (#93) ·
NASDAQ resolution / **closed** (#94) · 5-day trial **5h** contingency + back-up (#95) · TOC → **left** menu
drawer (#96) · Work Group (#97, #101) · **Editorial system** — newsletters + **VP of Editorial (Ellery Vance)**
+ subscribe (#98) · **Ellery portrait** on Team + every byline (#100) · **42 Macro competitor audit** (#102) ·
**Editorial-access module (A)** — role-aware menu + free/paid teaser gating (#103) · board minutes (#89, #99).

### ✅ Completed 2026-07-23 (merged to `main`)
RBAC foundation (#104) · Newsletter server-side PDF, role-aware (#109) · **Re-land** of institutional
type-scale + two-step subscription cancellation + god-eye menu fix (#115, replacing the falsely-"merged"
#108) · Editorial **E1** house style + methodology disclosure (#113) · board minutes 07-23 + storefront
hash-marks removed (#110) · launch-readiness package (#112) · **E2 vendor shortlist** (#114).

### 🔵 Open PR — review / merge
- [ ] **#106** — Back-office / ERP build plan (docs).
- [ ] **#107** — Enterprise architecture review (docs).
- [ ] **#105** — this Work Group refresh.
- [x] **Close #108** (superseded by #115) and **#111** (Newsletter link already on `main` via #104).

### 🆕 New this session (2026-07-23) — Founder review feedback
- [ ] **🔴 Institutional-grade storefront copy rewrite.** The marketing descriptions (home hero, "What you get", "How it works", "Who it's for", pricing feature lines) are **not** the professional voice required for **JHI Research & Analytics Firm, Inc.** *Founder to provide voice/scope; then Cy executes the rewrite.* Also **reconcile the legacy "John Henry Investments" brand mark** on the home hero to the single institutional entity name. (Board minutes 2026-07-23 §5.)
- [ ] **🟡 Activate "Generate report preview."** Root cause: unwired placeholder button (no `onClick`) on `src/app/reports/page.tsx`. Proposed: wire report cards to the #109 server-side PDF engine / matching `/newsletters` edition. *Needs founder authorization on the report→output mapping* (3 editions vs. 4 report cards). (Board minutes 2026-07-23 §6.)
- [x] **Hash-marks removed on the storefront** (gold "/" list markers on pricing/marketing lists). In-app + newsletters were already clean (Rule B #91). (Board minutes 2026-07-23 §7.)
- [ ] **Per-plan feature/seat gating** (clarified): not enforced yet — scheduled at **Gatekeeper P0** (mechanism) → **P1** (entitlements + seat self-management) → **Phase 6** (full seat/billing + premium-route enforcement).
>>>>>>> origin/main

### 1. 🔴 Founder actions (unblock the next builds)
- [ ] **Add `AUTH_JWT_SECRET` to Secrets** (strong value) — **without it the backend 500s on every login/register** (a dev secret was used to test #104). Blocks real auth in a fresh environment.
- [ ] **Upload the new NASDAQ Order Form** → Cy pins the **5h** pass/fail test.
- [ ] **Add email-provider (SES) credentials** → Cy turns on newsletter email (Step B send).
- [ ] Add `TWELVEDATA` / `NASDAQ_DATA_LINK` / `FUNDAMENTALS` keys when ready (extra feeds).
- [ ] **Decision:** approve a distinct **"staff/employee" role** so Accounting/admin is staff-gated (today every registrant is org `admin`; Accounting is auth-gated only).

### 2. 🟣 NOMENCLATURE (Founder mulling; will lock terms)
- [ ] Finalize **List 1 (Macro scrub)** + **List 2 (elementary page titles)** → lock display names.
- [ ] Founder-decided: Economics title → **Economic Tracking**; heading → **Federal & Global Markets** *(supersedes #92's shipped strings — reconcile on the sweep).*
- [ ] Execute the sweep in one consistent pass (display-only; internals untouched).

### 3. 🟢 Build phases (foundation-first; each its own tested PR off `main`)
- [ ] **Phase 3.1** — backend entity schema (Postgres nodes/edges + `/api/v1/entities` + seed; rewire `src/lib/entities.ts`). *(Unblocks 4–5.)*
- [ ] **Phase 4** — "Diligence a Target" shared engines + **Buyer Match** (LSR ↔ Buyer Match loop).
- [ ] **Phase 5** — EDGAR financials/valuation depth on records; client-upload later.
- [ ] **Phase 6** — launch gates: mobile parity, seat/billing enforcement, empty/error states.

### 4. 🔒 RBAC hardening (follow-ups to #104)
- [ ] Add the **staff role** + staff-gate Accounting/admin (proxy + API).
- [ ] Verify the JWT in the proxy (call `/auth/me`) and/or move issuance to an **httpOnly** server cookie.
- [ ] Extend `require_permission`/RBAC coverage across all premium backend APIs (Gatekeeper P0).

### 5. ✍️ Editorial roadmap (VP of Editorial) — informed by the 42 Macro audit (#102)
- [ ] **Visual layer:** per-edition hero image + **regime quadrant** + **signal heat map** → then time-series charts + risk/reward scatter (biggest credibility gap vs. 42 Macro).
- [ ] **Step B email send** (after SES): email-ready render + scheduler + unsubscribe/CAN-SPAM.
- [ ] New editions: **Insider Briefs**; expand Red Alerts / Opportunity Scans. Differentiate on **macro × company/deal** links (our moat).

### 6. 🟠 NASDAQ / legal (`docs/legal/nasdaq/`)
- [ ] If **5h fails** in the trial → refute MSA, execute back-up (FMP → Tiingo → Intrinio → EODHD, + free EDGAR).
- [ ] Enforce **no data-set spillage** when wiring Nasdaq Data Link (isolate licensed set, derived-only, provenance tags).
- [ ] Seat basis: Tiers 1–3 = 1 user-seat; additional at current rates; revisit at 1,000 subs/seats.

### 7. ⚪ Design / UX follow-ups
- [ ] Review **Rule B** (full-grayscale or two-tone option; centralized on `.app-main` + `--severity`).
- [ ] Align remaining page titles/eyebrows to menu labels (elementary List 2); optional storefront "macro" pass.

### 8. 💡 Ideas meeting (when ready)
Buyer Match design · data-sourcing depth · lock the monochrome-vs-accent principle · 30-rep GTM · mobile parity.

---

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
