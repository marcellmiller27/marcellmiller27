# Software Platform Audit — Checklist, Current-State Assessment & Due-Diligence Binder

> JHI-SIG: 69M2705M · Full life-cycle (cradle-to-grave) audit framework **adopted** for
> JHI Research & Analytics Firm, Inc., plus an **honest first-pass, code-grounded status**
> and the permanent **Software Due-Diligence Binder** index. Prepared for management,
> internal audit, an external CPA firm, investors, and potential acquirers.
> Not legal, tax, or security-audit certification. First pass — grades to be re-confirmed each cycle.

## How to read this
Status legend: **✅ In place** · **🟡 Partial / documented-not-implemented** · **🔴 Missing / not started** · **⚪ N/A yet** (pre-launch or not built). Severity for gaps: 🔴 High · 🟠 Medium · 🟡 Low.

---

## Executive summary (honest)
**Headline:** JHI is **strong on strategy, IP/valuation documentation, and core product/security building blocks**, and **thin on production operations, formal legal/compliance instruments, and access-control enforcement.** The platform is a **well-built pre-launch prototype**, not yet an operated production system. That is the correct posture for "make it robust and complete *before* launch."

**Notable strengths (✅):** working FastAPI + Postgres backend with **136 passing tests**, lint/format gates (ruff/eslint), Dockerized dev, same-origin API proxy; real **auth primitives** (JWT, PBKDF2, TOTP 2FA encrypted at rest, WebAuthn/biometric, Stripe **webhook signature verification**); accounting module (GL, journal posting, trial balance); a validated-with-tests **DCF/Deal X-Ray** engine; deep strategy/valuation/IP documentation; proprietary `LICENSE` + founder code signature (`JHI-SIG`).

**Top risks (🔴 High):**
1. **Authorization not enforced.** Most product endpoints have no auth (`require_admin` guards one endpoint) — see `SYSTEM_ADMINISTRATOR_MODULE.md`. Gatekeeper is P0.
2. **No CI/CD, branch protection, or automated secret/dependency scanning** (`.github/` absent) — quality/security gates are manual.
3. **No backups / disaster recovery / RTO-RPO** and **no production cloud** deployed — data-loss and continuity exposure before real customer data.
4. **No monitoring/observability/incident process** — the platform would run blind.
5. **Missing formal legal instruments** — Terms of Service, Privacy Policy, Cookie Policy, DPA, Acceptable-Use, DR/Data-Retention policies not yet adopted documents.
6. **Score not validated** (H5) and **NASDAQ derived-data rights** pending — gate any predictive/data-serving claim.
7. **IP assignment + copyright/trademark registration pending** (founder + counsel) — the platform IP isn't yet formally assigned to the corp.

**Cross-cutting finding (🟠):** **document sprawl.** Substantial governance/security/IP documentation exists but sits in **unmerged branches**, not on `main`. A due-diligence binder must point to a **single source of truth** — merge canonical docs to `main`.

**Risk rollup (first pass):** 🔴 High ≈ 7 · 🟠 Medium ≈ 10 · 🟡 Low ≈ many. Detail below.

---

## Phase-by-phase current-state status
Evidence names refer to files in this repo (on `main` unless noted).

### Phase I — Corporate Governance — 🟡 Partial
- ✅ Board minutes cadence (`docs/board/BOARD_MINUTES_*`), NDAs (`docs/legal/NDA_ONE_WAY.md`, `NDA_MUTUAL.md`), entity formed (WY Inc.) + EIN, data-license review (`docs/legal/nasdaq/SERVICE_ORDER_00151172_REVIEW.md`).
- 🔴 **Missing/not-adopted:** Terms of Service, Privacy Policy, Cookie Policy, Acceptable-Use, Cybersecurity Policy, Disaster-Recovery Policy, Data-Retention Policy, Subscription Agreement, Regulatory-Compliance Matrix, capitalized-software policy (ASC 350-40) as a **formal adopted document**.
- 🔴 **IP/Founder/Employee/Contractor assignment agreements** — pending execution (founder + counsel). *(High.)*

### Phase II — Software Planning — ✅ Strong
- ✅ Thesis/BRD-equivalent (`RESEARCH_THESIS_PROBLEM_SOLUTION_FIT.md`, `PRODUCT_BLUEPRINT.md`), roadmap/milestones (`NEXT_PROGRAMMING_MILESTONE.md`, `CODE_OBJECTIVES.md`), market/competitor research (`COMPETITOR_TEARDOWN_AND_GAP_MAP.md`, `COMPETITOR_DEEP_DIVE_PAIN_POINTS.md`), budget/cost (`CASHFLOW_PROJECTION_12MO.md`, `OPERATING_COST_LEAN_VS_STAFFED.md`, `ESTIMATED_PLATFORM_COSTS.md`), PM checklist.
- 🟡 Formal BRD/PRD, User Stories/Use Cases, Project Charter, Resource Plan — exist in spirit across docs; not consolidated into named artifacts.

