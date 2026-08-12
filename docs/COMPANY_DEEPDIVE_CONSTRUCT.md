# Company Deep-Dive Construct — People & Segments & Operations Depth

**Date:** 2026-08-12 · **JHI-SIG:** `69M2705M`
**Product:** Aegira · **Publisher:** JHI Research & Analytics Firm, Inc. (proprietary)
**Owner:** Cy Henry (VP, Software Engineering — AI) · **Status:** construct of record (build target)

> The construct that brings Aegira's company/valuation workbooks and on-platform company view up to the
> depth **institutional buyers** expect — the **Mergr / Capital IQ**-style company profile: who runs it
> (People & Governance), what it actually is (Segments), and how it operates (Operations & Supply Chain).
> Built on **SEC EDGAR (free)** first, folded into **Valuation Framework 2.0**, and governed by the
> **Data Foundation doctrine** — *Always-Deliver · Cadence-Aware · As-Of-Disclosed*. Companions:
> `docs/VALUATION_FRAMEWORK_2.0.md`, `docs/DATA_FOUNDATION_CONSTRUCT.md`,
> `docs/CROSS_ASSET_VALUATION_ENGINE_SPEC.md`, `docs/AEGIRA_SIGNAL_ENGINE.md`,
> `docs/H5_SF1_VALIDATION_RESULTS.md`. **Research, not investment advice.**

---

## 0. Why this construct exists

Aegira's current company surface is strong on **fundamentals** (SF1-derived financials, DCF, moat/innovation
from R&D intensity) but thin on the **qualitative and structural** depth an institutional buyer scans first:
*who is the management team, what are they paid, what does insider ownership say, what are the real reportable
segments and their mix, where are the facilities and the customer/supplier concentration, and how much of the
value is intangible/technology and executive-team quality.* Mergr and Capital IQ win the first ten minutes of
diligence on exactly this depth.

This construct closes that gap **without inventing a single number**. It adds three depth pillars —
**People/Governance**, **Segments**, and **Operations/Supply Chain** — each mapped to an **exact, mostly free
(SEC EDGAR)** data source, each labeled **numeric vs sourced-narrative**, each with **cadence + as-of
discipline**, and each wired into both the **Excel workbook tabs** and the **on-screen company view**. It also
ties directly into the **Valuation Framework 2.0** goal of pricing **executive-team quality, future
technology, and intangible assets** (V2.0 components **C4/C5/C6/C7**).

### 0.1 The three doctrines every line item inherits

Per `docs/DATA_FOUNDATION_CONSTRUCT.md`, every field below is:

- **Always-Deliver (P1)** — a missing proxy, segment note, or extraction never blocks the company view; the
  element degrades to a labeled gap (`pending` / `unavailable`), the rest renders.
- **Cadence-Aware (P4/§5)** — each field carries its filing cadence (DEF 14A ≈ annual, 10-K annual, Form 4
  event-driven) so the scheduler polls on the right window and the UI can say "next update expected."
- **As-Of-Disclosed (P3/§3.4)** — every figure and every narrative extraction renders its **as-of date +
  filing + source** (e.g., "per FY2025 10-K, filed 2026-02-14; SEC EDGAR"). No number, no quote, no score is
  ever shown without provenance.

And two non-negotiables from the doctrine (P2/P6):

- **Never-fabricate** — numeric fields come only from filings/derived math; **narrative** fields are
  **AI-extracted with a citation to the exact filing section** and are **fact-locked** — no invented figures,
  no unsourced claims.
- **Governed** — raw **licensed** (SF1) rows never surface; raw line-items surface only from **public-domain
  SEC EDGAR**. Everything new in this construct is **SEC EDGAR (free)** or derived, so it carries **no
  licensing spillage risk**.

### 0.2 Field-type legend (used in every table)

| Type | Meaning | Governance rule |
| --- | --- | --- |
| **N** | **Numeric** — a figure lifted directly from a filing/XBRL, or derived by transparent math | As-of + source stamp; never estimated silently |
| **SN** | **Sourced-Narrative** — AI-extracted text/qualitative signal | Must carry a **citation to the filing + section**; fact-locked; labeled AI/editorial |
| **D** | **Derived** — computed from N inputs (ratios, trends, concentration) | Formula disclosed; inherits worst as-of of its inputs |

