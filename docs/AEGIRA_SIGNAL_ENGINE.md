# Aegira Signal Engine — Multi-Horizon · Multi-Asset · Validation-Gated

**Date:** 2026-08-11 · **JHI-SIG:** `69M2705M`
**Product:** Aegira · **Publisher:** JHI Research & Analytics Firm, Inc. (proprietary)
**Owner:** Cy Henry (VP, Software Engineering — AI) · **Status:** master construct of record (Founder-approved)

> The single construct that governs **every trade signal Aegira ships** — across horizons (day →
> long-term → short-side) and asset classes (equities, ETFs, commodities, crypto, forex, options).
> Reverse-engineered from real trader pain points, gated by pre-registered back-tests (the **H5
> method**), fact-locked, and as-of/source-disclosed. Companion docs:
> `docs/VALUATION_FRAMEWORK_2.0.md`, `docs/CROSS_ASSET_VALUATION_ENGINE_SPEC.md`,
> `docs/DATA_FOUNDATION_CONSTRUCT.md`, `docs/MARKET_DATA_SOURCES.md`,
> `docs/H5_SF1_VALIDATION_RESULTS.md`. **Research, not investment advice.**

---

## 0. Why this exists

Traders lose money for structural, repeatable reasons: they buy tops on hype, hold losers past
their thesis, mistime entries, ignore regime, and misprice optionality. Aegira's edge is not "more
data" — it is **discipline made systematic**. This construct turns each trader pain point into a
concrete, validated signal, with an honest label on how much to trust it. **Discipline over hype.**

---

## 1. Principles (binding across every signal)

| # | Principle | What it means in practice |
| --- | --- | --- |
| **P1** | **Reverse-engineered from pain** | Every signal maps to a documented trader failure mode (§7). We build the fix, not the fad. |
| **P2** | **Validation-gated (H5)** | No signal ships to a paying user as *validated* until it clears a **pre-registered back-test** on its own horizon×asset cell (§8). Method mirrors `docs/H5_SF1_VALIDATION_RESULTS.md`. |
| **P3** | **Fact-locked** | AI write-ups are locked to model outputs. The engine computes numbers; the narrator never invents, rounds away, or contradicts them. |
| **P4** | **As-of / source disclosed** | Every signal carries its **data date**, **cadence**, and **source/vendor**. Users always know how fresh a call is and where it came from. |
| **P5** | **Never fabricate** | Missing/stale inputs are labeled (`pending`, `as-of <date>`, `estimated`, `unavailable`) — never silently backfilled. Degrade gracefully to what *is* available (per `DATA_FOUNDATION_CONSTRUCT.md`). |
| **P6** | **Discipline over hype** | Conviction is earned from evidence, not momentum of the crowd. The engine is willing to say *neutral / stay sidelined*. |
| **P7** | **Honest labeling** | Signals are shipped as **`validated`** (cleared H5) or **`directional`** (plausible, not yet cleared). The label is always visible. |

---

## 2. Horizons in scope (v1)

Each horizon has its **own tuned composite** (different layer weights, lookbacks, and thresholds)
and its **own validation cell**. A signal is never reused across horizons without re-validation.

| Horizon | Holding window (typical) | Dominant layers | Primary user |
| --- | --- | --- | --- |
| **Day** | Intraday → close | Technical/Momentum, Volatility/Regime, Flow (intraday) | Day trader |
| **Swing** | ~2–15 trading days | Technical/Momentum, Volatility/Regime, Flow/Sentiment | Swing trader |
| **Position** | Weeks → few months | Momentum + Fundamental/Value blend, Regime | Position trader |
| **Long-term** | Quarters → years | Fundamental/Value (Valuation 2.0), Income/Yield, Moat | Investor |
| **Short-side** | Symmetric across windows | Momentum breakdown, Valuation stretch, Flow (short-interest/squeeze), Regime | Short seller / hedger |

*Short-side is treated as a first-class horizon, not an afterthought: it has its own composite, its
own squeeze-risk guardrails, and its own validation.*

---

## 3. Asset classes in scope (v1)

