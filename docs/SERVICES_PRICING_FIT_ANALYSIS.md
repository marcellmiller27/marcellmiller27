# Top 5 Services — Problem‑Fit & Pricing Analysis

Honest review of John Henry Investments' five core services: the problem each solves,
the audience, whether it is a **real solution today** (vs aspirational given current
build status), and whether it is **priced properly** vs the market.

> Method: platform scope (`README.md`, `docs/PRODUCT_BLUEPRINT.md`, `src/lib/platform-data.ts`),
> current build status (this codebase), our pricing tiers (Consumer $50 / Professional
> $299 / Enterprise–Family Office $1,500+ per month), and public market comparables.
> Status is rated honestly: **Functional**, **Partial**, or **Prototype**.

## At a glance

| # | Service | Primary audience | Tier | Real-solution status | Pricing verdict |
| --- | --- | --- | --- | --- | --- |
| 1 | John Henry Opportunity Score / AI discovery | Retail + pros | Consumer→Pro | **Partial** (defined + live data; predictive validity unproven) | Reasonable at maturity; too high today |
| 2 | Business Acquisition Engine (EBITDA/DSCR/SBA) | Business buyers, advisors | Professional | **Partial** (engine logic works; UX prototype) | Well-priced for the niche |
| 3 | AI Due Diligence Center | Buyers, lenders, CPAs | Professional/Ent | **Prototype** (workflow concept) | Not yet justified at price |
| 4 | Global Macro Intelligence & Weekly Reports | All segments | Consumer→Ent | **Partial** (live data; reports not auto-generated) | Fair vs comparables |
| 5 | Portfolio Tracking & Wealth Projection | Investors, family offices | Consumer→Ent | **Prototype** (modeled valuations exist; no account aggregation) | Overpriced until aggregation ships |

## 1. John Henry Opportunity Score / AI opportunity discovery
- **Problem:** no standardized way to compare opportunities across asset classes.
- **Audience:** retail investors (Consumer) and advisors/pros (Professional).
- **Real solution?** Partial. The score is now a *defined, transparent* model on *live*
  multi-asset data — but its **predictive validity is unproven** (back-test IC weak/
  insignificant; needs licensed point-in-time fundamentals). So it's a credible
  decision-support signal, not yet a validated edge.
- **Comparables:** Seeking Alpha ($30–40/mo), Morningstar ($35), Simply Wall St ($10–20),
  Koyfin ($50). **Consumer $50** sits at the top of retail.
- **Verdict:** Price is defensible *once the score is validated*; **charging $50 today
  on an unproven score is hard to justify** — use intro/early-access pricing until H5 passes.

## 2. Business Acquisition Engine (normalized EBITDA, DSCR, SBA eligibility)
- **Problem:** SMB/search-fund acquisition analysis is under-tooled vs public markets.
- **Audience:** business buyers, search funds, advisors, brokers (Professional).
- **Real solution?** Partial — the **engine logic is implemented** (normalized EBITDA,
  DSCR, SBA flags, Buy/Watch/Pass) and tested; the **front-end is still a prototype**.
- **Comparables:** deal-analysis/search tools and advisor subscriptions run ~$100–500/mo;
  this is a genuinely under-served niche.
- **Verdict:** **Professional $299 is well-positioned** for this niche and is the
  strongest differentiator — prioritize finishing its UX; the willingness-to-pay is real.

## 3. AI Due Diligence Center
- **Problem:** document-heavy diligence (tax returns, P&L, bank statements) is slow and
  error-prone.
- **Audience:** acquirers, lenders, CPAs (Professional/Enterprise).
- **Real solution?** **Prototype** — currently a workflow concept (upload/review UI),
  not a working document-analysis engine.
- **Comparables:** QoE/diligence software and analyst tools are premium ($300–1,000+/mo).
- **Verdict:** High potential, but **not yet a deliverable worth its implied price**;
  don't gate paid tiers on it until the analysis engine exists.

## 4. Global Macro Intelligence & Weekly Reports
- **Problem:** fragmented macro context (rates, inflation, commodities, crypto).
- **Audience:** all segments.
- **Real solution?** Partial — **live market/macro data is real** (CoinGecko/Yahoo/BLS,
  FX/curve/bonds; FRED gated) and the dashboard auto-refreshes, but the **"weekly
  reports" are not auto-generated** yet.
- **Comparables:** macro/newsletter research ($20–100/mo).
- **Verdict:** **Fairly priced as a bundled value**; ship automated report generation to
  fully justify it. Strong retention hook.

## 5. Portfolio Tracking & Wealth Projection
- **Problem:** scattered holdings across brokerages, real estate, private assets, crypto.
- **Audience:** investors and family offices (Consumer→Enterprise).
- **Real solution?** **Prototype** — modeled real-time valuations exist for illiquid
  classes, but there is **no live account aggregation** (Plaid/MX are connector stubs).
- **Comparables:** Kubera (~$15/mo), Empower (free), Addepar (enterprise).
- **Verdict:** **Overpriced until aggregation ships** — at the free/cheap end the market
  is competitive; the differentiator must be multi-asset + private-asset modeling.

## Cross-cutting: AI assistant & 24/7 AI support team
The 5-agent AI customer-service team is **Functional** and a genuine cost/quality
advantage; the *investment* research assistant page is still a prototype.

## Are we priced properly? — Overall verdict

**The tier structure is sound and market-aligned in concept**, but **the current prices
are ahead of delivered, validated value.** Today, the functional, defensible value is:
live market data, the (unvalidated) Opportunity Score, and AI support. The marquee
services (due diligence, acquisition UX, portfolio aggregation, auto-reports) are
largely prototype, and the score's edge is unproven.

### Recommendations
1. **Launch with early-access / intro pricing** (e.g., 40–60% off, or a free Consumer
   tier) until the score is validated and the prototype modules are functional. Lock in
   founding users; raise to target prices as value ships.
2. **Lead with the strongest, real differentiator** — the **Business Acquisition Engine**
   (Professional $299) — where willingness-to-pay is clearest and the niche is underserved.
3. **Validate the Opportunity Score (H5)** with licensed fundamentals before pricing it
   as predictive; until then market it as decision-support.
4. **Use value-based pricing per audience:** Consumer ≈ research/screener comps ($20–50),
   Professional ≈ acquisition/advisor value ($200–400), Enterprise/Family Office ≈
   accessible alternative to $2k+ terminals (justify with team/oversight/branded reports).
5. **Don't gate tiers on prototype features** — price for what's delivered now, with a
   clear roadmap to the full bundle.

**Bottom line:** real problems, well-chosen services, and a credible tier structure —
but **price to current, delivered value now (intro/early-access), and grow into the
target prices** as the prototype modules become functional and the score is validated.
