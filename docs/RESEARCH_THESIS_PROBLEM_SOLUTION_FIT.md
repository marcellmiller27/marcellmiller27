# Does John Henry Investments Solve a Real Industry Problem? A Problem–Solution Fit Thesis

*A research-paper-style thesis evaluating whether the John Henry Investments
platform addresses a genuine, identifiable problem in the investment-intelligence
and wealth-technology market.*

**Status of evidence:** the platform in this repository is a working **prototype**.
This paper confirms problem–solution fit at the **architecture and design** level
using direct evidence from the codebase, and specifies the empirical methodology
required to confirm fit at **market** scale. As of the 2026-06-24 update below,
parts of the §8 program have been executed, upgrading the evidence to
**design-confirmed + partially market-evidenced** (see "Status update").

> **PROVEN AS A MARKET-CONFIRMED SOLUTION: FALSE.** Proven at the architecture and
> live-data level (TRUE); not proven at market efficacy (H5 unproven; coverage and
> datasets incomplete). See the "Verdict" table below.

---

## Verdict — Proven? **FALSE** (as a market-confirmed solution)

Explicit, claim-by-claim ruling as of 2026-06-24:

| Claim | Proven? |
| --- | --- |
| The targeted market problem is real and structural | **TRUE** |
| Design-level problem–solution fit (features map 1:1 to the problem) | **TRUE** |
| Live real-world data is wired for liquid/tradable asset classes | **TRUE** |
| A runnable, honest evaluation harness exists | **TRUE** |
| Real-time data across **all** asset classes | **FALSE** (partial: live for liquid + public proxies; FRED macro key-gated; private/illiquid inherently non-real-time) |
| Opportunity Score has demonstrated predictive validity (H5) | **FALSE** (back-test IC weak & statistically insignificant) |
| Representative adoption / retention / willingness-to-pay evidence | **FALSE** (test accounts only) |
| Acquisition engine validated against expert underwriters | **FALSE** (synthetic fixture only) |
| **Overall: a proven, market-confirmed solution** | **FALSE** |

**Bottom line:** the thesis is **proven at the architecture and live-data-plumbing
level (TRUE)** but **not proven at the market-efficacy level (FALSE)**. Calling it a
"proven solution" overall would be false until H5 passes a pre-registered IC floor
on a defined score and representative usage/expert datasets exist.

---

## Status update — 2026-06-24 (post-§8 execution)

Several §8 items have now been **built and run on real data** (companion PR #8;
results in `docs/SECTION_8_VALIDATION_RESULTS.md`). This materially strengthens the
thesis, but does **not** make it a fully "proven solution," and the platform does
**not** yet have real-time data for *all* market classes. Precise standing:

**What is now demonstrated (upgrades to the thesis):**

- **Live real-world market data is wired** for the tradable/liquid classes —
  crypto (CoinGecko), equities/indices/commodities/treasury yields/REIT proxy
  (Yahoo Finance), and inflation/CPI (US BLS) — surfaced via `/api/v1/market/quotes`
  and rendered on an auto-refreshing dashboard. This **closes §8.1** and removes the
  earlier "static data" limitation for those classes.
- **A runnable, honest evaluation harness exists** (`/api/v1/research/*`): score
  back-test, segment-adoption KPIs, acquisition-engine validation, and a data-
  coverage matrix — i.e., the thesis is now **empirically testable**, not just
  asserted.
- **The acquisition engine is internally consistent** (100% agreement vs a labeled
  fixture), and the **adoption measurement instrument** computes correct KPIs from
  real platform tables.

**What is NOT yet proven (claims deliberately not made):**

- **Predictive validity (H5) is unconfirmed.** The score back-test on real history
  produced a **weak, statistically insignificant** information coefficient
  (mean IC ≈ 0.01, t-stat ≈ 0.25, hit rate ≈ 46%). This is first-pass signal only;
  it does **not** prove the score works.
