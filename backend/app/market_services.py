"""Real market-data integration.

Providers (free / no-key, stdlib-only HTTP):
  - CoinGecko       -> crypto spot prices + 24h change
  - Yahoo Finance   -> equities, indices, commodities, treasury yields, REIT proxy
  - US BLS          -> CPI inflation series (year-over-year)

Bloomberg and TradingView are intentionally NOT live: Bloomberg requires a paid
Data License / BLPAPI entitlement, and TradingView exposes no official public data
API. They are advertised by ``providers()`` as ``requires_credentials`` /
``unsupported`` so an adapter can be slotted in when access exists.

Design notes:
  - Pure standard library (``urllib``) — no new runtime dependency.
  - Short TTL in-memory cache to respect provider rate limits and smooth latency.
  - Per-symbol resilience: a provider/network failure marks that symbol
    ``unavailable`` (with a note) instead of failing the whole response.
"""

from __future__ import annotations

import json
import os
import threading
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable

from app.market_models import (
    InflationResponse,
    ProviderInfo,
    ProvidersResponse,
    Quote,
    QuotesResponse,
    SymbolInfo,
    SymbolsResponse,
)

USER_AGENT = "JohnHenryInvestments/1.0 (+market-data)"
HTTP_TIMEOUT = 6.0
CACHE_TTL_SECONDS = 60
CPI_SERIES_ID = "CUUR0000SA0"  # CPI-U, US city average, all items, NSA
YAHOO_HOSTS = ("query1.finance.yahoo.com", "query2.finance.yahoo.com")


def fred_api_key() -> str | None:
    return os.getenv("FRED_API_KEY")


def twelvedata_api_key() -> str | None:
    """Licensed-vendor API key (Twelve Data). When set, it becomes the primary
    quote source for equities/FX with Yahoo as fallback."""
    return os.getenv("TWELVEDATA_API_KEY")


def nasdaq_data_link_api_key() -> str | None:
    """Point-in-time fundamentals key (Nasdaq Data Link / Sharadar SF1)."""
    return os.getenv("NASDAQ_DATA_LINK_API_KEY") or os.getenv("FUNDAMENTALS_API_KEY")


def bls_api_key() -> str | None:
    """BLS registration key. When set, unlocks the v2 API (higher daily limits,
    more series per request, longer history). Keyless falls back to v1."""
    return os.getenv("BLS_API_KEY") or os.getenv("BLS_REGISTRATION_KEY")


class ProviderError(RuntimeError):
    """A market-data provider call failed."""


# --------------------------------------------------------------------------- #
# Symbol registry
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class SymbolSpec:
    symbol: str
    name: str
    provider: str
    provider_symbol: str
    asset_class: str
    unit: str
    aliases: tuple[str, ...] = field(default_factory=tuple)
    vendor_symbol: str | None = None  # symbol form for the licensed vendor (Twelve Data)


