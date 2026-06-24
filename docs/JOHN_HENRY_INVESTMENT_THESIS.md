# John Henry Investments — Consolidated Investment Thesis (Living Document)

*One document, assembled in chronological order. The original thesis is preserved
in full (Part I), followed by each dated update in sequence (Parts II–III), and a
comprehensive current status across the whole platform (Part IV). Source of record
for the original analysis: `docs/RESEARCH_THESIS_PROBLEM_SOLUTION_FIT.md`.*

**Current headline (2026-06-24):** Proven as a *market-confirmed* solution? **FALSE.**
Proven at the **architecture + live-data plumbing** level? **TRUE.** The platform now
streams real-world data across the liquid asset classes and ships a runnable
validation harness, but the Opportunity Score's predictive validity (H5) tested
weak/insignificant and several datasets/asset classes remain incomplete.

---

## Timeline (chronological milestones)

| # | Phase | Milestone | Thesis effect |
| --- | --- | --- | --- |
| 1 | Brand | Logo + behavioral-science color system; mission statement & family narrative | Positioning/identity (no efficacy change) |
| 2 | Access | Mobile companion app — dual (web+mobile) access: password, 2FA (TOTP), biometric | Strengthens P2 (access) |
| 3 | Data audit | Identified market data was **static** literals | Exposed a core deficiency |
| 4 | Security decision | Rejected custodial crypto wallets; kept platform **non-custodial** (no key storage) | Risk/scope discipline |
| 5 | Thesis v1 | **Original problem–solution fit thesis** composed (Part I) | Design-confirmed |
| 6 | Live data | `/api/v1/market/quotes` wired to CoinGecko / Yahoo / BLS | Closes the static-data gap (liquid classes) |
| 7 | §8 execution | Live dashboard + score back-test + adoption + acquisition + coverage | **Update II:** partially market-evidenced |
| 8 | Verdict | Explicit True/False ruling | **Update III:** proven = FALSE (market) |
| 9 | Coverage | Real-time extended: FX, full curve, bond/PE/SMB proxies; FRED macro (key-gated); licensed-vendor adapter | Broadened coverage; deficiencies enumerated |
| 10 | Service | AI-agent customer-service FAQ (`/support`) | Onboarding/support surface |
| 11 | Audit | Platform conditions audit — 16 anomalies | Honest risk ledger |

---

## Part I — Original thesis (Thesis v1, preserved)

### Abstract

Individual investors, small-to-mid business acquirers, and family offices operate
in a market where decision-grade investment intelligence is **fragmented across
many tools** and **structurally gated** behind institutional cost and access
barriers. This thesis asks whether John Henry Investments (JHI) constitutes a
genuine problem-solving response to that condition. We define the problem, decompose
it into four sub-problems, and map each to concrete platform capabilities: a
standardized cross-asset **Opportunity Score**, an **AI due-diligence** workflow, a
**global macro** layer, **multi-asset portfolio tracking**, and multi-factor
**dual-access** authentication packaged as B2C + B2B SaaS. We **confirm** that (a) the
targeted problem is real and well-documented, and (b) the prototype implements a
coherent, internally consistent solution that maps 1:1 to the sub-problems. We
**withhold** confirmation of market-level efficacy pending the falsifiable validation
program in §I.8.

**Thesis statement (v1).** *John Henry Investments targets a real and structural
market problem — the fragmentation and access-asymmetry of investment intelligence
across heterogeneous asset classes — and the prototype demonstrates a coherent,
defensible solution architecture; however, confirmed market-level problem-solving is
contingent on validating the proprietary scoring model against realized outcomes and
on replacing simulated data with live, auditable feeds.*

### I.1 Introduction

The "democratization of finance" lowered the cost of *executing* trades but did not
equally democratize the *intelligence* that precedes good capital allocation.
Institutions retain an edge built on integrated research, standardized risk scoring,
disciplined due diligence, and macro context. Retail investors, SMB acquisition
entrepreneurs, and emerging family offices must instead assemble that edge from a
patchwork of disconnected products. JHI positions itself as a unified
"investment-intelligence operating system" for those under-served allocators.

