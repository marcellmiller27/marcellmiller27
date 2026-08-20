# JHI-SIG: 69M2705M | US government economic data adapter tests | JHI Research & Analytics Firm, Inc. (proprietary)
import pytest
from fastapi.testclient import TestClient

from app import data_gov_services as dgs
from app import market_services
from app.data_gov_services import DataGovService
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def _clear_cache(monkeypatch):
    dgs.reset_cache()
    # Never sleep during retry backoff in tests.
    monkeypatch.setattr(dgs.time, "sleep", lambda *a, **k: None)
    yield
    dgs.reset_cache()


# --------------------------------------------------------------------------- #
# Fakes
# --------------------------------------------------------------------------- #
def _fake_treasury(path, params):
    if path.endswith("debt_to_penny"):
        return [{
            "record_date": "2026-08-18",
            "tot_pub_debt_out_amt": "40047425768420.22",
            "debt_held_public_amt": "32265798542898.08",
        }]
    if path.endswith("avg_interest_rates"):
        return [
            {"record_date": "2026-07-31", "security_desc": "Total Marketable",
             "avg_interest_rate_amt": "3.401"},
            {"record_date": "2026-07-31", "security_desc": "Treasury Bills",
             "avg_interest_rate_amt": "3.758"},
            {"record_date": "2026-07-31", "security_desc": "Treasury Notes",
             "avg_interest_rate_amt": "3.309"},
            {"record_date": "2026-07-31", "security_desc": "Treasury Bonds",
             "avg_interest_rate_amt": "3.210"},
            # An older record for one security that must be ignored (not latest date).
            {"record_date": "2026-06-30", "security_desc": "Treasury Bills",
             "avg_interest_rate_amt": "9.999"},
        ]
    return []


def _fake_fdic(path, params):
    if path == "institutions":
        return {"meta": {"total": 4250}, "data": [{"data": {"CERT": 10004}}]}
    if path == "financials" and params.get("fields") == "REPDTE":
        return {"data": [{"data": {"REPDTE": "20250331"}}]}
    if path == "financials":  # per-institution lookup
        return {"data": [{"data": {
            "CERT": 628, "NAME": "JPMORGAN CHASE BANK NA", "ASSET": 3643099000,
            "DEP": 2601221000, "NETINC": 12708000, "ROA": 1.4314, "ROE": 16.15,
            "REPDTE": "20250331",
        }}]}
    return {"meta": {}, "data": []}


def _fake_eia(route, params):
    if route.startswith("petroleum"):
        return {"data": [{"period": "2026-08-18", "value": 63.42}]}
    if route.startswith("natural-gas"):
        return {"data": [{"period": "2026-08-18", "value": 2.87}]}
    if route.startswith("electricity"):
        return {"data": [{"period": "2026-05", "price": 13.83}]}
    return {"data": []}


# --------------------------------------------------------------------------- #
# Treasury (keyless)
# --------------------------------------------------------------------------- #
def test_treasury_parses_debt_and_rates_with_as_of(monkeypatch):
    monkeypatch.setattr(dgs, "fetch_treasury", _fake_treasury)
    resp = DataGovService().treasury_fiscal()
    by = {i.key: i for i in resp.indicators}
    assert resp.provider == "us_treasury_fiscal"
    assert resp.requires_key is False
    assert by["total_public_debt"].value == pytest.approx(40047425768420.22)
    assert by["total_public_debt"].period == "2026-08-18"
    assert by["total_public_debt"].status == "ok"
    assert "as of" in by["total_public_debt"].as_of_label
    assert by["debt_held_by_public"].value == pytest.approx(32265798542898.08)
    # Latest-date selection wins over the stale 2026-06-30 Treasury Bills row.
    assert by["avg_rate_tbills"].value == pytest.approx(3.758)
    assert by["avg_rate_tbills"].period == "2026-07-31"
    assert by["avg_rate_marketable"].value == pytest.approx(3.401)


def test_treasury_degrades_to_unavailable(monkeypatch):
    def _boom(path, params):
        raise dgs.ProviderError("network down")

    monkeypatch.setattr(dgs, "fetch_treasury", _boom)
    resp = DataGovService().treasury_fiscal()
    assert all(i.status == "unavailable" for i in resp.indicators)
    assert all(i.value is None for i in resp.indicators)


# --------------------------------------------------------------------------- #
# FDIC (keyless)
# --------------------------------------------------------------------------- #
def test_banking_parses_institution_count(monkeypatch):
    monkeypatch.setattr(dgs, "fetch_fdic", _fake_fdic)
    resp = DataGovService().banking()
    ind = {i.key: i for i in resp.indicators}["insured_institutions"]
    assert ind.value == 4250
    assert ind.status == "ok"
    assert ind.period == "2025-03-31"  # latest REPDTE formatted to ISO
    assert ind.unit == "count"


def test_institution_financials_parses_health(monkeypatch):
    monkeypatch.setattr(dgs, "fetch_fdic", _fake_fdic)
    resp = DataGovService().institution_financials("628")
    by = {i.key: i for i in resp.indicators}
    assert by["roa"].value == pytest.approx(1.4314)
    assert by["roe"].value == pytest.approx(16.15)
    assert by["asset"].value == pytest.approx(3643099000)
    assert by["net_income"].period == "2025-03-31"
    assert "JPMORGAN" in by["roa"].label


