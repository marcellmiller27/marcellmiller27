# Acquisition Intelligence Framework — Educational + Tool Map for Acquirers

**Date:** 2026-08-10 · **JHI-SIG:** `69M2705M`
**Product:** Aegira · **Publisher:** JHI Research & Analytics Firm, Inc. (proprietary)
**Owner:** Cy Henry (VP, Software Engineering — AI) · **Status:** framework of record (educational IP + tool map + funnel)

> A teaching framework for **search-fund / ETA / SMB acquirers** that pairs **how-to education** with the **Aegira
> tool** that performs each step, an **exportable checklist/template**, its **data source**, and its **current
> status/gap**. Doubles as the top of the lead-gen funnel. Companions: `docs/FINANCIAL_DILIGENCE_SUITE_CONCEPT.md`,
> `docs/CROSS_ASSET_VALUATION_ENGINE_SPEC.md`, `docs/GTM_FUNNELS_NEXTJS.md`, `docs/PRICING_BILLING_SCHEMA.md`.
> Educational content — not investment, legal, tax, or accounting advice.

---

## How to read this framework

For **each element** of acquisition analysis we map five things:

1. **Explainer** — how to do it + **what to look for** + **why it matters**.
2. **Linked Aegira tool** — the platform capability that performs (or will perform) the step.
3. **Exportable checklist / template** — the artifact the acquirer takes away (PDF/Excel).
4. **Data source** — where the numbers come from (per `docs/DATA_FOUNDATION_CONSTRUCT.md`).
5. **Current status / gap** — ✅ live · 🟡 partial · 🔴 gap (build target).

Tool nomenclature: **LSR** = Limited Scope Review (formerly "Deal X-Ray") · **QoE** = Quality-of-Earnings lens ·
**Valuation Engine** = Cross-Asset Valuation & DCF · **Opportunity Scan** = equity idea generation · **Pipeline** =
deal tracker · **Workbook** = institutional Excel export.

---

## The ten elements

### 1. How to research a target
- **Explainer:** Build the target's fact base before valuing it — legal entity, filings, industry, size, ownership,
  reason for sale. **Look for:** verifiable sources, consistency across documents, seller motivation. **Why:** every
  later step compounds on this; garbage-in poisons the model.