- **"All market classes" is not accurate.** Only **7 of 14** tracked categories
  have real-time feeds. FX, corporate/muni bonds, and full macro (FRED) are not
  wired; direct real estate, private businesses, and private equity are inherently
  non-real-time.
- **No representative market dataset.** Adoption KPIs run on development/test
  accounts; acquisition labels are a synthetic fixture, not expert-underwriter
  ground truth.

**Net standing:** problem–solution fit is **design-confirmed and now partially
market-evidenced**. It is **not** a fully proven, market-confirmed solution: that
still requires a defined, outcome-validated score (H5) and representative
usage/expert datasets. The remaining gaps are enumerated in
`docs/SECTION_8_VALIDATION_RESULTS.md` ("Confirmed deficiencies").

---

## Abstract

Individual investors, small-to-mid business acquirers, and family offices operate
in a market where decision-grade investment intelligence is **fragmented across
many tools** and **structurally gated** behind institutional cost and access
barriers. This thesis asks whether John Henry Investments (JHI) constitutes a
genuine problem-solving response to that condition. We define the problem,
decompose it into four sub-problems, and map each to concrete platform
capabilities evidenced in the codebase: a standardized cross-asset **Opportunity
Score**, an **AI due-diligence** workflow, a **global macro** layer, **multi-asset
portfolio tracking** (including a non-custodial crypto holdings store), and
multi-factor **dual-access** authentication packaged as B2C + B2B SaaS. We
**confirm** that (a) the targeted problem is real and well-documented, and (b) the
prototype implements a coherent, internally consistent solution that maps 1:1 to
the sub-problems. As of the 2026-06-24 update, we have **partially executed** §8: live market data is
wired for the liquid asset classes and the evaluation harness runs on real data. We
still **withhold** confirmation of market-level efficacy, because the score's
predictive validity (H5) tested **weak and insignificant**, several asset classes
lack real-time feeds, and there is no representative usage cohort.

**Thesis statement.** *John Henry Investments targets a real and structural market
problem — the fragmentation and access-asymmetry of investment intelligence across
heterogeneous asset classes — and the prototype demonstrates a coherent,
defensible solution architecture now backed by live real-world data across the
liquid asset classes and a runnable evaluation harness; however, fully confirmed
market-level problem-solving still depends on validating the proprietary scoring
model against realized outcomes (H5 remains unconfirmed) and on extending live data
to the asset classes that still lack it.*

---

## 1. Introduction

The "democratization of finance" lowered the cost of *executing* trades but did
not equally democratize the *intelligence* that precedes good capital allocation.
Institutions retain an edge built on integrated research, standardized risk
scoring, disciplined due diligence, and macro context. Retail investors, SMB
acquisition entrepreneurs, and emerging family offices must instead assemble that
edge from a patchwork of disconnected products. JHI positions itself as a unified
"investment-intelligence operating system" for exactly those under-served
allocators (see `README.md`, `docs/PRODUCT_BLUEPRINT.md`).

This paper evaluates the central question: **has the platform created a genuine
problem-solving artifact for this market, or is it a feature collection in search
of a problem?**

---

## 2. Problem statement

The market pain decomposes into four sub-problems:

- **P1 — Tool fragmentation.** Allocators stitch together screeners, brokerage
  apps, macro dashboards, spreadsheet diligence, and portfolio trackers. Context is
  lost between tools, and there is no single decision surface.
- **P2 — Access asymmetry.** Institutional-grade research, standardized scoring,
  and structured diligence are priced and packaged for funds, not for individuals,
  SMB buyers, advisors, CPAs, or small family offices.
- **P3 — No standardized cross-asset comparison.** Public equities, private
  businesses, real estate, and digital assets are evaluated with incomparable,
  ad-hoc heuristics, making portfolio-level prioritization subjective.
