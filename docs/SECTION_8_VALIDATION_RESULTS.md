# §8 Validation Results — From Design-Confirmed Toward Market-Confirmed

This document records the execution of the validation program defined in
`docs/RESEARCH_THESIS_PROBLEM_SOLUTION_FIT.md` §8. Each study is a **real,
reproducible computation** exposed under `/api/v1/research/*` and run live.
Exact figures refresh because the back-test reads live history; representative
values from a run on 2026-06-24 are shown.

> Honest bottom line: live market data is now wired across the tradable asset
> classes, and the studies are runnable, but the evidence **upgrades** the thesis
> only partially. Predictive validity of the score (H5) is **not** confirmed, and
> several data deficiencies remain open. The thesis moves from "design-confirmed"
> to "design-confirmed + partially market-evidenced," not "market-confirmed."

## §8.1 — Wire live data ✅ done

The dashboard "Market watch" now consumes `GET /api/v1/market/quotes` client-side
and auto-refreshes (`src/components/live-market.tsx`, `src/app/dashboard/page.tsx`),
replacing the former static `marketSignals`. Live providers: CoinGecko (crypto),
Yahoo Finance (equities/indices/commodities/treasury yields/REIT), US BLS (CPI).
See `docs/MARKET_DATA_SOURCES.md`.

## §8.2 — Score back-test ⚠️ run; H5 NOT confirmed

Endpoint: `GET /api/v1/research/score-backtest`
(`backend/app/research_services.py:score_backtest`).

- **Method:** cross-sectional monthly factor information coefficient (IC) on real
  Yahoo monthly history for a 16-name multi-asset universe (~24 evaluable months).
- **Score (transparent proxy):** `z(12-month momentum) − 0.5·z(6-month volatility)`,
  scored against next-month forward return.
- **Result (2026-06-24 run):** mean IC ≈ **0.014**, IC t-stat ≈ **0.25**,
  hit rate ≈ **46%**, mean top-minus-bottom tercile return ≈ **+0.28%/mo**.
- **Verdict:** the signal is **weak and statistically insignificant** (|t| ≪ 2).
  This is first-pass evidence only and **does not confirm H5**. It also shows the
  harness works end-to-end on real data.
- **Caveats:** transparent proxy (the marketed Opportunity Score has no published
  formula); tiny universe / short window; single vendor; no costs/slippage or
  survivorship control.

## §8.4 — Segment adoption study ⚠️ instrument validated; dataset not

Endpoint: `GET /api/v1/research/adoption` (auth required)
(`backend/app/research_services.py:adoption_study`).

- **Method:** KPIs computed directly from real platform tables (organizations,
  users, subscriptions, user_security, device_credentials, audit_logs).
- **Result (2026-06-24 run):** counts populated from the live DB (e.g., plan mix
  across consumer/professional/enterprise; 2FA and biometric adoption rates;
  login activation rate).
- **Verdict:** the **measurement instrument is validated** (it returns correct
  KPIs from real rows), but the **dataset is non-representative** — current rows
  are development/test accounts, not a paying cohort.
- **Open deficiencies:** no real acquisition funnel / paying cohort; no
  longitudinal retention or NRR; no willingness-to-pay or conversion experiments.

## §8.5 — Acquisition-engine validation ⚠️ engine consistent; labels are a fixture

Endpoint: `GET /api/v1/research/acquisition-validation`
(`backend/app/research_services.py:acquisition_validation`).

- **Method:** deterministic engine — normalized EBITDA = reported + add-backs;
  DSCR = normalized EBITDA / annual debt service; recommendation from DSCR and
  entry multiple — compared to a labeled case set.
- **Result (2026-06-24 run):** **100% agreement (5/5)** with expected labels;
  DSCR/SBA flags computed per case.
- **Verdict:** confirms the engine is **internally consistent and correct against
  its labels**. It does **not** confirm real-world accuracy, because the labels are
  a **constructed fixture, not expert-underwriter judgments**.
- **Open deficiencies:** no inter-rater reliability vs human underwriters;
  document-level diligence (fraud / quality of earnings) not modeled.

## Data coverage / deficiency matrix

Endpoint: `GET /api/v1/research/data-coverage`.

| Category | Real-time | Status |
| --- | --- | --- |
| Crypto, Equities, Indices, Commodities, Treasury yields, REIT proxy, Inflation/CPI | yes | **live (7)** |
| FX / currencies | no | none — no FX provider wired |
| Bonds (corporate/muni) | no | none — no fixed-income source |
| Direct real estate (per-property) | no | none — illiquid; needs appraisal/estimate feed |
| Private businesses / SMB | no | none — model/diligence-driven, not a quote |
| Private equity holdings | no | none — periodic/manual marks |
| Macro (rates curve, M2, GDP, unemployment) | partial | only CPI wired; add FRED series |
| Opportunity Score predictive validity | partial | back-test only; production validation pending |

**Summary:** 7 of 14 categories have real-time live data. Liquid/tradable classes
are covered; illiquid/private classes are inherently non-real-time; FX, bonds, and
full macro remain to be wired.

## Confirmed deficiencies (the explicit ask)

1. **Predictive validity unproven (H5).** Back-test IC is weak/insignificant; the
   proprietary score still needs a defined formula and an outcome-validated study.
2. **Score formula undefined.** Only a transparent proxy exists; the marketed score
   has no published, testable definition.
3. **No representative adoption dataset.** Metrics run on test accounts; no real
   funnel, retention/NRR, or willingness-to-pay.
4. **Acquisition labels are synthetic.** No expert-underwriter ground truth or
   inter-rater reliability; no document-level QoE/fraud modeling.
5. **Asset-class data gaps.** FX, corporate/muni bonds, full macro (FRED) not wired;
   direct real estate, private businesses, and PE are inherently non-real-time.
6. **Operational hardening pending.** Dev token signing, SQLite default, and rate
   limits/keys for providers (per `backend/README.md`).

## Net effect on the thesis

Design-level problem–solution fit remains **confirmed**. With live data wired and
the studies runnable, the thesis gains **partial market evidence** (working data
pipeline + a runnable, honest evaluation harness), but **market-level
problem-solving is not yet confirmed**: it requires a defined, outcome-validated
score and representative usage/expert datasets. The deficiencies above are the
concrete backlog to close that gap.
