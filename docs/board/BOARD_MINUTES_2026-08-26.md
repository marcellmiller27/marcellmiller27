# Board Minutes — JHI Research & Analytics Firm, Inc.

**Meeting date:** 2026-08-26 (living document — extended 2026-08-27) · **Type:** Founder directive — product build blueprint (financial ratios + PE/search-fund workbook toolkit + institutional financial dashboards + personal-finance dashboards) · **Recorder:** Cy Henry (VP, Software Engineering — Cloud Agent)
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

## 9. Personal-finance dashboard — build specification (adopted verbatim)

*(Founder addendum, 2026-08-27 — Investopedia reference on how to build a personal financial dashboard. Capture every detail. Complements §8, which specified the **institutional / operating-company** dashboard; §9 specifies the **personal-finance / household** dashboard that becomes the basis of an Aegira subscriber-facing personal-finance deliverable.)*

### 9.1 Key takeaways (non-negotiable framing)
1. **Start with clear goals**, then select **only** the metrics that show progress toward them.
2. **Consolidate** income, spending, debt, savings, and investments into **one regularly updated view.**
3. Use **monthly budget-versus-actual** tracking and a **net-worth trend** to monitor financial progress.
4. **Separate essential, flexible, and non-monthly spending** to make the budget more actionable.
5. **Keep the main dashboard simple;** use supporting tabs for transaction detail and investment analysis.

### 9.2 Step 1 — Define the purpose and format
Decide what decisions the dashboard should support: **controlling monthly spending, paying down debt, building an emergency fund, tracking retirement savings, or monitoring a portfolio**. Begin with **specific goals** and choose **key performance indicators (KPIs)** that measure them; **avoid cramming every available number onto one page**. The dashboard should **evolve as needs, priorities, and financial circumstances change**.

**Format options** (both are valid):
- **A spreadsheet** — works well because it can **consolidate data from multiple sheets** and **calculate returns, gains/losses, and risk measures.**
- **A financial portal or app** — can **aggregate accounts** and show **spending, budgets, investments, debt, and net worth in one place.**

### 9.3 Step 2 — Build a simple workbook structure
Use these tabs or sections:

| Tab | What to track | Update frequency |
|---|---|---|
| **Dashboard** | KPI summary, charts, alerts, goals | Monthly |
| **Transactions** | Date, account, category, amount, notes | Weekly or automatically |
| **Budget** | Planned versus actual spending by category | Monthly |
| **Accounts & net worth** | Cash, savings, investments, loans, credit cards, property | Monthly |
| **Investments** | Holdings, cost basis, current value, return, allocation | Monthly or quarterly |
| **Goals & debt** | Emergency fund, debt balances, retirement, other targets | Monthly |

**For a clear budget**, track **all income sources** and **categorize expenses**. Common categories include:
- **Fixed costs** — housing, utilities, insurance, and loan payments
- **Discretionary spending** — dining, shopping, and travel
- **Savings**

**Regular tracking identifies where money is actually going and where spending can be reduced.**

### 9.4 Step 3 — Create the monthly budget view
- Enter **take-home income** rather than **gross pay**, then compare **planned spending with actual spending**.
- A practical structure separates expenses into **fixed, flexible, and non-monthly** categories; this makes **annual bills and irregular costs visible rather than treating them as surprises.**
- Include a **chart of spending by category** and a **planned-versus-actual bar chart.**
- A **budgeting calculator** similarly uses income and expense inputs to show **category percentages, remaining funds, and whether spending is within available income.**

### 9.5 Step 4 — Track net worth, cash, and debt
Create a **monthly net-worth statement**:

> **Net worth = total assets − total liabilities.**

- **Assets** can include checking and savings balances, retirement accounts, brokerage holdings, real estate, and other significant property.
- **Liabilities** include credit cards, student loans, auto loans, mortgages, and other debt.
- Track the **monthly change in net worth** and break it into:
  - **contributions,**
  - **debt reduction,**
  - **investment gains or losses, and**
  - **major purchases.**
- A **consolidated view** of everything you earn, spend, and own **can keep these figures current and easier to interpret.**

Add:
- **Emergency-fund progress measure** = *emergency-fund balance ÷ target emergency fund.*
- **Per-debt row** showing **balance, interest rate, required payment, and payoff progress.**
- **Budgeting and debt tracking support an action plan** to repay outstanding debt and improve net worth.

### 9.6 Step 5 — Add an investment tracker
**For each holding**, record: **account, ticker or fund name, units, average purchase price, current value, cost basis, gain/loss, and portfolio weight.**

**At the portfolio level**, show: **total value, contributions, total return, asset allocation, and performance over time.**

- Excel can calculate **percentage returns, profit and loss, and standard deviation**, which can help assess **volatility.**
- **Keep investment performance separate from contributions.** A rising portfolio may reflect **new deposits rather than market returns**, so **showing both prevents misleading conclusions.**
- **Use only information you understand** and **hide unnecessary columns** to keep the tracker readable.

### 9.7 Step 6 — Choose a concise KPI panel (top of Dashboard tab)
Put the following measures at the top of the Dashboard tab:
- **Monthly income, expenses, and surplus/deficit**
- **Savings and investment contribution rate**
- **Budget variance by category**
- **Cash balance and emergency-fund progress**
- **Total debt and debt-paydown progress**
- **Net worth and month-over-month change**
- **Investment balance, allocation, and return**
- **One to three goal-progress bars**, such as **debt payoff, home down payment, or retirement contribution target**

