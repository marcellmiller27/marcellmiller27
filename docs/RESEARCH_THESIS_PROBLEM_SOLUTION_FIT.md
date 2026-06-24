# Does John Henry Investments Solve a Real Industry Problem? A Problem–Solution Fit Thesis

*A research-paper-style thesis evaluating whether the John Henry Investments
platform addresses a genuine, identifiable problem in the investment-intelligence
and wealth-technology market.*

**Status of evidence:** the platform in this repository is a working **prototype**.
This paper confirms problem–solution fit at the **architecture and design** level
using direct evidence from the codebase, and specifies the empirical methodology
required to confirm fit at **market** scale (which a prototype cannot yet prove).

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
the sub-problems. We **withhold** confirmation of market-level efficacy pending the
falsifiable validation program defined in §8, because the prototype currently uses
static market data and has no live cohort, retention, or model-accuracy evidence.

**Thesis statement.** *John Henry Investments targets a real and structural market
problem — the fragmentation and access-asymmetry of investment intelligence across
heterogeneous asset classes — and the prototype demonstrates a coherent,
defensible solution architecture; however, confirmed market-level problem-solving
is contingent on validating the proprietary scoring model against realized
outcomes and on replacing simulated data with live, auditable feeds.*

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

1. **Live-data substitution.** Replace static `marketSignals`
   (`src/lib/platform-data.ts`) with auditable market/macro feeds; this is a
   prerequisite for any outcome study.
2. **Score back-test (tests H5).** Compute historical Opportunity Scores and measure
   association with realized forward risk-adjusted returns (e.g., information
   coefficient, decile spread, hit rate vs benchmark). Pre-register thresholds.
3. **Workflow-efficiency study (tests H1).** Time-to-decision and tool-switch count
   for JHI users vs a multi-tool control group.
4. **Access/adoption study (tests H2).** Activation, conversion, and retention by
   segment and tier; willingness-to-pay.
5. **Acquisition-engine validation (tests H4).** Agreement of DSCR/SBA/diligence
   outputs with expert underwriters on a labeled deal set.
6. **Consistency study (tests H3).** Inter-rater variance of prioritization with vs
   without the standardized score.

**Primary success metrics:** retention/NRR by segment; score information
coefficient > pre-registered floor; measurable reduction in decision latency.

---

## 9. Risks, limitations, and threats to validity

- **Simulated data.** Market values are currently static literals, not a live feed
  (`src/lib/platform-data.ts`); confirmed in the codebase. No real-time intelligence
  exists yet, so the "live" framing is aspirational until §8.1 is completed.
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
3. **Market-level problem-solving is not yet confirmed.** It is *conditional* on
   (a) live, auditable data and (b) demonstrated predictive validity of the
   Opportunity Score, per the falsifiable program in §8.

In short: **yes, the platform is a legitimate problem-solving artifact for a real
market gap — and its ultimate, durable value rests on validating the proprietary
score against realized outcomes once live data is in place.**

---

## 11. Conclusion and future work

JHI is a defensible answer to a genuine market problem rather than a solution in
search of one. The highest-leverage next steps are not more features but
**evidence**: wire live data, back-test the score, and run the segment adoption and
acquisition-engine validation studies. Completing §8 would convert a
design-confirmed thesis into a market-confirmed one.

---

## References (in-repo evidence)

- `README.md` — product scope and routes.
- `docs/PRODUCT_BLUEPRINT.md` — modules, macro layer, segments, monetization.
- `src/lib/platform-data.ts` — segments, scoring categories, opportunities, static market signals.
- `src/app/opportunities/page.tsx`, `src/app/dashboard/page.tsx`, `src/app/due-diligence/page.tsx`, `src/app/portfolio/page.tsx` — decision surfaces.
- `src/components/platform-shell.tsx`, `src/app/mobile/page.tsx` — unified shell and dual-access mobile app.
- `backend/app/main.py`, `backend/app/routers/*` — auth, billing, accounting, reports, dashboards, CRM, integrations, mobile auth.
- Non-custodial crypto holdings store and `docs/CRYPTO_HOLDINGS_STORAGE.md` — companion change (PR #5).
- `backend/README.md` — persistence/security production next steps.
