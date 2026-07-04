import pytest
from fastapi.testclient import TestClient

from app import market_services
from app.main import app
from app.market_services import MarketDataService, ProviderError

client = TestClient(app)


@pytest.fixture(autouse=True)
def _clear_cache():
    market_services.reset_cache()
    yield
    market_services.reset_cache()


def _fake_coingecko(ids):
    table = {
        "bitcoin": {"usd": 59000.0, "usd_24h_change": -5.27},
        "ethereum": {"usd": 1560.98, "usd_24h_change": -5.83},
        "ripple": {"usd": 1.048, "usd_24h_change": -4.64},
        "stellar": {"usd": 0.182, "usd_24h_change": -5.52},
    }
    return {cid: table[cid] for cid in ids if cid in table}


def _fake_yahoo(provider_symbol):
    table = {
        "^GSPC": {"regularMarketPrice": 7352.59, "chartPreviousClose": 7365.46, "currency": "USD"},
        "GC=F": {"regularMarketPrice": 3180.4, "chartPreviousClose": 3150.0, "currency": "USD"},
        "^TNX": {"regularMarketPrice": 4.12, "chartPreviousClose": 4.08, "currency": "USD"},
        "AAPL": {"regularMarketPrice": 240.5, "chartPreviousClose": 238.0, "currency": "USD"},
        "EURUSD=X": {"regularMarketPrice": 1.085, "chartPreviousClose": 1.08, "currency": "USD"},
        "AGG": {"regularMarketPrice": 99.2, "chartPreviousClose": 99.0, "currency": "USD"},
        "PSP": {"regularMarketPrice": 62.1, "chartPreviousClose": 61.5, "currency": "USD"},
        "IWM": {"regularMarketPrice": 230.7, "chartPreviousClose": 232.0, "currency": "USD"},
    }
    if provider_symbol not in table:
        raise ProviderError(f"No data for {provider_symbol}")
    return table[provider_symbol]


def _fake_cpi():
    return [
        {"year": "2026", "period": "M05", "periodName": "May", "value": "335.123"},
        {"year": "2025", "period": "M05", "periodName": "May", "value": "325.000"},
    ]


@pytest.fixture
def patched_providers(monkeypatch):
    monkeypatch.setattr(market_services, "coingecko_simple_price", _fake_coingecko)
    monkeypatch.setattr(market_services, "yahoo_chart", _fake_yahoo)
    monkeypatch.setattr(market_services, "bls_cpi_series", _fake_cpi)


def test_default_quotes_blend_all_providers(patched_providers) -> None:
    response = client.get("/api/v1/market/quotes")
    assert response.status_code == 200
    body = response.json()
    quotes = {q["symbol"]: q for q in body["quotes"]}

    assert quotes["BTC"]["price"] == 59000.0
    assert quotes["BTC"]["source"] == "coingecko"
    assert quotes["BTC"]["change_percent"] == -5.27
    assert quotes["BTC"]["status"] == "ok"

    # S&P 500: % change derived from price vs previous close.
    assert quotes["SPX"]["source"] == "yahoo"
    assert quotes["SPX"]["change_percent"] == round((7352.59 - 7365.46) / 7365.46 * 100, 2)

    # Inflation: YoY from CPI index (335.123 / 325.0 - 1) * 100.
    assert quotes["INFLATION"]["source"] == "bls"
    assert quotes["INFLATION"]["price"] == round((335.123 / 325.0 - 1) * 100, 2)

    assert set(body["sources"]) >= {"coingecko", "yahoo", "bls"}


def test_specific_symbols_param(patched_providers) -> None:
    response = client.get("/api/v1/market/quotes", params={"symbols": "BTC,GOLD"})
    assert response.status_code == 200
    symbols = {q["symbol"] for q in response.json()["quotes"]}
    assert symbols == {"BTC", "GOLD"}


def test_unknown_symbol_falls_back_to_yahoo_equity(patched_providers) -> None:
    response = client.get("/api/v1/market/quotes", params={"symbols": "AAPL"})
    assert response.status_code == 200
    quote = response.json()["quotes"][0]
    assert quote["symbol"] == "AAPL"
    assert quote["asset_class"] == "equity"
    assert quote["price"] == 240.5
    assert quote["status"] == "ok"


def test_provider_failure_marks_symbol_unavailable_not_500(monkeypatch) -> None:
    market_services.reset_cache()

    def _boom(_symbol):
        raise ProviderError("network down")

    monkeypatch.setattr(market_services, "yahoo_chart", _boom)
    monkeypatch.setattr(market_services, "coingecko_simple_price", _fake_coingecko)

    response = client.get("/api/v1/market/quotes", params={"symbols": "BTC,SPX"})
    assert response.status_code == 200
    quotes = {q["symbol"]: q for q in response.json()["quotes"]}
    assert quotes["BTC"]["status"] == "ok"
    assert quotes["SPX"]["status"] == "unavailable"
    assert "failed" in quotes["SPX"]["note"].lower()