### I.2 Problem statement

- **P1 — Tool fragmentation.** Allocators stitch together screeners, brokerage apps,
  macro dashboards, spreadsheet diligence, and portfolio trackers; context is lost
  between tools and there is no single decision surface.
- **P2 — Access asymmetry.** Institutional-grade research, standardized scoring, and
  structured diligence are priced/packaged for funds, not individuals, SMB buyers,
  advisors, CPAs, or small family offices.
- **P3 — No standardized cross-asset comparison.** Public equities, private
  businesses, real estate, and digital assets are evaluated with incomparable,
  ad-hoc heuristics.
- **P4 — Under-served business-acquisition workflow.** SMB/SBA acquisition analysis
  (normalized EBITDA, DSCR, SBA eligibility, document diligence) lacks the tooling
  depth that public markets enjoy.

### I.3 Market and industry context

- **Segments:** B2C retail/accredited investors and wealth builders; B2B advisors,
  CPAs, attorneys, bankers, investment firms, and family offices.
- **Demand trends:** elevated self-directed investing; an SMB ownership-transition
  wave; rising family-office formation.
- **Monetization:** Consumer ($50/mo), Professional ($299/mo), Enterprise/Family
  Office ($1,500+/mo).

### I.4 Research question and hypotheses

- **H1 (Unification):** one platform reduces tool-switching and decision latency vs a
  multi-tool baseline. (P1)
- **H2 (Access):** institutional-style workflows at consumer/professional prices
  expand access. (P2)
- **H3 (Standardization):** a single 0–100 score yields more consistent
  prioritization than ad-hoc heuristics. (P3)
- **H4 (Acquisition tooling):** a dedicated acquisition engine serves an under-tooled
  workflow. (P4)
- **H5 (Predictive validity):** the Opportunity Score is positively and significantly
  associated with realized risk-adjusted outcomes. *(The decisive, hardest claim.)*

### I.5 Proposed solution (architecture mapped to the problem)

- **Unified decision surface (P1):** dashboard, opportunities, due-diligence,
  portfolio, reports, assistant, account modules in one shell.
- **Standardized cross-asset score (P3):** the 0–100 "John Henry Opportunity Score"
  with asset-specific factor sets.
- **AI due-diligence (P4):** document-upload/risk-review plus accounting/financial
  reporting primitives.
- **Global macro layer (P1/P3):** central banks, rates, commodities, Bitcoin, and
  economic indicators.
- **Multi-asset portfolio (P1/P3):** stocks, private equity, real estate, crypto.
- **Access + trust layer (P2):** organization/role accounts, billing tiers, and dual
  (web + mobile) access with password, TOTP two-factor, and biometric sign-in.

### I.6 Problem–solution fit analysis

| Problem | Response | Fit status (v1) |
| --- | --- | --- |
| P1 Fragmentation | Unified shell | Confirmed (design) |
| P2 Access asymmetry | Tiered SaaS + multi-factor dual access | Confirmed (design) |
| P3 No cross-asset standard | 0–100 Opportunity Score | Confirmed (design); predictive validity unproven |
| P4 Acquisition tooling gap | Acquisition engine + AI diligence | Confirmed (design) |

**Interpretation (v1):** not a feature collection in search of a problem — every
capability maps to a stated sub-problem. This satisfies the **design-level**
definition of problem–solution fit, not the **market-level** one.

### I.7 Differentiation

Edge vs single-purpose tools is *integration* + a *common scoring grammar*; vs
institutional terminals it is *price/accessibility*; vs robo-advisors it is
acquisition capability across private assets. The moat depends on the **validated**
score and data network effects — neither established at v1.

### I.8 Methodology to confirm market-level fit (falsifiable)

