import pytest
from fastapi.testclient import TestClient

from app import edgar_services
from app.edgar_services import EdgarService, ProviderError, ticker_to_cik
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def _clear_cache():
    edgar_services.reset_cache()
    yield
    edgar_services.reset_cache()


def _fake_tickers():
    return {
        "0": {"cik_str": 320193, "ticker": "TEST", "title": "Test Corp"},
        "1": {"cik_str": 789019, "ticker": "OTHR", "title": "Other Inc."},
    }


def _sample_facts():
    def annual(end, val, fy, form="10-K"):
        return {"end": end, "val": val, "fy": fy, "fp": "FY", "form": form}

    return {
        "entityName": "Test Corp",
        "facts": {
            "us-gaap": {
                "Revenues": {"units": {"USD": [
                    annual("2022-12-31", 1000, 2022),
                    annual("2023-12-31", 1200, 2023),
                    {"end": "2023-09-30", "val": 300, "fy": 2023, "fp": "Q3", "form": "10-Q"},
                ]}},
                "CostOfRevenue": {"units": {"USD": [annual("2023-12-31", 700, 2023)]}},
                "NetIncomeLoss": {"units": {"USD": [annual("2023-12-31", 200, 2023)]}},
                "OperatingIncomeLoss": {"units": {"USD": [annual("2023-12-31", 250, 2023)]}},
                "Assets": {"units": {"USD": [annual("2023-12-31", 5000, 2023)]}},
                "Liabilities": {"units": {"USD": [annual("2023-12-31", 3000, 2023)]}},
                "StockholdersEquity": {"units": {"USD": [annual("2023-12-31", 2000, 2023)]}},
                "CashAndCashEquivalentsAtCarryingValue": {
                    "units": {"USD": [annual("2023-12-31", 800, 2023)]}
                },
            }
        },
    }


@pytest.fixture
def _mock_edgar(monkeypatch):
    monkeypatch.setattr(edgar_services, "company_tickers", _fake_tickers)
    monkeypatch.setattr(edgar_services, "company_facts", lambda cik10: _sample_facts())


def test_ticker_to_cik_resolves_and_zero_pads(monkeypatch):
    monkeypatch.setattr(edgar_services, "company_tickers", _fake_tickers)
    cik, name = ticker_to_cik("test")
    assert cik == "0000320193"
    assert name == "Test Corp"


def test_ticker_to_cik_unknown_raises(monkeypatch):
    monkeypatch.setattr(edgar_services, "company_tickers", _fake_tickers)
    with pytest.raises(ProviderError):
        ticker_to_cik("NOPE")


def test_normalize_picks_latest_annual_and_computes_margins(_mock_edgar):
    fin = EdgarService().financials("TEST")
    assert fin.cik == "0000320193"
    assert fin.entity_name == "Test Corp"
    assert fin.fiscal_year == 2023
    assert fin.period_end == "2023-12-31"
    # Latest annual revenue (ignores the Q3 10-Q figure)
    assert fin.revenue == 1200
    assert fin.net_income == 200
    assert fin.total_assets == 5000
    assert fin.stockholders_equity == 2000
    # Gross profit derived (no GrossProfit tag): 1200 - 700
    assert fin.gross_profit == 500
    assert fin.gross_margin == pytest.approx(0.4167, abs=1e-3)
    assert fin.operating_margin == pytest.approx(0.2083, abs=1e-3)
    assert fin.net_margin == pytest.approx(0.1667, abs=1e-3)


def test_endpoint_returns_financials(_mock_edgar):
    resp = client.get("/api/v1/fundamentals/edgar/TEST")
    assert resp.status_code == 200
    body = resp.json()
    assert body["ticker"] == "TEST"
    assert body["revenue"] == 1200
    assert body["source"].startswith("SEC EDGAR")


def test_endpoint_unknown_ticker_returns_404(monkeypatch):
    monkeypatch.setattr(edgar_services, "company_tickers", _fake_tickers)
    resp = client.get("/api/v1/fundamentals/edgar/NOPE")
    assert resp.status_code == 404
