# Board Minutes — JHI Research & Analytics Firm, Inc.

**Meeting date:** 2026-08-26 (living document — extended 2026-08-27) · **Type:** Founder directive — institutional product build blueprint (financial ratios + PE/search-fund workbook toolkit + institutional financial dashboards + ratio-dashboard build guide + audit reference + EBITDA/QoE normalization) · **Recorder:** Cy Henry (VP, Software Engineering — Cloud Agent)
**Product:** Aegira · **Publisher:** JHI Research & Analytics Firm, Inc.
**Present:** Founder (Galen Marcellus Miller).

> NOT legal/tax/accounting/investment advice. Prior session: `docs/board/BOARD_MINUTES_2026-08-13.md`.
> Signature of record — `JHI-SIG: 69M2705M`. Ethos: *How we do anything is how we do everything.*

> **Standing Founder directive (2026-08-27):** *"These previous and moving forward write-ups are the tools which are required for building our platform. Please ensure these documents are added to board of minutes. There will be more following."* — every reference write-up delivered by the Founder is captured **verbatim and in full** in this living document (or a successor session), adopted of record, and mapped to a concrete Aegira build target. New sections are appended as they arrive.

---

## 0. Founder directive (verbatim intent)

The current QoE deliverable (e.g. `Aegira_QoE_Carrollton_Design_Build.xlsx`) is **too thin** — it leans on a single EBITDA/NWC model and is "not a deep-dive." **Aegira does not sell five-year projections built off a CIM.** Instead we must deliver a **complete, ratio-rich financial deliverable** — accounting ratios, finance ratios, and economic/industry-context ratios — that justifies **Tier 1 & Tier 2** rates and is **genuinely competitive** with the toolkits used by PE firms, search-fund investors, operators, and search-fund entrepreneurs.

**This document is the adopted build blueprint** (sourced from Investopedia reference material provided by the Founder), captured in full detail. It governs the redesign of the Financial Diligence / QoE deliverable and the broader per-ticker/company workbook suite.

---

## 1. Financial ratios — categories & formulas (capture in full)

Financial ratios are numerical relationships between financial-statement line items (balance sheet, income statement, cash-flow statement). They convert raw figures into comparable measures of a company's ability to pay obligations, earn profits, use assets efficiently, and manage debt. **No single ratio is decisive** — analysis must compare **trends over time** and **industry peers**, and combine multiple measures.

### 1.1 Liquidity (near-term bill-paying capacity)
- **Current ratio** = current assets ÷ current liabilities
- **Quick ratio (acid-test)** = quick assets ÷ current liabilities  *(quick assets = current assets less inventory; include highly-liquid marketable securities)*
- **Cash ratio** = (cash + marketable securities) ÷ current liabilities
- **Net working capital** = current assets − current liabilities
- **Defensive interval** = liquid assets ÷ daily operating expenses
- Note: a current ratio < 1 can signal short-term repayment pressure; a cash ratio ≥ 1 means liquid assets cover current liabilities — but appropriate levels vary by sector.

