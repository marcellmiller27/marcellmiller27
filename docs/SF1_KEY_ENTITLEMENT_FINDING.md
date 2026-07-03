# SF1 Key Review & Entitlement Finding (2026-06-30)

Review of the NASDAQ secrets placed by the founder, and what they unlock for H5 validation.

## Secrets reviewed
Two secrets are injected and **both authenticate** against the live Nasdaq Data Link SF1 API:
- **`NASDAQ_MY_API_KEY`** — standard key format; authenticates (HTTP 200). **Primary.**
- **`NASDAQ_PYTHON`** — also authenticates; only one key is actually needed.

## Code fixes applied (so the platform uses these keys)
1. **Key-name recognition:** `nasdaq_data_link_api_key()` now also reads `NASDAQ_MY_API_KEY`
   and `NASDAQ_PYTHON` (in addition to `NASDAQ_DATA_LINK_API_KEY` / `FUNDAMENTALS_API_KEY`).
   → `/research/fundamentals-status` now reports `available: true`.
2. **Adapter URL bug:** the SF1 datatables call was missing the required `.json` format
   suffix (`/SHARADAR/SF1` → `/SHARADAR/SF1.json`). Fixed — the adapter now returns real
   data (verified: AAPL revenue $383B, EPS 6.16, PE 27.6, ROE 1.61).

## ⚠️ Entitlement finding — this key is the FREE SAMPLE, not full/paid SF1
Enumerating what the key can actually pull from `SHARADAR/SF1`:

| Attribute | This key returns | What H5 validation needs |
| --- | --- | --- |
| Rows accessible | **60** | ~hundreds of thousands |
| Distinct tickers | **30** (current mega-caps: AAPL, MSFT, XOM, …) | ~16,000 (survivorship-free) |
| Dimensions | **MRY only** (Most-Recent **restated** annual) | **As-Reported ARQ/ART/ARY** (point-in-time) |
| History (datekey) | **~2022-05 → 2024-01** (~2 annual points/ticker) | ~20+ years |
| Survivorship | current survivors only | delisted included |

**Why this can't validate H5 (blunt):**
- **Not point-in-time.** Only `MRY` (restated) is accessible — that bakes in **look-ahead
  bias**. The As-Reported dimensions (`ARQ/ART/ARY`) needed for honest PIT factors return
  **0 rows** on this key.
- **Not enough data.** 30 survivor tickers × ~2 annual points = **60 rows** — statistically
  meaningless for a factor back-test (and survivorship-biased).

**Conclusion:** validation is **blocked on data entitlement, not code.** The code is now
ready; the current key is the free sample.

## What unlocks the real validation
The **paid Sharadar SF1 subscription** (the **single-user/developer** license is sufficient
for R&D — see `docs/FUNDAMENTALS_DATA_VENDORS.md`) unlocks:
- **As-Reported** dimensions (`ARQ/ART/ARY`) → true point-in-time, no look-ahead.
- **~20 years** of history, quarterly.
- **~16k companies**, survivorship-bias-free (active + delisted).

## Next steps
1. **Founder:** on the Nasdaq Data Link / Sharadar account, **subscribe to the paid SF1**
   (single-user/developer) so the key gains As-Reported + full history. Keep the same secret
   name; no code change needed.
2. **Cy (once paid SF1 is active):** build the PIT fundamentals integration (value/quality/
   growth from As-Reported, aligned on `datekey`), fold into the costed OOS back-test, and
   report an honest PASS/FAIL vs the pre-registered **|t| ≥ 2.0** bar
   (`docs/RND_VALIDATION_PROTOCOL.md`).

> Good news: the plumbing is proven end-to-end on real SF1 responses — we're one dataset
> upgrade away from the real run.

## Readiness built (2026-07-02) — for the 5-day eval
To execute immediately when full-data (As-Reported + history) access is granted:
- **`market_services.sharadar_sf1_history(ticker, dimension)`** — pulls all SF1 rows for a
  ticker, sorted by `datekey` (verified live against the sample).
- **`app/fundamentals.py`** — pure, unit-tested PIT factor computation
  (`pit_fundamental_factors`): value (earnings yield, book/price), quality (ROE, net
  margin), growth (revenue/EPS YoY), with a strict **no-look-ahead** cutoff (`datekey <=
  as_of`). 6 unit tests + verified on a real SF1 sample row.
- **Remaining step (during eval):** wire these factors into the costed OOS backtest
  (`equity_oos_backtest`) alongside price factors, run over full history, report PASS/FAIL
  vs **|t| ≥ 2.0**. Kept for the eval so it's built against real full-data shapes.

**5-day-eval prerequisites to confirm in the contract:** (1) the eval exposes the **full**
dataset (As-Reported ARQ/ART/ARY + ~20yr + full universe), not the sample; (2) exact
**$0 cancellation** mechanic within 5 days (and whether it auto-renews into the $18k/yr).
