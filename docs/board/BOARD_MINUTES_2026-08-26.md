# Board Minutes — JHI Research & Analytics Firm, Inc.

**Meeting date:** 2026-08-26 · **Type:** Founder directive — product build blueprint (financial ratios + PE/search-fund workbook toolkit) · **Recorder:** Cy Henry (VP, Software Engineering — Cloud Agent)
**Product:** Aegira · **Publisher:** JHI Research & Analytics Firm, Inc.
**Present:** Founder (Galen Marcellus Miller).

> NOT legal/tax/accounting/investment advice. Prior session: `docs/board/BOARD_MINUTES_2026-08-13.md`.
> Signature of record — `JHI-SIG: 69M2705M`. Ethos: *How we do anything is how we do everything.*

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

*Recorded by Cy Henry, VP Software Engineering (AI). JHI-SIG: 69M2705M. This blueprint is adopted of record as the target for Aegira's financial-analysis deliverables. How we do anything is how we do everything. TeamWork makes the DreamWork.*
