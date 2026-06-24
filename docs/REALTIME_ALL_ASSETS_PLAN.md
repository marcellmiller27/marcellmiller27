# Real-Time Live Feeds Across All Market Asset Classes — Solution, Issues, Corrective Actions

This document describes the implemented solution to extend real-time market data
to (effectively) all world-class asset classes, the **issues** that remain, and the
**corrective actions** an AI agent should take to get each one fully working.

Endpoints: `GET /api/v1/market/quotes`, `/market/providers`, `/market/symbols`,
`/market/inflation`, and `GET /api/v1/research/data-coverage`.

## What is now live (real-time, no credentials required)

| Asset class | Symbols | Provider |
| --- | --- | --- |
| Crypto | BTC, ETH, XRP, XLM, SOL | CoinGecko |
| Equities | any ticker (AAPL, …) | Yahoo Finance |
| Equity indices | SPX, DJIA, NASDAQ | Yahoo Finance |
| Commodities | GOLD, OIL | Yahoo Finance |
| **Treasury yield curve** | UST3M, UST5Y, UST10Y, UST30Y | Yahoo Finance |
| **FX / currencies** | EURUSD, GBPUSD, USDJPY, DXY | Yahoo Finance |
| **Fixed income (proxies)** | BOND_AGG, BOND_IG, BOND_HY, BOND_MUNI, BOND_TIPS | Yahoo Finance |
| **Private-equity proxy** | PE_PROXY (PSP) | Yahoo Finance |
| **SMB / small-cap proxy** | SMB_PROXY (IWM) | Yahoo Finance |
| Inflation | INFLATION (CPI YoY) | US BLS |
| Real estate (proxy) | REIT (VNQ) | Yahoo Finance |

## What is implemented but credential-gated

| Asset class | Symbols | Provider | Activation |
| --- | --- | --- | --- |
| Full macro | M2, GDP, UNEMPLOYMENT | FRED | set `FRED_API_KEY` |

The FRED adapter is fully coded; without the key these symbols return
`status: "unavailable"` with a note, and `/market/providers` reports FRED as
`requires_credentials` (graceful, non-breaking).

## Issues and corrective actions (for the AI agent)

1. **Macro (M2/GDP/unemployment) needs a key.**
   - *Issue:* FRED requires `FRED_API_KEY`; not set in this environment.
   - *Corrective action:* add the `FRED_API_KEY` secret. No code change needed — the
     adapter activates automatically and `data-coverage` flips this row to `live`.

2. **Direct fixed-income (CUSIP-level) pricing is not real-time.**
   - *Issue:* only liquid ETF proxies (AGG/LQD/HYG/MUB/TIP) are live; individual
     bond pricing requires a licensed vendor.
   - *Corrective action:* add a licensed fixed-income adapter (e.g., a quotes vendor
     with bond coverage) keyed by env var; map a `bond` provider in
     `MarketDataService._quote_for`.

3. **Yahoo Finance is an unofficial endpoint (ToS + reliability risk).**
   - *Issue:* no SLA; may rate-limit, change shape, or require a crumb/cookie.
   - *Corrective action (partly done):* host failover across `query1`/`query2` and a
     60s cache are implemented. For production, add a **licensed vendor**
     (Polygon.io / Twelve Data / Finnhub / Tiingo) adapter and switch the equity/
     index/FX/commodity providers to it; keep Yahoo as fallback.

4. **Direct (per-property) real estate is not a live quote.**
   - *Issue:* illiquid; only a REIT/ETF proxy is live.
   - *Corrective action:* integrate an AVM/appraisal data API for per-property
     estimates; treat as a modeled estimate, clearly labeled, not a market quote.

5. **Private businesses / private equity have no public price.**
   - *Issue:* specific SMBs/PE positions are valued by model/marks, not quotes.
   - *Corrective action:* keep the live public proxies (IWM/PSP) for sentiment, and
     use the acquisition/diligence engine for deal-specific valuation; ingest GP
     capital-account statements for actual PE marks.

6. **Bloomberg / TradingView are not usable as programmatic feeds here.**
   - *Issue:* Bloomberg needs a paid Data License/BLPAPI entitlement; TradingView
     has no official public data API (widgets only).
   - *Corrective action:* only integrate Bloomberg behind provisioned credentials;
     prefer a licensed quotes vendor for programmatic data.

7. **Opportunity Score predictive validity is unproven.**
   - *Issue:* the back-test signal is weak/insignificant (separate from feeds).
   - *Corrective action:* define a score formula and outcome-validate it to a
     pre-registered information-coefficient floor (thesis H5).

## Robustness already built in

- **Host failover** for Yahoo (`query1` → `query2`).
- **60s TTL cache** per provider call; crypto batched into one CoinGecko request.
- **Per-symbol graceful degradation:** any provider/network failure yields
  `status: "unavailable"` with a note instead of failing the whole response.
- **Credential-gated providers** advertise themselves via `/market/providers` so an
  operator/agent can see exactly what is `live` vs `requires_credentials`.

## How to verify

```bash
curl "$API/market/quotes?symbols=EURUSD,DXY,UST3M,UST5Y,BOND_AGG,BOND_HY,PE_PROXY,SMB_PROXY"
curl "$API/market/quotes?symbols=M2,GDP,UNEMPLOYMENT"   # unavailable until FRED_API_KEY is set
curl "$API/market/providers"
curl "$API/research/data-coverage"
```