---

## 1. PEOPLE / GOVERNANCE

**What institutional buyers want:** who runs the company, how they are paid, how long they have been there, who
sits on the board, how much of the company insiders own, and whether capital-allocation behavior signals a
quality steward. This pillar feeds **V2.0 C5 (Management / capital-allocation quality)** and the executive-team
half of the V2.0 optionality/intangibles goal.

**Primary source (free):** **SEC EDGAR** — **DEF 14A** (annual proxy statement: officers, board, compensation,
tenure, ownership tables), **Form 3/4/5** (insider ownership & transactions), and the 10-K's directors/officers
references. All **public-domain / free**.

### 1.1 Line items

| # | Line item | Type | Source (free = SEC EDGAR) | Cadence / as-of | Notes |
| --- | --- | --- | --- | --- | --- |
| P-1 | **Executive roster** (name, title, age, officer-since) | N + SN | DEF 14A + 10-K | Annual (proxy) | Officer-since → **tenure** (D) |
| P-2 | **Named-executive compensation** (base, bonus, equity, total; NEO table) | N | DEF 14A Summary Comp Table | Annual (as-of proxy FY) | Exact figures only; no estimates |
| P-3 | **Pay-vs-performance** (CEO total comp vs TSR / peer TSR / net income) | N + D | DEF 14A Pay-vs-Performance table | Annual | SEC-mandated table since 2023 |
| P-4 | **Board of directors** (name, independence, committees, tenure, other boards) | N + SN | DEF 14A | Annual | Independence % (D); busy-board flag (SN) |
| P-5 | **Insider ownership %** (officers/directors aggregate, top holders) | N | DEF 14A beneficial-ownership table + Form 3/4/5 | Annual + event-driven | Aligns with V2.0 C5 Form-4 plan |
| P-6 | **Insider transaction trend** (net buy/sell, last 4 quarters) | N + D | Form 4 (event-driven) | Irregular / event | Net-buy signal (D), labeled directional |
| P-7 | **Management-quality signals** (capital-allocation track record: ROIC trend, buyback/dividend discipline, M&A history) | SN + D | 10-K MD&A + derived from SF1/EDGAR fundamentals | Annual | **Labeled AI/editorial**, fact-locked to metrics (V2.0 C5) |
| P-8 | **Governance red flags** (dual-class, staggered board, related-party txns, auditor changes, restatements) | SN | DEF 14A + 10-K + 8-K | Annual + event | Extraction w/ citation; no scoring inflation |
| P-9 | **CEO/founder tenure & ownership alignment** | N + D | DEF 14A | Annual | Skin-in-the-game read for C5 |

### 1.2 Numeric vs narrative split (People)

- **Numeric (N):** comp figures, ages, officer/director-since dates, ownership %, insider net buy/sell counts,
  pay-vs-performance figures. These are **lifted verbatim** from proxy/Form-4 tables.
- **Sourced-narrative (SN):** management-quality read, governance red flags, board-quality commentary. Each is
  **AI-extracted from a named filing section with a citation** and **labeled AI/editorial** (per V2.0 §5 and
  Data Foundation §8 fact-lock). No SN field may assert a number that is not already an N field.

---

## 2. SEGMENTS

**What institutional buyers want:** what the company *actually is* — its reportable **business** and
**geographic** segments, the **revenue / operating-income mix**, segment **growth and margin trends**, and
**concentration risk** (one segment carrying the firm). This pillar feeds **V2.0 C3 (scenario / sum-of-parts
DCF)** and **C7 (sector re-tagging)** — you cannot do SoP or honest peer-tagging without the segment map.

**Primary source (free):** **SEC EDGAR — 10-K / 10-Q XBRL segment disclosures** (ASC 280 segment footnote:
`us-gaap:` segment members with revenue, operating income, assets, depreciation, capex by segment; geographic
breakout). Structured **XBRL** = machine-readable, **free**.

### 2.1 Line items