def test_inflation_endpoint(patched_providers) -> None:
    response = client.get("/api/v1/market/inflation")
    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "us_bls"
    assert body["yoy_percent"] == round((335.123 / 325.0 - 1) * 100, 2)
    assert body["status"] == "ok"


def test_providers_lists_live_and_credentialed_sources() -> None:
    response = client.get("/api/v1/market/providers")
    assert response.status_code == 200
    providers = {p["key"]: p for p in response.json()["providers"]}
    assert providers["coingecko"]["status"] == "live"
    assert providers["yahoo"]["status"] == "live"
    assert providers["bloomberg"]["status"] == "requires_credentials"
    assert providers["tradingview"]["status"] == "unsupported"
    # FRED is implemented but key-gated; without a key it advertises credentials needed.
    assert providers["fred"]["key"] == "fred"
    assert providers["fred"]["status"] in {"live", "requires_credentials"}


def test_fx_bond_and_proxy_symbols_are_live(patched_providers) -> None:
    response = client.get(
        "/api/v1/market/quotes",
        params={"symbols": "EURUSD,BOND_AGG,PE_PROXY,SMB_PROXY"},
    )
    assert response.status_code == 200
    quotes = {q["symbol"]: q for q in response.json()["quotes"]}
    assert quotes["EURUSD"]["asset_class"] == "fx"
    assert quotes["EURUSD"]["status"] == "ok"
    assert quotes["BOND_AGG"]["asset_class"] == "bond_proxy"
    assert quotes["PE_PROXY"]["status"] == "ok"
    assert quotes["SMB_PROXY"]["status"] == "ok"


def test_fred_macro_symbol_gated_without_key(monkeypatch) -> None:
    market_services.reset_cache()
    monkeypatch.delenv("FRED_API_KEY", raising=False)
    response = client.get("/api/v1/market/quotes", params={"symbols": "M2"})
    assert response.status_code == 200
    quote = response.json()["quotes"][0]
    assert quote["symbol"] == "M2"
    assert quote["status"] == "unavailable"
    assert "fred" in quote["note"].lower()


def test_licensed_vendor_used_as_primary_when_keyed(monkeypatch, patched_providers) -> None:
    market_services.reset_cache()
    monkeypatch.setenv("TWELVEDATA_API_KEY", "vendor-key")
    monkeypatch.setattr(
        market_services,
        "twelvedata_quote",
        lambda vsym: {"price": 1.2345, "percent_change": 0.42, "currency": "USD"},
    )
    response = client.get("/api/v1/market/quotes", params={"symbols": "EURUSD"})
    quote = response.json()["quotes"][0]
    assert quote["source"] == "twelvedata"
    assert quote["price"] == 1.2345
    assert quote["change_percent"] == 0.42


def test_licensed_vendor_falls_back_to_yahoo_on_error(monkeypatch, patched_providers) -> None:
    market_services.reset_cache()
    monkeypatch.setenv("TWELVEDATA_API_KEY", "vendor-key")

    def _vendor_down(_vsym):
        raise market_services.ProviderError("vendor 429")

    monkeypatch.setattr(market_services, "twelvedata_quote", _vendor_down)
    response = client.get("/api/v1/market/quotes", params={"symbols": "EURUSD"})
    quote = response.json()["quotes"][0]
    assert quote["status"] == "ok"
    assert quote["source"] == "yahoo"  # graceful fallback


def test_providers_includes_twelvedata() -> None:
    providers = {p["key"]: p for p in client.get("/api/v1/market/providers").json()["providers"]}
    assert providers["twelvedata"]["status"] in {"live", "requires_credentials"}


def test_fred_macro_symbol_live_with_key(monkeypatch) -> None:
    market_services.reset_cache()
    monkeypatch.setenv("FRED_API_KEY", "test-key")
    monkeypatch.setattr(
        market_services, "fred_series_latest", lambda series_id: (21000.5, "2026-05-01")
    )
    response = client.get("/api/v1/market/quotes", params={"symbols": "M2"})
    assert response.status_code == 200
    quote = response.json()["quotes"][0]
    assert quote["status"] == "ok"
    assert quote["price"] == 21000.5


def test_symbols_catalog_includes_defaults() -> None:
    response = client.get("/api/v1/market/symbols")
    assert response.status_code == 200
    body = response.json()
    assert "BTC" in body["default"]
    catalog = {s["symbol"] for s in body["symbols"]}
    assert {"BTC", "SPX", "GOLD", "UST10Y", "INFLATION"}.issubset(catalog)


def test_service_cache_ttl_zero_bypasses_cache(monkeypatch) -> None:
    calls = {"n": 0}

    def _counting_yahoo(symbol):
        calls["n"] += 1
        return {"regularMarketPrice": 100.0, "chartPreviousClose": 99.0, "currency": "USD"}

    monkeypatch.setattr(market_services, "yahoo_chart", _counting_yahoo)
    service = MarketDataService(cache_ttl=0)
    service.quotes(["SPX"])
    service.quotes(["SPX"])
    assert calls["n"] == 2  # no caching when ttl=0
