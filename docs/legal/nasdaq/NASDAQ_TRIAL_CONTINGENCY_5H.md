# NASDAQ 5-Day Trial — Line-Item 5h Contingency & Back-up Plan

> JHI-SIG: 69M2705M · JHI Research & Analytics Firm, Inc. (proprietary)
> Contingency of record for the NASDAQ (Nasdaq Data Link / Sharadar SF1) engagement.
> **Not legal advice.** Companions: `FOUNDER_RESOLUTION_2026-07-20.md`,
> `DATA_LICENSE_TERMS_REVIEW.md`; vendors: `../../FUNDAMENTALS_DATA_VENDORS.md`,
> `../../MARKET_DATA_VENDOR_COMPARISON.md`.

## The rule (Founder directive, 2026-07-20)
- There is a **5-day trial** window on the NASDAQ engagement.
- During it we must **validate line-item 5h**.
- **If 5h is NOT validated by the end of the trial, we immediately refute/decline the MSA** and **move forward without NASDAQ** — using the back-up below.
- Regardless of vendor, the firm's binding commitment stands: **no data-set spillage** (licensed data isolated + server-side; derived-only outputs).

## Line-item 5h — validation criteria (TO CONFIRM from the uploaded Order Form)
> Placeholder until the Founder uploads the new Order Form. Once uploaded, this
> section states, in one line, **what 5h grants/guarantees** and the **objective
> pass/fail test** we run during the trial (e.g., a specific data right, coverage
> guarantee, or delivery capability). Fill:
- **What 5h grants:** _[to confirm]_
- **Pass test (must be true by day 5):** _[to confirm]_
- **Owner of the check:** Founder + Cy · **Deadline:** end of 5-day trial.

## Back-up plan (executes if 5h fails)
NASDAQ Data Link hosts **Sharadar SF1** (point-in-time US fundamentals). If we walk,
we replace *that capability*, not the whole platform. Already-vetted, API-first,
self-serve alternatives (from `../../FUNDAMENTALS_DATA_VENDORS.md`):

| Priority | Replacement | Replaces | Notes |
| --- | --- | --- | --- |
| 1 | **Financial Modeling Prep (FMP)** | SF1 PIT fundamentals | Broad US coverage, cheap, REST; confirm PIT + commercial/external-distribution tier in writing |
| 2 | **Tiingo Fundamentals** | SF1 PIT fundamentals | Affordable, clean API; verify history depth + redistribution rights |
| 3 | **Intrinio** | SF1 PIT fundamentals | Granular entitlements; commercial tier required for SaaS |
| 4 | **EOD Historical Data (EODHD)** | Fundamentals + EOD prices | Global, low cost; check as-reported/PIT depth |
| — | **SEC EDGAR (free)** | As-reported filings/financials | Already integrated (`edgar` router); zero-license fallback for public-company depth — bridges gaps while a paid vendor is onboarded |

Enterprise gold-standard (Compustat PIT / FactSet / Refinitiv / Bloomberg) remain
future options only when revenue justifies; not the trial back-up.

**Market-data (non-fundamentals) back-up** is separate and already tracked in
`../../MARKET_DATA_VENDOR_COMPARISON.md`: Twelve Data (pending terms), Polygon, EODHD;
free Yahoo/CoinGecko/FRED/BLS remain the prototype surface.

## The commercial-tier trap (applies to every replacement)
Every vendor's retail/personal tier is **internal-use-only**. Before committing to any
back-up we must confirm **in writing** that the plan grants **external distribution of
our derived analytics** to subscribers (+ end-user cap + any exchange fees). This is the
same gate that governs NASDAQ — do not assume the sticker price includes SaaS rights.

## Switch mechanics (low lock-in by design)
- Fundamentals/market access already sits behind service layers in the backend; a
  replacement is a **new adapter + API key (via Secrets)**, not a rewrite.
- Keep the integration **vendor-agnostic** so swapping SF1 → FMP/Tiingo/etc. is
  configuration, not surgery.
- Preserve **data-set isolation**: whichever licensed set we use stays server-side and
  never commingles into a repurposed third-party set.

## Decision record
- **Trigger:** 5h not validated within the 5-day trial → **refute MSA, execute back-up.**
- **Default back-up:** FMP (1) with **EDGAR** covering public-company depth immediately at zero license cost.
- **Owner:** Founder (go/no-go) · **Build:** Cy (adapter + key wiring on decision).

**Recorded by:** Cy Henry (VP, Software Engineering — AI teammate) · signature `69M2705M`.
