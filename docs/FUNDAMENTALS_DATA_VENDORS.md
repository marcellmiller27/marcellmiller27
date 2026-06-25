# Licensed Point-in-Time Fundamentals — Definitions, Vendors, Integration Plan

This is the data-procurement guide for closing H5 (Opportunity Score predictive
validity). It defines the required data, ranks the top vendors, and specifies how
the platform will consume the API key once purchased.

## Definitions

- **Point-in-time (PIT) fundamentals.** Data stored *as it was actually known on
  each historical date* — original/unrestated filings tagged with their real
  report and effective dates. A back-test only uses information available at that
  moment, removing **look-ahead bias** (using later restatements) and **filing-lag
  bias** (using figures before they were public). Must also be
  **survivorship-bias-free** (include delisted/bankrupt names).
- **Larger/longer sample (power target).** Breadth **≥1,000–3,000 names**
  (e.g., Russell 3000 / global developed) and **≥20 years** of monthly history,
  survivorship-bias-free. Power scales with breadth × periods, so an IC ≈ 0.03–0.04
  (already observed) would clear **|t| ≥ 2.0** at this depth (vs t = 0.87 on the
  free 30-name / 44-month sample).
- **Fundamentals-data API key.** Authenticated credential for programmatic
  (REST/bulk) access to a vendor's PIT fundamentals, tiered by coverage/history.

## Top five providers (point-in-time fundamentals)

| # | Provider | PIT dataset | Access | Coverage / history | Tier |
| --- | --- | --- | --- | --- | --- |
| 1 | **S&P Global Market Intelligence** | Compustat Point-in-Time (Snapshot) | S&P APIs / WRDS | US ~1980s+, global; gold standard | Enterprise |
| 2 | **FactSet** | Fundamentals (PIT / as-reported) + estimates | FactSet API | Global, deep | Enterprise |
| 3 | **LSEG / Refinitiv** | Worldscope + I/B/E/S (point-in-time) | Refinitiv Data Platform / Datastream | Global | Enterprise |
| 4 | **Bloomberg** | Data License PIT fundamentals (BLPAPI) | Terminal / Data License | Global | Enterprise |
| 5 | **Nasdaq Data Link — Sharadar (SF1)** | Core US Fundamentals, true PIT, survivorship-free | Simple REST API | ~5,000+ US equities, ~20y | **Affordable / self-serve** |

**Affordable API-first runners-up:** Tiingo Fundamentals, Financial Modeling Prep
(FMP), Intrinio, EOD Historical Data (EODHD).

## Recommendation

- **Highest accuracy:** Compustat PIT (#1) — enterprise contract.
- **Best practical buy-now choice:** **Sharadar SF1 via Nasdaq Data Link** (#5) —
  genuinely PIT, survivorship-bias-free, self-serve API key, integrates fastest.

## Integration plan (after purchase)

1. Add the key in the **Secrets** panel. Default env vars the adapter will read:
   `FUNDAMENTALS_VENDOR` (e.g., `sharadar`) and `FUNDAMENTALS_API_KEY`
   (Sharadar/Nasdaq Data Link may also use `NASDAQ_DATA_LINK_API_KEY`).
2. Implement a PIT fundamentals adapter feeding value (E/P, B/P), quality (ROE,
   margins, low accruals), and growth factors into `opportunity_score.py`
   (`/research/fundamentals-status` flips to `available`).
3. Expand the universe + history to the vendor's survivorship-bias-free coverage.
4. Re-run the equity-only, **costed, out-of-sample** protocol
   (`/research/equity-oos-backtest`) and report honestly against a **|t| ≥ 2.0** bar.