| # | Line item | Type | Source (free = SEC EDGAR) | Cadence / as-of | Notes |
| --- | --- | --- | --- | --- | --- |
| S-1 | **Reportable business segments** (list + description) | N + SN | 10-K segment footnote (XBRL) | Annual | Segment names from XBRL members |
| S-2 | **Segment revenue** (per segment, multi-year) | N | 10-K/10-Q XBRL (ASC 280) | Annual + quarterly | Basis of mix + trend |
| S-3 | **Segment operating income / margin** | N + D | 10-K/10-Q XBRL | Annual + quarterly | Margin = OI/Rev (D) |
| S-4 | **Revenue & OI mix** (% of total by segment) | D | Derived from S-2/S-3 | Annual + quarterly | The "what is this company" chart |
| S-5 | **Segment growth trend** (multi-year revenue/OI CAGR by segment) | D | Derived from S-2/S-3 history | Annual | Feeds SoP scenario deltas (C3) |
| S-6 | **Geographic segments** (revenue by region, multi-year) | N | 10-K XBRL geographic disclosure | Annual | Region mix + concentration |
| S-7 | **Concentration risk** (top-segment % of revenue/OI; HHI-style index) | D + SN | Derived + 10-K Risk Factors | Annual | Numeric concentration + narrative context |
| S-8 | **Segment re-tag** (map firm to what it *really* is for peer/expectation context) | SN + D | Derived from S-1..S-6 | Annual | Directly implements V2.0 **C7** |
| S-9 | **Sum-of-parts scaffolding** (per-segment growth/margin inputs for SoP DCF) | D | Derived → Valuation Engine | Annual | Feeds V2.0 **C3** SoP |

### 2.2 Numeric vs narrative split (Segments)

- **Numeric (N) / Derived (D):** segment revenue, operating income, geographic revenue, all mix %, growth
  CAGRs, concentration indices. Machine-lifted from **XBRL** — the highest-fidelity, lowest-risk path.
- **Sourced-narrative (SN):** segment descriptions, re-tag rationale, concentration commentary — extracted from
  the segment footnote and Risk Factors **with citation**, fact-locked to the numeric mix.

---

## 3. OPERATIONS / SUPPLY CHAIN

**What institutional buyers want:** the operating shape of the business — **properties/facilities**,
**headcount**, **key customers/suppliers & concentration**, **R&D intensity**, **capex**, and the qualitative
**moat/intangibles** story. This pillar feeds **V2.0 C4 (Innovation & Moat)** and **C6 (technology
optionality)** and supplies the operating texture institutional buyers expect.

**Primary source (free):** **SEC EDGAR — 10-K** *Item 1 Business*, *Item 1A Risk Factors*, *Item 2 Properties*,
plus XBRL for capex/R&D. Structured figures from XBRL; qualitative items via **AI extraction with citations**
from the specific 10-K section — **no fabricated numbers**.

### 3.1 Line items

| # | Line item | Type | Source (free = SEC EDGAR) | Cadence / as-of | Notes |
| --- | --- | --- | --- | --- | --- |
| O-1 | **Properties / facilities** (owned/leased, location, size, use) | N + SN | 10-K Item 2 (Properties) | Annual | Footprint table; SN for use/role |
| O-2 | **Headcount** (total employees; segment/region split if disclosed) | N | 10-K Item 1 (Human Capital) | Annual | Rev-per-employee (D) |
| O-3 | **Key customers & concentration** (named customers, % of revenue) | N + SN | 10-K (customer concentration disclosure) | Annual | 10%+ customers disclosed under ASC 280 |
| O-4 | **Key suppliers & supply-chain risk** | SN | 10-K Business + Risk Factors | Annual | Extraction + citation; concentration flags |
| O-5 | **R&D intensity** (R&D / revenue, multi-year) | N + D | 10-K XBRL (`rnd`, revenue) | Annual | Feeds V2.0 **C1/C4** |
| O-6 | **Capex** (capex, capex/revenue, capex/D&A) | N + D | 10-K/10-Q XBRL | Annual + quarterly | Reinvestment texture (C2) |
| O-7 | **Moat / intangibles (qualitative)** (switching costs, network effects, brand, IP, scale) | SN | 10-K Business + Risk Factors (AI extraction, cited) | Annual | **No fabricated numbers**; feeds V2.0 **C4** |
| O-8 | **Technology / future-tech optionality (named bets)** | SN | 10-K Business + MD&A + 8-K (AI extraction, cited) | Annual + event | Each option **named + cited**; feeds V2.0 **C6** |
| O-9 | **Recognized intangibles & goodwill** (balance-sheet intangibles, amortization) | N | 10-K XBRL balance sheet | Annual | Ties to `docs/IP_INTANGIBLES_AMORTIZATION.md` |
| O-10 | **Operating risk factors** (top risks, ranked, cited) | SN | 10-K Item 1A | Annual | Extraction w/ citation; no invented severity |

