# Cross-Asset Valuation & Action Engine — Spec

**Owner:** Cy Henry (VP Software Engineering — AI) · **Signature:** `69M2705M` · **Status:** spec for Founder review
**Purpose:** A one-stop engine that **values every asset class with the *right* method** and, on top of the
number, delivers an **action write-up** — *enter, stay sidelined, hold dry powder, or repurpose/rebalance*.
Includes the **detailed DCF** (equities + private deals) and its delivery **inside the Excel workbook**.
Pillar A (public markets) sibling to the Pillar B (private-deal) diligence tools. Not investment advice.

---

## 1. Guiding principle (why not "DCF everywhere")
**DCF values cash-flow assets** — equities and private businesses (they generate free cash flow).
It is **not** valid for commodities, crypto, or forex (no cash flows). To stay institutionally credible
(and honor the NASDAQ-grade audience), each asset class uses its **own appropriate method**; the *shape*
of the output is unified (fair-value vs. price → signal → action), the *math* is asset-appropriate.

## 2. Method per asset class
| Asset class | Valuation method(s) | Core inputs | Output signal |
|---|---|---|---|
| **Equities / Stocks** | **DCF** (primary) + trading multiples cross-check | EDGAR financials, QoE-style adjusted FCF, WACC, growth | intrinsic value vs. price → under/fair/over |
| **Private businesses** | **DCF** + multiple (already in Deal X-Ray/QoE) | CIM/seller financials, adjusted EBITDA | value vs. asking price |
| **Commodities** (Gold, Oil…) | Real-rate & cost-of-carry, supply/demand, futures-curve/z-score vs. history | real yields, inventories, curve, USD | rich / fair / cheap vs. regime |
| **Crypto** (BTC…) | Network/adoption, liquidity, scarcity, volatility-scaled positioning (**labeled speculative**) | on-chain/adoption proxies, liquidity, realized vol | regime / positioning bias |
| **Forex** (pairs) | Rate differentials, PPP, carry | policy-rate spreads, inflation, real rates | over- / under-valued vs. fair |

## 3. The unified output (every asset)
1. **Fair-value estimate** (or fair *range*) + **current price**.
2. **Signal:** Undervalued / Fair / Overvalued (+ confidence).
3. **Action write-up** (the differentiator) — one of:
   - **Enter** (opportunity to add / initiate),
   - **Stay sidelined** (wait; not attractive yet),
   - **Hold dry powder** (be patient; conditions improving — keep capital ready),
   - **Repurpose / rebalance** (trim/rotate; redeploy the balance sheet).
   With the **why**, tied to the model + the macro regime.
4. **Methodology & sources** disclosure + "**not investment advice**" line.

## 4. The detailed DCF (equities & private)
- **Starting cash flow:** QoE-adjusted EBITDA → unlevered free cash flow (EBIT·(1−tax) + D&A − capex − ΔNWC).
- **Projection:** explicit **5-year** FCF with disclosed assumptions (revenue growth, margins, capex, working capital, tax) — sourced from **CIM** (private) or **EDGAR** (public), each labeled.
- **Discount rate (WACC) build-up:** risk-free + equity-risk + **size/illiquidity** + **concentration/key-person** (private) — transparent, not a black box. *The macro regime (rates) feeds this — the loop from Pillar A.*
- **Terminal value:** shown **both ways** — Gordon growth **and** exit multiple.
- **Bridge:** Enterprise Value → less net debt → **Equity Value**; vs. price/asking.
- **Sensitivity table:** WACC × growth (honest range, not false precision).
- **Cross-check:** the multiple-based value (Deal X-Ray already curbs its DCF against this).

## 5. Delivery — inside the Excel workbook (Founder's ask)
Add to the institutional workbook (`backend/app/excel_export.py` / `edgar_workbook.py` pattern):
- **`DCF` sheet** — editable inputs (growth/margins/WACC/terminal), the 5-yr FCF build, EV→equity bridge, sensitivity grid.
- **Per-asset-class valuation sheets** (Commodities, Crypto, Forex) — method inputs → signal.
- **`Action Summary` tab** — every tracked asset with **fair value · price · signal · action** (enter/sideline/dry-powder/rebalance) + one-line rationale.
- **Provenance:** `JHI-SIG`, sources, "as of," disclaimer watermark (consistent with existing workbooks).
- Also surfaced **on-screen** and in the **PDF** (same engine), and the **AI action write-up** authored by Ellery/Bedrock, **fact-locked** to the model outputs (never invents figures).

## 6. Fits the architecture
- **Pillar A** capability (public markets) — sibling to Pillar B (private-deal DCF/QoE), kept distinct so the two worlds stay clean (`docs/PLATFORM_ARCHITECTURE_MAP.md`).
- **Expands the Opportunity Score** — from a single 0–100 into a **per-asset, action-oriented** score with a written rationale.
- **Consumes the loop** — the macro/rate read (Economics) drives discount rates and regime calls.

## 7. Data dependencies
- **Equities DCF:** **EDGAR** fundamentals (a planned data phase) + market price.
- **Commodities/Crypto/Forex:** the **market feeds + macro** we already poll (rates, inflation, prices, change); some need added series (real yields, curve, on-chain proxies) — flagged per method.

## 8. Governance (non-negotiable)
Decision-support only — **not** an appraisal, fairness opinion, or investment advice. Every output carries
the disclosure + "verify with licensed professionals." Crypto explicitly labeled speculative. Fact-lock on
all AI text. Licensed-data (NASDAQ) isolation preserved — derived outputs only.

## 9. Phasing (recommended)
- **Phase 1 — Equity DCF in the workbook** (closest to what we have): detailed DCF sheet feeding off adjusted earnings/EDGAR + the AI action write-up. *(Highest value, lowest new-data risk.)*
- **Phase 2 — Commodities** valuation sheet → Action Summary.
- **Phase 3 — Crypto**, then **Phase 4 — Forex**, each rolling into the Action Summary.
- Each phase = its own tested PR; on-screen + PDF + workbook parity.

## 10. Open questions for the Founder
1. **Universe:** which tickers/assets in v1 (a curated set, or the current dashboard set: SPX, Gold, UST10Y, BTC + a few equities)?
2. **Action thresholds:** your preferred bands for enter/sideline/dry-powder/rebalance (e.g., >X% undervalued = enter) — or start with my proposed defaults and you tune?
3. **Equity coverage:** US-only via EDGAR to start?
4. **Workbook vs. on-screen priority** for v1 (I recommend: build the engine once, render to all three — workbook, screen, PDF).

*Next: on approval, I build **Phase 1 (equity DCF in the workbook + AI action write-up)** as its own tested PR.*