def test_banking_degrades_to_unavailable(monkeypatch):
    def _boom(path, params):
        raise dgs.ProviderError("fdic down")

    monkeypatch.setattr(dgs, "fetch_fdic", _boom)
    resp = DataGovService().banking()
    assert resp.indicators[0].status == "unavailable"


# --------------------------------------------------------------------------- #
# EIA (requires a key)
# --------------------------------------------------------------------------- #
def test_energy_requires_credentials_without_key(monkeypatch):
    monkeypatch.delenv("EIA_API_KEY", raising=False)
    monkeypatch.delenv("DATA_GOV_API_KEY", raising=False)
    resp = DataGovService().energy()
    assert resp.requires_key is True
    assert resp.key_status == "requires_credentials"
    assert all(i.status == "requires_credentials" for i in resp.indicators)
    assert all(i.value is None for i in resp.indicators)


def test_energy_parses_values_with_key(monkeypatch):
    monkeypatch.setenv("DATA_GOV_API_KEY", "shared-key")
    monkeypatch.setattr(dgs, "fetch_eia", _fake_eia)
    resp = DataGovService().energy()
    by = {i.key: i for i in resp.indicators}
    assert resp.key_status == "live"
    assert by["wti_crude"].value == pytest.approx(63.42)
    assert by["wti_crude"].period == "2026-08-18"
    assert by["henry_hub_natgas"].value == pytest.approx(2.87)
    assert by["electricity_price"].value == pytest.approx(13.83)
    assert by["electricity_price"].period == "2026-05"
    assert all(i.status == "ok" for i in resp.indicators)


def test_energy_degrades_when_fetch_fails_with_key(monkeypatch):
    monkeypatch.setenv("DATA_GOV_API_KEY", "shared-key")

    def _boom(route, params):
        raise dgs.ProviderError("eia 500")

    monkeypatch.setattr(dgs, "fetch_eia", _boom)
    resp = DataGovService().energy()
    assert all(i.status == "unavailable" for i in resp.indicators)


# --------------------------------------------------------------------------- #
# Key accessors (whitespace-stripped, with fallback)
# --------------------------------------------------------------------------- #
def test_keys_are_whitespace_stripped(monkeypatch):
    monkeypatch.setenv("DATA_GOV_API_KEY", "\n  shared-key \n")
    assert dgs.data_gov_api_key() == "shared-key"


def test_blank_key_treated_as_absent(monkeypatch):
    monkeypatch.setenv("DATA_GOV_API_KEY", "   ")
    monkeypatch.delenv("EIA_API_KEY", raising=False)
    assert dgs.data_gov_api_key() is None
    assert dgs.eia_api_key() is None


def test_eia_key_falls_back_to_data_gov_key(monkeypatch):
    monkeypatch.delenv("EIA_API_KEY", raising=False)
    monkeypatch.setenv("DATA_GOV_API_KEY", "shared-key")
    assert dgs.eia_api_key() == "shared-key"
    # A dedicated EIA key overrides the shared key.
    monkeypatch.setenv("EIA_API_KEY", "dedicated-eia")
    assert dgs.eia_api_key() == "dedicated-eia"


# --------------------------------------------------------------------------- #
# Provider surface + endpoints
# --------------------------------------------------------------------------- #
def test_providers_surface_new_gov_sources(monkeypatch):
    monkeypatch.delenv("EIA_API_KEY", raising=False)
    monkeypatch.delenv("DATA_GOV_API_KEY", raising=False)
    providers = {p["key"]: p for p in client.get("/api/v1/market/providers").json()["providers"]}
    assert providers["us_treasury_fiscal"]["status"] == "live"
    assert providers["us_treasury_fiscal"]["requires_key"] is False
    assert providers["fdic_bankfind"]["status"] == "live"
    assert providers["eia"]["status"] == "requires_credentials"
    # With a key present, EIA flips to live.
    monkeypatch.setenv("DATA_GOV_API_KEY", "shared-key")
    providers = {p["key"]: p for p in client.get("/api/v1/market/providers").json()["providers"]}
    assert providers["eia"]["status"] == "live"


def test_endpoints_return_200(monkeypatch):
    monkeypatch.setenv("DATA_GOV_API_KEY", "shared-key")
    monkeypatch.setattr(dgs, "fetch_treasury", _fake_treasury)
    monkeypatch.setattr(dgs, "fetch_fdic", _fake_fdic)
    monkeypatch.setattr(dgs, "fetch_eia", _fake_eia)
    for path in ("/api/v1/macro/gov/treasury-fiscal", "/api/v1/macro/gov/banking",
                 "/api/v1/macro/gov/energy", "/api/v1/macro/gov/banking/institution/628"):
        resp = client.get(path)
        assert resp.status_code == 200, path
        assert resp.json()["indicators"]


def test_new_series_registered(monkeypatch):
    from app import data_registry as dr
    for sid in ("TREASURY_TOTAL_DEBT", "TREASURY_AVG_RATE_TBILLS",
                "FDIC_INSURED_INSTITUTIONS", "EIA_WTI", "EIA_HENRY_HUB",
                "EIA_ELECTRICITY_PRICE"):
        assert dr.get_series(sid) is not None, sid
    # Government feeds are excluded from the market refresh harness.
    refreshable = market_services.MarketDataService._refreshable_symbols()
    assert "EIA_WTI" not in refreshable
    assert "TREASURY_TOTAL_DEBT" not in refreshable