### Phase III — Architecture Review — 🟡 Partial
- ✅ Flowcharts/process maps (`SYSTEM_FLOWCHARTS_AND_PROCESS_MAPS.md`), auth/DB/billing foundation (`AUTH_DATABASE_BILLING_FOUNDATION.md`), cloud/capacity plans (`CLOUD_STORAGE_AND_CAPACITY_PLAN.md`, `AWS_COST_10K_USERS.md`), data sources (`MARKET_DATA_SOURCES.md`).
- 🟡 Formal architecture/DB/API/network/security **diagrams** are partial; encryption model, HA, DR, logging & monitoring architecture documented only as targets. AI architecture minimal (deterministic today).

### Phase IV — Source Code Audit — 🟡 Partial
- ✅ Git repo + full commit history; coding standards + **static analysis** (ruff, eslint); proprietary `LICENSE`; prior code audits (`SRC_CODE_AUDIT.md`, `PLATFORM_AUDIT_ANOMALIES.md`).
- 🔴 **No branch protection, no required PR reviews, no CI** (`.github/` absent); **no automated secret scanning / dependency (SCA) / open-source-license scanning**; no CODEOWNERS. *(High — process controls are manual.)*
- 🟡 Technical-debt register and API-key-management policy not formalized. **Recommend:** enable branch protection + a CI workflow (tests, ruff, eslint, secret scan, dependency review) and Dependabot.

### Phase V — Database Audit — 🟡 Partial
- ✅ Relational model (SQLAlchemy, Postgres), constraints/indexes on keys, parameterized ORM (no raw SQL injection surface), encryption in transit (TLS in prod), **field-level encryption** for TOTP secrets.
- 🔴 **No automated backups, no recovery testing, no archival/retention job.** *(High.)* Full at-rest encryption depends on the (not-yet-deployed) cloud DB. Data dictionary partial.

### Phase VI — Infrastructure Audit — ⚪/🔴 Not built (dev only)
- ✅ Dockerized dev (compose), SSL/DNS/CDN/load-balancing planned (`AWS_COST_10K_USERS.md`).
- 🔴 **No production cloud deployed** — most items (IAM, firewalls, VPN, containers/K8s, patch mgmt, backup testing, monitoring) are **planned, not implemented.** Expected pre-launch build-out.

### Phase VII — Security Audit — 🟡 Partial
- ✅ **MFA** (TOTP + WebAuthn ES256), PBKDF2, scoped tokens, Stripe webhook verification, env-gated rate limiting, OWASP considerations documented.
- 🔴 **AuthZ not enforced** on most endpoints; **no vulnerability scanning / penetration test / SIEM / SOC logging / threat detection / endpoint protection / Zero-Trust review**; **no key rotation**; **no formal incident-response plan**; password policy minimal (length only). *(High.)* **Recommend:** endpoint lockdown (System Admin P0), a pre-launch pen-test, and a written incident-response plan.

### Phase VIII — Mobile App Audit — ⚪ N/A (no native app yet)
- **Clarification needed:** JHI currently has a **mobile *web* companion** (`/mobile`, Next.js) with real auth/2FA/biometric calls — **not** native iOS/Android apps (no Xcode/Gradle/React-Native/Capacitor project present).
- ⚪ Therefore App Store/Play compliance, code signing, APK/IPA security, push, native secure storage, etc. are **N/A until native apps are built.** If native is on the roadmap, this becomes a dedicated workstream.

### Phase IX — Application Testing — 🟡 Partial
- ✅ **Unit + integration tests** (136 backend via pytest), frontend build/lint, API tests.
- 🔴 No formal **load/stress/scalability, UAT, accessibility, cross-browser, or localization** testing; no coverage gate in CI (no CI). *(Medium.)*

### Phase X — Data Governance — 🟡 Partial
- ✅ **Audit trail** table (`AuditLogDB`, auth events), classification/privacy discussed in posture docs.
- 🔴 Formal **Data Dictionary, data ownership, classification policy, GDPR/CCPA review, retention/deletion policy, data-subject export/delete** not implemented. *(Medium.)*