SYMBOLS: list[SymbolSpec] = [
    SymbolSpec("BTC", "Bitcoin", "coingecko", "bitcoin", "crypto", "USD"),
    SymbolSpec("ETH", "Ethereum", "coingecko", "ethereum", "crypto", "USD"),
    SymbolSpec("XRP", "XRP", "coingecko", "ripple", "crypto", "USD"),
    SymbolSpec("XLM", "Stellar", "coingecko", "stellar", "crypto", "USD"),
    SymbolSpec("SOL", "Solana", "coingecko", "solana", "crypto", "USD"),
    SymbolSpec("SPX", "S&P 500", "yahoo", "^GSPC", "index", "index", ("S&P500", "SP500", "GSPC")),
    SymbolSpec("DJIA", "Dow Jones", "yahoo", "^DJI", "index", "index", ("DOW",)),
    SymbolSpec("NASDAQ", "Nasdaq Composite", "yahoo", "^IXIC", "index", "index", ("IXIC",)),
    SymbolSpec("GOLD", "Gold (front future)", "yahoo", "GC=F", "commodity", "USD/oz", ("XAU",)),
    SymbolSpec("OIL", "WTI Crude (front future)", "yahoo", "CL=F", "commodity", "USD/bbl", ("WTI",)),
    # --- Treasury yield curve (Yahoo, no key) --------------------------------
    SymbolSpec("UST3M", "US 13-week T-bill yield", "yahoo", "^IRX", "rate", "%", ("IRX", "US3M")),
    SymbolSpec("UST5Y", "US 5Y Treasury yield", "yahoo", "^FVX", "rate", "%", ("FVX", "US5Y")),
    SymbolSpec(
        "UST10Y", "US 10Y Treasury yield", "yahoo", "^TNX", "rate", "%",
        ("TNX", "UST10", "TREASURY", "TREASURY10Y", "US10Y"),
    ),
    SymbolSpec("UST30Y", "US 30Y Treasury yield", "yahoo", "^TYX", "rate", "%", ("TYX", "US30Y")),
    SymbolSpec("REIT", "US Real Estate (VNQ)", "yahoo", "VNQ", "reit", "USD", ("VNQ", "REALESTATE")),
    # --- FX (Yahoo, no key) --------------------------------------------------
    SymbolSpec(
        "EURUSD", "Euro / US Dollar", "yahoo", "EURUSD=X", "fx", "USD", ("EUR",),
        vendor_symbol="EUR/USD",
    ),
    SymbolSpec(
        "GBPUSD", "British Pound / US Dollar", "yahoo", "GBPUSD=X", "fx", "USD", ("GBP",),
        vendor_symbol="GBP/USD",
    ),
    SymbolSpec(
        "USDJPY", "US Dollar / Japanese Yen", "yahoo", "JPY=X", "fx", "JPY", ("JPY",),
        vendor_symbol="USD/JPY",
    ),
    SymbolSpec("DXY", "US Dollar Index", "yahoo", "DX-Y.NYB", "fx", "index", ("USDOLLAR",)),
    # --- Fixed income via liquid ETF proxies (Yahoo, no key) -----------------
    SymbolSpec("BOND_AGG", "US Aggregate Bond (AGG)", "yahoo", "AGG", "bond_proxy", "USD", ("AGG",)),
    SymbolSpec("BOND_IG", "IG Corporate Bond (LQD)", "yahoo", "LQD", "bond_proxy", "USD", ("LQD",)),
    SymbolSpec("BOND_HY", "High-Yield Bond (HYG)", "yahoo", "HYG", "bond_proxy", "USD", ("HYG",)),
    SymbolSpec("BOND_MUNI", "Municipal Bond (MUB)", "yahoo", "MUB", "bond_proxy", "USD", ("MUB",)),
    SymbolSpec("BOND_TIPS", "TIPS (TIP)", "yahoo", "TIP", "bond_proxy", "USD", ("TIP",)),
    # --- Public proxies for private/illiquid classes (Yahoo, no key) ---------
    SymbolSpec("PE_PROXY", "Listed Private Equity (PSP)", "yahoo", "PSP", "pe_proxy", "USD", ("PSP",)),
    SymbolSpec("SMB_PROXY", "US Small Caps (IWM)", "yahoo", "IWM", "smb_proxy", "USD", ("IWM",)),
    # --- Macro via BLS (no key) ---------------------------------------------
    SymbolSpec(
        "INFLATION", "US CPI (YoY)", "bls", CPI_SERIES_ID, "macro", "%",
        ("CPI", "INFLATIONRATE"),
    ),
    # --- Macro via FRED (requires FRED_API_KEY) ------------------------------
    SymbolSpec("M2", "US M2 Money Supply", "fred", "M2SL", "macro", "USD bn", ("MONEYSUPPLY",)),
    SymbolSpec("GDP", "US GDP", "fred", "GDP", "macro", "USD bn", ()),
    SymbolSpec("UNEMPLOYMENT", "US Unemployment Rate", "fred", "UNRATE", "macro", "%", ("UNRATE",)),
    SymbolSpec("FED_FUNDS", "US Fed Funds Rate", "fred", "FEDFUNDS", "macro", "%", ("FEDFUNDS",)),
    SymbolSpec(
        "CONSUMER_CREDIT", "US Consumer Credit (total)", "fred", "TOTALSL", "macro", "USD mn",
        ("CONSUMERDEBT", "CONSUMERCREDIT"),
    ),
    SymbolSpec(
        "REVOLVING_CREDIT", "US Revolving Consumer Credit", "fred", "REVOLSL", "macro", "USD mn",
        ("REVOLVINGCREDIT", "CREDITCARDDEBT"),
    ),
    SymbolSpec(
        "HOUSEHOLD_DEBT_GDP", "US Household Debt to GDP", "fred", "HDTGPDUSQ163N", "macro", "%",
        ("HOUSEHOLDDEBT",),
    ),
    SymbolSpec(
        "CC_DELINQUENCY", "Credit Card Delinquency Rate", "fred", "DRCCLACBS", "macro", "%",
        ("CREDITCARDDELINQUENCY", "CCDELINQUENCY"),
    ),
    SymbolSpec(
        "LOAN_DELINQUENCY", "All Bank Loans Delinquency Rate", "fred", "DRALACBN", "macro", "%",
        ("LOANDELINQUENCY", "DELINQUENCY"),
    ),
    SymbolSpec(
        "MORTGAGE_DELINQUENCY", "Mortgage Delinquency Rate", "fred", "DRSFRMACBS", "macro", "%",
        ("MORTGAGEDELINQUENCY",),
    ),
    SymbolSpec("RETAIL_SALES", "US Retail Sales", "fred", "RSAFS", "macro", "USD mn", ("RETAIL",)),
    SymbolSpec(
        "CONSUMER_SENTIMENT", "US Consumer Sentiment (UMich)", "fred", "UMCSENT", "macro", "index",
        ("SENTIMENT",),
    ),
    SymbolSpec(
        "INDUSTRIAL_PRODUCTION", "US Industrial Production", "fred", "INDPRO", "macro", "index",
        ("INDPRO",),
    ),
]

