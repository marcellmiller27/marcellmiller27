# Competitive Differentiation — Top ~20 Teardown, Pain-Point Matrix & Aegira Wedge

**Date:** 2026-08-13 · **JHI-SIG:** `69M2705M`
**Product:** Aegira · **Publisher:** JHI Research & Analytics Firm, Inc. (proprietary)
**Owner:** Cy Henry (VP, Software Engineering — AI) · **Status:** strategy / analysis document (drives product + pricing). No UI code.

> A rigorous reverse-engineering of the **top ~20 entities** the independent investor and the Main-Street/search-fund
> acquirer actually run into — sell-side research, independent/macro research, data terminals, PE/M&A intelligence,
> hedge-fund/quant screening, and SMB acquisition resources. For each we capture *what they do, who they serve, price,
> core value prop,* and — critically — the **pain points / gaps** they leave open. We then synthesize a **pain-point
> matrix**, map each gap to an **existing Aegira capability** (honestly flagging where we have a **gap to build**),
> recommend **Tier 1 vs Tier 2 packaging**, and hand off a **prioritized "pain-points to own" backlog (P1/P2/P3)**.
>
> Companion docs: `docs/COMPETITOR_TEARDOWN_AND_GAP_MAP.md`, `docs/COMPETITOR_DEEP_DIVE_PAIN_POINTS.md`,
> `docs/COMPETITOR_AUDIT_42MACRO.md`, `docs/VALUATION_FRAMEWORK_2.0.md`,
> `docs/ACQUISITION_INTELLIGENCE_FRAMEWORK.md`, `docs/AEGIRA_SIGNAL_ENGINE.md`,
> `docs/MAIN_STREET_ACQUIRER_CONSTRUCT.md`, `docs/PRICING_BILLING_SCHEMA.md`.
> Pricing is public-research-grounded (2026); most incumbents publish no list price, so ranges are cited from verified
> procurement/benchmark data and marked accordingly. Not affiliated with any entity named. Research/education — not
> investment, legal, tax, or accounting advice.

---

## 0. Executive summary

The independent investor and the SMB/search-fund acquirer are served by a market that is **expensive, fragmented,
walled-off, single-asset, sourcing-only, and jargon-heavy.** No incumbent does the *whole job* — screen → value →
diligence → close → stay-informed — at a subscriber price, in plain-English institutional output, across asset classes
*and* the acquisition angle. That white space is precisely where Aegira's existing constructs already sit.

The five recurring, monetizable gaps (detailed in §2):
1. **Price wall** — the useful tools cost $12k–$32k+/seat/yr with opaque, negotiated, multi-year contracts.
2. **Fragmentation** — a real workflow needs 5–8 tools stitched with Excel and a CPA; nobody integrates them.
3. **Sourcing/data stops before the decision** — they sell *data* and *listings*; none automate the first-pass read,
   the QoE, or the valuation the user actually needs to say *yes/no*.
4. **Single-asset silos + no acquisition angle** — equities-only screeners, macro-only research, PE-only databases;
   the cross-asset investor *and* the operating-business buyer are both underserved.
5. **Trust opacity** — proprietary scores with no published t-stat; "free trials" that are sales demos; redistribution
   limits that stop you re-using what you paid for.

Aegira's answer, using capabilities that already exist as constructs of record: **cross-asset Valuation 2.0 + Signal
Engine**, **technicals/multi-horizon depth**, **Opportunity Scan / SF1 screens**, the **Acquisition Intelligence
Framework** (LSR → QoE → DCF → SBA-DSCR), the **Main Street Acquirer** newsletter, **auto-generated branded
institutional output**, **plain-English fact-locked narration**, **published H5 validation**, and **transparent
subscriber pricing** ($110 / $299 / $1,500). The honest gaps we must build are in §3.4.

---

## 1. Method & scope

Same discipline as `COMPETITOR_TEARDOWN_AND_GAP_MAP.md`: for each entity we extract **what they do · who they serve ·
price · core value prop · the pain points / gaps** for the independent investor or acquirer. Pain points are the asset —
each is a wound we can dress as a feature. Where an entity is named for illustration (retail cannot buy it directly, or
it stands in for a group), it is flagged **[illustrative]**.

**~20 entities across six categories** (23 listed; some grouped):

| # | Category | Entities |
| --- | --- | --- |
| A | Wall St. sell-side research | Goldman Sachs GIR · Morgan Stanley Research · J.P. Morgan Research |
| B | Independent / macro research | 42 Macro · Fundstrat / FSInsight · BCA Research · Morningstar · CFRA |
| C | Data / terminal platforms | Bloomberg Terminal · LSEG (Refinitiv) · S&P Capital IQ Pro · FactSet · Koyfin · AlphaSense (+Tegus/Sentieo) |
| D | PE / M&A intelligence | PitchBook · CB Insights · Preqin |
| E | Hedge-fund / quant / screening | YCharts · Portfolio123 · QuiverQuant |
| F | Search-fund / SMB acquisition | BizBuySell · Axial · Grata / SourceScrub |