1. Live-data substitution.
2. Score back-test (tests H5): information coefficient, decile spread, hit rate vs a
   pre-registered floor.
3. Workflow-efficiency study (H1).
4. Access/adoption study (H2): activation, conversion, retention, willingness-to-pay.
5. Acquisition-engine validation (H4) vs expert underwriters on a labeled deal set.
6. Consistency study (H3).

### I.9 Risks and threats to validity (as of v1)

Simulated data; unvalidated model (H5); prototype persistence/security (dev token,
SQLite); regulatory surface; construct validity of self-reported pains.

### I.10 Findings (v1)

1. The problem is real (P1–P4).
2. The solution is coherent and complete against the problem — **design-level fit
   confirmed.**
3. Market-level problem-solving **not yet confirmed** — conditional on live data and
   demonstrated predictive validity.

---

## Part II — Update 2026-06-24 (post-§8 execution): partially market-evidenced

Several §8 items were **built and run on real data** (`docs/SECTION_8_VALIDATION_RESULTS.md`).

**Demonstrated (upgrades):**

- **Live real-world market data wired** for the liquid classes — crypto (CoinGecko),
  equities/indices/commodities/treasury yields/REIT (Yahoo), inflation/CPI (US BLS) —
  via `/api/v1/market/quotes` and an auto-refreshing dashboard. **Closes §8.1.**
- **A runnable, honest evaluation harness** (`/api/v1/research/*`): score back-test,
  adoption KPIs, acquisition-engine validation, data-coverage matrix.
- **Acquisition engine internally consistent** (100% vs a labeled fixture);
  **adoption instrument** computes correct KPIs from real tables.

**Not proven (claims withheld):**

- **Predictive validity (H5):** back-test produced a **weak, statistically
  insignificant** information coefficient (mean IC ≈ 0.01, t-stat ≈ 0.25, hit rate
  ≈ 46%). First-pass signal only.
- **"All asset classes":** only a subset stream real-time; private/illiquid classes
  are inherently non-real-time.
- **No representative dataset:** adoption KPIs on test accounts; acquisition labels a
  synthetic fixture.

**Net standing after Update II:** **design-confirmed + partially market-evidenced.**
The §8 checklist: §8.1 ✅ done; §8.2 ⚠️ run but not passed; §8.4 ⚠️ instrument built;
§8.5 ⚠️ engine validated vs fixture; §8.1/8.3/8.6 cohort-dependent items pending.

---

## Part III — Update 2026-06-24 (verdict): proven? FALSE (market)

| Claim | Proven? |
| --- | --- |
| Market problem is real and structural | **TRUE** |
| Design-level problem–solution fit | **TRUE** |
| Live real-world data for liquid asset classes | **TRUE** |
| Runnable evaluation harness | **TRUE** |
| Real-time data across **all** asset classes | **FALSE** |
| Opportunity Score predictive validity (H5) | **FALSE** |
| Representative adoption/retention evidence | **FALSE** |
| Acquisition engine validated vs experts | **FALSE** |
| **Overall: proven, market-confirmed solution** | **FALSE** |

---

## Part IV — Current status (2026-06-24, latest)

### IV.1 What is built and live now

- **Brand & narrative:** logo + behavioral-science color system; concise hedge-fund
  mission statement and family-legacy narrative.
- **Dual access:** mobile companion app with password, TOTP two-factor (live
  auto-refreshing demo code), and biometric (WebAuthn-style) sign-in; web + mobile
  share one account. (Strengthens **P2**.)
- **Non-custodial by decision:** the platform stores **no** crypto private keys, seed
  phrases, or wallet addresses; a prototyped watch-only store was deliberately
  removed. (Risk discipline.)
- **Live market data across liquid asset classes** via `/api/v1/market/quotes`:
  crypto (CoinGecko); equities, indices, commodities, **FX**, **full treasury curve
  (3M/5Y/10Y/30Y)**, **bond ETF proxies (AGG/IG/HY/MUNI/TIPS)**, **REIT/PE/SMB
  proxies** (Yahoo); **inflation/CPI** (US BLS). Dashboard auto-refreshes (incl. new
  FX and fixed-income sections).