DEFAULT_SYMBOLS = ["BTC", "ETH", "GOLD", "SPX", "UST10Y", "INFLATION"]

_ALIAS_INDEX: dict[str, SymbolSpec] = {}
for _spec in SYMBOLS:
    _ALIAS_INDEX[_spec.symbol.upper()] = _spec
    for _alias in _spec.aliases:
        _ALIAS_INDEX[_alias.upper()] = _spec


def resolve_symbol(symbol: str) -> SymbolSpec:
    """Resolve a friendly symbol/alias, falling back to a Yahoo equity passthrough."""
    key = symbol.strip().upper()
    if key in _ALIAS_INDEX:
        return _ALIAS_INDEX[key]
    # Unknown symbol: treat as an equity ticker (works for both Yahoo and the vendor).
    return SymbolSpec(key, key, "yahoo", key, "equity", "USD", vendor_symbol=key)


# --------------------------------------------------------------------------- #
# TTL cache
# --------------------------------------------------------------------------- #
_CACHE: dict[str, tuple[float, Any]] = {}
_CACHE_LOCK = threading.Lock()


def reset_cache() -> None:
    with _CACHE_LOCK:
        _CACHE.clear()


def _cached(key: str, ttl: int, producer: Callable[[], Any]) -> Any:
    now = time.time()
    with _CACHE_LOCK:
        hit = _CACHE.get(key)
        if hit and hit[0] > now:
            return hit[1]
    value = producer()
    with _CACHE_LOCK:
        _CACHE[key] = (now + ttl, value)
    return value


# --------------------------------------------------------------------------- #
# Low-level HTTP + provider adapters (module-level so they are easy to mock)
# --------------------------------------------------------------------------- #
def _http_get_json(url: str, data: bytes | None = None) -> Any:
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 - normalize all network/parse failures
        raise ProviderError(str(exc)) from exc


