# Twelve Data — Leverage Playbook (License-Safe Design)

How JHI uses the Twelve Data feed across **reports, newsletters, analytics, and
Excel** while staying inside the **Venture ($499/mo)** license. Companion to
`docs/MARKET_DATA_VENDOR_COMPARISON.md` and `docs/PRICING_BILLING_SCHEMA.md`.

## Confirmed license boundary (Twelve Data, 2026-07-15)
Confirmed by Twelve Data (Liam) via email:
- ✅ Exporting **derived** metrics/scores to client **Excel / PDF** — permitted.
- ✅ **Derived-content newsletters** with attribution — permitted.
- ⛔ **Raw-series export/feed** to clients — requires **distribution rights** (not Venture).

Prior confirmations:
- ✅ **No restrictions** on derived metrics, scores, rankings, or AI-generated insights.
- ✅ **Display** raw data in-app — permitted.
- ⛔ **Redistribution via our own API** (raw feed to clients) — not permitted on Venture.
- 💵 **Flat pricing** (~$499/mo, ~$414/mo annual) — not per-end-user; scales to 100k+ subscribers at the same fee.

## The one rule: "Derive, then serve"
> Anything a client can **download, keep, or receive** (report, newsletter, Excel,
> client API) must carry **DERIVED** outputs. **RAW** Twelve Data stays in the
> **in-app display layer** (ephemeral render) only.

Follow this one rule and every channel below is clean on Venture.

## Per-channel: GREEN (Venture) vs GATED (needs distribution/Enterprise)
| Channel | ✅ GREEN on Venture | ⛔ GATED (needs distribution rights) |
|---|---|---|
| In-app analytics / dashboards / ticker | Display raw **and** derived | — |
| Reports (PDF / in-app) | Derived metrics, scores, valuations, charts-as-images | Raw price/history **tables** a client extracts |
| Newsletters | Derived commentary, scores, rankings, "movers" summaries + **attribution** | Mass republication of raw quote tables/feeds |
| Excel workbooks | Derived analytics, models, computed benchmarks/multiples | Raw-series dumps; live `=TWELVEDATA()` / client-side pulls |
| Client-facing API | Our **derived** outputs (e.g., Opportunity Score) | Raw Twelve Data quotes/feed |

## Attribution
Show **"Powered by Twelve Data"** where raw data is displayed and per their terms.

## Architecture — the "display boundary"
```
Twelve Data (raw) ─► server-side compute (cached ~60s) ─► DERIVED outputs
                                                          │
   in-app DISPLAY only ◄─ raw (ephemeral render) ────────┤
                                                          ▼
        reports · newsletters · Excel · client API  = DERIVED only
```
No client-facing raw-data API; no raw-series file exports (from Twelve Data).

## Free-source complement (for raw exports clients want)
Where a client genuinely needs **raw series in a file**, source it from
**redistribution-cleared public data** — **FRED** (macro), **SEC EDGAR** (filings),
**Treasury/BLS/BEA** — which are public-domain and freely exportable. Reserve
Twelve Data for **in-app display + derived** intelligence. See
`public/downloads/JHI_Data_Sources_Comparison.xlsx`.

## Monetization
- **Derived report packs** and **Excel analysis workbooks** become Professional/
  Enterprise deliverables (add-on revenue) — high value, near-zero marginal cost.
- **Newsletters** drive top-of-funnel (Consumer) and cross-tier retention.
- Twelve Data is a **flat ~$5k/yr** cost → keeps blended gross margin ~90%+.

## When to upgrade to Enterprise / distribution
Only if **raw-series exports or a client data feed** become a real revenue driver.
Until then, Venture + the derive-then-serve rule covers reports, newsletters,
analytics, and Excel at the lowest cost.