### 3.2 Numeric vs narrative split (Operations)

- **Numeric (N) / Derived (D):** headcount, property counts/areas where tabulated, customer-concentration %,
  R&D intensity, capex ratios, recognized intangibles/goodwill, rev-per-employee. All from **XBRL or filing
  tables**.
- **Sourced-narrative (SN):** moat/intangibles story, named technology bets, supplier risk, ranked risk
  factors. **AI-extracted with a citation to the exact 10-K section**, fact-locked, **explicitly barred from
  asserting numbers not present in an N field**. This is the strict "no fabricated numbers" guardrail applied to
  qualitative extraction.

---

## 4. Intangibles / Tech & Executive-Team tie-in to Valuation Framework 2.0

This construct is the **data-supply layer** for the qualitative half of `docs/VALUATION_FRAMEWORK_2.0.md`.
Where V2.0 declares the *intent* to price management quality, future technology, and intangibles, this document
specifies *the exact fields, sources, and cadence that make those components computable* — without fabrication.

| V2.0 goal / component | What it needs | Supplied by this construct |
| --- | --- | --- |
| **C4 — Innovation & Moat score** | R&D intensity, gross-margin durability, moat qualitative signals, (later) patents | **O-5** (R&D intensity), **O-7** (moat/intangibles qual), **O-9** (recognized intangibles), **S-3/S-5** (margin durability by segment) |
| **C5 — Management / capital-allocation quality** | ROIC trend, buyback/dividend discipline, M&A track record, **insider ownership** | **P-2..P-9** (comp, tenure, insider ownership/transactions, capital-allocation read) |
| **C6 — Technology optionality premium** | *named* option bets, disclosed & bounded | **O-8** (named, cited technology/future-tech bets) — the "identified + separated" inputs C6 requires |
| **C7 — Sector re-tagging** | what the firm *actually is* by segment/KPI | **S-1..S-8** (business + geographic segment map, re-tag) |
| **C3 — Scenario / SoP DCF** | per-segment growth/margin inputs | **S-9** (SoP scaffolding), **S-5** (segment growth) |

**Executive-team quality (V2.0 objective):** captured through **P-1/P-2/P-3/P-7/P-9** — tenure, comp alignment,
pay-vs-performance, and the fact-locked capital-allocation read. Presented as a **labeled** management-quality
signal feeding C5, never as hard "score = fact."

**Future technology & intangibles (V2.0 objective):** captured through **O-7/O-8/O-9** — recognized intangibles
(numeric) plus **named, cited** moat and technology bets (narrative). These become the **identified,
separated** inputs V2.0 **C6** requires (per V2.0 §2.1 optionality guardrails: bounded, named, separated,
scenario-first).

---

## 5. Governance & citation rules (binding)

Inherits `docs/DATA_FOUNDATION_CONSTRUCT.md` §8 in full. Specific to this construct:

1. **SEC EDGAR is the spine, and it is free.** Every pillar here is sourced from **public-domain SEC EDGAR**
   (DEF 14A, 10-K/10-Q XBRL, Form 3/4/5, 8-K). No new vendor is required for P1/P2 (see §7). This is
   deliberately the **raw-line-item-safe** path — EDGAR is the only source allowed to surface raw line-items
   (Data Foundation §1.1).
2. **Numeric fields (N/D):** verbatim from filings/XBRL or transparent derivation; every figure carries
   **value + as-of (filing date + fiscal period) + source**. Derived formulas are disclosed.
3. **Narrative fields (SN):** **AI-extracted with a mandatory citation** to the exact filing + item/section
   (e.g., "10-K FY2025, Item 1A Risk Factors, filed 2026-02-14"). **Fact-locked** — an SN field may not assert
   any number that is not already an N field. **Labeled AI/editorial.**