def coingecko_simple_price(ids: list[str]) -> dict[str, dict[str, float]]:
    joined = ",".join(sorted(set(ids)))
    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        f"?ids={urllib.parse.quote(joined)}&vs_currencies=usd&include_24hr_change=true"
    )
    return _http_get_json(url)


def _yahoo_get(provider_symbol: str, query: str) -> dict[str, Any]:
    """GET a Yahoo chart payload, failing over across hosts for resilience."""
    quoted = urllib.parse.quote(provider_symbol)
    last_error: Exception | None = None
    for host in YAHOO_HOSTS:
        url = f"https://{host}/v8/finance/chart/{quoted}?{query}"
        try:
            return _http_get_json(url)
        except ProviderError as exc:
            last_error = exc
    raise ProviderError(f"Yahoo unavailable for {provider_symbol}: {last_error}")


def yahoo_chart(provider_symbol: str) -> dict[str, Any]:
    payload = _yahoo_get(provider_symbol, "interval=1d&range=5d")
    result = (payload.get("chart") or {}).get("result") or []
    if not result:
        raise ProviderError(f"No Yahoo data for {provider_symbol}.")
    return result[0].get("meta") or {}


def twelvedata_quote(vendor_symbol: str) -> dict[str, Any]:
    """Quote from the licensed vendor (Twelve Data). Requires TWELVEDATA_API_KEY.

    Returns a dict with at least ``price``; ``percent_change`` and ``currency`` when
    available. Normalizes the vendor's error payloads into ProviderError.
    """
    key = twelvedata_api_key()
    if not key:
        raise ProviderError("TWELVEDATA_API_KEY is not configured.")
    url = (
        "https://api.twelvedata.com/quote"
        f"?symbol={urllib.parse.quote(vendor_symbol)}&apikey={urllib.parse.quote(key)}"
    )
    payload = _http_get_json(url)
    if not isinstance(payload, dict) or payload.get("status") == "error" or "close" not in payload:
        message = payload.get("message") if isinstance(payload, dict) else "bad response"
        raise ProviderError(f"Twelve Data error for {vendor_symbol}: {message}")
    result: dict[str, Any] = {"price": float(payload["close"])}
    if payload.get("percent_change") not in (None, ""):
        result["percent_change"] = float(payload["percent_change"])
    if payload.get("currency"):
        result["currency"] = payload["currency"]
    return result


def fred_series_latest(series_id: str) -> tuple[float, str]:
    """Latest observation (value, date) for a FRED series. Requires FRED_API_KEY."""
    key = fred_api_key()
    if not key:
        raise ProviderError("FRED_API_KEY is not configured.")
    url = (
        "https://api.stlouisfed.org/fred/series/observations"
        f"?series_id={urllib.parse.quote(series_id)}&api_key={urllib.parse.quote(key)}"
        "&file_type=json&sort_order=desc&limit=1"
    )
    payload = _http_get_json(url)
    observations = payload.get("observations") or []
    if not observations:
        raise ProviderError(f"No FRED observations for {series_id}.")
    obs = observations[0]
    try:
        return float(obs["value"]), str(obs.get("date", ""))
    except (KeyError, ValueError) as exc:
        raise ProviderError(f"Unparseable FRED value for {series_id}.") from exc


def yahoo_chart_history(
    provider_symbol: str, range_: str = "3y", interval: str = "1mo"
) -> list[tuple[int, float]]:
    """Return [(unix_ts, close), ...] historical closes from Yahoo Finance."""
    payload = _yahoo_get(provider_symbol, f"interval={interval}&range={range_}")
    result = (payload.get("chart") or {}).get("result") or []
    if not result:
        raise ProviderError(f"No Yahoo history for {provider_symbol}.")
    node = result[0]
    timestamps = node.get("timestamp") or []
    quote = ((node.get("indicators") or {}).get("quote") or [{}])[0]
    closes = quote.get("close") or []
    series: list[tuple[int, float]] = []
    for ts, close in zip(timestamps, closes):
        if ts is not None and close is not None:
            series.append((int(ts), float(close)))
    if not series:
        raise ProviderError(f"Empty Yahoo history for {provider_symbol}.")
    return series