Price convention: **/yr per seat** unless noted; "custom" = no public list, range from verified buyer/procurement data.

---

## 2. Per-entity teardown

### Category A — Wall Street sell-side research **[all illustrative — no direct retail purchase]**

| Entity | What they do | Who they serve | Price | Core value prop | Pain points / gaps for the independent investor or acquirer |
| --- | --- | --- | --- | --- | --- |
| **Goldman Sachs Global Investment Research** | Single-stock, sector, macro, thematic research; conviction lists; analyst models | Institutional brokerage clients (funds, IBD) | Bundled into trading commissions / MiFID-unbundled institutional fees (effectively **$$$**, not retail-purchasable) | Brand authority, analyst access, market-moving calls, deep sector models | **Walled garden** — you cannot buy it as an individual; **conflict-laden** (banking/trading relationships); **no acquisition/diligence layer**; **equities/macro only**; distributed as PDF you can't re-run or personalize |
| **Morgan Stanley Research** | Equity/credit/macro research, thematic ("blue papers"), model portfolios | Institutional / private-wealth clients | Institutional/bundled (**not retail**) | Franchise analysts, thematic depth, PWM distribution | Same walls: **access-gated to clients**, **no SMB/private-company or diligence angle**, **static PDFs**, no personalization, redistribution forbidden |
| **J.P. Morgan Research** | Global equity/FICC/macro research + data science overlays | Institutional clients | Institutional/bundled (**not retail**) | Breadth, data-science augmentation, global desk | **Not accessible** to independents; **no cross-asset personal portfolio view**, **no acquisition tools**, no plain-English "what do I do" for a non-institution |

**Read on Category A:** the sell-side sets the *authority aesthetic* Aegira should emulate (named analysts,
conviction, thematic depth) but is structurally closed to our ICP, conflicted, equities/macro-only, and never touches
the operating-business buyer. We copy the *voice and rigor*, not the wall.

---

### Category B — Independent research & macro

| Entity | What they do | Who they serve | Price (2026) | Core value prop | Pain points / gaps |
| --- | --- | --- | --- | --- | --- |
| **42 Macro** | Process-driven macro research (GRID regimes, Weather Model, VAMS) + signals dashboard + education funnel | Self-directed + pro investors wanting institutional macro | **$95/mo** (weekly) · **$195/mo** (daily+weekly+monthly); free "The Weekly" funnel | Repeatable *named system* + heavy visuals + free→paid funnel; "hedge-fund-caliber, accessible" | **Top-down macro only** — no bottom-up companies, transactions, or diligence; **no acquisition angle**; **no cross-asset valuation of a specific name**; heavy jargon (mitigated by Playbook) |
| **Fundstrat / FSInsight** | Tom Lee's macro + equity + crypto research, technical work, model portfolios | Serious self-directed investors | **$79/mo** Crypto · **$169/mo** Macro · **$219/mo** Pro (app-store tiers run higher) | Named personality, track-record claims, macro+crypto+technical in one voice | **Research, not tools** — no live valuation engine, no screening you drive, **no private-company/acquisition layer**; personality-dependent; **no cross-asset portfolio decisioning** |
| **BCA Research** | Institutional global macro/strategy across services | Institutions, RIAs, sophisticated allocators | **Custom / institutional** (commonly **$10k–$50k+/yr**; free 30-day trial) | 75-yr macro brand, deep strategy | **Institutional price + posture**; **no company/deal depth**, **no diligence**, **no self-serve tools**; PDF-led |
| **Morningstar** (Investor + methodology) | Fund/equity research, star ratings, quant fair value, Portfolio X-Ray | Self-directed investors, advisors | **Morningstar Investor $249/yr** (~$199 intro); pro/data tiers far higher | **Transparency king** — published, buffered, out-of-sample methodology; trusted fair value + moat | **Equities/funds only**; **no private-company or acquisition tooling**; no cross-asset trade signals; **no plain-English deal decisioning**; advisor/pro features gated up-market |
| **CFRA** | Independent equity + fund research, STARS ratings, forensic accounting | Institutions, advisors; **indirect retail** via brokerages | **Institutional / bundled** (accessed free inside Fidelity/IBKR etc.) | Independent (post-S&P) equity research + forensic accounting rigor | **Not a self-serve product** for our ICP; **equities-only**; **no acquisition/diligence/cross-asset**; distributed inside someone else's walled garden |

