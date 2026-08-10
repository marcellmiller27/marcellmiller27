# The Main Street Acquirer — Newsletter Construct

**Date:** 2026-08-10 · **JHI-SIG:** `69M2705M`
**Product:** Aegira · **Publisher:** JHI Research & Analytics Firm, Inc. (proprietary)
**Owner:** Cy Henry (VP, Software Engineering — AI) · **Status:** construct of record (build target; legit-data-only)

> A newsletter for **SMB / search-fund buyers**, built on **LEGIT public data only** — **NO scraping** of BizBuySell
> or other marketplaces. Every section maps to a **free or licensed** data source. Companions:
> `docs/ACQUISITION_INTELLIGENCE_FRAMEWORK.md`, `docs/CROSS_ASSET_DISTRIBUTION_CONSTRUCT.md`,
> `docs/DATA_FOUNDATION_CONSTRUCT.md`, `docs/EDITORIAL_CHARTER.md`. Not investment advice.

---

## Positioning

*The Main Street Acquirer* serves the buyer of a **real Main Street business** — the searcher, the ETA operator, the
SMB acquirer. Its edge is **legitimacy**: institutional-grade analysis built entirely on **legal, sourced public
data**, with **as-of disclosure** on every figure (per the data doctrine). It is the recurring nurture asset for the
Acquisition Intelligence funnel.

**Cadence:** **weekly pulse** + **monthly deep-dive** (per `docs/CROSS_ASSET_DISTRIBUTION_CONSTRUCT.md` §A).

**Voice:** independent JHI professional perspective; authored by **Ellery Vance (VP of Editorial — AI)**, fact-locked
to the data. Research/education only.

---

## Section-by-section format

Each section is mapped to a **free or licensed** data source. No section depends on scraped marketplace data.

| # | Section | Content | Data source (legit) |
| --- | --- | --- | --- |
| 1 | **Executive thesis** | The week's/month's read for SMB buyers — rates, credit, demand backdrop → what it means for deal-making. | **Economic Tracking / FRED** (public) |
| 2 | **SBA Lending Intelligence** | Which **NAICS / industries get funded**, typical **deal sizes**, active **lenders**, **approval trends** — the financeability signal. | **SBA 7(a) / 504 open loan data** (public) |
| 3 | **Recession-Resilient Industry Spotlight** | A durable industry: durability + **boomer-succession gap**, typical **multiples/margins**, **pros/cons**, **red flags**. | **BLS / Census / BEA** (public) |
| 4 | **Acquisition Playbook** | A rotating **Framework lesson** (from the Acquisition Intelligence Framework). | Framework IP |
| 5 | **Deal Teardown** | A representative deal run through the **LSR / QoE / valuation / SBA-DSCR** lens. | Derived (public inputs + engine) |
| 6 | **Financing Corner** | Rate/credit conditions for acquisition debt; SBA terms, DSCR math, structure notes. | FRED + SBA (public) |
| 7 | **Metric of the issue** | One number that matters this issue, explained (e.g., median 7(a) size in a NAICS). | Derived from source data |
| 8 | **Charts** | Server-rendered charts with cited historical context (Fed "Economic Research" style). | Any of the above |
| 9 | **Ask Aegira** | Reader-question format answered from the platform's tools/data. | Platform tools |
| 10 | **Methodology / disclaimers** | Sources, as-of dates, and the standard research/education disclaimer. | — |

### Section detail notes

- **SBA Lending Intelligence** is the signature section: **SBA 7(a) / 504 open loan datasets are public**, so we can
  legitimately surface *which industries get funded, at what sizes, by which lenders, and how approvals are trending*
  — a genuine, non-scraped financeability signal. Built by the **SBA engine** (see §Build).
- **Recession-Resilient Industry Spotlight** ties **BLS/Census/BEA durability** to the **boomer-succession gap** (the
  structural supply of sellers), with typical multiples/margins and honest **pros/cons + red flags**.
- **Deal Teardown** uses a **representative** deal (illustrative), analyzed with the real engine (LSR/QoE/valuation +
  **SBA-DSCR** lens) — teaching by worked example, not a live marketplace listing.

---

## Listings sourcing note (legit-only)

**We do not scrape** BizBuySell, Flippa web pages, or any marketplace. Where listings context is used it is
**legit-only**:

- **Flippa API** (where terms permit programmatic access) and/or **manual curation with link-back** to the source.
- **No scraping**, no republishing of marketplace-proprietary data, and clear **link-back** attribution.
- The newsletter's value comes from **analysis on public data** (SBA, BLS, Census, BEA, FRED) — not from reselling
  listing inventory.

This keeps the product **legally clean** and consistent with the firm's derived-only / no-spillage governance.

---

## Governance & disclosure

- **Public-data sourced** (SBA/FRED/BLS/Census/BEA); any licensed data folded in is **derived-only** (no spillage).
- **As-of disclosure** on every figure (data date + cadence + source), per `docs/DATA_FOUNDATION_CONSTRUCT.md`.
- **Fact-lock** on all AI-authored narrative — no invented figures.
- **CAN-SPAM** compliance on every send (one-click unsubscribe, physical address, suppression list); free list is
  **double opt-in**.
- Standard research/education disclaimer — **not** investment, legal, tax, or accounting advice.

---

## Build

- **SBA engine** — ingests **SBA 7(a) / 504 open loan data**; derives NAICS/industry funding patterns, deal sizes,
  lender activity, approval trends → powers the SBA Lending Intelligence + Financing Corner + Metric sections.
- **Distribution** — rides the cadence scheduler + SES + free double-opt-in list from
  `docs/CROSS_ASSET_DISTRIBUTION_CONSTRUCT.md`.
- **Editorial** — Ellery/Bedrock authors sections; charts server-rendered; RAG for historical context.

---

## Conversion / retention rationale

- **Attract & capture:** the free, legit, genuinely-useful **SBA Lending Intelligence** is a strong email-gate magnet
  for searchers/SMB buyers (double opt-in → free list).
- **Nurture:** weekly pulse + monthly deep-dive builds trust and a recurring habit; the rotating **Playbook** lessons
  seed the Framework.
- **Convert:** Deal Teardowns and Metric sections demonstrate the **working tools** (LSR/QoE/valuation/DSCR),
  motivating upgrade to **Tier 2 → Tier 1** for live, deal-linked analysis.
- **Retain:** ongoing cadence + the deal-linked Pipeline/Workbook keep active buyers engaged through their search.

---

*Built on legit public data only — no marketplace scraping. Authored by Ellery Vance (VP of Editorial — AI),
fact-locked. Not investment advice.*