def sharadar_sf1_fundamentals(ticker: str, dimension: str = "ARQ") -> dict[str, Any]:
    """Point-in-time fundamentals for one ticker from Sharadar SF1 (Nasdaq Data Link).

    Uses the As-Reported dimension (``ARQ``) by default so values are point-in-time
    (no look-ahead). Requires NASDAQ_DATA_LINK_API_KEY. Returns a column->value dict.
    """
    key = nasdaq_data_link_api_key()
    if not key:
        raise ProviderError("NASDAQ_DATA_LINK_API_KEY is not configured.")
    url = (
        "https://data.nasdaq.com/api/v3/datatables/SHARADAR/SF1"
        f"?ticker={urllib.parse.quote(ticker)}&dimension={urllib.parse.quote(dimension)}"
        f"&qopts.per_page=1&api_key={urllib.parse.quote(key)}"
    )
    payload = _http_get_json(url)
    table = payload.get("datatable") or {}
    rows = table.get("data") or []
    if not rows:
        raise ProviderError(f"No Sharadar SF1 data for {ticker}.")
    columns = [c.get("name") for c in (table.get("columns") or [])]
    return dict(zip(columns, rows[0]))


def bls_cpi_series() -> list[dict[str, Any]]:
    # Registered key -> v2 (500 req/day, 20yr, net/pct changes); keyless -> v1.
    key = bls_api_key()
    if key:
        url = (
            f"https://api.bls.gov/publicAPI/v2/timeseries/data/{CPI_SERIES_ID}"
            f"?registrationkey={urllib.parse.quote(key)}"
        )
    else:
        url = f"https://api.bls.gov/publicAPI/v1/timeseries/data/{CPI_SERIES_ID}"
    payload = _http_get_json(url)
    series = (payload.get("Results") or {}).get("series") or []
    if not series:
        raise ProviderError("No CPI series returned.")
    return series[0].get("data") or []


# --------------------------------------------------------------------------- #
# Service
# --------------------------------------------------------------------------- #
def _now() -> datetime:
    return datetime.now(timezone.utc)