4. **No fabricated numbers — ever.** Missing inputs render `pending` / `unavailable` (never backfilled). The
   qualitative-extraction path may **quote and summarize** but may **not invent** figures, dates, names, or
   severities.
5. **As-of on every surface** — screen, PDF, Excel — per Data Foundation §3.4.
6. **No licensing spillage** — nothing here depends on SF1 raw rows; SF1 contributes only **derived** metrics
   (ROIC trend, margins) that already surface today. Vendor-sourced enrichments (§7, optional) inherit the same
   derived-only + attribution rules if ever adopted.

---

## 6. Mapping — workbook tabs & on-screen company view

Extends the existing workbook (`docs/CROSS_ASSET_VALUATION_ENGINE_SPEC.md`: `DCF` sheet, per-asset sheets,
`Action Summary` tab) and the on-platform company view with three new depth areas. Every cell/section carries
its as-of + source.

### 6.1 Excel workbook tabs (new / extended)

| Tab | Contents | Pillar | Fields |
| --- | --- | --- | --- |
| **`People & Governance`** (new) | Exec roster + tenure, NEO comp, pay-vs-performance, board table, insider ownership & net-buy trend, management-quality read (labeled), governance flags | People | P-1..P-9 |
| **`Segments`** (new) | Business & geographic segment revenue/OI, mix %, growth trend, concentration index, re-tag, SoP scaffolding | Segments | S-1..S-9 |
| **`Operations`** (new) | Properties, headcount, customer/supplier concentration, R&D intensity, capex, recognized intangibles, moat/tech bets (cited), risk factors | Operations | O-1..O-10 |
| **`DCF`** (extended) | SoP inputs from `Segments`; R&D-as-investment from `Operations`; management/optionality flags surfaced as disclosed lines | V2.0 tie-in | S-9, O-5, O-8, P-7 |
| **`Sources & As-Of`** (extended) | Provenance block: every field's source + filing + as-of + citation for SN fields | All | — |

### 6.2 On-screen company view (new sections)

| Section | Contents | Pillar |
| --- | --- | --- |
| **People & Governance** | Exec/board cards (name, title, tenure, comp, ownership), insider-activity sparkline, management-quality badge (labeled AI/editorial), governance-flag chips | People |
| **Business Segments** | Revenue/OI mix donut + multi-year trend, geographic split, concentration meter, "what this company really is" re-tag line | Segments |
| **Operations & Supply Chain** | Facilities map/table, headcount + rev/employee, customer/supplier concentration, R&D & capex intensity, moat/tech-bet callouts (each with a "per 10-K …" citation link) | Operations |
| **Valuation tie-in strip** | How People/Segments/Operations feed V2.0 C3/C4/C5/C6/C7 (with the optionality line shown separately, per guardrails) | V2.0 |

Both surfaces obey **Always-Deliver**: any missing field renders a labeled gap, the rest of the view/tab still
loads.

---

## 7. Data sources — free vs vendor

| Pillar | Field group | Primary source | Free? | Vendor needed? |
| --- | --- | --- | --- | --- |
| People | Roster, comp, board, ownership (P-1..P-5, P-9) | SEC EDGAR DEF 14A | **Free** | No |
| People | Insider transactions (P-6) | SEC EDGAR Form 3/4/5 | **Free** | No |
| People | Management-quality read (P-7, P-8) | 10-K/8-K + derived + AI | **Free** | No |
| Segments | Business/geo segments, mix, trend (S-1..S-9) | SEC EDGAR 10-K/10-Q **XBRL** (ASC 280) | **Free** | No |
| Operations | Properties, headcount, customers, R&D, capex, intangibles (O-1..O-10) | SEC EDGAR 10-K + XBRL | **Free** | No |
| *Optional enrichment* | Cleaner parsed proxies/segments, org charts, exec bios | Vendor (e.g., segment/KPI or people-data feeds) | Paid | **Only if** EDGAR parsing quality/coverage proves insufficient at scale |

**Bottom line:** P1 and P2 are deliverable on **100% free SEC EDGAR**. A vendor is a **P3+ optional
accelerant** for parsing quality/coverage, not a dependency — and would inherit derived-only + attribution
governance.

