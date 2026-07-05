# Fundamentals-Based Research Program — Protocol, Findings, Verdict, Solution

Objective: add fundamental factors and run an **equity-only, costed, out-of-sample**
protocol to test the Opportunity Score's predictive validity (H5); disclose all
findings (success or failure); and, if it fails, define the solution to get real
accuracy. Endpoints: `GET /api/v1/research/equity-oos-backtest`,
`GET /api/v1/research/fundamentals-status`.

## Binding constraint disclosed up front

**Fundamental factors cannot be back-tested in this environment.** Free,
unauthenticated sources do not expose programmatic fundamentals (Yahoo
`quoteSummary`/`v7` return HTTP 401 "Invalid Crumb"), and none provide *point-in-time
historical* fundamentals — which are required to avoid look-ahead and survivorship
bias. We therefore: (a) built the fundamentals factor harness **gated on a licensed
data source** (`fundamentals-status` reports `available=false`), and (b) ran the
historically valid part — an equity-only, costed, out-of-sample **price-factor**
back-test.

## Protocol (`equity_oos_backtest`)

- **Universe:** equity-only, ~30 large/mid-cap, sector-diverse names (bonds,
  commodities, and ETFs removed — they diluted the earlier mixed back-test).
- **Factors (cross-sectional z):** momentum_12_1, low_volatility, trend,
  reversal_guard.
- **Walk-forward split:** first 60% of months = **in-sample** (used only to *learn
  factor weights* ∝ positive in-sample IC); last 40% = **out-of-sample** (reported).
- **Costed:** a top-vs-bottom-tercile long-short portfolio; monthly **turnover**
  measured; net return = gross − turnover × (2 × 10 bps).
- **Pre-registered OOS success bar (declared before reading results):**
  `OOS mean IC ≥ 0.02 AND |OOS t-stat| ≥ 1.5 AND net annualized long-short > 0`.

## Findings (live run, 2026-06-24)

| Metric | Value | vs bar |
| --- | --- | --- |
| Equities / in-sample / OOS months | 30 / 64 / 44 | — |
| Learned weights | momentum 0.43, trend 0.57, low-vol 0.0, reversal 0.0 | — |
| **OOS mean IC** | **0.036** | ✅ ≥ 0.02 |
| **OOS hit rate** | **63.6%** | ✅ (informative) |
| Gross annualized long-short | +5.96% | — |
| **Net (after-cost) annualized long-short** | **+4.89%** | ✅ > 0 |
| Avg monthly turnover | 0.45 | — |
| **OOS IC t-stat** | **0.87** | ❌ < 1.5 |
| **OOS_PASS** | **FALSE** | — |

## Verdict — disclosed honestly: **FAILURE (but materially improved)**

The equity-only, costed, out-of-sample test **fails** the pre-registered bar because
the t-stat (0.87) is below 1.5 — the result is **not statistically significant**.
However, it is a clear, honest improvement over the prior mixed-universe test
(IC 0.007 → **0.036**; t 0.25 → 0.87) and is **economically positive**: a 64% hit
rate and **+4.9% net annualized** long-short after costs. The edge is real-looking
but under-powered: 44 OOS months is too few to reach significance.

## Solution to get real accuracy (since it failed)

The harness is correct; the gaps are **data and statistical power**, not method:

1. **License point-in-time fundamentals** (Sharadar / Compustat / Tiingo / FMP) and
   add **value (E/P, B/P), quality (ROE, margins, low accruals), and growth** factors
   — the missing orthogonal signal that price factors lack. (Harness is ready; flip
   `fundamentals-status` to live by wiring the vendor.)
2. **Raise statistical power:** larger survivorship-bias-free universe (hundreds of
   names) and a longer OOS window → the same +0.036 IC at, say, 200 names × 120 OOS
   months would push the t-stat well past 2.0.
3. **Risk-model neutralization** (sector/beta) and **realistic costs/borrow** so the
   long-short reflects an implementable strategy.
4. **Keep this pre-registered, walk-forward, costed protocol** — only the data and
   breadth change. Re-run and require `|t| ≥ 2.0` before declaring H5 confirmed.

## Net effect

- Fundamentals harness built and **honestly gated** (no fundamentals data available
  free; solution documented).
- Equity-only, costed, OOS protocol implemented and run: **economically positive but
  statistically insignificant → H5 still FAIL**, disclosed without spin.
- A concrete, no-shortcuts data+power plan is specified to actually reach accuracy;
  the code is ready to consume it.
