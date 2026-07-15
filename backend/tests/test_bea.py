import pytest
from fastapi.testclient import TestClient

from app import bea_services
from app.bea_services import BeaService
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def _clear_cache():
    bea_services.reset_cache()
    yield
    bea_services.reset_cache()


def _fake_nipa(table, frequency="A", years=None):
    if table == "T10105":
        return [
            {"LineNumber": "1", "TimePeriod": "2023", "DataValue": "27,811,517"},
            {"LineNumber": "1", "TimePeriod": "2024", "DataValue": "29,298,013"},
            {"LineNumber": "2", "TimePeriod": "2024", "DataValue": "19,000,000"},
        ]
    if table == "T10101":
        return [{"LineNumber": "1", "TimePeriod": "2024", "DataValue": "2.8"}]
    if table == "T20100":
        return [{"LineNumber": "1", "TimePeriod": "2024", "DataValue": "24,000,000"}]
    return []


def test_macro_requires_key(monkeypatch):
    monkeypatch.delenv("BEA_API_KEY", raising=False)
    monkeypatch.delenv("BEA_USER_ID", raising=False)
    resp = BeaService().macro()
    assert all(i.status == "requires_credentials" for i in resp.indicators)


def test_macro_extracts_latest_values(monkeypatch):
    monkeypatch.setenv("BEA_API_KEY", "test-key")
    monkeypatch.setattr(bea_services, "bea_nipa", _fake_nipa)
    resp = BeaService().macro()
    by_key = {i.key: i for i in resp.indicators}
    assert by_key["gdp"].value == 29_298_013  # latest annual (2024), not 2023
    assert by_key["gdp"].period == "2024"
    assert by_key["pce"].value == 19_000_000
    assert by_key["real_gdp_growth"].value == pytest.approx(2.8)
    assert by_key["personal_income"].value == 24_000_000
    assert all(i.status == "ok" for i in resp.indicators)


def test_endpoint_returns_macro(monkeypatch):
    monkeypatch.setenv("BEA_API_KEY", "test-key")
    monkeypatch.setattr(bea_services, "bea_nipa", _fake_nipa)
    resp = client.get("/api/v1/macro/bea")
    assert resp.status_code == 200
    body = resp.json()
    assert body["source"].startswith("US Bureau of Economic Analysis")
    keys = {i["key"] for i in body["indicators"]}
    assert {"gdp", "pce", "real_gdp_growth", "personal_income"} <= keys


def test_unavailable_when_table_fails(monkeypatch):
    monkeypatch.setenv("BEA_API_KEY", "test-key")

    def _boom(table, frequency="A", years=None):
        raise bea_services.ProviderError("boom")

    monkeypatch.setattr(bea_services, "bea_nipa", _boom)
    resp = BeaService().macro()
    assert all(i.status == "unavailable" for i in resp.indicators)