---

## 8. Phased rollout (P1 / P2 / P3) with dependencies

Sequenced to ship the highest-value, lowest-data-risk depth first, mirroring the V2.0 rollout (§6 there) and
the Data Foundation phasing.

### Phase 1 — Segments + core Operations numerics *(highest value, all free, machine-readable)*
- **Ship:** **Segments** tab/section (S-1..S-9) from 10-K/10-Q **XBRL**; core **Operations** numerics
  (O-2 headcount, O-5 R&D intensity, O-6 capex, O-9 intangibles).
- **Why first:** XBRL is structured → lowest fabrication risk, immediately feeds V2.0 **C3 (SoP)** and **C7
  (re-tag)** and strengthens **C4** (R&D intensity by segment).
- **Dependencies:** existing SEC EDGAR fundamentals ingestion (already live per Data Foundation §1.1);
  XBRL segment/geo parsing; workbook + company-view scaffolding.

### Phase 2 — People / Governance + insider ownership
- **Ship:** **People & Governance** tab/section (P-1..P-9) from **DEF 14A** + **Form 3/4/5**; management-quality
  read (P-7) fact-locked to metrics.
- **Why second:** directly delivers V2.0 **C5 (management / capital-allocation quality)**, which V2.0 itself
  schedules in its Phase 2 (Form 4 insider ownership).
- **Dependencies:** DEF 14A + Form 4 ingestion + parsing; Phase-1 fundamentals for the capital-allocation
  (ROIC-trend/buyback) read; AI-extraction + citation pipeline (shared with Phase 3).

### Phase 3 — Qualitative moat/tech extraction + full Operations depth (+ optional vendor)
- **Ship:** AI-extracted, **cited** qualitative fields — **O-4** (suppliers), **O-7** (moat/intangibles),
  **O-8** (named tech bets), **O-10** (ranked risks), **O-1** (properties detail), **O-3** (customer
  concentration narrative), **P-8** (governance flags), **S-8** re-tag narrative depth.
- **Why last:** highest extraction complexity and review burden; feeds V2.0 **C6 (technology optionality)** and
  deepens **C4**. Optional **vendor** enrichment considered here if EDGAR parsing coverage is insufficient.
- **Dependencies:** AI-extraction + **citation/fact-lock** pipeline (Data Foundation §8); Phase-1 segment map
  and Phase-2 people data for context; V2.0 C6 optionality guardrails (bounded/named/separated) in place.

---

## 9. Testing & acceptance

Acceptance mirrors the Data Foundation acceptance bar (§10 there), scoped to this construct:

1. **As-of everywhere** — automated check: every People/Segments/Operations field on screen, PDF, and Excel
   carries actual-data-date + filing + source.
2. **Citation on every SN field** — no sourced-narrative field renders without a resolvable citation to a filing
   + section; fact-lock check confirms SN fields assert no number absent from an N field.
3. **Never-fabricate** — with a filing missing (e.g., no current DEF 14A), the field renders `pending` /
   `unavailable`; no invented value.
4. **Always-deliver** — with any one filing/source forced offline, the company view and workbook still render
   (labeled gaps), no request 500s.
5. **XBRL fidelity** — segment/geo numbers reconcile to the filed 10-K/10-Q segment footnote.
6. **V2.0 wiring** — S-9 feeds SoP inputs; O-5/O-8 and P-7 surface into the DCF tab as disclosed, separated
   lines (optionality never blended silently).
7. **Governance** — no licensed SF1 raw row appears in any new surface; all raw line-items trace to SEC EDGAR.

**Test types:** unit (XBRL/segment parsing, derivation math, citation presence) · integration (ingest → cache →
workbook/company-view render + degradation) · contract (as-of + citation presence on outputs) · governance
(no-spillage + no-fabrication assertions).

---

*Prepared under JHI-SIG `69M2705M`. Aegira is a product of JHI Research & Analytics Firm, Inc. Built on free
SEC EDGAR first; feeds Valuation Framework 2.0 (C3/C4/C5/C6/C7); governed by the Data Foundation doctrine —
Always-Deliver · Cadence-Aware · As-Of-Disclosed. Research, not investment advice.*