class MarketDataService:
    def __init__(self, cache_ttl: int = CACHE_TTL_SECONDS) -> None:
        self.cache_ttl = cache_ttl

    # -- public API -------------------------------------------------------- #
    def quotes(self, symbols: list[str] | None = None) -> QuotesResponse:
        requested = symbols if symbols else list(DEFAULT_SYMBOLS)
        specs = [resolve_symbol(symbol) for symbol in requested]

        crypto_prices = self._maybe_load_crypto(specs)
        quotes: list[Quote] = []
        sources: set[str] = set()

        for spec in specs:
            quote = self._quote_for(spec, crypto_prices)
            sources.add(spec.provider)
            quotes.append(quote)

        return QuotesResponse(
            as_of=_now(),
            count=len(quotes),
            sources=sorted(sources),
            quotes=quotes,
        )

    def inflation(self) -> InflationResponse:
        try:
            data = self._cpi_series()
            yoy, latest, period = self._cpi_yoy(data)
            return InflationResponse(
                series=CPI_SERIES_ID,
                period=period,
                yoy_percent=yoy,
                index_value=latest,
                source="us_bls",
                as_of=_now(),
                note="US CPI-U (all items, NSA), year-over-year.",
            )
        except (ProviderError, ValueError, KeyError, IndexError) as exc:
            return InflationResponse(
                series=CPI_SERIES_ID,
                period="",
                yoy_percent=None,
                index_value=None,
                source="us_bls",
                as_of=_now(),
                status="unavailable",
                note=f"CPI fetch failed: {exc}",
            )

    def providers(self) -> ProvidersResponse:
        return ProvidersResponse(
            providers=[
                ProviderInfo(
                    key="coingecko",
                    name="CoinGecko",
                    asset_classes=["crypto"],
                    status="live",
                    requires_key=False,
                    notes="Free public API. Spot USD price and 24h change for crypto assets.",
                ),
                ProviderInfo(
                    key="yahoo",
                    name="Yahoo Finance",
                    asset_classes=["index", "equity", "commodity", "rate", "reit"],
                    status="live",
                    requires_key=False,
                    notes="Unofficial chart endpoint; last price + previous close for % change.",
                ),
                ProviderInfo(
                    key="us_bls",
                    name="US Bureau of Labor Statistics",
                    asset_classes=["macro"],
                    status="live",
                    requires_key=False,
                    notes=(
                        "Registered v2 API (higher limits, 20yr history)."
                        if bls_api_key()
                        else "CPI via keyless v1 (low-volume). Set BLS_API_KEY for the registered v2 API."
                    ),
                ),
                ProviderInfo(
                    key="fred",
                    name="FRED (St. Louis Fed)",
                    asset_classes=["macro"],
                    status="live" if fred_api_key() else "requires_credentials",
                    requires_key=True,
                    notes=(
                        "M2, GDP, unemployment, and full yield curve. "
                        "Adapter implemented; set FRED_API_KEY to activate."
                    ),
                ),
                ProviderInfo(
                    key="twelvedata",
                    name="Twelve Data (licensed vendor)",
                    asset_classes=["equity", "fx", "crypto", "index"],
                    status="live" if twelvedata_api_key() else "requires_credentials",
                    requires_key=True,
                    notes=(
                        "Production-grade, ToS-compliant quotes. Adapter implemented; set "
                        "TWELVEDATA_API_KEY to make it the PRIMARY source for equities/FX "
                        "(Yahoo remains the automatic fallback)."
                    ),
                ),
                ProviderInfo(
                    key="sharadar_sf1",
                    name="Sharadar Core US Fundamentals (Nasdaq Data Link)",
                    asset_classes=["fundamentals"],
                    status="live" if nasdaq_data_link_api_key() else "requires_credentials",
                    requires_key=True,
                    notes=(
                        "Point-in-time fundamentals (As-Reported, survivorship-bias-free) for "
                        "the Opportunity Score validation. Adapter implemented; set "
                        "NASDAQ_DATA_LINK_API_KEY to activate."
                    ),
                ),
                ProviderInfo(
                    key="bloomberg",
                    name="Bloomberg",
                    asset_classes=["index", "equity", "commodity", "rate", "fx"],
                    status="requires_credentials",
                    requires_key=True,
                    notes=(
                        "Requires a paid Bloomberg Data License / BLPAPI entitlement and the "
                        "blpapi SDK. Add an adapter once credentials are provisioned."
                    ),
                ),
                ProviderInfo(
                    key="tradingview",
                    name="TradingView",
                    asset_classes=[],
                    status="unsupported",
                    requires_key=True,
                    notes=(
                        "No official public market-data REST API; only embeddable widgets. "
                        "Use a licensed quotes vendor for programmatic data."
                    ),
                ),
            ]
        )

    def symbols(self) -> SymbolsResponse:
        return SymbolsResponse(
            default=list(DEFAULT_SYMBOLS),
            symbols=[
                SymbolInfo(
                    symbol=spec.symbol,
                    name=spec.name,
                    asset_class=spec.asset_class,
                    provider=spec.provider,
                    unit=spec.unit,
                    aliases=list(spec.aliases),
                )
                for spec in SYMBOLS
            ],
        )

    # -- internals --------------------------------------------------------- #
    def _maybe_load_crypto(self, specs: list[SymbolSpec]) -> dict[str, dict[str, float]]:
        ids = [spec.provider_symbol for spec in specs if spec.provider == "coingecko"]
        if not ids:
            return {}
        try:
            return self._cached(f"coingecko:{','.join(sorted(set(ids)))}", lambda: coingecko_simple_price(ids))
        except ProviderError:
            return {}

    def _quote_for(self, spec: SymbolSpec, crypto_prices: dict[str, dict[str, float]]) -> Quote:
        base = Quote(
            symbol=spec.symbol,
            name=spec.name,
            asset_class=spec.asset_class,
            currency="USD",
            unit=spec.unit,
            source=spec.provider,
            as_of=_now(),
        )
        try:
            if spec.provider == "coingecko":
                entry = crypto_prices.get(spec.provider_symbol)
                if not entry or "usd" not in entry:
                    raise ProviderError("No crypto price returned.")
                base.price = float(entry["usd"])
                if entry.get("usd_24h_change") is not None:
                    base.change_percent = round(float(entry["usd_24h_change"]), 2)
            elif spec.provider == "yahoo":
                if not self._fill_from_vendor(spec, base):
                    meta = self._cached(
                        f"yahoo:{spec.provider_symbol}",
                        lambda: yahoo_chart(spec.provider_symbol),
                    )
                    price = meta.get("regularMarketPrice")
                    prev = meta.get("chartPreviousClose") or meta.get("previousClose")
                    if price is None:
                        raise ProviderError("No price in Yahoo response.")
                    base.price = float(price)
                    base.currency = meta.get("currency") or "USD"
                    if prev:
                        base.change_percent = round(
                            (float(price) - float(prev)) / float(prev) * 100, 2
                        )
            elif spec.provider == "bls":
                data = self._cpi_series()
                yoy, _latest, period = self._cpi_yoy(data)
                base.price = yoy
                base.note = f"CPI YoY ({period})."
            elif spec.provider == "fred":
                value, date = self._cached(
                    f"fred:{spec.provider_symbol}",
                    lambda: fred_series_latest(spec.provider_symbol),
                )
                base.price = value
                base.note = f"FRED {spec.provider_symbol} as of {date}."
            else:
                raise ProviderError(f"Unknown provider '{spec.provider}'.")
        except (ProviderError, ValueError, KeyError, IndexError, TypeError) as exc:
            base.status = "unavailable"
            base.note = f"{spec.provider} fetch failed: {exc}"
        return base

    def _fill_from_vendor(self, spec: SymbolSpec, base: Quote) -> bool:
        """Try the licensed vendor first when configured; return True on success."""
        if not twelvedata_api_key() or not spec.vendor_symbol:
            return False
        try:
            data = self._cached(
                f"twelvedata:{spec.vendor_symbol}",
                lambda: twelvedata_quote(spec.vendor_symbol),
            )
        except ProviderError:
            return False  # fall back to Yahoo
        base.price = float(data["price"])
        base.source = "twelvedata"
        if data.get("currency"):
            base.currency = data["currency"]
        if data.get("percent_change") is not None:
            base.change_percent = round(float(data["percent_change"]), 2)
        return True

    def _cpi_series(self) -> list[dict[str, Any]]:
        return self._cached("bls:cpi", bls_cpi_series)

    @staticmethod
    def _cpi_yoy(data: list[dict[str, Any]]) -> tuple[float, float, str]:
        if not data:
            raise ValueError("Empty CPI series.")
        latest = data[0]
        latest_value = float(latest["value"])
        target_year = str(int(latest["year"]) - 1)
        prior = next(
            (row for row in data if row["year"] == target_year and row["period"] == latest["period"]),
            None,
        )
        period_label = f"{latest.get('periodName', latest['period'])} {latest['year']}"
        if prior is None:
            raise ValueError("No year-ago CPI datapoint to compute YoY.")
        yoy = round((latest_value / float(prior["value"]) - 1.0) * 100.0, 2)
        return yoy, latest_value, period_label

    def _cached(self, key: str, producer: Callable[[], Any]) -> Any:
        if self.cache_ttl <= 0:
            return producer()
        return _cached(key, self.cache_ttl, producer)
