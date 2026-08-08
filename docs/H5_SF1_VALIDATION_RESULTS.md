# H5 Validation — SF1 Fundamental-Factor Opportunity Score

**Verdict: FAIL (out-of-sample), narrow miss on the t-stat.** Honest result reported
against a pre-registered bar; no configuration was tuned to the outcome.

This is the FUNDAMENTAL-factor follow-up to the prior **price-only** H5 run, which
FAILED (mean IC 0.0074, t 0.25, hit 50.9%; see `docs/H5_GAP_CLOSURE_RESULTS.md`). That
run's stated fix was to add point-in-time value/quality/growth fundamentals on
equities. This study does exactly that using Sharadar SF1 (Nasdaq Data Link), and
measures it against the **same pre-registered bar**.

> **Trial-deadline context.** The Nasdaq Data Link 5-day trial ends **Sunday**, which
> forces a keep/cancel decision on the MSA. On the strength of the SF1 fundamentals
> signal shown below, this study gives the founder a defensible, honest read within the
> window. The decisive out-of-sample result is **FAIL**, so **Nasdaq line-item 5h is NOT
> validated** — but the signal is materially stronger than the price-only model and
> misses only the significance (t-stat) leg, which informs the decision (see
> "Decision implication" below).

Internal R&D only. Raw SF1 rows are LICENSED and stay internal (gitignored cache);
this document and all outputs surface **derived metrics only** (governance mandate).

---

## Pre-registered design (fixed BEFORE reading any results)

**Success bar (unchanged, pre-registered, evaluated out-of-sample):**

> **mean information coefficient ≥ 0.03 AND |t-stat of the IC series| ≥ 2.0 AND hit
> rate ≥ 0.55**

**Factor set + weights (declared up front, never tuned to results):**

| Block | Weight | Factors (equal within block) |
| --- | --- | --- |
| Value | 0.40 | `earnings_yield` (E/P), `book_yield` (B/P), `fcf_yield` (FCF/P) — 0.1333 each |
| Quality | 0.35 | `roe`, `operating_margin`, `net_margin` — 0.1167 each |
| Growth | 0.25 | `revenue_cagr` (trailing, up to 5 point-in-time fiscal years) |

All factors are oriented "higher = more attractive" (cheaper / higher quality / faster
growth). At each rebalance date the raw factors are cross-sectionally z-scored,
**winsorized to ±3 SD** (pre-registered, to bound negative-book-value large-caps), then
weighted and summed into a composite. Higher composite = higher Opportunity Score.

**Universe:** `equity_opportunity_scan.LARGE_MID_CAP_UNIVERSE` — **41** large/mid-cap US
equities across sectors. Curated (survivorship-aware; not fully survivorship-bias-free —
this biases results *upward*, yet the study still fails the bar).

**Panel / method:**

- **Point-in-time, no look-ahead:** at rebalance date `d`, a name may only use SF1
  annual rows whose `datekey` (SEC filing date) is `≤ d`. SF1 `ARY` is as-first-reported,
  so there is no restatement bias. Market cap = **rebalance-date** price (Yahoo) × PIT
  basic shares — never SF1's stale as-of-filing price.
- **Rebalance:** monthly. **Forward return:** next-month Yahoo close-to-close.
- **IC:** per-period Spearman rank correlation of composite vs forward return.
- **Long-short:** top-tercile minus bottom-tercile monthly return, annualized ×12,
  **net of 10 bps/side** costs via portfolio turnover (reuses the price-only harness
  machinery in `app/research_services.py`).
- **Out-of-sample:** history split in half chronologically; the **second half is the
  decisive OOS window**. A **recent-third holdout** is also reported.
- **Window:** 2006-09 → 2026-08 (240 evaluable months; SF1 availability gates early
  cross-sections, e.g. META from 2013, V from 2007).

Reproduce: `/.venv/bin/python backend/scripts/run_h5_sf1_validation.py`
(or `GET /api/v1/research/sf1-factor-backtest`). Requires `NASDAQ_DATA_LINK_API_KEY`.

---

## Results (live run, 2026-08-08)