**Also-rans (grouped, illustrative):** **ARK Invest** (free research, thematic-only, no tools/valuation),
**Gavekal** (institutional macro, custom price, no bottom-up/deal layer), **Zacks / Motley Fool** ($199–$249/yr,
equities-only stock-picking, no diligence or cross-asset). The pattern holds: **great research, no integrated doing,
single-asset, no acquisition angle.**

**Read on Category B:** the closest philosophical peers. 42 Macro is the **funnel + system + education** blueprint;
Morningstar is the **transparency** blueprint. Every one of them is **research-only, single-asset, and blind to the
operating-business buyer.** Aegira pairs the *same institutional voice* with **integrated tools + cross-asset +
acquisition depth** — the fusion none of them offer.

---

### Category C — Data / terminal platforms

| Entity | What they do | Who they serve | Price (2026) | Core value prop | Pain points / gaps |
| --- | --- | --- | --- | --- | --- |
| **Bloomberg Terminal** | The reference terminal: real-time data, analytics, IB chat, trading, news across 35M+ instruments | Institutions, traders, PMs | **~$31,980/yr single seat** (~$28,320 multi); 2-yr min; no public price | Unmatched breadth + IB messaging network + newsroom; deep lock-in | **Prohibitive price**; **institutional-only**; steep learning curve; **no SMB/private-business acquisition workflow**; **no "get to no fast" deal decisioning**; redistribution restricted |
| **LSEG (Refinitiv / Eikon / Workspace)** | Data + analytics terminal, deep FX/fixed income | Institutions | **~$14k–$22k/yr** | Breadth, FX/FI depth, Reuters news | Same wall: **cost, complexity, institutional-only, no acquisition angle, no plain-English output** |
| **S&P Capital IQ Pro** | Deep public+private financials, credit, comps, ChatIQ | IB, public-markets, credit | **~$12k–$30k+/seat/yr** (custom) | Financial breadth + S&P brand + workflow lock-in | **Cost/complexity overkill for SMB buyers**; **redistribution limits**; steep curve; sub-$5M coverage thin; not built for the searcher |
| **FactSet** | Analytics, models, portfolio + quant workflows, Excel add-in | Buy/sell-side pros | **~$12k–$18k/seat/yr** (custom) | Model/portfolio workflow depth, integrations | **Price + complexity**; enterprise-only; **no acquisition/diligence layer**; **no plain-English decisioning** for independents |
| **Koyfin** | Bloomberg-lite research/charting/screening on S&P CapIQ data | Individual investors, analysts, advisors | **Free → $39/$79/$209/$299 per mo (annual)** | *Accessible* institutional-quality data; strong price/value | **No private-company / acquisition tooling**; **no QoE/DCF diligence**; screening-and-charts, not deal decisioning; **no validated trade signals**; advisor tiers climb |
| **AlphaSense (+ Tegus, Sentieo)** | AI search over filings, transcripts, broker research + 200k+ expert-call transcripts | Analysts, PE, corp strategy | **Custom**, ~**$10k–$20k/seat** core; **$25k–$50k+** with Tegus/broker content; enterprise $100k–$500k+ | AI search across licensed content + expert-call moat | **Search/insight, not diligence/valuation**; **very expensive with content add-ons**; **redistribution/licensed-content walls**; **no SMB deal workflow**, no cross-asset valuation output |