**Set targets for each KPI**, such as a **desired savings amount** or **maximum discretionary-spending limit.** **Effective dashboards connect metrics to stated goals, remain adaptable as conditions change, and avoid overwhelming users with too many indicators.**

### 9.8 Step 7 — Establish a monthly review routine
**Once a month**, do all of the following:
- **Reconcile account balances.**
- **Categorize uncategorized transactions.**
- **Compare actual spending with the budget.**
- **Update investments and debt.**
- **Write a brief explanation for major variances.**
- **Review whether goals advanced**, then **adjust next month's spending plan** for income changes, inflation, or unexpected expenses.

**A flexible budget that is reviewed and revised monthly is more useful than a static plan.**

Finally, **use the dashboard to make decisions, not merely record data**:
- If **discretionary spending exceeds plan**, **reduce a category or redirect funds.**
- If **debt is costly**, **prioritize repayment.**
- If **savings fall short**, **automate a contribution after essential expenses.**
- **Consistent tracking of earnings and spending helps keep the budget on target and reveals opportunities to save or invest.**

### 9.9 Mapping to Aegira (implementation contract)

**A. New subscriber-facing deliverable — Aegira Personal Financial Dashboard (Excel workbook).**
- **Six tabs, exactly as specified in §9.3:** `Dashboard`, `Transactions`, `Budget`, `Accounts_and_Net_Worth`, `Investments`, `Goals_and_Debt`.
- **Dashboard tab** — top-row KPI panel per §9.7 (income/expense/surplus, contribution rate, budget variance, cash + emergency-fund progress, total debt + paydown, net worth + MoM Δ, investment balance/allocation/return, 1–3 goal-progress bars); mid-row spending-by-category chart + planned-vs-actual bar chart (§9.4); bottom-row net-worth trend + debt-paydown chart.
- **Budget** — take-home-income entry, **fixed / flexible / non-monthly** split (§9.4), category-percentages + remaining-funds computation.
- **Investments** — per-holding rows (account, ticker, units, avg price, current value, cost basis, gain/loss, weight) + portfolio-level totals; **contributions kept separate from performance** so returns are not confused with deposits.
- **Goals & debt** — emergency-fund progress bar (balance ÷ target); per-debt row (balance, interest rate, required payment, payoff progress); goal-progress bars linked to the Dashboard.
- **Compliance layer (unchanged):** derived-only, fact-locked, dated, `JHI-SIG: 69M2705M`, **research/decision-support — not investment, tax, or legal advice.**

**B. Platform — new on-screen module: "My Aegira" (personal-finance dashboard).**
- **Same three-row canonical layout** — top KPI strip, middle trend charts, bottom net-worth/debt panels.
- **Manual-entry-first** (workbook import + hand-entry), with a documented adapter surface for future account aggregation (Plaid / MX / open-banking) — **no third-party account aggregation is enabled until a formal privacy/security review is completed and the Founder approves.** No PII crosses AI-agent boundaries.
- **Sits under a new "Personal" section in the TOC**, separate from Aegira's institutional/research modules to prevent scope confusion.
- **Tier gating (proposed, Founder to confirm):** basic net-worth + budget-vs-actual visible to free/newsletter tier; full KPI panel, per-debt tracker, investment analytics, and goal-progress reserved for Tier 1/2.

**C. Positioning — how §9 differs from §8.**
- **§8 = institutional / operating-company dashboard** — Revenue/EBITDA/Net income/OCF/Cash balance/Net debt; peer-benchmarked; part of the QoE / per-ticker / diligence workbooks.
- **§9 = personal-finance / household dashboard** — take-home income, category spend, net worth, emergency fund, per-debt payoff, per-holding investment tracker; monthly review routine.
- **Both share the same doctrine** — clear goals, KPI focus, targets & variance, trend context, drill-down tabs, review cadence, and the *Always-Deliver · Cadence-Aware · As-Of-Disclosed* data-foundation posture.

### 9.10 Governance & change control (extends §8.7)
The personal-finance dashboard is reviewed **monthly** (its own cadence — see §9.8). Metric definitions still live in the **canonical metric registry** (`backend/app/data_registry.py`) so terms shared with §8 (e.g. net debt, cash flow, investment return) have **one definition** across institutional and personal deliverables — no drift.

### 9.11 Action items (§9 addendum to §§6, 8.8)
1. **Build the Personal Financial Dashboard workbook** (six tabs per §9.3, KPI panel per §9.7, budget/net-worth/investment logic per §§9.4–9.6). *(Cy → tested PR, sequenced after §8 Dashboard sheet ships.)*
2. **Scaffold the "My Aegira" on-screen module** (manual-entry first, three-row canonical layout, no third-party aggregation until Founder-approved). *(Cy → tested PR.)*
3. **Extend the metric registry** with the personal-finance line items (income, expense categories, emergency-fund progress, per-debt schedule, per-holding returns). *(Cy.)*
4. **Founder confirm** — tier-gating proposal in §9.9-B and any privacy/security review requirements before enabling third-party account aggregation.
5. Keep the **derived-only, fact-locked, research-not-advice, as-of-dated** posture on every personal-finance surface.

---

*Recorded by Cy Henry, VP Software Engineering (AI). JHI-SIG: 69M2705M. This blueprint — §§1–9 — is adopted of record as the target for Aegira's financial-analysis and personal-finance deliverables. Reference write-ups from the Founder will continue to be appended as they arrive (see standing directive above). How we do anything is how we do everything. TeamWork makes the DreamWork.*