### 1.2 Profitability (returns earned)
- **Gross margin** = gross profit ÷ sales
- **Operating margin** = operating profit (EBIT) ÷ sales
- **EBITDA margin** = EBITDA ÷ sales
- **SDE margin** = seller's discretionary earnings ÷ sales *(private/SMB deals)*
- **Net profit margin** = net income ÷ net sales
- **ROA** = net income ÷ total assets
- **ROE** = net income ÷ shareholders' equity
- **ROIC** = NOPAT ÷ invested capital
- **ROCE** = EBIT ÷ (total assets − current liabilities)
- **DuPont decomposition:** ROE = (net income ÷ sales) × (sales ÷ total assets) × (total assets ÷ shareholders' equity) = **profit margin × asset turnover × equity multiplier** — isolates whether an ROE change came from operations, asset efficiency, or leverage.

### 1.3 Leverage / solvency (debt sustainability)
- **Debt-to-equity** = total debt ÷ shareholders' equity
- **Long-term-debt-to-total-assets** = long-term debt ÷ total assets *(< 0.5 often viewed as healthier, industry-dependent)*
- **Debt-to-assets** = total debt ÷ total assets
- **Debt-to-EBITDA** = total debt ÷ EBITDA
- **Net debt** = total debt − cash & equivalents *(central to enterprise value & acquisition analysis)*
- **Interest coverage (TIE)** = EBIT ÷ interest expense *(higher = greater capacity to service debt)*
- **Fixed-charge coverage** = (EBIT + fixed charges) ÷ (fixed charges + interest)
- **DSCR (debt-service coverage)** = net operating income ÷ total debt service *(make-or-break for SBA/leveraged acquisitions)*

### 1.4 Efficiency / activity (asset & working-capital productivity)
- **Asset turnover** = sales ÷ total assets
- **Inventory turnover** = COGS ÷ average inventory  *(average inventory = (beginning + ending) ÷ 2)*
- **Days inventory outstanding (DIO)** = 365 ÷ inventory turnover
- **Receivables turnover** = sales ÷ average accounts receivable
- **Days sales outstanding (DSO)** = 365 ÷ receivables turnover
- **Payables turnover** = COGS ÷ average accounts payable
- **Days payable outstanding (DPO)** = 365 ÷ payables turnover
- **Cash conversion cycle** = DIO + DSO − DPO
- **Working-capital turnover** = sales ÷ average working capital

### 1.5 Cash-flow quality
- **Operating cash flow ratio** = operating cash flow ÷ current liabilities
- **Free cash flow (FCF)** = operating cash flow − capital expenditures
- **FCF margin** = FCF ÷ sales
- **Cash-flow-to-debt** = operating cash flow ÷ total debt
- **EBITDA-to-cash conversion** = operating cash flow ÷ EBITDA
- **Capex intensity** = capex ÷ sales
- **Proof-of-cash variance** = bank deposits vs. reported revenue *(QoE core)*

### 1.6 Valuation
- **P/E** = share price ÷ earnings per share *(assess alongside growth, margins, balance-sheet strength, peers)*
- **EV** = market capitalization + total debt − cash & equivalents *(market cap = share price × shares outstanding)*
- **EV/EBITDA**, **EV/Revenue**, **EV/EBIT**
- **SDE multiple** *(SMB acquisitions)*
- **FCF yield** = FCF ÷ market cap
- **Dividend yield** = dividends per share ÷ price

### 1.7 Ratio-analysis principles (non-negotiable framing)
1. Pull **≥ 3 years** of income-statement, balance-sheet, and cash-flow data.
2. Use **average balance-sheet values** for annual ratios where practical.
3. Compare across **time**, against **direct competitors**, and against **sector norms** — not universal thresholds.
4. Investigate the **drivers** (price/volume, costs, asset investment, working capital, acquisitions, debt issuance, buybacks).
5. Conclude only after combining **profitability + liquidity + solvency + efficiency + valuation** evidence.
6. Ratios can be **distorted** by accounting choices, buybacks, acquisitions, cyclicality, and one-time events — combine several measures.

### 1.8 Illustrative market snapshot (why context matters) — as of Aug 26, 2026
| Company | Price | YTD | Trailing P/E | Market cap | Notable indicator |
|---|---|---|---|---|---|
| Eli Lilly (LLY) | $1,233.66 | +14.74% | 42.2 | $1.11T | 33.5% profit margin |
| Novo Nordisk (NVO) | $48.66 | −2.68% | 11.42 | $207.48B | 35.3% profit margin |
| Apple (AAPL) | $309.90 | +14.66% | 35.47 | $4.53T | 27.6% profit margin |
| Pfizer (PFE) | $28.57 | +19.35% | 36.8 | $159.42B | 6.13% dividend yield |
| Tesla (TSLA) | $350.25 | −20.05% | 332.33 | $1.38T | 3.67% profit margin |

Lesson: TSLA's P/E (332.33) dwarfed peers while its margin was 3.67%; LLY/NVO showed far higher margins; PFE paired a smaller cap with a 6.13% yield. **Descriptive, not a recommendation** — ratios must be read alongside price performance, volatility, growth, and industry context.

---

## 2. The PE / search-fund Excel workbook toolkit (build target — all 7 categories)

There is **no single standard package**; the working set is a collection of **linked workbooks, each with a specific decision purpose, supported by one integrated operating model** (the source of truth). Model quality depends on **assumptions and source data**, not spreadsheet complexity.

### 2.1 Deal sourcing & pipeline management
- **Target pipeline / CRM export** — searchable database: industry, geography, revenue, EBITDA/SDE, ownership, broker/source, contact history, probable valuation range, next action, deal-status stage. (Prioritization/process-control, not valuation.)
- **Initial screening / investment-criteria** — fast test vs. fund criteria: size, margins, recurring revenue, customer concentration, growth, capital intensity, leverage capacity, likely entry multiple, likely return → **pass / investigate / decline**.
- **Market-map & outreach tracker** — sector list of companies, intermediaries, advisers, lenders, executives; tracks outreach volume, management meetings, IOIs, NDAs, data-room access.

### 2.2 Acquisition analysis & initial underwriting
- **Three-statement operating model (foundation)** — linked IS/BS/CF, monthly for year 1–2 then annual; revenue by segment/units/pricing/cohorts; costs, working capital, capex, taxes, debt flow through; **base / upside / downside** cases.
- **Quality-of-earnings bridge** — reconciles reported EBITDA → adjusted EBITDA: owner comp, one-time expenses, discontinued activities, unusual legal/repair costs, customer anomalies, other adjustments. Goal: distinguish **sustainable** operating earnings.
- **Purchase-price / sources-and-uses** — translates valuation into cash at closing: enterprise value, cash, debt, transaction expenses, working-capital adjustments, rollover equity, seller financing; sources = senior debt, sub debt, preferred, common equity. (EV incorporates market cap + net debt.)
- **Returns summary / IC dashboard** — entry multiple, forecast revenue & EBITDA, debt paydown, exit multiple, exit EV, equity proceeds, **IRR, MOIC**; linked to the operating/LBO models (no manual outputs).

### 2.3 Due-diligence workbooks
- **Financial diligence workbook** — normalized historical monthly revenue, gross profit, EBITDA, cash conversion, working capital, customer concentration, forecast-vs-actual; tabs: IS trend, BS analysis, CF analysis, normalization items, debt-like obligations.
- **Customer & revenue-quality model** — customer-level concentration, churn, retention, cohorts, pricing, recurring vs. nonrecurring, contract duration, cross-sell.
- **Working-capital & cash-conversion schedule** — receivables, inventory, payables, deferred revenue, seasonality (current/quick ratios supplement).
- **Diligence-request list & issue tracker** — requested/received docs, open questions, owners, deadlines, risks, management responses, findings.

### 2.4 Valuation models
- **DCF** — forecast FCF → discount to PV → ± net cash/debt → ÷ shares (public) or EV (private); appropriate discount rate + terminal value.
- **Trading-comparables** — peer table: EV/Revenue, EV/EBITDA, P/E, growth, margins, returns on capital.
- **Precedent-transactions** — completed deals by sector, date, size, EV/Revenue, EV/EBITDA, consideration, control premium, rationale.
- **LBO model** — connects price + S&U → operating forecast → financing → debt repayment → exit → sponsor returns; capital structures incl. bonds, bridge, equity, senior/sub debt, mandatory amortization.
- **APV model** — for complex/changing financing (leverage, tax shields, subsidies): separates all-equity business value from financing effects.

### 2.5 Financing & closing models
- **Debt schedule** — monthly/quarterly opening balance, mandatory amortization, optional paydown, cash sweeps, interest expense, floating-rate assumptions, fees, maturity, covenants, closing balance; links to statements + LBO.
- **Covenant & liquidity model** — leverage, fixed-charge/interest coverage (EBIT ÷ interest), minimum liquidity, borrowing-base availability, lender reporting.
- **Equity capitalization & waterfall** — sponsor equity, management/seller rollover, co-investment, preferred, option pools, dilution, liquidation preferences, distribution waterfalls.
- **Closing checklist & funds-flow** — legal entities, wire instructions, purchase-price adjustments, fees, debt/equity funding, closing deliverables.

### 2.6 Post-acquisition operating workbooks
- **100-day plan / value-creation tracker** — initiatives (pricing, sales hiring, procurement, systems, add-ons, working-capital, talent) → owners, deadlines, expected & actual EBITDA/cash impact.
- **Budget, forecast & variance** — monthly budget, actual-vs-budget & actual-vs-prior-year: revenue, gross margin, opex, EBITDA, cash flow, working capital, capex, debt, covenant headroom.
- **KPI dashboard** — bookings, revenue, gross margin, retention, backlog, utilization, inventory turnover, labor productivity, cash conversion, leverage, covenant compliance.
- **Add-on acquisition model** — bolt-on underwriting: standalone performance, synergies, integration costs, financing, pro-forma leverage, impact on returns.

### 2.7 Investor & board reporting workbooks
- **Monthly operating package** — actuals, KPIs, liquidity, debt, covenant status, forecast changes, value-creation progress, risks, actions.
- **Quarterly investor reporting** — portfolio-company valuation, invested capital, distributions, unrealized value, debt, performance vs. plan, events, risks/priorities narrative.
- **Portfolio valuation & returns** — ownership, fair-value changes, gross/net returns, realized vs. unrealized, fees/expenses, cash flows by investor; auditable bridge from investment case to current valuation.

### 2.8 Recommended workbook architecture
Make the **integrated operating/LBO model the source of truth**; link IC summary, debt schedule, valuation outputs, board package, and investor report to it. **Separate inputs, calculations, outputs, and sensitivity tables**; clearly identify assumptions; retain both original underwriting case and revised forecasts. *Sophisticated modeling does not replace judgment — models are only as reliable as their data and assumptions.*

---

## 3. LBO debt schedule & investor returns (methodology to build)

Chain: **purchase price → sources & uses → operating forecast → free cash flow → debt repayment → exit net debt → exit equity value → MOIC & IRR.**

1. **Transaction & sources/uses.** Uses = purchase EV (entry EBITDA × entry EV/EBITDA), refinance existing debt, transaction fees, financing fees, minimum cash retained. Sources = senior debt, sub/mezz debt, seller rollover, management rollover, sponsor equity. Check: **Total Sources − Total Uses = 0**; sponsor equity is the initial outflow for MOIC/IRR.
2. **Operating forecast & cash flow available for debt repayment** — linked IS/BS/CF; model revenue, costs, EBITDA, working capital, capex, taxes; increase in working capital = cash outflow (a decline releases cash).
3. **Debt schedule by tranche** — revolver, term loan, second-lien, mezzanine, seller note; each: beginning balance, rate, interest, required amortization, optional repayment, ending balance. Interest = rate × ((beginning + ending) ÷ 2); the circularity (ending debt ↔ interest) is handled with beginning/prior-period average debt, then an iterative-calc toggle if needed.
4. **Mandatory amortization + optional cash sweep** — cash after mandatory amort = CF available − mandatory amort; excess cash = max(0, cash after amort − minimum cash); optional paydown = min(excess cash, remaining balance); ending debt = beginning + borrowings − mandatory amort − optional paydown. Never repay beyond outstanding; draw the revolver rather than a negative cash balance.
5. **Exit value & equity proceeds** — exit EV = exit-year EBITDA × exit multiple; exit equity = exit EV − ending net debt − exit fees; investor proceeds = exit equity × ownership %; include interim dividends as inflows.
6. **MOIC & IRR** — MOIC = total distributions ÷ initial equity (example: $60M ÷ $20M = 3.0×). IRR = annualized, timing-aware; Excel `=IRR(range)` for regular intervals, `=XIRR(cash_flows, dates)` for actual dates; initial investment negative, proceeds positive.
7. **Returns sensitivity table** — flex the highest-impact variables (entry/exit multiple, leverage, growth, margin); show MOIC, IRR, exit net debt, debt paydown per scenario. Makes clear whether returns come from **EBITDA growth, multiple expansion, or debt paydown**.

---

## 4. Excel ratio-analysis template architecture (to implement)

**Five worksheets:** (1) **Inputs** — historical IS/BS/CF, share data, market price; (2) **Ratios** — all ratios by year (formulas reference Inputs, never typed); (3) **Trends** — charts + YoY changes; (4) **Peers** — competitor ratios & industry benchmarks; (5) **Dashboard** — concise summary + flags. Keep raw data separate from calculations and presentation.

**Inputs sheet — line items (periods across columns FY-3/FY-2/FY-1; same units, labeled):** revenue/net sales; COGS; EBIT/operating income; interest expense; net income; operating cash flow; capital expenditures; cash & equivalents; marketable securities; accounts receivable; inventory; current assets; total assets; current liabilities; total debt; long-term debt; total liabilities; shareholders' equity; shares outstanding; market price per share.

**Ratios sheet** — link each formula to Inputs; wrap in `IFERROR(...,"")` to suppress `#DIV/0!`. Group by **profitability, liquidity, solvency/leverage, efficiency, valuation** (Section 1 formulas). Use **average balances** for asset/inventory/receivable/working-capital ratios when beginning+ending data exist.

**Trend & peer features** — per ratio: 3-year trend, YoY change, peer/industry benchmark; conditional formatting (green improving, red deteriorating). A concise dashboard includes: net margin, ROA, ROE, current ratio, debt-to-equity, interest coverage, revenue growth, inventory turnover, P/E, FCF yield, plus **DuPont** decomposition.

**Integrity checks (top of Ratios sheet):** `Total Assets − (Total Liabilities + Shareholders' Equity) = 0`; flag missing inputs (`=IF(RequiredCell="","Missing input","OK")`); flag negative/zero denominators; label assumptions/forecasts separately from historical actuals; record filing date, fiscal year-end, currency, and unit scale.

---

## 5. Mapping to the Aegira build (what we implement)

- **Financial Diligence / QoE deliverable redesign** → replace the thin single-model dashboard with the **five-sheet, ratio-rich workbook** (Inputs → Ratios by all 6+ categories with formula + industry benchmark + plain-English read → Earnings-Quality/QoE bridge → Deal & Debt-Capacity/LBO → Legal). Expand the input schema to capture full IS/BS/CF; compute every ratio possible, mark the rest **"input required"** — never fabricate.
- **Public tickers** → the institutional per-ticker workbook already auto-pulls full financials (SF1/EDGAR), so the entire ratio suite + DuPont + valuation multiples compute automatically, with **peer/industry benchmarking**.
- **Peer/industry context** → benchmark using our live data (SEC EDGAR sector, FRED, Treasury/FDIC/EIA, SBA financing) so no metric sits in a vacuum.
- **Pipeline / Portfolio / Reports** → map to the sourcing, IC-dashboard, and investor/board-reporting workbook concepts over time.
- **Phasing:** P1 = ratio-rich QoE + institutional-workbook ratio suite + benchmarking; P2 = LBO/S&U + debt schedule + returns (MOIC/IRR) + sensitivity; P3 = precedent transactions, waterfall, post-close operating/board packages.

**Compliance (unchanged):** all outputs are **decision-support / research, informational only — not investment, valuation, audit, or CPA advice**; formal assurance opinions come only from a licensed **partner CPA** who engages the target. Numbers are **derived/deterministic and fact-locked** (no fabrication); every value dated. Provenance `JHI-SIG: 69M2705M`.

---

## 6. Action items

1. **Build P1** — ratio-rich Financial Diligence / QoE workbook (five-sheet architecture, full ratio suite, industry benchmarking, integrity checks) + extend the institutional per-ticker workbook's ratio coverage with DuPont + valuation multiples + peer benchmarks. *(Cy → tested PR.)*
2. **Founder confirm** — final ratio set / any additions before P1 build kicks off (Founder had directed "explore all"; this blueprint is the agreed superset).
3. **Sequence P2 (LBO/returns) and P3 (precedent/waterfall/board packages)** into the Build Queue.
4. Keep the **derived-only, fact-locked, research-not-advice** posture across every new deliverable.

---

## 7. Peer-comparison workbook, composite scoring & audit controls (extends §4)

*(Founder addendum — the peer-comparison methodology to build alongside the ratio suite. Capture in full.)*

### 7.1 Workbook structure (five sheets)
1. **Raw_Data** — company financial-statement inputs by year (one row per company-year).
2. **Ratios** — profitability, liquidity, leverage, efficiency, valuation metrics.
3. **Peer_Comparison** — one selected year compared across companies + industry benchmarks.
4. **Trends** — multi-year charts + YoY changes.
5. **Dashboard** — summary scores, rankings, key flags.
Keep raw data separate from calculations and outputs. Use several ratios (each tests a distinct aspect of health).

### 7.2 Data tables & rules
- Format inputs as an Excel Table (`Ctrl+T`) named **`tblFinancials`**, one row per company-year; add fields for cash, marketable securities, AR, interest expense, operating cash flow, capex, preferred dividends. (Marketable securities count in current assets for liquidity.)
- **Data-quality rules:** same currency/units for every company; align comparable fiscal years; distinguish **annual vs. trailing-twelve-month**; flag comparisons across different accounting conventions/business models; ratios are most meaningful **against similar industry peers**.
- Build a multi-year **`tblRatios`** (one row per company-year); pull raw values with **`XLOOKUP`** matching company + fiscal year (or compute in one table). Wrap in `IFERROR`; format % as percent, turnover/coverage/P-E as numbers/multiples. Use **average balances** for asset/inventory/receivable/working-capital ratios.

### 7.3 Peer_Comparison grid
- Selector cells at top: **metric, fiscal year, industry**.
- Columns: current-year metric, prior-year, YoY change, industry average/median, variance-to-peer, rank, percentile.
- Example formulas:
  - Current-year ROE: `=XLOOKUP(1,(tblRatios[Company]=$A8)*(tblRatios[Fiscal Year]=$B$2),tblRatios[ROE],"")`
  - Prior-year ROE: `=XLOOKUP(1,(tblRatios[Company]=$A8)*(tblRatios[Fiscal Year]=$B$2-1),tblRatios[ROE],"")`
  - YoY change: `=IFERROR(B8-C8,"")`
  - Peer average: `=AVERAGEIFS($B$8:$B$20,$D$8:$D$20,$B$3)`
  - Variance to peer average: `=B8-E8`

### 7.4 Industry benchmarks
- Separate **`tblBenchmarks`**: industry, year, metric, **median, average, 25th, 75th percentile**.
- Retrieve median: `=XLOOKUP(1,(tblBenchmarks[Industry]=$B$3)*(tblBenchmarks[Year]=$B$2)*(tblBenchmarks[Metric]=B$7),tblBenchmarks[Median],"")`; then `Selected Ratio − Industry Median`.
- **Prefer median** (outlier-robust); compare profitability only against suitable industry peers (sectors have structurally different margins).

### 7.5 Rankings & percentiles (direction-aware — critical)
- **Higher-is-better** (ROE, interest coverage, current ratio): Rank `=RANK.EQ(B8,$B$8:$B$20,0)`; Percentile `=PERCENTRANK.INC($B$8:$B$20,B8)`.
- **Lower-is-better** (debt-to-assets, P/E): Rank `=RANK.EQ(B8,$B$8:$B$20,1)`; Percentile `=1-PERCENTRANK.INC($B$8:$B$20,B8)`.
- **Do NOT rank all metrics in the same direction** — lower debt = lower risk; higher coverage = better; interpretation stays industry-specific.

### 7.6 Composite score (screening aid, not a verdict)
- Assign a percentile score per ratio → `AVERAGE`, or **weighted**:
  `=0.30*ProfitabilityScore + 0.25*LiquidityScore + 0.25*SolvencyScore + 0.20*EfficiencyScore`
- Keep weights **visible and editable**. The score is a screening aid — not a substitute for analysis of business quality, accounting adjustments, and industry economics.

### 7.7 Conditional formatting & trends
- Apply **direction-aware** rules to the peer grid (not one universal color scale); e.g. top-quartile `=B8>=QUARTILE.INC($B$8:$B$20,3)`. Formatting must communicate the direction of economic strength (high debt ≠ high profitability); a current ratio < 1 flags short-term pressure.
- **Trends sheet:** line charts (revenue growth, net margin, ROA, ROE; and current ratio, D/E, interest coverage), a bar chart of latest vs. peer median, and a **DuPont bridge** (net margin × asset turnover × equity multiplier) to explain *why* ROE moved.

### 7.8 Illustrative peer snapshot (drug manufacturers, Aug 26 2026)
NVO / LLY / PFE — same industry (more relevant peers): **NVO** lowest trailing P/E; **LLY** strongest ROA & ROE; **PFE** lowest profitability but lowest forward P/E. Lesson: one ranking is insufficient — valuation, current profitability, projected earnings, and market performance can point in different directions.

### 7.9 Audit controls (on every main output sheet)
- Ratio completeness: `=COUNTBLANK(RatioRange)`
- Duplicate company-year: `=COUNTIFS(tblRatios[Company],[@Company],tblRatios[Fiscal Year],[@[Fiscal Year]])`
- Balance-sheet check: `=Total Assets-(Total Liabilities+Equity)` → 0
- Outlier flag: `=IF(ABS(VarianceVsIndustry)>Threshold,"Review","OK")`
- Data timestamp: filing date, market-price date, currency, unit scale, source.

### 7.10 Mapping to Aegira
The Peer_Comparison + composite score + benchmarks become the **Peers sheet + a 0–100 quality/opportunity score + benchmarking layer** in our ratio workbook (ties to the existing Opportunity Score). Benchmarks are sourced from **SEC EDGAR sector data + SF1**; direction-aware ranking and median-preference are built in; audit-control checks ship on every output sheet. Derived-only, fact-locked, dated, `JHI-SIG: 69M2705M`.

---

## 8. Financial dashboards — build specification (adopted verbatim)

*(Founder addendum — Investopedia reference on financial dashboards. Capture every detail. Governs the Dashboard sheet of every Aegira ratio/QoE/institutional workbook and — by mapping — the on-screen executive dashboards inside the platform.)*

### 8.1 Key takeaways (non-negotiable framing)
1. A **financial dashboard** is a concise view of business financial performance **for decision-making** — not a data dump.
2. **Choose metrics from specific business goals**, not a generic list of every available measure.
3. **Core measures typically cover:** revenue, profitability, cash flow, liquidity, debt, and operating efficiency.
4. **Add targets, prior-period comparisons, and trend views** to make results actionable (numbers alone are not).
5. **Keep dashboards focused** and **update metrics as business conditions and priorities change** — a dashboard is a living instrument, not a static artifact.

### 8.2 Definition & purpose
A financial dashboard is a **visual, decision-oriented report** that brings key financial and operating measures into one place. Its purpose is to help **executives, managers, investors, or operators** quickly:
- **assess performance,**
- **compare it with goals, and**
- **identify where action may be needed.**

As Julie Young explains in *Understanding Metrics: Key to Performance Tracking and Analysis*, **"Managers typically build a dashboard of key performance indicators (KPIs)."**

### 8.3 Key metrics to include (six-area canonical map)
The exact mix should reflect the company's **goals, sector, and business model**. A broadly useful dashboard commonly includes the following six areas:

| Area | Example measures | Why it matters |
|---|---|---|
| **Growth** | Revenue, revenue growth, sales by segment or customer | Shows whether demand and top-line performance are expanding or contracting. |
| **Profitability** | Gross profit, gross margin, operating profit or margin, EBITDA, net income | Reveals how much revenue remains after direct, operating, financing, and other costs. |
| **Cash flow** | Operating cash flow, free cash flow, cash balance, cash conversion | Tests whether accounting profits translate into cash available for operations, debt service, or investment. |
| **Liquidity & leverage** | Current ratio, debt-to-equity, interest coverage, net debt | Shows short-term payment capacity and financial risk from borrowing. |
| **Efficiency** | Accounts-receivable days, inventory turnover, asset turnover, working-capital trend | Identifies how effectively the company converts resources into sales and cash. |
| **Returns & valuation** | ROA, ROE, ROIC or CROCI; EV/EBITDA or P/E for public companies | Measures returns earned on assets and capital, and — where relevant — market valuation. |

**Operating-company emphasis:** for an operating company, **revenue growth, margins, and cost trends** are especially important because **strong sales growth does not necessarily translate into stronger profits when costs rise faster**. **Earnings per share, quarterly revenue growth, and margins/cost trends** are among the financial results most closely watched in earnings reporting.

### 8.4 Essential dashboard features (all five must be present)

**1. Goals, targets, and variance.** Show each KPI's:
- **actual result,**
- **budget or target,**
- **prior-period result, and**
- **variance in dollars *and* percentages.**
Select KPIs **only after establishing the decision goal**, then set targets that are **integrated with business decisions** (not decorative).

**2. Time comparisons and trends.** Include:
- **Month-to-date (MTD)**
- **Quarter-to-date (QTD)** — tracks performance from the quarter's start through the current point, helping management assess whether it remains on pace for quarterly targets and adjust early if needed.
- **Year-to-date (YTD)**
- **Prior-year** views as appropriate.

**3. Drill-downs and segmentation.** Let users move from a **company-level number** into **business unit, product, geography, customer, or cost-category detail**. For instance, **gross margin by geography** can reveal whether profitability and pricing differ materially across regions.

**4. Focused design.** **Avoid presenting every possible metric on one page.** Separate dashboards or report tabs by **objective** — such as:
- executive overview,
- cash and debt,
- commercial performance, or
- operations —
because **too many KPIs can obscure what requires attention.**

**5. Relevant benchmarks and context.** Compare results with **historical performance, budget, and suitable peer or sector benchmarks**. **Ratios are most informative when viewed alongside peers**, since appropriate levels differ by **industry and capital structure**.

### 8.5 A useful layout — one-page executive dashboard (canonical template)

| Row | Content | Purpose |
|---|---|---|
| **Top row** | **Revenue, EBITDA, net income, operating cash flow, cash balance, net debt** — each with **actual, target, and prior-year** comparisons | Instant health snapshot: are we hitting plan on the six numbers that matter most? |
| **Middle row** | **Revenue and margin trends** + a **cash-flow or working-capital chart** | Direction of travel: is the trajectory improving, deteriorating, or seasonal? |
| **Bottom row** | **Liquidity and leverage ratios, operating KPIs, risks, and a short list of management actions** | Risk & action layer: what could break, and what is being done about it? |

**Sector variant — banks/lenders:** replace the standard industrial-company metric set with **net interest margin, return on assets, return on equity, credit-loss provisions, and solvency/liquidity measures**. Never apply an industrial dashboard to a financial institution unchanged.

### 8.6 Mapping to Aegira (implementation contract)

**A. Workbook — Dashboard sheet (added to every ratio/QoE/institutional workbook per §4 and §7).**
- **Top row (KPI strip, 6 tiles):** Revenue · EBITDA · Net income · Operating cash flow · Cash balance · Net debt. Each tile shows **Actual | Target | Prior-year | Variance $ | Variance %**. Direction-aware color (green/red) applied per §7.7.
- **Middle row (trend panel):** three server-rendered charts (matplotlib PNG embedded, or native Excel chart where linked) — (i) revenue & YoY growth, (ii) margin ladder (gross → operating → EBITDA → net), (iii) operating cash flow / free cash flow / working-capital trend.
- **Bottom row (risk & action panel):** liquidity & leverage tile (current ratio, D/E, interest coverage, DSCR, net-debt/EBITDA), operating KPIs tile (DSO, DIO, DPO, cash-conversion cycle, inventory turnover), **Risks** callout list (populated by audit-control flags from §7.9), and **Management actions** — short prioritized list (from 100-day plan / value-creation tracker in §2.6 when available; otherwise blank with placeholder).
- **Focused design rule:** dashboard is **one page**. Depth lives on the **Ratios / Trends / Peers / Sensitivity** sheets. Any metric that does not drive a decision is pushed off the dashboard.
- **Sector switch:** for banks/lenders/BDCs, swap in the §8.5 variant (NIM, ROA, ROE, credit-loss provisions, solvency/liquidity) via a `SectorProfile` selector on the Inputs sheet.
- **Cadence & context:** every tile carries an **as-of date, source, currency, and unit scale** (aligns with the data-foundation doctrine — *Always-Deliver · Cadence-Aware · As-Of-Disclosed*).

**B. Platform — on-screen executive dashboards (Aegira app modules).**
- **Dashboard module** — mirror the same three-row canonical layout across the launchpad-level view.
- **Per-company / per-ticker (Portfolio, Diligence a Target, Valuation, Reports)** — the same one-page pattern with drill-downs into segment/product/geography where the data exists.
- **Founder/staff (God-Eye) views** — dashboards for **executive overview, cash and debt, commercial performance, and operations** are separate tabs (per §8.4-4) — not stacked on one screen.

**C. Data plumbing (already in place, reused).**
- Growth / profitability / cash flow / liquidity / leverage / efficiency / returns metrics: **derived from SEC EDGAR + SF1 (public) or Inputs sheet (private/QoE)** — no fabrication.
- Peer benchmarks: **SEC EDGAR sector + SF1 industry aggregates** (median-preferred per §7.4).
- Macro / rates context: **FRED, Treasury Fiscal Data, FDIC BankFind, EIA** (via the DATA_GOV adapter).

**D. Non-negotiable compliance layer (unchanged).**
- Dashboards are **decision-support / research, informational only — not investment, valuation, audit, or CPA advice**.
- Numbers are **derived/deterministic and fact-locked**; every value carries an **as-of date and source**.
- Provenance: `JHI-SIG: 69M2705M` on every output.

### 8.7 Governance & change control
Dashboards **must be reviewed at least quarterly** and updated as **business conditions and priorities change** — this is doctrine, not a suggestion. Ratio/KPI definitions live in a single **canonical registry** (extend `backend/app/data_registry.py`) so the dashboard, the ratio workbook, the peer-comparison sheet, and any external report share **one definition per metric** — no drift across surfaces.

### 8.8 Action items (§8 addendum to §6)
1. **Add the Dashboard sheet spec above** to the P1 QoE/ratio workbook build and to the institutional per-ticker workbook. *(Cy → tested PR.)*
2. **Ship the on-screen Executive Dashboard** in the Aegira app (Dashboard module + per-company/ticker views) using the same three-row canonical layout. *(Cy → tested PR, sequenced after P1 workbook.)*
3. **Extend the metric registry** so the Dashboard sheet, Ratios sheet, Peers sheet, and platform dashboards all pull from **one definition per metric** (no drift). *(Cy.)*
4. **Sector variants** — implement the bank/lender variant as the first alternate sector profile; expand as we take on financials-sector work. *(Cy.)*
5. Keep the **derived-only, fact-locked, research-not-advice, as-of-dated** posture on every dashboard surface. *(Ongoing.)*

---

---

## 9. Financial-ratio dashboard — build guide from company financial statements (adopted verbatim)

*(Founder addendum, 2026-08-27 — Investopedia reference: "How do I build a financial ratio dashboard from a company's financial statements?" Capture every detail. This is the **operational, step-by-step "how to build" spec** for the ratio dashboard whose taxonomy is in §1, whose Excel architecture is in §4, and whose peer-comparison methodology is in §7 — the section that binds them into a working analyst deliverable.)*

### 9.1 Key takeaways (non-negotiable framing)
1. **Build the dashboard from consistently defined income-statement, balance-sheet, and cash-flow inputs.**
2. **Group ratios into profitability, liquidity, solvency, efficiency, cash flow, and valuation sections.**
3. **Use several ratios together** because each reveals only one part of a company's financial condition.
4. **Compare each result with prior periods and direct industry peers**, not a universal threshold.
5. **Add trend and alert columns** so the dashboard **explains changes** rather than merely displaying formulas.

### 9.2 Step 1 — Create a clean financial-statement input sheet
Set up **one source-data tab** with columns for the **latest fiscal year, prior years, and optionally trailing 12 months**. Pull **every** line item required by the ratios:
- **Income statement:** revenue, gross profit, EBIT, net income, interest expense, EPS
- **Balance sheet:** current assets, current liabilities, total assets, total liabilities, total equity, debt
- **Cash flow:** cash flow from operations (CFO), capital expenditures (CapEx)
- **Market:** shares outstanding, current share price

Ratio analysis **combines line items from the income statement, balance sheet, and cash-flow statement** to show **liquidity, profitability, debt use, and earnings strength**.

**Averaging rule (mandatory):** use **average balance-sheet balances** when pairing a balance-sheet item with an income-statement flow. For example, calculate **average total assets** as `(beginning assets + ending assets) ÷ 2` before calculating **ROA**.

**Data hygiene (mandatory):**
- **Keep units consistent** — do not divide revenue reported in millions by debt reported in thousands.
- **Use the same reporting periods** across all calculations.

### 9.3 Step 2 — Use a dashboard layout with trend and comparison columns
Create **one row per ratio** and the following **columns**:
1. **Latest period**
2. **Prior period**
3. **3- to 5-year trend**
4. **Peer median**
5. **Industry benchmark**
6. **Status flag**
7. **Explanation**

This lets you identify **whether a ratio is improving** and **whether that improvement is competitive**. **Key ratios summarize financial condition relative to peers**, but **the most relevant measures vary by industry and company type.**

**Six canonical dashboard sections** (adopted verbatim):

| Dashboard section | Core question answered | Typical metrics |
|---|---|---|
| **Profitability** | Does the company convert sales and capital into profit? | Gross margin, operating margin, net margin, ROA, ROE, ROCE |
| **Liquidity** | Can it meet near-term obligations? | Working-capital ratio / current ratio, quick ratio |
| **Solvency** | Is debt manageable over the long term? | Debt-to-equity, debt-to-assets, interest coverage |
| **Efficiency** | How productively are assets and receivables used? | Asset turnover, receivables turnover, days sales outstanding |
| **Cash flow** | Can operations fund investment? | CFO-to-CapEx, CFO trend |
| **Valuation** | How is the market pricing earnings and equity? | P/E, P/B, P/S |

This structure follows the common approach:
- **Balance-sheet measures** → liquidity, leverage, operating efficiency
- **Income-statement measures** → profit margins and coverage
- **Cash-flow measures** → cash-generation capacity
- **Comprehensive return measures** (ROA, ROE) → combined view

### 9.4 Step 3 — Add profitability and return ratios
- **ROA** measures the profit earned relative to the company's **asset base**.
- **ROE** measures how effectively management generates profit from **shareholders' capital**.
- **ROCE** uses **EBIT relative to capital employed** and is **best considered alongside ROA, ROE, and other return measures — not in isolation.**
- **Capital employed** = **total assets − current liabilities**, applied **consistently across all periods and peers.**

**Interpretation caveats:**
- Rising margins and returns **can** reflect stronger operations, pricing, or capital use.
- A **high ROE** can also be **influenced by a smaller equity base** — so **read it with debt metrics** (§9.6).

### 9.5 Step 4 — Add liquidity and operating-efficiency ratios
- **Working-capital ratio** = **current assets ÷ current liabilities** — measures capacity to meet current obligations.
- Common balance-sheet-oriented metrics: **asset turnover, quick ratio, receivables turnover, days sales outstanding.**

**Read them together:**
- A **stable current ratio** accompanied by **worsening receivables turnover** may mean the reported current assets are **becoming less liquid** (receivables aging up).
- Conversely, **better turnover** can support **stronger operating cash flow** — assuming **sales quality remains sound.**

### 9.6 Step 5 — Add solvency and debt-service ratios
- **Debt-to-equity** compares **liabilities with shareholder equity**; a **high** result can indicate **greater investment risk** because the company has more obligations to support.
- **Interest coverage** tests whether **EBIT is sufficient to cover interest expense**; a **higher** figure is generally more favorable. **A ratio below 2 can signal difficulty servicing long-term debt.**

**Dashboard mechanics:**
- Add **conditional formatting** to flag **rising leverage, falling interest coverage, or a combination of both.**
- **Do not** label a company **healthy or distressed from debt-to-equity alone** — **capital structures differ materially by sector.**

### 9.7 Step 6 — Include cash-flow capacity
- **CF/CapEx** = **CFO ÷ CapEx** (both from the cash-flow statement).
- A **higher ratio** generally indicates **greater capacity to fund capital investments internally.**
- **Negative operating cash flow** means **CapEx is being financed from external sources.**

**Why this section is required:**
- Avoid relying solely on **accounting earnings**.
- A company may report **attractive profitability ratios** but **still lack sufficient operating cash** to sustain **expansion, debt service, or investment.**
- Conversely, a **temporary drop** in CF/CapEx **may be reasonable** if management is investing in **productive long-term assets.**

### 9.8 Step 7 — Add valuation ratios (public companies)
- **P/E** — what investors pay for each dollar of earnings.
- **P/B** — share price vs. book value.
- **P/S** — price vs. sales.
- A **lower ratio** *may* suggest a **relatively inexpensive stock**, but **meaningful interpretation requires comparison with peers** and **consideration of growth, profitability, risk, and the business model.**

**Guardrails:**
- **Do not calculate P/E when EPS is negative or economically insignificant.**
- **Place valuation ratios next to revenue growth, margins, ROE, interest coverage, and CFO-to-CapEx** so the dashboard can distinguish a **potentially attractive discount from weak fundamentals.**

### 9.9 Step 8 — Turn the dashboard into a decision tool
- **For each ratio, include a short driver note** — such as:
  - *"margin increased because revenue grew faster than operating costs"*
  - *"interest coverage fell because borrowing rose and EBIT declined"*
- Use **green/yellow/red status** **only after setting thresholds that suit the industry** — **technology, banks, and industrial companies may require different key ratios and normal ranges.**
- **Finish with a one-page summary** containing **all five** elements:
  1. **the latest ratios,**
  2. **three- to five-year sparklines,**
  3. **peer medians,**
  4. **the biggest positive and negative changes, and**
  5. **a concise conclusion** on **profitability, liquidity, solvency, operating efficiency, cash-generation ability, and valuation.**

**Multiple key ratios give a fuller view than any single metric** because each highlights a different aspect of financial health.

### 9.10 Mapping to Aegira (implementation contract)

**A. Ratio-dashboard sheet — schema (applies to every institutional / QoE / per-ticker workbook).**
- **One row per ratio.** Fixed column set per §9.3: `Metric | Latest | Prior | 3–5y Trend (sparkline) | Peer Median | Industry Benchmark | Status | Driver Note`.
- **Six sections, in this order** (per §9.3): **Profitability → Liquidity → Solvency → Efficiency → Cash Flow → Valuation.** No re-ordering — the order is the reading order for the analyst.
- **Averages enforced** — the Ratios engine (`backend/app/equity_ratios.py`) computes average balances for every asset/receivable/inventory/working-capital ratio automatically (per §9.2, §1.7).
- **Unit-consistency guard** — Inputs sheet declares `Currency` + `Unit Scale`; a top-of-sheet audit check (per §7.9) fails loudly if any input row's unit differs.
- **Valuation section guard** — **P/E, P/B, P/S are only rendered when EPS/BV/S are positive & economically meaningful**; otherwise the cell shows `"N/M"` (not meaningful) — never `#DIV/0!`, never a misleading number.
- **Cross-read rows** — sparkline + peer median + industry benchmark on every ratio, so §9.5's "read liquidity and efficiency together" and §9.4's "read ROE with debt metrics" are visual, not something the analyst has to remember.

**B. Status flags & driver notes (deterministic + LLM-elevated, fact-locked).**
- **Deterministic status logic first** — green/yellow/red is computed from **industry-appropriate thresholds** loaded from a **`SectorProfile`** (tech / bank / industrial / consumer / energy / etc. — per §9.9 + §8.5). No universal threshold anywhere in the code.
- **Driver notes** are drafted **deterministically** from the underlying ratio change decomposition (e.g. margin change ⇒ revenue growth vs. cost growth; interest coverage change ⇒ EBIT change vs. interest change) and then **elevated by the E2 LLM (Ellery)** in the existing fact-locked pipeline — **numbers never sent, only prose rephrased**, per the E2 fact-lock (`backend/app/editorial_llm.py`).
- **Section flags roll up** — six section badges appear on the Cover/Dashboard sheet so the reader sees the overall posture before drilling in.

**C. One-page summary (per §9.9) becomes the Cover sheet.**
- **Latest ratios** — top KPI strip (echoes §8.5 canonical layout, sector-aware).
- **3–5 year sparklines** — one per ratio, rendered by `backend/app/ticker_charts.py` (already in place).
- **Peer medians** — pulled from **`tblBenchmarks`** (per §7.4), median-preferred (§7.4).
- **Biggest positive & negative changes** — top 3 improvers / top 3 deteriorators, YoY, direction-aware (§7.5).
- **Concise conclusion** — a six-line paragraph, one line per canonical section (Profitability / Liquidity / Solvency / Efficiency / Cash flow / Valuation), Ellery-voiced via E2, strictly fact-locked.

**D. Compliance layer (unchanged).**
- Dashboards are **decision-support / research, informational only — not investment, valuation, audit, or CPA advice.**
- All numbers **derived, deterministic, and fact-locked**, every value dated with source.
- Provenance: `JHI-SIG: 69M2705M` on every output surface.

### 9.11 Governance & change control (extends §8.7)
- **Sector profiles** (thresholds + relevant KPI list per §9.9) live in the **metric registry** (`backend/app/data_registry.py`), versioned. Reviewed **at least quarterly** or when a new sector goes into production.
- **Ratio definitions** are shared across §§1, 4, 7, 8, 9 — **one definition per metric** across dashboard, ratios sheet, peer sheet, and on-screen surfaces. **No drift.**
- **P/E "N/M" rule** and **industry-threshold rule** are enforced by tests, not by convention.

### 9.12 Action items (§9 addendum to §§6, 8.8)
1. **Implement the ratio-dashboard sheet schema** in every institutional / QoE / per-ticker workbook per §9.10-A (six sections, fixed 8-column layout, `N/M` guard, unit-consistency guard). *(Cy → tested PR, folded into the P1 QoE + institutional-workbook build.)*
2. **Build the `SectorProfile` registry** (thresholds + relevant KPI list per §9.9) — start with **tech, banks, industrials, consumer, energy** — extend as we take on new sectors. *(Cy.)*
3. **Wire deterministic driver-note generation** for every ratio (margin decomposition, coverage decomposition, turnover decomposition, ROE via DuPont); pipe through E2 LLM for prose elevation, keeping numeric fact-lock intact. *(Cy.)*
4. **Cover sheet = one-page §9.9 summary** — top KPI strip + sparklines + peer medians + top movers + six-line conclusion — canonical on every workbook. *(Cy.)*
5. Keep the **derived-only, fact-locked, research-not-advice, as-of-dated** posture on every dashboard surface. *(Ongoing.)*

---

---

## 10. Audit — reference framework and Aegira scope boundary (adopted verbatim)

*(Founder addendum, 2026-08-27 — Investopedia reference on financial-statement audits. Capture every detail. **Critical scope note:** Aegira does **not** perform statutory audits and does **not** issue audit opinions — that work is reserved to a licensed **partner CPA** who engages the target (established in §5). This section is adopted because the **audit doctrine — risk-based procedures, evidence triangulation, working-paper discipline, professional skepticism, audit trail — is the standard our QoE bridge, document-review pipeline, and diligence workbooks are built to.** The Aegira mapping in §10.8 formalizes that boundary.)*

### 10.1 Key takeaways (non-negotiable framing)
1. A **financial-statement audit** is an **independent examination** of records, controls, and evidence supporting the statements.
2. The **core phases** are **planning, execution, and reporting.**
3. Auditors **assess material-misstatement risk** and **establish materiality** before testing.
4. **Effective procedures combine** inquiries, analytics, document testing, observations, and **third-party confirmations.**
5. **Sufficient, reliable, and relevant evidence** — especially **external or original evidence** — is central to a credible opinion.
6. **Strong documentation, professional skepticism, independence, and clear communication** make the audit more dependable.

### 10.2 Step 1 — Plan the engagement
Start by defining the audit's **scope, objectives, reporting framework** (such as **GAAP** or **IFRS**), **timetable, and methodology**. The auditor develops an **understanding of the business**, its **operations, financial-reporting process, internal controls, and known fraud or error risks**; then **assesses the risk of material misstatement** and **sets materiality thresholds** to focus work on matters capable of affecting users' decisions.

> As **Tobi Opeyemi Amure** explains in *Audit: Meaning in Finance and Accounting and 3 Main Types*, **"The audit begins with comprehensive planning, where auditors define the scope, objectives, and methodology of the engagement."**

**Best practices at this stage:**
- **Maintain auditor independence** and **apply professional judgment.**
- **Identify higher-risk accounts and assertions** — such as **revenue, receivables, inventory, estimates, related parties, and significant disclosures.**
- **Design procedures responsive to the assessed risks** rather than using a **one-size-fits-all checklist.**
- **Establish clear communication** with **management and those charged with governance** about **timing, information requests, and significant audit matters.**

### 10.3 Step 2 — Understand and test internal controls
**Evaluate the processes and controls that produce the financial statements.** Controls commonly include:
- **authorization,**
- **documentation,**
- **reconciliations,**
- **security safeguards,**
- **physical controls, and**
- **segregation of duties.**

Auditors test relevant controls to determine whether they are **designed appropriately** and **operating effectively**; this helps determine the **nature, timing, and extent of substantive testing.**

**Control-exception handling.** Where control exceptions are identified, **evaluate their severity.** A **material weakness** is a **major internal-control flaw that could lead to a material financial-statement error**; auditors **report such weaknesses to the audit committee**, which oversees corrective action.

*(Aegira mapping note: Aegira is not an audit firm and its client is typically a buyer, not the target's audit committee. We surface the same content in a plain-English **"Findings & Recommended Actions"** section of the deliverable — same substance, buyer-appropriate framing. See §10.8.)*

### 10.4 Step 3 — Perform substantive procedures and gather audit evidence
Obtain evidence **directly from records, third parties, and observation**. Typical procedures include:
- **inspecting** invoices, contracts, journals, bank statements, and general-ledger entries;
- **tracing** transactions through the **audit trail**;
- **testing** account balances and transaction samples;
- **performing analytical procedures**;
- **observing** physical inventory counts;
- **confirming** receivables or other third-party balances.

**Evidence quality standard.** Evidence should be **sufficient in quantity** and **reliable and relevant in quality.** **Original documents, independent third-party confirmations, and firsthand observation generally provide stronger support than management representations alone.** For example, auditors may **obtain bank statements directly from the bank, inspect sales invoices and receipts, and physically observe inventory.**

**Sampling.** **Use sampling thoughtfully** when testing large populations. **Attribute sampling** can efficiently test whether controls were followed — for example, **whether purchase orders received required approval** — but **the sample must be large enough for the intended assurance level**, and auditors must **consider sampling error when extrapolating results.**

### 10.5 Step 4 — Investigate exceptions, estimates, and disclosures
Follow up on:
- **unusual fluctuations,**
- **discrepancies,**
- **missing support,** or
- **control deviations.**

This may involve **management and staff interviews, expanded testing, review of accounting policies and estimates, and assessment of whether the financial statements include adequate disclosures.** Auditors should **examine both amounts and qualitative disclosures**, including **significant risks that could make the financial statements misleading.**

**Contingent legal matters.** For contingent legal matters, an **attorney's letter** helps verify management's information on **pending litigation**, including:
- the **nature and timing** of a potential loss,
- its **likelihood, and**
- the **estimated financial effect where material.**

This work supports a conclusion about whether **legal exposures are appropriately reflected or disclosed.**

### 10.6 Step 5 — Document, communicate, and report
**Working papers.** Keep **complete working papers** that show:
- the **work performed,**
- **evidence obtained,**
- **judgments made,**
- **exceptions found, and**
- **how those exceptions were resolved.**

**Audit documentation supports the final conclusion and makes the audit reviewable.** Communicate significant findings to **management and the audit committee or other governance body**, including **control deficiencies and recommended remediation.**

**Opinion outcomes.** Finally, form and issue the **audit opinion**:
- **Unqualified (clean) opinion** — concludes the statements **fairly present the company's financial position, in all material respects,** under the applicable accounting framework.
- **Qualified opinion,** **adverse opinion,** or **disclaimer** — if evidence is insufficient or problems are material.

**Boundary of the opinion.** An audit opinion **addresses fair presentation and material misstatement — not whether the company is economically healthy or guaranteed to remain successful.**

### 10.7 Practical audit-quality checklist (adopted verbatim)
- **Be independent and skeptical:** Do not accept explanations without **corroborating evidence**, particularly in high-risk areas.
- **Use a risk-based approach:** Direct more work to **accounts, transactions, estimates, and disclosures most likely to contain material misstatements.**
- **Triangulate evidence:** Reconcile management explanations to **original documents, external confirmations, audit trails, and physical observation** where possible.
- **Evaluate controls but do not over-rely on them:** Controls offer **reasonable — not absolute — assurance** and can fail because of **judgment errors, override, or collusion.**
- **Escalate and remediate findings:** Report **material weaknesses** promptly and ensure **corrective actions are tracked.**
- **Preserve a clear audit trail:** Documentation should allow **another qualified reviewer to understand the procedures, evidence, and basis for the opinion.**

### 10.8 Mapping to Aegira (scope boundary + doctrine adoption)

**A. Scope boundary (non-negotiable, restates §5).**
- Aegira **does not perform statutory audits.**
- Aegira **does not issue audit opinions** (unqualified / qualified / adverse / disclaimer).
- Aegira **does not attest to fair presentation** under GAAP or IFRS.
- Every Aegira deliverable is **decision-support / research, informational only — not audit, valuation, tax, or investment advice.**
- **Formal assurance opinions come only from a licensed partner CPA who engages the target.** Aegira may hand off its diligence workbook + evidence log to that CPA as a starting point — never as a substitute.
- Every workbook and dashboard carries this statement plus **`JHI-SIG: 69M2705M`.**

**B. Doctrine we DO adopt (audit-grade rigor inside our own deliverables).**

**Planning discipline (§10.2 → QoE & document-review kickoff).**
- Every Financial Diligence / QoE engagement starts with an explicit **Scope tab**: **objective, reporting framework (GAAP / IFRS / management accounts), period covered, methodology, timetable, deliverables.**
- **Business understanding tab** — industry, revenue model, customer/vendor concentration, key contracts, known risks — populated before any testing.
- **Risk register** — higher-risk areas flagged (**revenue, receivables, inventory, estimates, related parties, disclosures** — per §10.2). Procedures are **responsive to those risks**, not one-size-fits-all.
- **Materiality thresholds** are **set and recorded** (analog to audit materiality — for our QoE, expressed as a **% of EBITDA** and a **$ floor**; any adjustment above threshold surfaces on the summary).

**Controls awareness (§10.3 → private-target QoE + document review).**
- New **Controls Snapshot tab** — records the target's control environment across the six control categories (**authorization / documentation / reconciliations / security / physical / segregation of duties**), with a **strength rating** and **`Material Weakness?` flag** per category.
- Flags feed the QoE narrative and elevate the sampling intensity in §10.4.

**Evidence-gathering doctrine (§10.4 → document-review pipeline).**
- The document-review engine already ingests bank statements, invoices, contracts, ledgers; §10 formalizes an **Evidence Quality Grade** on every artifact: **A (external/independent), B (original internal), C (management-prepared / representation only)** — surfaced in the review record and rolled up on the summary.
- **Sampling procedure recorded** — for attribute tests (e.g. approvals on POs), the workbook records **population size, sample size, method (random / haphazard / judgmental), exceptions, projected error, assurance level, sampling-error caveat** — per §10.4.
- **Analytical procedures** — expected-vs-actual by month/segment already generated by the QoE engine; §10 formalizes an **"unexpected fluctuation" callout list** with explanations required before sign-off.

**Exceptions, estimates, disclosures (§10.5 → QoE bridge + attorney-letter path).**
- Exceptions log (per §7.9 audit controls) is now the **§10 formal exceptions workbook** — every unusual fluctuation, discrepancy, missing support, or control deviation gets a **status (Open / Explained / Adjusted / Escalated)**, an **owner**, and a **resolution note**.
- **Estimates & judgments tab** — records management estimates (allowances, reserves, useful lives, purchase-price allocations) and Aegira's independent read.
- **Legal & contingencies callout** — captures management's litigation schedule and a **single-cell callout on the Legal & Contingencies section**: *"For material contingencies, an attorney letter is required — engagement responsibility rests with partner CPA."* Aegira **does not** obtain attorney letters directly — that stays with the CPA who engages the target (per §10.5).

**Working-paper discipline (§10.6 → every Aegira workbook run).**
- **Working-paper artifact** auto-generated on every workbook / document-review run: **procedure performed, evidence reviewed (with hash + timestamp), judgment made, exception found, resolution.** Analog to auditor working papers — **another qualified reviewer must be able to retrace our work.**
- **Reviewable by design** — same fact-lock rules, same dated citations, same `JHI-SIG: 69M2705M` provenance.

**"Opinion" language ban (§10.6 → house style).**
- No Aegira deliverable ever uses the words **"audited," "opinion," "unqualified," "qualified," "adverse," "disclaimer,"** or **"fair presentation"** to describe its own output. Reserved wording exists **only** when quoting the partner CPA's actual opinion.
- Enforced by a lint check on newsletter / workbook / report generation (`backend/app/editorial_llm.py` fact-lock + a docs lint job).

**C. The §10.7 audit-quality checklist becomes our internal ops rubric.**
- **Independent & skeptical** — no management assertion accepted without corroborating evidence in the document-review pipeline.
- **Risk-based** — higher-risk accounts get deeper sampling; standardized in the QoE engine.
- **Triangulate** — reconcile to originals, external confirmations, audit trail, physical observation where possible; graded via the Evidence Quality Grade above.
- **Controls ≠ absolute assurance** — Controls Snapshot never on its own supports a "clean" narrative; substantive procedures always run.
- **Escalate & remediate** — material findings surface on the Cover sheet and in the CTA panel of the client deliverable.
- **Clear audit trail** — enforced by the working-paper artifact above.

### 10.9 Governance & change control (extends §§8.7, 9.11)
- **Materiality thresholds** (default and any per-engagement override), **sampling standards**, and the **Evidence Quality Grade rubric** live in the metric registry (`backend/app/data_registry.py`), versioned.
- **Reviewed quarterly** alongside the ratio and sector-profile registries.
- **Independence check** — every engagement records that Aegira has no ownership, advisory, or conflicting economic interest in the target; the check is a required cell on the Scope tab.

### 10.10 Action items (§10 addendum to §§6, 8.8, 9.12)
1. **Add Scope / Business-Understanding / Risk-Register / Materiality / Controls-Snapshot / Estimates / Legal-Contingencies / Exceptions tabs** to the QoE workbook per §10.8-B. *(Cy → tested PR, folded into the P1 QoE build.)*
2. **Ship the Evidence Quality Grade (A/B/C)** on every document-review artifact and roll it up on the summary. *(Cy → tested PR.)*
3. **Auto-generate the working-paper artifact** on every workbook / review run (procedure · evidence hash · judgment · exception · resolution) — one file per run, provenance-signed. *(Cy → tested PR.)*
4. **Lint / fact-lock the reserved-opinion vocabulary** — no "audit," "opinion," "unqualified," "fair presentation," etc. in Aegira-authored outputs. *(Cy → tested PR.)*
5. **Independence-check cell** on every Scope tab; **materiality thresholds recorded**; **sampling standard applied and disclosed.** *(Cy.)*
6. **Founder confirm** — default materiality thresholds (proposal: **5% of EBITDA** or **$50k floor**, whichever is greater; per-engagement override permitted).
7. Keep the **decision-support / research-not-audit, derived-only, fact-locked, as-of-dated** posture on every surface. *(Ongoing.)*

---

---

## 11. EBITDA / QoE normalization — doctrine + adjustment library (adopted)

*(Founder-provided research 2026-08-27 — Investopedia sources on QoE and EBITDA adjustments + Cy-authored practitioner-common library. Where Investopedia legitimately did not prescribe an operational rule — owner-comp bands, related-party normalization, discontinued-ops treatment, minimum category count — the doctrine layer is captured verbatim from the Founder's research, and the operational library is built from first principles + free public accounting standards, sourced per adjustment.)*

### 11.1 Doctrine (captured verbatim from Founder research)

**A. EBITDA definition (canonical).**
- `EBITDA = net income + taxes + interest + depreciation + amortization`
- Equivalently: `EBITDA = operating income + depreciation + amortization`
- Designed to facilitate comparisons of **operating profitability** across differing depreciation assumptions and financing choices.

**B. Normalized-earnings framework.**
Apply **sustainable operating margins across a cycle** to **sustainable revenue**, then make **documented adjustments** for material items — including **restructuring charges, unconsolidated subsidiaries, and pricing power** — rather than accepting reported operating earnings at face value.

**C. Recurring-vs-one-time test (buyer-side rule).**
A QoE adjustment must be supported by **evidence** that the cost or revenue item is **unusual and not expected to continue.** **If the same item persists or recurs, it stays in normalized EBITDA — regardless of what management calls it.** Buyers and sellers **may disagree** on what qualifies as one-time; every adjustment therefore requires **clear evidence and explanation.**

**D. Owner-compensation doctrine.**
For closely-held businesses: **include the owner's total compensation, then adjust to market value** by subtracting **the amount required to pay an employee to perform the same services.** Post-acquisition EBITDA must bear a **reasonable replacement cost** for operational work the seller previously performed. **Labor assumptions post-close matter** — buyer and seller may expect to contribute different levels of work after closing.

**E. Run-rate doctrine (Daniel Liberto, *Owner Earnings Run Rate Explained*).**
Run-rate annualization is a **forecast assumption — not proof of sustainable EBITDA.**

> *"The owner earnings run rate is flawed when applied to companies whose financial performance fluctuates from quarter to quarter."* — Liberto

Distortion sources: **seasonality, new-product-release-driven sales surges, large one-time sales.** A defensible QoE bridge shows the **underlying monthly or quarterly trend** and explains **why the selected period is representative** before annualizing it. **Validate against a longer historical period** and **distinguish durable operating changes from temporary revenue or margin effects.**

**F. Adjustment-discipline invariants.**
- Each add-back or deduction is a **separately reconciled, evidence-based adjustment to reported EBITDA.**
- **Distinguish a one-time item from an ongoing operating requirement.**
- **Avoid equating an isolated recent period with sustainable performance.**
- **No published source prescribes a minimum number of adjustment categories** — practitioner convention only; the library below reflects that convention.

**G. Scope reminder (from §10 — non-negotiable).**
Aegira's QoE bridge is **decision-support / research — not an audit, not a formal QoE opinion.** Formal QoE opinions come from a licensed partner CPA who engages the target. Every bridge output carries this reservation + `JHI-SIG: 69M2705M`.

### 11.2 Practitioner-common adjustment library (20 categories)

*(Categories authored from first principles + free public accounting standards. Each has: definition · detection rule · computation rule · required evidence · recurrence test · authoritative reference. This is the operational library the QoE bridge engine implements.)*

**Buyer/seller sidedness convention throughout:**
- **Seller-side (add-back inflates EBITDA):** owner-comp overpay, personal expenses, one-time settlements/severance/legal, discontinued-ops loss, one-time bad debt, related-party rent/service overpay.
- **Buyer-side (add-back deflates EBITDA):** owner-comp underpay (below market), related-party rent/service underpay, missing replacement CapEx, missing insurance/benefits burden.
- **Both directions permitted; every adjustment carries a sign and a rationale.**

| # | Category | Definition | Detection rule | Computation | Evidence required | Recurrence test | Authoritative reference |
|---|---|---|---|---|---|---|---|
| **1** | **Owner / executive compensation to market** | Adjust reported owner/executive comp (incl. bonuses, distributions treated as comp) to arm's-length market rate for the role. | Owner-comp > 150% or < 50% of BLS OEWS median for occupation × MSA. | `Adj = Reported comp − Market comp (BLS OEWS median for role + geography, adjusted for revenue-tier)` | BLS OEWS citation (role code, geography, year) + role-fit justification + post-close staffing plan. | Recurring — always adjusted, never treated as one-time. | Replacement-cost doctrine (§11.1D); BLS OEWS (public) |
| **2** | **Related-party rent to fair-market rent** | Adjust rent paid to owner-controlled real estate entity to arm's-length market rent. | Any lease where landlord is related party per ASC 850. | `Adj = Reported rent − Market rent (broker BOV, CoStar / LoopNet MSA benchmark)` | Third-party rent benchmark (broker letter, CoStar comp, LoopNet comp) + lease terms. | Recurring — adjusted permanently. | ASC 850 Related Party Disclosures (FASB, free) |
| **3** | **Related-party service arrangements to arm's-length** | Adjust management fees, consulting fees, admin services from related entities to arm's-length pricing. | Any service paid to related party per ASC 850. | `Adj = Reported fee − Arm's-length fee (industry benchmark or documented cost-plus)` | Written third-party benchmark or cost-plus study. | Recurring. | ASC 850 |
| **4** | **Personal / non-business expenses run through P&L** | Remove personal expenses (travel, meals, vehicles, club memberships, family payroll for no-show roles). | Charge codes flagged as personal; entity-name matches owner personal. | `Adj = Personal expenses (sum, evidence-linked)` | Individual expense-report lines + owner attestation + receipts sampled. | Recurring — treated as permanent add-back. | Reg S-K Item 10(e); practitioner convention |
| **5** | **One-time legal / settlement expenses** | Remove non-recurring legal fees + settlement costs tied to closed matters (litigation, IP, employment). | Legal expense spike > 200% of trailing 3-yr baseline; settlement reserve movements. | `Adj = Non-recurring legal + settlements, netted against recurring counsel run-rate` | Matter list + closure evidence + counsel confirmation + no-repeat basis. | One-time — but only if closed; open matters DO NOT qualify. | ASC 450 Contingencies |
| **6** | **One-time restructuring / severance** | Remove severance + facility closure + reorganization costs from a defined restructuring event. | Restructuring reserve activity (ASC 420); event-defined severance schedule. | `Adj = Total restructuring cost, netted against ongoing severance run-rate` | Board-approved restructuring plan + severance schedule + facility disposal docs. | One-time per event — not per year. | ASC 420 Exit or Disposal Cost Obligations |
| **7** | **Discontinued / divested operations** | Remove revenue + costs of a component of an entity that has been disposed of or is held for sale. | ASC 205-20 conformity: (a) component of an entity, (b) strategic shift, (c) disposal-group criteria met. | `Adj = Discontinued-ops revenue − Discontinued-ops direct costs − allocated overhead (traceable only)` | ASC 205-20 test documentation + disposal date + P&L allocation methodology. | One-time (removed permanently from run-rate). | ASC 205-20 Discontinued Operations (FASB, free); IFRS 5 |
| **8** | **Non-recurring bad-debt write-offs** | Remove concentrated bad-debt losses tied to a single failed customer or event; retain ongoing bad-debt provision. | Bad-debt spike > 300% of trailing 3-yr provision rate; single-customer concentration > 50% of the spike. | `Adj = Non-recurring write-off − expected recurring provision (per trailing rate)` | Customer-level A/R aging + failure evidence (bankruptcy, dispute file). | One-time only if isolated; systemic collection deterioration is recurring. | ASC 326 Financial Instruments — Credit Losses |
| **9** | **One-time gain/loss on asset sale** | Remove gain/loss from disposal of PP&E, subsidiaries, non-operating assets. | Asset-disposal G/L line item; non-operating income section. | `Adj = Reported gain/loss on disposal (removed in full)` | Asset ledger + disposal document + book-value vs. proceeds. | One-time per disposal. | ASC 610-20 Gains and Losses from the Derecognition of Nonfinancial Assets |
| **10** | **Insurance-recovery / catastrophe recovery** | Remove insurance proceeds tied to a specific incident (fire, weather, cyber, business interruption); remove matching one-time loss. | Insurance-recovery line item + incident report. | `Adj = Insurance proceeds netted against directly-related one-time loss` | Insurance claim documentation + incident report + policy terms. | One-time per incident. | Evidence + recurrence test (§11.1C) |
| **11** | **Deferred-revenue / cash-vs-accrual timing** | Adjust for revenue-recognition timing distortions (deferred revenue drawdown; contract-modification catch-ups). | Deferred-revenue balance change > 15% of period revenue; ASC 606 modification disclosures. | `Adj = Timing-neutral revenue (accrual basis re-cast)` | Contract population + revenue-schedule reconciliation. | Depends on driver — timing normalization is typically recurring in some, non-recurring in others. | ASC 606 Revenue from Contracts with Customers |
| **12** | **Founder-only healthcare / insurance / retirement** | Remove above-market benefits paid on behalf of owner/family that would not persist post-close. | Benefits-per-headcount > 200% of employee-population average, concentrated in owner family. | `Adj = Owner-family benefits − replacement cost of standard benefits package` | Benefits ledger + owner attestation + post-close benefits plan. | Recurring add-back. | Replacement-cost doctrine (§11.1D) |
| **13** | **Above-market / below-market key contracts** | Adjust customer or supplier contracts materially off-market that will re-price on renewal. | Contract price ≥ 20% away from market benchmark + renewal in ≤ 24 months. | `Adj = (Market price − Contract price) × annualized units × probability-of-re-price` | Contract copy + market benchmark + renewal terms + probability rationale. | Recurring — but flagged as an **estimate**, not a hard adjustment. | Purchase-accounting analog (ASC 805) |
| **14** | **Pro-forma synergies (BUYER-SIDE FLAG ONLY)** | Buyer-planned cost savings or revenue synergies. | Any adjustment labeled "synergy," "combination benefit," "consolidation savings." | **Flagged, never applied in the seller-side bridge.** Presented separately as "Buyer synergy view — Aegira does not underwrite these." | Buyer's own 100-day plan + owner + realization timeline. | N/A — never in normalized-seller EBITDA. | Practitioner convention |
| **15** | **Run-rate revenue adjustments** | Annualize recent-period revenue to reflect a durable step-change (new contract, price change, capacity add). | Two consecutive quarters of ≥ 15% level shift + operational anchor (contract, capacity, pricing). | `Adj = (Run-rate period revenue × 4) − LTM revenue`, gated by stability test (see 11.3-B). | Contract / capacity / pricing evidence + monthly detail ≥ 24 months + stability test pass. | Highest-scrutiny category. Never applied to seasonal or volatile businesses (Liberto rule). | §11.1E (Liberto); COV / seasonality gate (§11.3-B) |
| **16** | **Discontinued product-line contribution margin** | Remove revenue + direct costs of a product line the target has exited (short of a full discontinued-op). | Product-line exit announcement + no forward sales pipeline. | `Adj = Product-line revenue − direct COGS − direct SG&A (traceable only)` | Product-line P&L + exit-decision documentation. | One-time (removed permanently). | ASC 205-20 analog for below-component-of-entity exits |
| **17** | **COVID / pandemic-era anomalies** | Remove PPP forgiveness income, ERTC credits, one-time pandemic operating disruptions. | Line items dated 2020-04 through 2022-06 with pandemic-related descriptors. | `Adj = Sum of pandemic-tagged one-time items (both sides)` | Documentation date-tagged; both revenue-side (PPP, ERTC) and cost-side (safety, closure) adjustments shown. | One-time. | Evidence + recurrence test (§11.1C) |
| **18** | **Litigation-in-progress reserves** | Do **not** remove reserves for **open** matters; only close-out adjustments after settlement. | Any legal-reserve movement tied to a still-open matter. | **Flagged, not removed** unless matter is closed. Open reserves stay in EBITDA. | Matter status + counsel letter (partner CPA path, §10.5). | Recurring while matter is open. | ASC 450 Contingencies |
| **19** | **Non-cash stock-based compensation** | **DO NOT reflexively add back SBC.** SBC is a real cost of retaining talent; treat as recurring in most cases. Add back only if the plan is (a) grandfathered / closed post-close AND (b) not being replaced with equivalent cash comp. | Explicit SBC add-back proposed. | `Adj = 0` in the default seller bridge; `Adj = SBC` only if the two conditions above are both met with evidence. | Plan documents + post-close comp design + board resolution. | Almost always recurring; add-back is the exception. | ASC 718 Compensation — Stock Compensation; buyer-side skepticism convention |
| **20** | **Change in accounting policy** | Restate historical results for a change in accounting method (e.g. inventory LIFO→FIFO, revenue-recognition policy) to a common basis. | ASC 250 policy-change disclosure or auditor-noted change. | `Adj = ASC 250 restated amount − reported amount` | ASC 250 disclosure + auditor confirmation. | One-time restatement effect; new policy going forward is recurring. | ASC 250 Accounting Changes and Error Corrections |

### 11.3 Guardrails (non-negotiable — enforced by code, not by convention)

**A. Evidence Quality Grade (from §10.8) required on every adjustment.**
- **A** = external / independent (attorney letter, third-party benchmark, government source, counterparty confirmation).
- **B** = original internal document (contract, invoice, plan document, board resolution).
- **C** = management-prepared / representation only.
- **No adjustment ships with grade < B** without an explicit `EVIDENCE_C_OVERRIDE` flag and a written rationale in the working-paper artifact.

**B. Run-rate stability gate (Liberto rule enforced deterministically).**
Before any run-rate annualization (category #15) can be applied, the code enforces:
- **Coefficient of variation (COV)** of monthly revenue over the trailing 24 months **< 0.30** — else annualization blocked.
- **Seasonality F-statistic** (12-month decomposition, additive) — must fall below threshold — else annualization blocked and seasonality-adjusted normalization required instead.
- **Operational anchor test** — contract, capacity add, or pricing change **must be documented**, dated, and quantifiable — else blocked.
- **Longer-period comparison** — the run-rate result must be shown alongside LTM and 3-year-average in the workbook; the analyst chooses with visible evidence.

**C. Owner-compensation calculator (deterministic).**
- Inputs: role code, geography (MSA), business revenue tier, owner's actual comp.
- Lookup: BLS OEWS median for role × MSA (via DATA_GOV adapter, cached, dated, sourced).
- Revenue-tier adjustment: no published band exists (Founder research confirmed); we apply a documented multiplier ladder (< $2M rev → 1.0×, $2M-$10M → 1.15×, $10M-$50M → 1.30×, > $50M → 1.50× of BLS median) as a **stated Aegira convention**, editable by engagement.
- Output: `Adj = Reported comp − Market comp × Revenue-tier multiplier`.

**D. Related-party rent benchmark.**
- No hardcoded benchmark; requires **at least one** of: broker letter (Grade A), CoStar/LoopNet comparable (Grade A), or three arm's-length lease citations for comparable properties (Grade B). C-grade owner assertion **blocked**.

**E. Buyer-view vs. seller-view columns.**
- Every adjustment carries a `SellerSide` and `BuyerSide` value (usually equal; opposite when reasonable perspectives diverge).
- Bridge presents **three totals:** Reported EBITDA · Seller Adjusted EBITDA · Buyer Adjusted EBITDA. **No hidden disagreements.**

**F. Bridge summary output (mandatory format).**
```
Reported EBITDA                         X,XXX
  + Cat 1 owner-comp to market            XXX  [Grade A · Recurring · BLS OEWS 11-1021 Chicago 2025]
  + Cat 2 related-party rent              XXX  [Grade A · Recurring · CoStar comp #45231 2026-01]
  + Cat 4 personal expenses               XXX  [Grade B · Recurring · Expense-report sample n=142]
  + Cat 5 legal (one-time)                XXX  [Grade A · One-time · Matter closed 2026-Q1]
  ...
Adjusted EBITDA (Seller view)           Y,YYY
Adjusted EBITDA (Buyer view)            Y,YYY
LTM / Run-Rate / 3-Yr-Avg presentation  Z,ZZZ | Z,ZZZ | Z,ZZZ  (run-rate shown only if stability gate passes)
```

**G. Opinion-vocabulary lint (from §10.8) applies.**
No word of the bridge output uses "audited," "opinion," "fair presentation," "certified," or "attested."

### 11.4 Mapping to Aegira build (implementation contract)

**A. New backend module — `backend/app/qoe_bridge.py`.**
- 20 category detectors + calculators from §11.2.
- Evidence Quality Grade enforcement (from §10.8).
- Run-rate stability gate (COV + seasonality F-stat + operational-anchor tests).
- Owner-comp calculator with BLS OEWS lookup (via existing DATA_GOV adapter).
- Buyer/seller sidedness.
- Deterministic driver notes per adjustment (LLM elevation via existing E2 fact-lock).

**B. New workbook sheet — `EBITDA_Bridge` embedded in every QoE + private-target diligence workbook.**
- Reported → adjustments (name, amount, evidence grade, recurrence flag, source, driver note) → Adjusted (Seller / Buyer views) → LTM / Run-Rate / 3-Yr-Avg comparison.
- Native Excel formatting; matplotlib waterfall PNG for the bridge visual.

**C. Wired to §10 QoE workbook tabs.**
- Feeds into the **Findings & Recommended Actions** section on the Cover.
- Materiality-flag rollup: any adjustment > materiality threshold (default 5% of reported EBITDA or $50k, whichever greater — §10.9 pending Founder confirm) surfaces on the Cover.

**D. Tests (P1 build — mandatory).**
- 20-category unit tests (one detector + one calculator per category, plus overriding rules).
- Run-rate stability-gate tests (pass / fail on synthetic seasonal / volatile / stable series).
- Owner-comp calculator tests against known BLS role codes.
- Evidence-grade enforcement tests.
- Buyer/seller-view divergence test.
- Opinion-vocabulary lint test.

### 11.5 Governance & change control (extends §§8.7, 9.11, 10.9)
- **Adjustment library, materiality thresholds, stability-gate parameters, and owner-comp revenue-tier multipliers** live in the metric registry (`backend/app/data_registry.py`) as `QoEAdjustmentProfile`, versioned.
- **Reviewed quarterly** alongside ratio and sector-profile registries.
- **Every published adjustment carries** its version stamp so historical deliverables remain reproducible.

### 11.6 Action items (§11 addendum to §§6, 8.8, 9.12, 10.10)
1. **Build `backend/app/qoe_bridge.py`** — 20 categories per §11.2 + guardrails per §11.3. *(Cy — this session, P1.)*
2. **Wire `EBITDA_Bridge` sheet** into the QoE workbook generator. *(Cy — this session, P1.)*
3. **BLS OEWS integration** for owner-comp calculator via existing DATA_GOV adapter. *(Cy — this session, P1.)*
4. **QoE adjustment library exposed** on the `Findings & Recommended Actions` Cover section with materiality flags. *(Cy — this session, P1.)*
5. **Founder confirm** — default materiality threshold (proposal: 5% of reported EBITDA or $50k floor, whichever greater; per-engagement override permitted).
6. **Founder confirm** — revenue-tier multiplier ladder for owner-comp calculator (proposal captured in §11.3C; editable per engagement).
7. Keep the **decision-support / research-not-audit, derived-only, fact-locked, evidence-graded** posture on every bridge output. *(Ongoing.)*

---

*Recorded by Cy Henry, VP Software Engineering (AI). JHI-SIG: 69M2705M. This blueprint — §§1–11 — is adopted of record as the target for Aegira's institutional financial-analysis deliverables (Tier 1 & 2 PE / search-fund / operator-buyer audience). Reference write-ups from the Founder will continue to be appended as they arrive (see standing directive above). How we do anything is how we do everything. TeamWork makes the DreamWork.*

> **§9 (personal-finance dashboard) was removed per Founder direction on 2026-08-27:** the original Investopedia write-up was misread as a personal-finance guide when the Founder's intent was business financial dashboards (already covered in §8). Aegira is an **institutional / operating-company research and diligence product** — personal-finance dashboards are out of scope.
