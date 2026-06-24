# Closing the Decisive Gap (H5) + Deficiency Fixes — Results

Objective of this work: attempt to close the decisive gap (Opportunity Score
predictive validity, H5), address incomplete datasets, and add real-time coverage
for the not-yet-real-time private/illiquid classes — then audit and clean up.

## 1. Opportunity Score is now DEFINED (deficiency fixed)

`backend/app/opportunity_score.py` replaces the previously undefined/ad-hoc score
with a transparent, fixed-weight, cross-sectional model:

`score = z(momentum_12_1)·0.50 + z(low_volatility)·0.20 + z(trend)·0.20 + z(reversal_guard)·0.10`,
percentile-ranked to 0-100. It is pure/unit-tested and reused by both the live
scorer (`GET /api/v1/research/opportunity-scores`) and the back-test.

## 2. Back-test dataset expanded (deficiency fixed)

The earlier test used 16 assets × ~24 months. It is now **32 assets × 108 months**
of real Yahoo monthly history (`GET /api/v1/research/score-backtest`), with
**pre-registered** H5 success criteria declared before reading results:
`mean IC ≥ 0.03 AND |t-stat| ≥ 2.0 AND hit rate ≥ 0.55`.

## 3. H5 verdict — honest result: still **FAIL**

Live run (2026-06-24):

| Metric | Value |
| --- | --- |
| Assets / periods | 32 / 108 |
| Mean information coefficient | **0.0074** |
| IC t-stat | **0.25** |
| Hit rate | **50.9%** |
| Annualized long-short | +3.5% |
| **H5 PASS?** | **FALSE** |

The defined score shows a *positive but weak and statistically insignificant*
association with forward returns — **below** the pre-registered bar. The decisive
gap is therefore **not closed by this price-only model on this universe**, and we
report that rather than fish for a passing configuration.

**Why, and the real path to close H5 (no shortcuts):**

- Price-only factors across a *mixed* asset universe (equities + bonds + commodities)
  dilute the signal; momentum is strongest *within* equities.
- Genuine validity needs **fundamental inputs** the marketed score advertises
  (valuation, growth, quality, liquidity, institutional activity), proper
  **portfolio construction** (risk model, costs), and **out-of-sample** testing.
- That is a research program, pre-registered to the same bar — not a one-shot.

## 4. Private / illiquid classes now have real-time MODELED estimates (gap addressed)

`GET /api/v1/valuations/estimate` returns request-time estimates from live inputs
(`backend/app/valuation_services.py`), updating as rates/proxies move:

| Class | Model | Example (live) |
| --- | --- | --- |
| Direct real estate | NOI ÷ (live 10Y + spread) cap rate | NOI 120k → ≈ $1.74M at 6.9% cap |
| Private business / SMB | EBITDA × live small-cap multiple (illiquidity-discounted) | EBITDA 1.5M → ≈ $8.47M |
| Private equity | committed × (1 + live listed-PE proxy move) | 2.0M, proxy −8.9% → ≈ $1.82M |

These are clearly labeled `modeled_estimate` (not quotes/appraisals) and carry a
disclaimer. The coverage matrix now lists these classes as real-time *modeled*.

## 5. Audit + cleanup performed

- **Dropped the orphaned `crypto_holdings` table** (with residual rows) from the dev
  DB — resolves the data-hygiene anomaly from `docs/PLATFORM_AUDIT_ANOMALIES.md`.
- Backend: `ruff` clean; **53 tests pass**; no debug/TODO debris in `app/`.
- Frontend: `eslint`, `tsc --noEmit`, and `next build` all pass.
- Module objectives documented in `docs/CODE_OBJECTIVES.md`.

## Net effect

Two deficiencies are genuinely fixed (the score is now **defined**; the test
dataset is **materially larger**), and the illiquid-class real-time gap is addressed
with **modeled estimates**. The decisive **H5** gap remains **open** with the honest
verdict FAIL — now measured rigorously against a pre-registered bar, with a clear,
no-shortcuts path to actually close it.
