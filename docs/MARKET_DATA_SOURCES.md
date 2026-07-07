# Market Data Sources

Real, live market data is served from `GET /api/v1/market/quotes` and related
endpoints (`backend/app/routers/market.py`, `backend/app/market_services.py`).
Implementation uses only the Python standard library (`urllib`) — no new runtime
dependency — with a short in-memory TTL cache and per-symbol graceful fallback.

## Endpoints (public)

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/market/quotes?symbols=BTC,ETH,GOLD,SPX,UST10Y,INFLATION` | Live quotes. Omit `symbols` for the default dashboard set. |
| `GET` | `/api/v1/market/inflation` | Latest US CPI year-over-year. |
| `GET` | `/api/v1/market/providers` | Provider catalog + status. |
| `GET` | `/api/v1/market/symbols` | Symbol catalog + default set. |

Each quote includes `price`, `currency`, `unit`, `change_percent`, `source`,
`as_of`, and a `status` (`ok` / `unavailable`) so the caller can detect a degraded
provider without the whole request failing.

## Providers

| Provider | Asset classes | Key? | Status | Notes |
| --- | --- | --- | --- | --- |
| **CoinGecko** | crypto | no | live | `simple/price` — spot USD + 24h change (BTC, ETH, XRP, XLM, SOL). |
| **Yahoo Finance** | indices, equities, commodities, treasury yields, REIT | no | live | `v8/finance/chart` — last price + previous close for % change (e.g. `^GSPC`, `GC=F`, `^TNX`, `VNQ`, any ticker). |
| **US BLS** | macro / inflation | no | live | CPI series `CUUR0000SA0`; YoY computed from index levels. (Higher limits with a BLS/FRED key.) |
| **Bloomberg** | broad | yes | requires_credentials | Needs a paid Data License / BLPAPI entitlement + `blpapi` SDK. Adapter slot reserved. |
| **TradingView** | — | — | unsupported | No official public market-data REST API (widgets only). Use a licensed quotes vendor for programmatic data. |

### Why Bloomberg/TradingView are not live
Both are intentionally **not** wired up: Bloomberg data requires paid entitlements
and the proprietary BLPAPI; TradingView offers embeddable widgets but no licensed
public data API. The provider registry advertises them so an adapter can be added
once credentials exist, without changing the endpoint contract.

## Symbols

Friendly symbols (with aliases) resolve to a provider + provider symbol; unknown
symbols fall back to a Yahoo **equity** lookup (so `AAPL`, `TSLA`, etc. work).
Defaults mirror the dashboard widgets: `BTC, ETH, GOLD, SPX, UST10Y, INFLATION`.
See `SYMBOLS` in `backend/app/market_services.py` for the full registry.

## Caching & resilience

- 60-second in-memory TTL cache per provider call (configurable via
  `MarketDataService(cache_ttl=...)`; `0` disables caching, used in tests).
- Crypto symbols are batched into a single CoinGecko request.
- Network/parse errors are normalized to `ProviderError`; the affected symbol is
  returned with `status = "unavailable"` and a note — the endpoint never 500s on a
  provider outage.

## Extending

- **More symbols:** add a `SymbolSpec` to `SYMBOLS`.
- **A new provider (e.g., Bloomberg/FRED/a licensed vendor):** add a module-level
  `fetch_*` function and a branch in `MarketDataService._quote_for`, then flip its
  `ProviderInfo.status` to `live`.
- **Frontend:** the dashboard can now replace its static `marketSignals`
  (`src/lib/platform-data.ts`) by polling `/api/v1/market/quotes` for genuine
  real-time updates.