| Asset class | In v1 | Notes |
| --- | --- | --- |
| **Equities** | ✓ | Single names; full layer stack incl. Valuation 2.0. |
| **ETFs** (incl. dividend) | ✓ | Broad/sector/thematic + dividend/income ETFs (feed Income/Yield layer). |
| **Commodities** | ✓ | Gold, oil, etc. — no cash flows → regime/curve/positioning methods (per `CROSS_ASSET_VALUATION_ENGINE_SPEC.md`). |
| **Crypto** | ✓ | BTC/ETH + majors — volatility-scaled, regime-labeled, speculative. |
| **Forex** | ✓ | Major/minor pairs — rate differentials, carry, PPP. |
| **Options** | ✓ | Chains, IV, greeks → strategy suggestions matched to the equity/ETF view (§5). |

Method-per-asset (fair-value math) is defined in `CROSS_ASSET_VALUATION_ENGINE_SPEC.md`; this
construct governs the **signal shape, layering, weighting, and validation** on top of it.

---

## 4. Signal layers (horizon-weighted)

Each signal is a **weighted composite** of layers. Weights are per horizon×asset (declared before
validation, never tuned to the result). The five core layers:

| Layer | What it measures | Example inputs |
| --- | --- | --- |
| **L1 — Fundamental / Value** | Intrinsic worth vs. price (Valuation 2.0) | R&D-adjusted DCF, ROIC/reinvestment, scenario/SoP, moat, mgmt quality (`VALUATION_FRAMEWORK_2.0.md`) |
| **L2 — Technical / Momentum** | Trend, breakout, mean-reversion, relative strength | price/volume, MA structure, RSI/MACD, ATR, RS vs. sector |
| **L3 — Volatility / Regime** | Risk state, trend-vs-chop, vol expansion/contraction | realized/implied vol, VIX/term structure, regime classifier, correlation |
| **L4 — Flow / Sentiment** | Positioning & crowd behavior (incl. short-interest / squeeze) | short interest, days-to-cover, options flow, put/call, breadth, funding (crypto) |
| **L5 — Income / Yield** | Cash return & sustainability | dividend yield, payout ratio, coverage, growth streak, distribution risk |

### 4.1 Illustrative horizon weighting (declared, pre-validation)

| Horizon | L1 Fund | L2 Tech | L3 Vol/Regime | L4 Flow | L5 Income |
| --- | --- | --- | --- | --- | --- |
| **Day** | 0% | 55% | 30% | 15% | 0% |
| **Swing** | 10% | 45% | 25% | 20% | 0% |
| **Position** | 35% | 30% | 20% | 15% | 0% |
| **Long-term** | 55% | 10% | 10% | 5% | 20% |
| **Short-side** | 20% (stretch) | 30% (breakdown) | 25% | 25% (squeeze-aware) | 0% |

*Weights above are the v1 **starting hypothesis**. Each cell's weights are frozen in the
pre-registration file before its H5 run; validated weights become the shipped config.*

---

## 5. Options layer (chains · IV · greeks → strategy)

The options layer reads the chain and translates the engine's directional view into a **concrete
options strategy** matched to conviction, horizon, and volatility regime.

**Signals read:**
- **IV rank / IV percentile** — is volatility rich or cheap vs. its own 52-week history?
- **Greeks** — delta (directional exposure), theta (decay), vega (vol exposure), gamma (convexity).
- **Skew** — put vs. call IV shape → tail pricing / directional fear.
- **Put/Call ratio** — sentiment / positioning.
- **Unusual options activity (UOA)** — outsized volume vs. open interest → informed-flow proxy (L4).

**Strategy mapping (matched to the view + IV regime):**

| Directional view | Vol regime | Suggested structure |
| --- | --- | --- |
| Mildly bullish, own shares | IV rich | **Covered call** (harvest premium) |
| Bullish, want to buy lower | IV rich | **Cash-secured put** (get paid to wait) |
| Bullish, defined risk | IV moderate | **Call vertical (debit)** |
| Bearish, defined risk | IV moderate | **Put vertical (debit)** |
| Big move expected, direction unclear | IV cheap | **Long straddle / strangle** |
| Range-bound | IV rich | **Short vertical / iron condor** (labeled higher-risk) |