- **P4 — Under-served business-acquisition workflow.** SMB/SBA acquisition
  analysis (normalized EBITDA, DSCR, SBA eligibility, document diligence) lacks the
  tooling depth that public markets enjoy, despite a large search-fund / SMB
  ownership-transition wave.

These are independently documented industry conditions, not artifacts invented to
justify the product; the platform's own blueprint frames the same pains
(`docs/PRODUCT_BLUEPRINT.md`).

---

## 3. Market and industry context

- **Segments served (TAM framing).** B2C retail/accredited investors and wealth
  builders; B2B advisors, CPAs, attorneys, bankers, investment firms, and family
  offices. The platform encodes these segments directly as `userTypes` and tiered
  packaging (`src/lib/platform-data.ts`, `src/app/pricing/page.tsx`).
- **Demand trends.** Retail participation and self-directed investing are
  structurally elevated; SMB ownership transition is fueling business acquisitions;
  family-office formation is rising. Each expands the population that needs
  institutional-style intelligence without institutional infrastructure.
- **Monetization model.** Consumer ($50/mo), Professional ($299/mo), and
  Enterprise/Family Office ($1,500+/mo) tiers (`src/lib/platform-data.ts`), a
  conventional and validated SaaS packaging shape for this market.

---

## 4. Research question and hypotheses

**RQ.** Does JHI's architecture constitute a genuine, differentiated solution to
P1–P4, and is that solution empirically validatable?

- **H1 (Unification).** A single platform that co-locates discovery, scoring,
  diligence, macro, and portfolio reduces tool-switching and decision latency vs a
  multi-tool baseline. *(Addresses P1.)*
- **H2 (Access).** Packaging institutional-style workflows at consumer/professional
  price points expands access to non-institutional allocators. *(Addresses P2.)*
- **H3 (Standardization).** A single 0–100 Opportunity Score across asset classes
  yields more consistent prioritization than ad-hoc heuristics. *(Addresses P3.)*
- **H4 (Acquisition tooling).** A dedicated business-acquisition engine
  (EBITDA/DSCR/SBA/diligence) serves a measurable, under-tooled workflow.
  *(Addresses P4.)*
- **H5 (Predictive validity — the hard one).** The Opportunity Score is positively
  and significantly associated with realized risk-adjusted outcomes. *This is the
  hypothesis on which durable problem-solving ultimately rests, and it is not yet
  tested.*

---

## 5. The proposed solution (architecture mapped to the problem)

JHI implements a multi-asset intelligence stack. Evidence from the codebase:

- **Unified decision surface (P1).** A single application shell exposes dashboard,
  opportunities, due-diligence, portfolio, reports, assistant, and account modules
  (`src/components/platform-shell.tsx`, `src/app/*`). The dashboard co-locates
  portfolio metrics, macro signals, and AI recommendations
  (`src/app/dashboard/page.tsx`).
- **Standardized cross-asset score (P3).** The "John Henry Opportunity Score"
  applies a common 0–100 scale across stocks, businesses, and crypto with
  asset-specific factor sets (`scoreCategories`, `opportunities` in
  `src/lib/platform-data.ts`; `src/app/opportunities/page.tsx`).
- **AI due-diligence workflow (P4).** Document-upload and risk-review flow for
  acquisition/lending diligence (`src/app/due-diligence/page.tsx`); backend
  financial/audit reporting and accounting primitives
  (`backend/app/routers/reports.py`, `accounting.py`, `services.py`).
- **Global macro layer (P1/P3).** A macro dashboard concept tracking central banks,
  rates, commodities, Bitcoin, and economic indicators (`docs/PRODUCT_BLUEPRINT.md`;
  surfaced as market signals in `src/app/dashboard/page.tsx`).