### Phase XI — Financial Software Audit — 🟡 Partial
- ✅ Accounting module: chart of accounts, **balanced double-entry journal posting**, trial balance, GL; **Stripe** integration + webhook verification; deferred-revenue & AR accounts modeled.
- 🟡/🔴 **No automated revenue recognition**, no ACH, no **refund controls**, sales-tax flagged for CPA, no journal **approval workflow**. Note: the **full 111-account GAAP chart of accounts (PR #54) is NOT on `main`** (see merge-hygiene finding) — `main` still has the 16-account placeholder. *(Medium.)*

### Phase XII — AI Review — 🟡 Partial (deterministic today)
- ✅ AI service agents are **deterministic** (no external LLM) with **human oversight/escalation**; scoring is algorithmic.
- 🟡 Model governance = the H5 validation protocol (**score not yet validated**). If/when an LLM is introduced: prompt-security, hallucination/bias testing, data-leakage review, AI logging/monitoring become required. Human-oversight design is documented in the System Admin write-up (agents-as-admins). *(Medium.)*

### Phase XIII — Research Platform Review — 🟡 Partial
- ✅ Valuation/DCF engine with **unit tests** (Deal X-Ray), five-stage valuation model, ratio/scoring methodology, acquisition/search-fund templates, educational/no-advice framing in posture docs.
- 🔴 **No research-publishing workflow / editorial approvals / research version control / audit trail of published research**; disclaimer placement not systematically enforced in-product. Rating methodology unvalidated (H5). *(Medium.)*

### Phase XIV — Compliance — 🟡 Early
- ✅ Software-publisher posture (not investment adviser), copyright/trademark plan, Stripe = **no card data stored** (favorable for PCI scope).
- 🔴 **SOC 2 / ISO 27001 readiness not started; ADA/accessibility not audited; SEC/FINRA advertising review, open-source-compliance scan not performed.** *(Medium.)*

### Phase XV — Operations — 🔴 Mostly missing (pre-launch)
- 🔴 No incident/change/release/patch management, monitoring, uptime/SLA tracking, RCA process, or capacity plan **in operation.** Expected pre-launch build-out. *(High for launch readiness.)*

### Phase XVI — Documentation — 🟡 Partial
- ✅ Extensive **internal** docs; **auto-generated API docs** via FastAPI OpenAPI (`/docs`).
- 🔴 No end-user manual, **administrator manual**, installation/ops/security/DR manuals, or training materials. *(Medium.)*

### Phase XVII — Intellectual Property Audit — 🟡 Partial (key items pending)
- ✅ Source/backend/DB code in-repo with **founder signature** (`JHI-SIG: 69M2705M`) + proprietary `LICENSE`; valuation/IP docs (`IP_INTANGIBLES_AMORTIZATION.md`, `COMPANY_VALUATION_ANALYSIS.md`); proprietary algorithms (score/DCF) documented.
- 🔴 **IP Assignment to the corp, trademark & copyright *registration*, and domain-ownership record are pending** (founder + counsel). Customer-list/trade-secret controls informal. *(High — the corp should formally own the IP before financing/valuation/sale.)*

### Phase XVIII — Software Asset Valuation Support — ✅/🟡 Good
- ✅ IP/intangibles amortization (`IP_INTANGIBLES_AMORTIZATION.md`), valuation models (`FIVE_STAGE_VALUATION_MODEL.md`, `COMPANY_VALUATION_ANALYSIS.md`, `investor_package/FINANCIAL_MODEL_DCF.md`), projected EBITDA, coding-effort/value analysis, ASC 350-40 referenced.
- 🟡 **Independent third-party valuation** and formal **capitalized-software cost audit** (payroll/contractor invoices tie-out, impairment test) not yet performed; source-code inventory to be formalized. *(Medium — needed for a defensible capitalization/valuation.)*

### Phase XIX — Business Continuity — 🔴 Missing
- 🔴 No DR test, **RTO/RPO undefined**, no verified backups, no cloud redundancy, no incident-communications or vendor-contingency plan. *(High — before real customer data.)*

### Phase XX — End-of-Life (Retirement) — ⚪ N/A yet
- ⚪ Pre-launch; no retirement/migration/escrow/secure-destruction plan. Add **source-code escrow** consideration if selling to enterprises. Revisit near/after launch.

---

## Expected deliverables — where we stand
| # | Deliverable | Status | Source / next step |
|---|---|---|---|
| 1 | Executive Summary | ✅ | This doc (§ Executive summary) |
| 2 | Risk Assessment (H/M/L) | ✅ first pass | This doc (per-phase severities) |
| 3 | Internal Controls Evaluation | 🟡 | Expand from Phases I/IV/VII/XI/XV |
| 4 | Cybersecurity Assessment | 🟡 | Phase VII + a pen-test |
| 5 | Source Code Quality Report | 🟡 | `SRC_CODE_AUDIT.md` + CI/static-analysis output |
| 6 | Mobile Application Assessment | ⚪ | N/A until native apps exist (web companion only) |
| 7 | Infrastructure Review | 🔴 | After cloud build-out |
| 8 | Compliance Review | 🟡 | Phase XIV + counsel |
| 9 | IP Audit Report | 🟡 | Phase XVII + executed assignment/registrations |
| 10 | Capitalized Software Cost Audit | 🟡 | Phase XVIII + CPA tie-out |
| 11 | Software Asset Valuation Support | ✅/🟡 | Valuation docs + independent valuation |
| 12 | BC/DR Assessment | 🔴 | After DR build-out + test |
| 13 | Management Letter | 🟡 | Compile from findings |
| 14 | Remediation Plan (prioritized) | ✅ | Below |

---

## Software Due-Diligence Binder (permanent digital data room)
Recommended folder structure — one folder per phase, each holding the canonical evidence. Valuable for SBA/bank financing, acquisitions, enterprise sales, company sale, third-party valuation, and a GAAP financial-statement audit.

```
/JHI_Due_Diligence_Binder
├── 01_Corporate_Governance/     board minutes, policies, IP assignments, NDAs
├── 02_Planning/                 BRD/PRD, roadmap, market/competitor, budget
├── 03_Architecture/             diagrams (system/DB/API/network/security)
├── 04_Source_Code/              audit reports, CI results, SCA/secret-scan, LICENSE
├── 05_Database/                 data model, backup/restore evidence, retention
├── 06_Infrastructure/           cloud config, IAM, network, patch/monitoring
├── 07_Security/                 posture, pen-test, incident-response, key mgmt
├── 08_Mobile/                   (web companion today; native if/when built)
├── 09_Testing/                  test reports, coverage, load/UAT/accessibility
├── 10_Data_Governance/          dictionary, classification, GDPR/CCPA, audit trail
├── 11_Financial_Software/       rev-rec, Stripe, GL/trial-balance, controls
├── 12_AI/                       model governance, validation, oversight, logging
├── 13_Research_Platform/        methodology, DCF validation, publishing/audit trail
├── 14_Compliance/               SOC2/ISO readiness, ADA, copyright/trademark
├── 15_Operations/               incident/change/release, SLA, monitoring, RCA
├── 16_Documentation/            user/admin/API/ops/security/DR manuals
├── 17_Intellectual_Property/    ownership, registrations, algorithms, trade secrets
├── 18_Software_Asset_Valuation/ ASC 350-40 policy, cost tie-out, amortization, valuation
├── 19_Business_Continuity/      DR test, RTO/RPO, backups, comms plan
└── 20_End_of_Life/              retirement, escrow, secure destruction
```
**Maintenance rule:** the binder points only to **canonical, merged-to-`main`** sources (or executed originals). Keep a top-level `INDEX` with document name, owner, version/date, and status.

---

## Prioritized remediation plan
Aligns with the launch-readiness gates in `docs/board/BOARD_MINUTES_2026-07-12.md` (unmerged) and the System Admin P0.

**Tier 1 — 🔴 do before onboarding any external users**
1. **Enforce authorization** across all endpoints + System Admin P0 (gatekeeper).
2. **Backups + tested restore** (RTO/RPO defined); basic BC/DR plan.
3. **CI/CD + branch protection + secret & dependency scanning**; required PR review.
4. **Observability**: error tracking, structured logs, uptime/alerting.
5. **Adopt core legal instruments**: ToS, Privacy, Cookie, Acceptable-Use, DPA; capitalized-software policy (ASC 350-40).
6. **Execute IP assignment to the corp**; file copyright/trademark; record domain ownership.

**Tier 2 — 🟠 before public/paid launch**
7. Validate the score (H5) or gate all predictive claims; secure NASDAQ derived-data rights.
8. Pen-test + incident-response plan + key rotation; enforce data entitlements.
9. Revenue-recognition + refund controls + journal approvals; sales-tax with CPA.
10. Data governance: dictionary, classification, GDPR/CCPA, deletion/export.
11. Merge canonical docs to `main` (fix document sprawl) and stand up the binder.

**Tier 3 — 🟡 maturity / scale**
12. SOC 2 / ISO 27001 readiness; ADA/accessibility; load/scalability testing.
13. Independent software valuation + capitalized-cost audit tie-out.
14. Native mobile audit workstream (if native apps are built); EOL/escrow plan.

---

## Questions for you
1. **Mobile:** confirm scope — is the roadmap a **native iOS/Android app**, or is the **`/mobile` web companion** the intended mobile experience? (Determines whether Phase VIII is a real workstream or N/A.)
2. **Binder build-out:** want me to **create the 20-folder binder** in-repo (as `docs/due_diligence_binder/` with an INDEX and stubs pointing to canonical docs), and **merge the canonical scattered docs to `main`** so the binder has a single source of truth?
3. **External audit:** will an **external CPA/security firm** perform the formal audit (this doc becomes their prep pack), or should I keep expanding it into the full internal audit?
4. **Sequencing:** confirm the Tier-1 remediation order, and whether it runs **before** or **in parallel** with the System Admin build.

---

*Provenance: founder signature of record `69M2705M`. © 2026 JHI Research & Analytics Firm, Inc. All rights reserved. Confidential.*