Every options suggestion ships with the **greeks at entry**, the **breakeven(s)**, the **max
loss/gain**, and an explicit **risk disclosure** (§9). Options suggestions are *directional* until
their horizon×options validation cell clears.

---

## 6. Common output schema (every signal, every asset)

The *shape* is unified even though the *math* is asset-appropriate:

```json
{
  "symbol": "TSLA",
  "asset_class": "equity",
  "horizon": "position",
  "direction": "long | short | neutral",
  "conviction": 0,                       // 0–100
  "level_context": {                     // entry/exit or level framing
    "entry": null,
    "exit_or_target": null,
    "invalidation": null,
    "fair_value_or_range": null
  },
  "rationale": "fact-locked narrative tied to the layer outputs",
  "layers": { "fundamental": 0, "technical": 0, "volatility": 0, "flow": 0, "income": 0 },
  "as_of": "2026-08-11",
  "cadence": "daily | intraday | realtime",
  "sources": ["EODHD", "..."],
  "status": "validated | directional"    // H5 gate result (P2/P7)
}
```

**Field rules:** `direction ∈ {long, short, neutral}` · `conviction ∈ [0,100]` (evidence-earned,
not crowd-earned) · `status` is always shown · `as_of`/`sources` are never blank (P4/P5).

---

## 7. Pain → signal map (per trader type)

| Trader type | Core pain point | Aegira signal (the fix) |
| --- | --- | --- |
| **Day** | Chasing intraday noise; no edge on entries/exits | Intraday momentum + regime filter; only fires in trend regimes; explicit invalidation level; hard "no-trade / neutral" in chop. |
| **Swing** | Buys breakouts that fail; exits winners too early | Swing composite (momentum + vol expansion + flow), target/invalidation levels, trail logic; validated hit-rate shown. |
| **Position** | Holds losers past thesis; averages down blindly | Blend of Valuation 2.0 + trend; **thesis-invalidation trigger** flips signal to neutral/short when fundamentals + trend both break. |
| **Long-term** | Under-values innovators; overpays for hype | Valuation 2.0 (R&D-as-investment, optionality, moat) → fair-value range vs. price; income sustainability check. |
| **Short-side** | Gets squeezed; shorts strong stocks too early | Breakdown + valuation-stretch composite **gated by squeeze risk** (short interest, days-to-cover, borrow); sizing/warning when squeeze-prone. |
| **Options** | Buys expensive premium; wrong structure for the view | IV rank/greeks/skew → structure matched to view + vol regime (§5); breakeven/greeks/max-loss disclosed. |
| **Income** | Reaches for unsustainable yield (dividend traps) | Income/Yield layer: yield **plus** payout/coverage/growth durability; flags distribution risk. |

---

## 8. Data plan & dependencies

The engine inherits the data doctrine of `DATA_FOUNDATION_CONSTRUCT.md` (always-deliver,
never-fabricate, as-of, resilient, governed). Vendor plan:

| Need | Recommended vendor | Class | Covers | Tier |
| --- | --- | --- | --- | --- |
| **Global fundamentals + EOD prices** | **EODHD** | Licensed (derived-only) | Equities, ETFs, commodities, forex — global | Core (P1/P2) |
| **Crypto** | **CoinGecko** | Free tier viable | BTC/ETH + majors, market data | Core |
| **US fundamentals (factors)** | **Sharadar SF1** (existing) | Licensed (derived-only, gitignored cache) | US equity value/quality/growth (feeds L1 + Valuation 2.0) | Existing |
| **Macro / rates / regime** | **FRED / BLS / BEA** (existing) | Public-domain | Rates, inflation, macro → L3 regime, WACC | Existing |
| **Options** | **Polygon** / **Tradier** / **ORATS** | Licensed | Chains, IV, greeks, skew, UOA | P3 |
| **Real-time / intraday** | Vendor real-time tier (EODHD intraday / Polygon / Tradier) | Licensed | Intraday bars, quotes | P3 (day-trading) |

**Per horizon×asset requirement flags (what each cell *must* have to ship validated):**