- **Multi-asset portfolio + crypto (P1/P3).** Portfolio tracking across stocks,
  private equity, real estate, and crypto (`src/app/portfolio/page.tsx`), plus a
  **non-custodial, watch-only crypto holdings store** (companion change, PR #5)
  that stores only public addresses and quantities and refuses private keys/seed
  phrases.
- **Access + trust layer (P2).** Organization/role accounts, billing tiers, and
  **dual (web + mobile) access** with password, TOTP two-factor, and biometric
  sign-in (`backend/app/routers/auth.py`, `mobile_auth.py`; `src/app/mobile/page.tsx`).
- **Operating backbone.** FastAPI services for auth, billing, accounting, reports,
  dashboards, CRM, and external integrations (`backend/app/main.py`).

Each sub-problem (P1–P4) has at least one concrete, runnable capability — i.e., the
solution is *internally complete* against its own problem decomposition.

---

## 6. Problem–solution fit analysis

| Problem | Platform response | Code evidence | Fit status |
| --- | --- | --- | --- |
| P1 Fragmentation | One shell unifying discovery/scoring/diligence/macro/portfolio | `platform-shell.tsx`, `dashboard/page.tsx` | **Confirmed (design)** |
| P2 Access asymmetry | Tiered SaaS + role accounts + multi-factor dual access | `pricing/page.tsx`, `mobile_auth.py` | **Confirmed (design)** |
| P3 No cross-asset standard | Single 0–100 Opportunity Score with per-asset factors | `opportunities/page.tsx`, `platform-data.ts` | **Confirmed (design); predictive validity unproven** |
| P4 Acquisition tooling gap | Business-acquisition engine + AI diligence + accounting/reports | `due-diligence/page.tsx`, `reports.py`, `accounting.py` | **Confirmed (design)** |

**Interpretation.** The platform is *not* a feature collection without a problem:
every major capability maps to a stated, real sub-problem, and the mapping is
coherent and non-redundant. This satisfies the **design-level** definition of
problem–solution fit. It does **not** by itself establish **market-level** fit.

---

## 7. Differentiation

- **Vs single-purpose tools** (screeners, trackers, macro dashboards): JHI's edge is
  *integration* and a *common scoring grammar* across asset classes.
- **Vs institutional terminals:** JHI targets price/accessibility for
  non-institutional allocators rather than competing on data breadth.
- **Vs robo-advisors:** JHI is decision-support and acquisition-capable
  (private businesses, real estate, crypto), not solely automated public-market
  allocation.
- **Defensibility risk:** the moat depends on the **proprietary score's** validated
  accuracy and proprietary data network effects — neither of which is established
  yet (see §9).

---

## 8. Methodology to confirm market-level problem-solving (falsifiable)

To move from "confirmed by design" to "confirmed by market," run:

1. **Live-data substitution.** ✅ **Done (2026-06-24).** Live `/api/v1/market/quotes`
   (CoinGecko/Yahoo/BLS) feeds an auto-refreshing dashboard for the liquid classes.
2. **Score back-test (tests H5).** ⚠️ **Run; not passed.** Real-history IC was weak
   and statistically insignificant (mean IC ≈ 0.01, t-stat ≈ 0.25). Harness exists;
   H5 remains unconfirmed (`docs/SECTION_8_VALIDATION_RESULTS.md`).
3. **Workflow-efficiency study (tests H1).** ⬜ Pending (needs real user cohort).
4. **Access/adoption study (tests H2).** ⚠️ **Instrument built and run** on real DB
   tables; dataset is non-representative (test accounts), so H2 is not yet evidenced.
5. **Acquisition-engine validation (tests H4).** ⚠️ **Engine validated** vs a labeled
   fixture (100% agreement); needs expert-underwriter ground truth for H4.
6. **Consistency study (tests H3).** ⬜ Pending (requires a defined score formula).

**Primary success metrics:** retention/NRR by segment; score information
coefficient > pre-registered floor; measurable reduction in decision latency.

---

## 9. Risks, limitations, and threats to validity

- **~~Simulated data.~~ Resolved for liquid classes (2026-06-24).** §8.1 is done:
  the dashboard now consumes live `/api/v1/market/quotes` (CoinGecko/Yahoo/BLS).
  The residual gap is **coverage breadth** — FX, corporate/muni bonds, and full
  macro are not wired, and private/illiquid classes are inherently non-real-time.
- **Unvalidated model.** The Opportunity Score's predictive validity (H5) is
  asserted, not demonstrated; model risk and overfitting are open threats.
- **Prototype persistence/security.** Backend uses development token signing and
  SQLite by default with documented production next steps
  (`backend/README.md`); custody-grade controls are explicitly out of scope (the
  crypto store is non-custodial by design).
- **Regulatory surface.** Investment guidance, billing, and any future custody carry
  compliance obligations (advice/RIA considerations, MiCA/MTL for crypto) that gate
  market deployment.
- **Construct validity.** Self-reported pains (P1–P4) require external corroboration
  via the §8 studies to avoid confirmation bias.

---

## 10. Findings — confirmation statement

1. **The problem is real.** P1–P4 describe documented, structural conditions in the
   investment-intelligence market, independent of this product.
2. **The solution is coherent and complete against the problem.** Every sub-problem
   maps to at least one concrete, runnable capability, with no major capability
   lacking a corresponding problem. **Design-level problem–solution fit is
   confirmed.**
3. **Market-level problem-solving is partially evidenced, not fully confirmed
   (updated 2026-06-24).** Live real-world data is wired for the liquid classes and
   the evaluation harness runs on real data — so condition (a) is largely met for
   tradable assets. Condition (b), demonstrated predictive validity (H5), is
   **not** met: the back-test signal is weak and insignificant. Coverage also
   remains incomplete (7/14 categories live).

In short: **yes, the platform is a legitimate problem-solving artifact for a real
market gap, now backed by live data and a runnable evaluation harness — but it is
not yet a fully proven, market-confirmed solution, because the score's predictive
validity is unproven and several asset classes still lack real-time data.**

---

## 11. Conclusion and future work

JHI is a defensible answer to a genuine market problem rather than a solution in
search of one. As of 2026-06-24, the highest-leverage §8 evidence steps have been
**partially executed**: live data is wired and the evaluation harness runs on real
data, moving the thesis to **design-confirmed + partially market-evidenced**. The
remaining steps to reach a fully market-confirmed thesis are now sharply defined:
(1) define and **outcome-validate** the Opportunity Score so H5 passes with a
pre-registered IC floor, (2) extend live data to the uncovered classes (FX, bonds,
full macro), and (3) gather a representative usage cohort and expert-underwriter
labels. Until then, the honest claim is "proven in architecture and live-data
plumbing; not yet proven in market efficacy."

---

## References (in-repo evidence)

- `README.md` — product scope and routes.
- `docs/PRODUCT_BLUEPRINT.md` — modules, macro layer, segments, monetization.
- `src/lib/platform-data.ts` — segments, scoring categories, opportunities.
- `src/app/opportunities/page.tsx`, `src/app/dashboard/page.tsx`, `src/app/due-diligence/page.tsx`, `src/app/portfolio/page.tsx` — decision surfaces.
- `src/components/platform-shell.tsx`, `src/app/mobile/page.tsx` — unified shell and dual-access mobile app.
- `backend/app/main.py`, `backend/app/routers/*` — auth, billing, accounting, reports, dashboards, CRM, integrations, mobile auth.
- Live market data — `/api/v1/market/quotes` (`backend/app/market_services.py`, `src/components/live-market.tsx`); see `docs/MARKET_DATA_SOURCES.md` (companion PR #7).
- §8 validation harness + results — `/api/v1/research/*` and `docs/SECTION_8_VALIDATION_RESULTS.md` (companion PR #8).
- Non-custodial crypto holdings store and `docs/CRYPTO_HOLDINGS_STORAGE.md` — companion change (PR #5).
- `backend/README.md` — persistence/security production next steps.
