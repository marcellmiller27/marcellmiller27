# H5 Validation — Status & Live Baseline

> Tracks the proof-of-concept validation of the John Henry Opportunity Score (H5:
> predictive validity). Protocol + bars: `docs/RND_VALIDATION_PROTOCOL.md`.

## Live baseline run — 2026-06-30 (price factors only)

Ran the equity-only, costed, **out-of-sample** backtest **live** (Yahoo price data; no SF1
key required for this run) to prove the validation harness end-to-end.

| Metric | Value |
| --- | --- |
| Universe | 30 US equities |
| In-sample / OOS periods | 64 / 44 months |
| Factor weights (learned in-sample, frozen) | momentum 0.425, trend 0.575, low-vol 0.0, reversal 0.0 |
| **OOS mean IC** | **0.041** |
| **OOS IC t-stat** | **0.98** |
| OOS hit-rate | 63.6% |
| Net annualized long–short (after costs) | +5.4% |
| Avg monthly turnover | 0.45 |
| Pass criteria | mean IC ≥ 0.02 AND \|t\| ≥ 1.5 AND net L/S > 0 |
| **Result** | **H5 = FAIL (price factors only)** |

**Read:** the harness works and produces honest, costed OOS numbers. Price factors alone
are **not** statistically significant (t 0.98 < the 1.5 bar; pre-registered target is the
stricter **\|t\| ≥ 2.0**). This is expected — it's the reason for adding **SF1
point-in-time fundamentals** (value/quality/growth).

## Key status

- `NASDAQ_DATA_LINK_API_KEY` was **provided** by the founder in Secrets. ✅
- It is **not injected into the session that ran the baseline** (secrets inject into a
  **new** Cloud Agent VM). A **fresh agent run** will expose the key, after which the live
  SF1 path runs. Network to `data.nasdaq.com` is reachable (verified).

## Next-session run plan (with the SF1 key live)

1. Confirm `NASDAQ_DATA_LINK_API_KEY` is present in the new session (`/research/fundamentals-status` → `available: true`).
2. Build the **PIT fundamentals integration**: pull SF1 **As-Reported** (`ARQ/ART/ARY`)
   aligned on **`datekey`** (no look-ahead); compute **value** (E/P, B/P), **quality**
   (ROE, margins, low accruals), **growth** (revenue/earnings YoY) factors.
3. Fold fundamentals into the costed OOS backtest alongside the price factors.
4. Re-run and report an honest **PASS/FAIL vs. the pre-registered \|t\| ≥ 2.0** bar, with
   robustness across subperiods/sectors.
5. If it passes → proof of concept confirmed (then entity formation per
   `docs/TODO_NEXT_SESSION.md` §6). If it fails → disciplined, limited iteration; report honestly.

> Honest note: a one-week pre-registered backtest is **historical evidence**, not a live
> track record or "proven alpha." Position outputs as **research/insight**, not advice.