| | Equities/ETF | Commodities | Crypto | Forex | Options |
| --- | --- | --- | --- | --- | --- |
| **Day** | intraday/real-time (P3) | intraday (P3) | CoinGecko + intraday (P3) | intraday FX (P3) | real-time chain + greeks (P3) |
| **Swing** | EOD + SF1 | EODHD EOD | CoinGecko | EODHD FX | EOD chain (P3) |
| **Position** | EOD + SF1 + Val 2.0 | EODHD + curve | CoinGecko | EODHD FX + rates | EOD chain (P3) |
| **Long-term** | SF1 + Val 2.0 + fundamentals | curve/real-rate | on-chain/adoption proxies | rate differentials | n/a (underlier view) |
| **Short-side** | EOD + short interest + borrow | EODHD | CoinGecko + funding | EODHD FX | put skew + IV (P3) |

*A cell cannot ship as `validated` until its required inputs above are live **and** its H5 run clears.*

---

## 9. Validation (H5, per horizon × asset)

Every horizon×asset cell is validated **independently** using the pre-registered back-test method of
`docs/H5_SF1_VALIDATION_RESULTS.md`:

1. **Pre-register** the composite, layer weights, lookbacks, thresholds, universe, and success bar
   **before** reading any results. No configuration is tuned to the outcome.
2. **Success bar** (per cell, horizon-appropriate — e.g. IC / t-stat / hit-rate for ranking signals;
   or return-vs-benchmark, Sharpe, max-drawdown, and hit-rate for directional entries).
3. **Out-of-sample**, survivorship-free where data allows.
4. **Ship rule:** clear the bar → ship as **`validated`**. Miss the bar → ship as **`directional`**
   (or withhold), with the honest result recorded in the audit trail. Never relabel a miss as a pass.

The validation matrix (horizon × asset) is the program's scoreboard; each cell records: status,
run date, bar, result, and the frozen config.

---

## 10. Governance & disclosures

- **Licensed data** (EODHD, SF1, options vendors) is **derived-only + attributed**: raw rows stay
  internal (gitignored cache); only derived metrics/signals surface. Attribution is mandatory.
- **Options risk disclosure** on every options suggestion (defined vs. undefined risk, assignment,
  early exercise, decay). Undefined-risk structures are labeled higher-risk.
- **Short-side risk disclosure**: unlimited loss potential, borrow/recall risk, squeeze risk.
- **Research, not investment advice** on every surface (screen, PDF, Excel, newsletter).
- **Fact-lock** enforced at the narration layer (P3): AI write-ups cannot contradict model outputs.
- **As-of / source** stamped on every signal (P4).

---

## 11. Rollout — Phases 1–3

### Phase 1 — Foundation on existing data *(build now)*
- **Horizons:** Long-term, Swing, Position, **Short-side**.
- **Assets:** Equities + ETFs.
- **Data:** existing SF1 + FRED/BLS/BEA + EOD prices; **Valuation 2.0** for L1.
- **Deliver:** composites per cell, common output schema, pain→signal write-ups, `directional`/
  `validated` labels; run H5 on each P1 cell.

### Phase 2 — Breadth via global vendor
- **Assets:** add Commodities, Crypto, Forex (+ global equities/ETFs).
- **Layers:** add **Income/Yield** (dividend ETFs + equities).
- **Data:** onboard **EODHD** (global fundamentals + EOD) and **CoinGecko** (crypto).
- **Deliver:** validate the new horizon×asset cells; expand the validation matrix.

### Phase 3 — Options, day-trading, real-time, full validation
- **Assets/Layers:** add **Options** layer (chains/IV/greeks/skew/UOA → strategy suggestions).
- **Horizon:** add **Day** trading (intraday composites).
- **Data:** onboard options vendor (Polygon/Tradier/ORATS) + real-time/intraday tier.
- **Deliver:** complete the validation matrix; every shipped cell carries an honest `validated` /
  `directional` label and full disclosures.

---

*Prepared under JHI-SIG `69M2705M`. Aegira is a product of JHI Research & Analytics Firm, Inc.
Research, not investment advice.*