| Segment | Months | Mean IC | IC t-stat | Hit rate | Gross ann. L/S | Net ann. L/S | Turnover | H5? |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| Full sample | 240 | 0.0108 | 0.78 | 52.1% | +1.9% | +1.6% | 0.117 | **FAIL** |
| In-sample (first half) | 120 | −0.0160 | −0.87 | 47.5% | −3.3% | −3.6% | 0.126 | **FAIL** |
| **Out-of-sample (second half)** | 120 | **0.0377** | **1.82** | **56.7%** | **+7.1%** | **+6.8%** | 0.115 | **FAIL** |
| Recent-third holdout | 80 | 0.0311 | 1.22 | 57.5% | +6.2% | +5.9% | 0.126 | **FAIL** |

**Decisive out-of-sample verdict: FAIL** (`h5_pass = false`).

### Bar-by-bar (out-of-sample, the decisive window)

| Criterion | Bar | OOS value | Pass? |
| --- | --- | --- | :---: |
| Mean IC | ≥ 0.03 | 0.0377 | ✅ |
| \|IC t-stat\| | ≥ 2.0 | 1.82 | ❌ |
| Hit rate | ≥ 0.55 | 56.7% | ✅ |

The out-of-sample score clears **two of the three** legs (mean IC and hit rate) but
**misses statistical significance**: t-stat 1.82 < 2.0. Because the bar is a conjunction
(all three must hold), the honest verdict is **FAIL**.

---

## Honest interpretation and limitations

- **Real improvement over price-only, but not enough.** Out-of-sample, fundamentals lift
  mean IC ~5× (0.0377 vs 0.0074) and hit rate to 56.7% (vs 50.9%), with a **+6.8%
  net-of-cost** annualized long-short. The fundamental signal is economically meaningful
  and directionally right — it just isn't statistically decisive at |t| ≥ 2.0 on this
  universe/window.
- **Regime dependence is the core weakness.** The **first-half (in-sample) IC is
  negative** (−0.0160), while the second half is positive. A factor whose sign flips
  across regimes cannot be declared validated. We deliberately did **not** relabel the
  favorable (recent) window as "in-sample" to manufacture a pass — that would be fishing.
- **Full-sample fails clearly** (mean IC 0.0108, t 0.78): averaging the negative early
  regime with the positive later one washes out the signal.
- **Survivorship works in our favor and it still fails.** The universe is today's
  large-caps, which biases returns *upward*; a clean, delisting-inclusive universe would
  likely be weaker, not stronger. This makes the FAIL more, not less, credible.
- **Other caveats:** single price vendor (Yahoo); no sector/beta neutralization; simple
  turnover-based cost model; small mega-cap cross-section (~41 names) limits the power of
  the t-stat, so a true signal of this size is hard to certify significant here.

## Decision implication (Nasdaq trial, due Sunday)

- **5h is NOT validated** by the pre-registered bar. If the keep/cancel decision hinges
  strictly on a passing H5, the honest input is **FAIL**.
- However, SF1 fundamentals are the **first inputs to clear even part** of the bar
  out-of-sample (mean IC and hit rate), a clear step up from the price-only failure.
  The residual gap is **significance/robustness**, not direction. If the founder values
  the fundamentals data pipeline (the equity Opportunity Scan already depends on SF1)
  and a credible research path to close the last leg, that is a rational reason to keep;
  if the criterion is a clean H5 PASS *now*, cancel is defensible.

## Next research iteration (to actually close H5 — no shortcuts)

1. **Widen the cross-section** to a survivorship-bias-free ~200–500 name universe (more
   names per period is the most direct way to raise the IC t-stat if the signal is real).
2. **Neutralize sector/size** before scoring (the mega-cap sample conflates factor and
   sector bets).
3. **Add the pre-registered-but-omitted quality leg** (low accruals) and consider EPS
   growth alongside revenue CAGR; keep weights fixed in advance.
4. **Blend fundamentals with the price momentum factor** (the two are complementary) and
   re-pre-register the combined bar.
5. Re-run the identical PIT/OOS protocol; report PASS/FAIL as-is.

_JHI-SIG: 69M2705M · JHI Research & Analytics Firm, Inc. (Aegira platform) · internal R&D · not investment advice._