- **Aegira tool:** LSR intake + company profile.
- **Export:** *Target Research Brief* (PDF).
- **Data source:** SEC EDGAR (public co's), seller-provided docs (private), SF1-derived comparables.
- **Status:** 🟡 partial — LSR intake exists; guided research brief is a gap-fill.

### 2. Financial analysis
- **Explainer:** Normalize and read the financials — revenue quality, margins, working capital, cash conversion,
  add-backs. **Look for:** owner add-backs that don't survive a sale, one-time items, margin trend. **Why:** the
  number you pay is a function of **adjusted** earnings, not reported.
- **Aegira tool:** LSR + **QoE** lens → Valuation Engine (adjusted EBITDA → unlevered FCF).
- **Export:** *Financial Analysis + QoE workbook* (Excel).
- **Data source:** seller financials (private); SF1 (primary) → EDGAR (fallback) for public/comps.
- **Status:** ✅ live (QoE + DCF in workbook, Phase 1).

### 3. Industry analysis
- **Explainer:** Understand the industry's structure, growth, cyclicality, and margins. **Look for:** secular vs.
  cyclical demand, fragmentation, input-cost exposure, regulatory risk. **Why:** a great operator in a dying industry
  still loses.
- **Aegira tool:** **Industry Analysis module (gap-fill)** — sector aggregates.
- **Export:** *Industry Profile* (PDF).
- **Data source:** **EDGAR / SF1 sector aggregates** (derived), BLS/BEA/Census macro.
- **Status:** 🔴 gap — see §Gap-fill modules.

### 4. Market analysis
- **Explainer:** Size the market and the target's position — TAM/SAM/SOM, competitive set, share, moat. **Look for:**
  defensible niche, customer concentration, pricing power. **Why:** growth headroom and durability drive the terminal
  value.
- **Aegira tool:** **Market Analysis module (gap-fill)** — TAM + competitive map.
- **Export:** *Market & Competitive Landscape* (PDF).
- **Data source:** Census/BEA (market sizing), EDGAR (public competitors), derived comps.
- **Status:** 🔴 gap — see §Gap-fill modules.

### 5. Company analysis
- **Explainer:** The business itself — operations, customers, org, systems, owner-dependence. **Look for:** key-person
  risk, revenue concentration, transferability, systems maturity. **Why:** SMB value often walks out the door with
  the founder.
- **Aegira tool:** LSR company teardown.
- **Export:** *Company Analysis* (PDF).
- **Data source:** seller docs, LSR structured intake.
- **Status:** 🟡 partial.

### 6. Valuation considerations
- **Explainer:** Choose the right method and inputs — DCF for cash-flow businesses, multiples cross-check, SDE/EBITDA
  bases for SMB. **Look for:** honest WACC build (size/illiquidity/key-person premia), terminal-value discipline.
  **Why:** false precision destroys credibility; a defensible range beats a fake point.
- **Aegira tool:** **Valuation Engine** (DCF + multiples + sensitivity) in the Workbook.
- **Export:** *Valuation (DCF + comps + sensitivity)* (Excel).
- **Data source:** adjusted financials; SF1→EDGAR for comps; rates (FRED) for WACC.
- **Status:** ✅ live (Phase 1 equity DCF; SMB DCF via LSR/QoE).

### 7. Risk analysis
- **Explainer:** Catalog and weight the risks — customer/supplier concentration, key-person, legal, cyclical,
  leverage. **Look for:** risks that break the thesis vs. those that are priced. **Why:** valuation is a
  risk-adjusted exercise; unpriced risk is the deal-killer.
- **Aegira tool:** LSR risk register + red-flag flags.
- **Export:** *Risk Register* (PDF/Excel).
- **Data source:** LSR intake, derived ratios, industry context.
- **Status:** 🟡 partial.

### 8. Due diligence
- **Explainer:** Systematic verification before close — financial, legal, operational, commercial. **Look for:**
  gaps between represented and verified; anything that changes price or breaks the deal. **Why:** DD is where the
  deal is confirmed or killed.
- **Aegira tool:** **DD Checklist module (gap-fill)** tied to the **Pipeline**.
- **Export:** *Due Diligence Checklist* (Excel/PDF, exportable, deal-linked).
- **Data source:** deal artifacts + LSR outputs; public verification via EDGAR.
- **Status:** 🔴 gap — see §Gap-fill modules.

### 9. Economic environment
- **Explainer:** Read the macro backdrop — rates, inflation, credit, cycle — that shapes financing and multiples.
  **Look for:** rate regime (cost of debt/WACC), credit availability (SBA), demand cyclicality. **Why:** the same
  business is worth different amounts in different rate/credit regimes.
- **Aegira tool:** **Economic Tracking** (macro dashboard) → feeds WACC + regime.
- **Export:** *Economic Environment snapshot* (PDF).
- **Data source:** FRED, BLS, BEA (public, live).
- **Status:** ✅ live.

### 10. Key financial ratios
- **Explainer:** The ratio toolkit — liquidity, leverage, coverage (incl. **SBA DSCR**), profitability, efficiency,
  returns — read **against benchmarks**. **Look for:** ratios outside industry norms; coverage that fails a debt-service
  test. **Why:** ratios are the fast diagnostic and the financeability test.
- **Aegira tool:** **Key-Ratios explainer + dashboard (gap-fill)** with benchmarks.
- **Export:** *Key Ratios vs. Benchmarks* (Excel).
- **Data source:** derived from financials; SF1/EDGAR sector aggregates for benchmarks.
- **Status:** 🔴 gap — see §Gap-fill modules.

---

## Element → tool → export → source → status (summary matrix)

| # | Element | Aegira tool | Export | Data source | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Research a target | LSR intake / profile | Target Research Brief | EDGAR / seller / SF1 comps | 🟡 |
| 2 | Financial analysis | LSR + QoE → Valuation | Financial + QoE workbook | seller; SF1→EDGAR | ✅ |
| 3 | Industry analysis | Industry module | Industry Profile | EDGAR/SF1 aggregates; BLS/BEA | 🔴 |
| 4 | Market analysis | Market module | Market & Competitive | Census/BEA; EDGAR comps | 🔴 |
| 5 | Company analysis | LSR teardown | Company Analysis | seller; LSR intake | 🟡 |
| 6 | Valuation | Valuation Engine (DCF) | Valuation workbook | adj. financials; FRED; comps | ✅ |
| 7 | Risk analysis | LSR risk register | Risk Register | LSR; derived ratios | 🟡 |
| 8 | Due diligence | DD Checklist + Pipeline | DD Checklist (deal-linked) | deal artifacts; EDGAR | 🔴 |
| 9 | Economic environment | Economic Tracking | Economic snapshot | FRED/BLS/BEA | ✅ |
| 10 | Key financial ratios | Key-Ratios dashboard | Ratios vs. Benchmarks | derived; SF1/EDGAR aggregates | 🔴 |

---

## Gap-fill modules (build targets)

1. **Industry Analysis module** — sector aggregates from **EDGAR / SF1** (derived-only): growth, margins, leverage,
   cyclicality by sector; renders an *Industry Profile* export.
2. **Market Analysis module** — **TAM/SAM/SOM** sizing (Census/BEA) + a **competitive map** from public comparables;
   renders *Market & Competitive Landscape*.
3. **Due Diligence Checklist** — **exportable**, structured (financial/legal/operational/commercial), **tied to the
   Pipeline** so each deal carries its live checklist state.
4. **Key-Ratios explainer + dashboard** — the ratio toolkit with **benchmarks** (sector aggregates), incl. **SBA
   DSCR**; explainer content + live dashboard + Excel export.

All gap-fill modules inherit the data doctrine (as-of disclosure, always-deliver, derived-only for licensed data).

---

## Lead-generation funnel

The framework is the **top of the funnel** — email-gated educational IP that converts to paid tiers.

| Stage | Mechanism | Aim |
| --- | --- | --- |
| **Attract** | Free **framework / toolkit** (this document's explainers + starter templates) | Establish authority; capture intent. |
| **Capture** | **Email-gate** the free toolkit (double opt-in, no account) → free newsletter list | Build the owned audience. |
| **Nurture** | Newsletter cadence (*The Main Street Acquirer* — see `docs/MAIN_STREET_ACQUIRER_CONSTRUCT.md`) + rotating Framework lessons | Trust + recurring touch. |
| **Convert** | Upgrade gates → **Tier 2** then **Tier 1** (full tools, live valuation, deal-linked DD) | Monetize with the working tools. |
| **Retain** | Deal-linked Pipeline + Workbook + ongoing editorial | Stickiness via active deals + habit. |

Conversion logic: give away the **teaching + templates** (high trust, low marginal cost); charge for the **doing**
(live data, DCF/QoE valuation, deal-linked DD, benchmarked ratios). Retention is the working pipeline + the cadence.

---

*Educational framework; each tool carries the standard research/education disclaimer. Not investment, legal, tax, or
accounting advice.*