- **Credential-gated, implemented:** full macro **M2/GDP/unemployment** (FRED) and a
  **licensed-vendor adapter** (Twelve Data) that becomes the primary equities/FX
  source when keyed, with Yahoo fallback. Both advertise `requires_credentials`
  until a key is set.
- **AI-agent customer service:** `/support` FAQ + `/api/v1/support/ask` retrieval
  assistant with confidence scoring, follow-ups, and human escalation.

### IV.2 Data coverage and remaining deficiencies (with corrective actions)

- **Live (no key):** crypto, equities, indices, commodities, treasury curve, FX, bond
  proxies, REIT/PE/SMB proxies, CPI.
- **Key-gated:** macro (FRED) and licensed vendor → *action:* add `FRED_API_KEY` /
  `TWELVEDATA_API_KEY`.
- **Inherently non-real-time:** direct (per-property) real estate, specific private
  businesses, private-equity marks → *action:* AVM/appraisal API + GP statements +
  the model/diligence engine; public proxies cover sentiment today.
- **Not yet wired:** direct (CUSIP) fixed-income pricing → *action:* licensed
  fixed-income vendor.

### IV.3 §8 validation results (current)

- **§8.1 live data:** ✅ done. **§8.2 score back-test:** ⚠️ run; **H5 not passed**
  (weak/insignificant IC). **§8.4 adoption:** ⚠️ instrument validated; dataset
  non-representative. **§8.5 acquisition:** ⚠️ engine consistent vs fixture; no expert
  labels. **§8.3/§8.6:** pending (need a real cohort and a defined score formula).

### IV.4 Open anomalies (from the platform audit)

16 anomalies recorded in `docs/PLATFORM_AUDIT_ANOMALIES.md`. Highest priority:
work fragmented across unmerged branches (app not on `main`); default dev token
secret; an **orphaned `crypto_holdings` table with residual rows** in the dev DB;
biometric assertion not cryptographically verified; public/unauthenticated market &
research endpoints without rate limiting; predictive validity unproven (H5).

### IV.5 Net verdict and path to "proven"

**Verdict:** *proven in architecture and live-data plumbing (TRUE); not yet proven in
market efficacy (FALSE).* To flip the overall verdict to TRUE:

1. **Define and outcome-validate the Opportunity Score** so H5 clears a pre-registered
   information-coefficient floor on real history.
2. **Extend/operationalize data:** activate FRED + a licensed vendor; add direct
   fixed-income pricing; integrate AVM for real estate.
3. **Gather representative evidence:** a real user cohort (activation/retention/NRR,
   willingness-to-pay) and expert-underwriter labels for the acquisition engine.
4. **Harden + consolidate:** address audit anomalies (secrets, WebAuthn verification,
   rate limiting, CI) and merge the work into a single mainline.

Until those close, the honest, current characterization stands: **a legitimate
problem-solving artifact for a real market gap, backed by live data and a runnable
evaluation harness — but not yet a proven, market-confirmed solution.**

---

## References (in-repo)

- `docs/RESEARCH_THESIS_PROBLEM_SOLUTION_FIT.md` — original thesis + inline updates.
- `docs/SECTION_8_VALIDATION_RESULTS.md` — §8 study results (PR #8).
- `docs/MARKET_DATA_SOURCES.md`, `docs/REALTIME_ALL_ASSETS_PLAN.md` — live data + coverage (PRs #7, #9).
- `docs/CRYPTO_HOLDINGS_STORAGE.md` — non-custodial decision (PR #5).
- `docs/PLATFORM_AUDIT_ANOMALIES.md` — anomaly ledger (PR #9).
- `docs/MISSION_STATEMENT.md`, `docs/BRAND_AND_COLOR_SYSTEM.md` — identity (PRs #4, #6).