**Read on Category C:** these are **data pipes and search**, priced for institutions, redistribution-restricted, and
they *stop at the data*. Koyfin proves the **accessible-price** appetite but still ends at charts/screens with **no
diligence, no acquisition, no validated signal, no branded output.** Aegira does not out-data them (per the
teardown's Rule 2) — we **integrate, decide, and package** on top of legitimately-licensed derived data.

---

### Category D — Private Equity / M&A intelligence

| Entity | What they do | Who they serve | Price (2026) | Core value prop | Pain points / gaps |
| --- | --- | --- | --- | --- | --- |
| **PitchBook** (Morningstar) | Private-market database (25 datasets), VC Exit Predictor, comps, Excel/PPT plugins | VC/PE/IB/corp-dev; $5M+ buyers | **Custom**, median **~$30k/yr**; ~$12k–$20k single seat; **+~$7k/extra seat** | Genuine **data network-effect moat** (crawlers + 1,800 researchers) | **Price + per-seat gouging + opaque pricing**; **thin sub-$5M SMB coverage**; **stops at data — no QoE/first-pass read**; Excel plugin "limited/restricted"; stale ownership gripes; hostile to small buyers |
| **CB Insights** | Predictive tech-market intel, Mosaic scores, market maps | Corp strategy, VC, enterprise | **Custom**, core **from ~$60k/yr** | Predictive tech/startup intelligence, Mosaic | **Very expensive**; **tech-startup-centric**; **can't ingest your own deal docs**; unintuitive search; **not for SMB acquisition diligence at all** |
| **Preqin** (BlackRock) | Alternatives/fund performance, LP-GP data, benchmarks | LPs/GPs, fund benchmarking | **~$25k–$81k+/yr** (module + seat based) | Fund-return dataset + BlackRock distribution; relatively transparent | **Institutional-only, not deal-level SMB**; **no operating-business diligence**; **no cross-asset personal decisioning**; module-priced up fast |

**Also-ran (illustrative):** **Mergr** — clean, honest "who uses" PE/M&A *directory* (a good presentation model), but a
directory, **not a diligence tool**. **Grata / SourceScrub** covered in Category F (sourcing).

**Read on Category D:** the data kings we will **not** out-data. Their shared, exploitable oversight is unanimous in
our repo research: **they stop at sourcing/data and leave the buyer to bolt on Excel + a CPA + a data room.** PitchBook
even documents that its Exit Predictor **omits financials/business model.** The **first-pass read, QoE, and valuation —
the decision — is unowned.** That is Aegira's Acquisition Intelligence Framework, end to end.

---

### Category E — Hedge-fund tooling / quant / screening

| Entity | What they do | Who they serve | Price (2026) | Core value prop | Pain points / gaps |
| --- | --- | --- | --- | --- | --- |
| **YCharts** | Research, charting, screening, proposal/report generation on institutional data | Advisors, analysts, firms | **$3,600/yr (Analyst)** · **$6,000/yr (Presenter)** · Enterprise custom | Advisor-grade research + branded client reports | **Expensive for individuals** (10–15× retail tools); **equities/funds only**; **no private-company/acquisition tooling**; **no validated trade signals**; **no QoE/DCF diligence** |
| **Portfolio123** | Rules-based quant screening + 20-yr point-in-time backtesting + ranking systems (FactSet data) | Systematic retail/semi-pro | **Free → $25/mo (Screener) → $83/mo (Pro)** | Deep, affordable **backtesting/ranking rigor** | **Steep curve, dated UI**; **equities-only**; **no acquisition/private-company layer**; **no plain-English output** (it's a quant IDE); no branded newsletter/deliverable |
| **QuiverQuant** | Alternative-data signals (Congress trades, gov contracts, WSB, insider) + screeners/backtests | Retail, alt-data enthusiasts | **Free → ~$25/mo** (API $30–$75/mo) | Novel, cheap **alt-data edge** | **Signal novelty, not decisioning**; **no valuation/diligence**; **no acquisition angle**; **no validation rigor / published t-stats**; equities-centric |

**Also-ran (illustrative):** **Tegus** (now AlphaSense) — expert-call transcripts, institutional-priced, **research
input not a decision engine**; **Stock Rover / Trade Ideas** — retail screening/scanning, equities-only, no diligence.

**Read on Category E:** proves the **low-price, self-serve, systematic** appetite (Portfolio123 at $25–83/mo;
QuiverQuant at ~$25/mo). But these are **equities-only, tool-fragments** — a screener *or* a backtester *or* an
alt-data feed — with **no valuation decision, no diligence, no acquisition, no validated cross-asset signal, no
plain-English or branded deliverable.** Aegira's Signal Engine + Valuation 2.0 fuse screen → value → signal with
**published H5 validation** these tools never disclose.

---

### Category F — Search-fund / SMB acquisition resources

| Entity | What they do | Who they serve | Price (2026) | Core value prop | Pain points / gaps |
| --- | --- | --- | --- | --- | --- |
| **BizBuySell** | Largest US business-for-sale marketplace (listings, comps, broker directory) | Individual buyers, searchers, brokers | **Free for buyers**; sellers **$65.95–$199.95/mo** | Inventory scale + geographic coverage | **Listings, not analysis**; **variable/low data quality + noise**; **no diligence/valuation/QoE**; **no financeability (SBA-DSCR) read**; top listings over-contested; nothing to *decide* with |
| **Axial** | Vetted lower-middle-market M&A marketplace (advisor-posted, diligence-ready teasers) | PE, family offices, funded searchers | Buyer access **~$12k–$24k/yr** (or success-fee model, per Axial) | Quality intermediated LMM deal flow | **Not proprietary** (everyone sees it); **$5M+ EBITDA tier** — above most searchers; **marketplace not toolset** — no valuation/QoE/close workflow; priced up for the solo searcher |
| **Grata / SourceScrub** (Datasite) | AI thesis-to-target sourcing over ~19M private cos + verified contacts + intent signals | Independent sponsors, search funds, thematic PE | **~$12k–$40k+/yr** (custom) | Mature AI sourcing + contact/intent data | **Stops at sourcing** — no QoE, no financial diligence, no valuation, no close; **still bolt on Excel + CPA + data room**; custom price climbs |

**Also-ran (illustrative / public data):** **SBA 7(a)/504 open loan data** (public, free, but **raw — no analysis
layer**; searchers can't easily turn it into a financeability signal), **ETA communities / Acquire.com / MicroAcquire**
(networks + digital-SMB listings, **no institutional diligence**). Typical searcher stack today: **Grata ($12–20k) +
Axial ($5–10k) + a network + Excel + a $20–30k QoE = $25–40k/yr and a manual, fragmented process.**

**Read on Category F:** this is Aegira's **beachhead** and the market's biggest hole. The economics (from
`COMPETITOR_DEEP_DIVE_PAIN_POINTS.md`): search costs **$250k–$350k over ~20 months; ~⅓ never acquire; 33% of LOIs
fail; 46.6% of dead deals die from diligence findings**; QoE is **$20k–$30k and only run after LOI.** The bottleneck is
**reading the CIM and getting to *no* fast** — and **nobody automates it.** BizBuySell has inventory but no analysis;
Axial/Grata source but stop before diligence; SBA data is raw. Aegira's LSR → QoE → DCF → **SBA-DSCR** + the **Main
Street Acquirer** newsletter are built exactly for this gap, on **legit public data (no scraping).**

---

## 3. Synthesis

### 3.1 Pain-point matrix — recurring gaps these audiences would pay to solve

| # | Recurring pain point | Who feels it most | Who's guilty | Willingness-to-pay signal |
| --- | --- | --- | --- | --- |
| **G1 — Price wall** | Useful tools are $12k–$32k+/seat, opaque, multi-year, per-seat gouged | Independents, searchers, small firms | Bloomberg, CapIQ, FactSet, PitchBook, CB Insights, AlphaSense, YCharts | Koyfin ($39–299/mo), Portfolio123 ($25–83/mo), 42 Macro ($95–195/mo) all scaled by *undercutting on price* |
| **G2 — Fragmentation** | Real workflow = 5–8 tools + Excel + a CPA + a data room | Searchers, independent sponsors | Everyone (each does one slice) | Searchers already pay **$25–40k/yr** stitching Grata+Axial+Excel; would pay to consolidate |
| **G3 — Stops before the decision** | They sell data/listings/sourcing, not the *yes/no* (first-pass read, QoE, valuation) | Acquirers especially | PitchBook, Grata, SourceScrub, Axial, BizBuySell, terminals | **$20–30k QoE only after LOI**; huge unmet demand for cheap early "get-to-no" screening |
| **G4 — Single-asset silos** | Equities-only, or macro-only, or private-only — no cross-asset view | Cross-asset independents | Morningstar, CFRA, Koyfin, YCharts, P123, Quiver, 42 Macro | Users pay for *multiple* subs to cover asset classes; a unified sub captures that spend |
| **G5 — No acquisition angle** | Investor tools ignore the operating-business buyer entirely | Searchers/ETA/SMB | All of A–E | Distinct $25–40k/yr acquisition stack exists *separately* today |
| **G6 — Trust opacity** | Proprietary scores with no published t-stat; "free trials" that are sales demos | All | PitchBook, CB Insights, most of B/E | Morningstar's *transparency* is a paid differentiator; searchers demand "show its work" |
| **G7 — Redistribution / walled gardens** | Can't re-use, re-run, or personalize what you paid for; PDFs, licensed-content locks | All | Sell-side, terminals, AlphaSense, CapIQ | Users value **exportable, ownable, re-runnable** outputs (PitchBook Excel gripes) |
| **G8 — Jargon / no plain-English decisioning** | Institutional output assumes an institutional reader; no "what do I do" | Independents, searchers | Sell-side, terminals, quant IDEs (P123) | 42 Macro's *disclosed-jargon Playbook* and "always actionable" style drove its growth |
| **G9 — Raw data, no analysis layer** | Public gold (SBA, EDGAR, FRED) exists but is unusable raw | Searchers | SBA data tools, BizBuySell | The Main Street Acquirer's SBA Lending Intelligence is a proven email-gate magnet |

### 3.2 Aegira's differentiation thesis — pain point → existing capability (honest status)

Status legend: ✅ live · 🟡 partial / building · 🔴 gap to build. Statuses reconciled to the source constructs.

| Pain | Aegira capability that wins it | Source construct | Status |
| --- | --- | --- | --- |
| **G1 Price wall** | Transparent published pricing: **$110 / $299 / $1,500**; 94–96% margin by design; no fake trial, no lock-in traps | `PRICING_BILLING_SCHEMA.md`, `COMPETITOR_DEEP_DIVE_PAIN_POINTS.md` | ✅ live (schema); 🟡 pricing-page/Stripe apply |
| **G2 Fragmentation** | One platform: **screen → value → diligence → close → stay-informed** (LSR/QoE → Valuation Engine → Pipeline → newsletter) | `ACQUISITION_INTELLIGENCE_FRAMEWORK.md` | 🟡 partial (LSR/QoE/DCF ✅; DD checklist, industry/market/ratios modules 🔴) |
| **G3 Stops before the decision** | **LSR (first-pass read) + QoE lens + DCF → adjusted EBITDA → unlevered FCF**; "get to *no* fast" pre-screen before the $20–30k QoE spend | `ACQUISITION_INTELLIGENCE_FRAMEWORK.md` §2 | ✅ live (QoE+DCF, Phase 1); 🟡 guided first-pass/CIM auto-extract (Deal X-Ray v2) 🔴 |
| **G4 Single-asset silos** | **Cross-Asset Valuation 2.0 + Signal Engine**: equities, ETFs, commodities, crypto, forex, options; per-asset fair-value math | `AEGIRA_SIGNAL_ENGINE.md`, `VALUATION_FRAMEWORK_2.0.md`, `CROSS_ASSET_VALUATION_ENGINE_SPEC.md` | 🟡 Phase 1 = equities/ETFs live/building; commodities/crypto/forex/options phased (P2/P3) |
| **G5 No acquisition angle** | The **Acquisition Intelligence Framework** + **Main Street Acquirer** newsletter — a whole product line the investor-tools ignore | `ACQUISITION_INTELLIGENCE_FRAMEWORK.md`, `MAIN_STREET_ACQUIRER_CONSTRUCT.md` | 🟡 framework + tools partial; newsletter build target |
| **G6 Trust opacity** | **Published H5 validation** (pre-registered IC/t-stat/hit-rate bars; ship `validated` vs `directional`; disclose FAILs) — out-transparent everyone | `AEGIRA_SIGNAL_ENGINE.md` §9, `H5_SF1_VALIDATION_RESULTS.md` | ✅ live method; 🟡 public methodology/validation page |
| **G7 Redistribution / walls** | **Exportable, ownable deliverables**: institutional Excel **Workbook** + branded PDF; interactive/editable, yours to keep | `ACQUISITION_INTELLIGENCE_FRAMEWORK.md` (exports), `COMPETITOR_DEEP_DIVE_PAIN_POINTS.md` | ✅ workbook live (Phase 1); 🟡 breadth of exports |
| **G8 Jargon / plain-English** | **Fact-locked AI narration** (P3): plain-English institutional output tied to model numbers; disclosed-jargon glossary | `AEGIRA_SIGNAL_ENGINE.md` P3, `GLOSSARY_AND_ACRONYMS.md` | ✅ fact-lock principle; 🟡 surface-by-surface |
| **G9 Raw data → analysis** | **SBA engine** turns public SBA 7(a)/504 into a financeability signal; FRED/BLS/BEA/EDGAR derived analysis | `MAIN_STREET_ACQUIRER_CONSTRUCT.md`, `DATA_FOUNDATION_CONSTRUCT.md` | 🔴 SBA engine build target; economic tracking ✅ |
| **cross-cutting** | **Auto-generated branded newsletters** (cross-asset + Main Street Acquirer) — a distribution/retention engine none of B/E/F own end-to-end | `MAIN_STREET_ACQUIRER_CONSTRUCT.md`, `CROSS_ASSET_DISTRIBUTION_CONSTRUCT.md` | 🟡 build target |

**The one-line thesis:** *Every incumbent sells one slice — data, or research, or listings, or a screener — expensive,
single-asset, and blind to the acquirer. Aegira fuses cross-asset valuation, validated signals, and the full
acquisition workflow into one plain-English, transparently-priced, exportable product — and proves its numbers with a
published t-stat nobody else discloses.*

### 3.3 Where we honestly still WIN vs. where we must be humble

- **We will not out-data** Bloomberg/CapIQ/FactSet/PitchBook (10M-research-hour, 1,800-researcher moats). Don't try.
- **We out-integrate, out-price, out-transparent, and own the acquisition + cross-asset fusion** none of them attempt.
- **We win the searcher/SMB beachhead** the giants ignore, then expand into the independent cross-asset investor.

### 3.4 Honest GAP list (what we must build to make the thesis real)

| Gap to build | Attacks | Priority (see §5) |
| --- | --- | --- |
| **CIM upload → first-pass auto-extract (Deal X-Ray / LSR v2)** | G2, G3 (the #1 searcher pain: "the bottleneck is *reading*") | **P1** |
| **SBA engine** (7(a)/504 → financeability signal + DSCR) | G3, G5, G9 | **P1** |
| **DD Checklist module tied to Pipeline** (deal-linked, exportable) | G2, G3 | **P1** |
| **Public Methodology & Validation page** (publish IC/t-stats + limits) | G6 | **P1** (marketing) |
| **Cross-asset breadth** (commodities/crypto/forex/options — Signal Engine P2/P3) | G4 | **P2** |
| **Industry / Market / Key-Ratios modules** (benchmarks) | G2, G3 | **P2** |
| **Auto-generated branded newsletters live** (cross-asset + Main Street Acquirer) | G5, G8, cross-cut | **P2** |
| **Score-stability buffering + fundamentals depth** (Valuation 2.0 P2/P3) | G6 | **P3** |

---

## 4. Tier 1 vs Tier 2 packaging recommendation

Per the **authoritative top-down convention** (`PRICING_BILLING_SCHEMA.md` §0): **T1 = Enterprise ($1,500/mo, premium)**,
**T2 = Professional ($299/mo, premium)**, **T3 = Consumer/Individual ($110/mo; $99/mo prepaid)**. Premium features gate
to **T1 + T2**; T3 is the funnel entry and upgrade lever. Packaging maps each differentiator to the **willingness-to-pay
signal** from the teardown.

| Capability (differentiator) | WTP anchor from teardown | **T3 Consumer $110** | **T2 Professional $299** | **T1 Enterprise $1,500** |
| --- | --- | --- | --- | --- |
| Cross-asset valuation + validated signals (read) | 42 Macro $95–195; Koyfin $39–299; FSInsight $79–219 | ✅ core read + limited names | ✅ full universe, all horizons/assets | ✅ + batch/portfolio + priority |
| Opportunity Scan / SF1 screens | Portfolio123 $25–83; Quiver ~$25; Koyfin | ✅ basic screens | ✅ full screens + saved/backtest | ✅ + team/portfolio screens |
| Plain-English fact-locked research + newsletters | 42 Macro / FSInsight $95–219 | ✅ free/low newsletter + digests | ✅ full editorial + Ask Aegira | ✅ + branded/white-label editions |
| **Company Workbook (institutional Excel export)** | YCharts $3,600–6,000; PitchBook Excel gripes | ❌ (upgrade lever) | ✅ company/comps workbook | ✅ **branded / portfolio / batch** |
| **Acquisition suite: LSR → QoE → DCF → SBA-DSCR** | Grata+Axial+QoE stack **$25–40k/yr** | 🟡 education + templates only | ✅ live valuation + QoE + DSCR | ✅ + deal-linked DD + Pipeline at scale |
| **Deal-linked Pipeline + DD Checklist** | broken-deal reserve ~$50k; QoE $20–30k | ❌ | ✅ single-user pipeline | ✅ **team accounts + RBAC + multi-seat** |
| Published methodology / validation transparency | Morningstar transparency premium | ✅ (marketed to all — trust) | ✅ | ✅ |
| Team seats / RBAC / white-label | PitchBook +$7k/seat; Bloomberg per-seat | ❌ single seat | ❌ single seat | ✅ **5 seats + $99/add'l (NASDAQ-mirrored)** |

**Packaging logic:**
- **T3 ($110)** mirrors the **retail research price band** (Morningstar $249/yr, Seeking Alpha $299/yr, 42 Macro
  $95/mo): read-only cross-asset + newsletters + education + the transparency story. It's the **funnel and upgrade
  lever** — it withholds the *doing* (workbook, live QoE/DCF, deal-linked DD).
- **T2 Professional ($299)** is the **independent-investor + solo-searcher workhorse**: full cross-asset tools, screens,
  the **Company Workbook**, and the **live acquisition suite (LSR/QoE/DCF/SBA-DSCR)** — priced *under* one YCharts seat
  ($3,600/yr) and a fraction of the $25–40k searcher stack. This is the tier the teardown says has the deepest,
  most-underserved WTP.
- **T1 Enterprise ($1,500 + $99/seat)** adds what **firms** pay per-seat for elsewhere: **team accounts, RBAC,
  multi-seat, branded/white-label output, portfolio/batch workbooks, deal-linked DD at scale.** The per-seat line is the
  deliberate mirror of NASDAQ's overage (margin locked in lockstep).

**Net:** the **acquisition suite + Company Workbook + deal-linked Pipeline** are the T2/T1 gates (highest WTP, hardest
to replicate); **cross-asset read + newsletters + transparency** anchor T3 and pull upgrades; **seats/RBAC/white-label**
justify T1.

---

## 5. Prioritized "pain-points to own" backlog (P1 / P2 / P3)

Each item = the **feature**, the **competitor gap it attacks**, and the **pain(s)** from §3.1. Sequenced to ship the
highest-WTP, most-defensible wedge first (the acquisition beachhead the giants ignore), then breadth, then depth.

### P1 — Own the acquisition decision & the trust story (beachhead; highest WTP, lowest competition)
| # | Feature to ship | Competitor gap it attacks | Pain |
| --- | --- | --- | --- |
| P1.1 | **CIM upload → first-pass auto-extract (LSR/Deal X-Ray v2)** — "get to *no* fast" | PitchBook/Grata/SourceScrub/Axial **stop before the read** | G2, G3 |
| P1.2 | **SBA engine → financeability signal + DSCR** (Main Street Acquirer signature) | BizBuySell/SBA tools = **raw data, no analysis**; terminals ignore SMB | G3, G5, G9 |
| P1.3 | **DD Checklist module tied to Pipeline** (deal-linked, exportable) | Nobody offers integrated diligence→close for SMB | G2, G3 |
| P1.4 | **Public Methodology & Validation page** (publish IC/t-stats + limits + FAILs) | No incumbent publishes a t-stat; "fake trials" erode trust | G6 |
| P1.5 | **Transparent pricing + real self-serve trial live on site** | Opaque/punitive pricing; sales-demo "trials"; lock-in traps | G1 |

### P2 — Broaden the cross-asset + editorial engine (capture multi-sub spend)
| # | Feature to ship | Competitor gap it attacks | Pain |
| --- | --- | --- | --- |
| P2.1 | **Cross-asset breadth** — commodities/crypto/forex/options (Signal Engine P2/P3) | Morningstar/CFRA/Koyfin/YCharts/P123/Quiver = **single-asset** | G4 |
| P2.2 | **Auto-generated branded newsletters live** (cross-asset + Main Street Acquirer) | 42 Macro owns *macro-only* funnel; nobody fuses macro+company+deal | G5, G8 |
| P2.3 | **Industry / Market / Key-Ratios modules** with sector benchmarks | Sourcing tools give data, not benchmarked *context* | G2, G3 |
| P2.4 | **Interactive, unrestricted Excel/PDF exports** across modules | PitchBook Excel "limited/restricted"; redistribution walls | G7 |

### P3 — Deepen credibility & institutional polish (retention, up-market)
| # | Feature to ship | Competitor gap it attacks | Pain |
| --- | --- | --- | --- |
| P3.1 | **Valuation 2.0 fundamentals depth + score-stability buffering** | Morningstar's buffered methodology is the trust bar to match | G6 |
| P3.2 | **Team accounts / RBAC / white-label branded editions** (T1) | PitchBook/Bloomberg per-seat gouging; sell-side no personalization | G1, G7 |
| P3.3 | **Plain-English decisioning layer everywhere** (fact-locked "what to do") | Terminals/quant IDEs/sell-side assume an institutional reader | G8 |

---

## 6. What we should NOT do (guardrails, carried from the teardown)
- **Don't out-data the data kings** — integrate, decide, and package on legitimately-licensed *derived* data instead.
- **Don't scrape** BizBuySell/marketplaces — the Main Street Acquirer is **legit-public-data-only** by design.
- **Don't overclaim scores** — publishing limits and FAILs *is* the differentiator; keep disclosing.
- **Don't cargo-cult the look without the funnel** — copy 42 Macro's *mechanics* (system + education + free→paid), not
  just its aesthetics.

---

## 7. Open decisions for the founder
1. Confirm the **P1 sequencing** (acquisition beachhead + validation page first).
2. Approve the **T2 = acquisition-suite gate** packaging (LSR/QoE/DCF/SBA-DSCR at $299 as the workhorse tier).
3. Green-light a **live-trial teardown pass** (sign up / demo Koyfin, FSInsight, 42 Macro, Portfolio123, Axial) to
   deepen §2 with real churn reasons and screen-recorded funnels — extends the plan in `COMPETITOR_TEARDOWN_AND_GAP_MAP.md` §10.
4. Confirm the **$110 / $299 / $1,500 + $99/seat** anchors used here match the latest pricing decision.

---

*Prepared under JHI-SIG `69M2705M`. Aegira is a product of JHI Research & Analytics Firm, Inc. (proprietary). Pricing
figures are public-research-grounded (2026) and, where incumbents publish no list price, cited as ranges from verified
procurement/benchmark data. Not affiliated with any entity named. Research/education — not investment, legal, tax, or
accounting advice.*
