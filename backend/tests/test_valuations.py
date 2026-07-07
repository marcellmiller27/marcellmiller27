from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app import valuation_services
from app.main import app

client = TestClient(app)


class _FakeMarket:
    """Returns fixed live inputs so valuation math is deterministic in tests."""

    def __init__(self, ust10y=4.0, smb_change=2.0, pe_change=-3.0):
        self._ust10y = ust10y
        self._smb_change = smb_change
        self._pe_change = pe_change

    def quotes(self, symbols):
        table = {
            "UST10Y": SimpleNamespace(symbol="UST10Y", price=self._ust10y, change_percent=-1.0, status="ok"),
            "SMB_PROXY": SimpleNamespace(symbol="SMB_PROXY", price=230.0, change_percent=self._smb_change, status="ok"),
            "PE_PROXY": SimpleNamespace(symbol="PE_PROXY", price=60.0, change_percent=self._pe_change, status="ok"),
        }
        return SimpleNamespace(quotes=[table[s] for s in symbols if s in table])


@pytest.fixture(autouse=True)
def _patch_market(monkeypatch):
    monkeypatch.setattr(valuation_services, "MarketDataService", _FakeMarket)


def test_estimate_returns_three_modeled_classes() -> None:
    body = client.get("/api/v1/valuations/estimate").json()
    classes = {e["asset_class"] for e in body["estimates"]}
    assert "Direct real estate (per-property)" in classes
    assert "Private business / SMB" in classes
    assert "Private equity holdings" in classes
    assert all(e["type"] == "modeled_estimate" for e in body["estimates"])
    assert "Modeled estimates only" in body["disclaimer"]


def test_real_estate_value_follows_cap_rate_math() -> None:
    body = client.get("/api/v1/valuations/estimate", params={"noi": 100000}).json()
    re_est = next(e for e in body["estimates"] if e["asset_class"].startswith("Direct real estate"))
    # cap_rate = (4.0 + 2.5)/100 = 0.065 ; value = 100000 / 0.065 ≈ 1,538,461.54
    assert re_est["assumptions"]["cap_rate"] == pytest.approx(0.065, abs=1e-4)
    assert re_est["estimated_value"] == pytest.approx(100000 / 0.065, rel=1e-3)


def test_estimates_move_with_live_inputs(monkeypatch) -> None:
    # Higher rates -> higher cap rate -> lower real-estate value.
    monkeypatch.setattr(valuation_services, "MarketDataService", lambda: _FakeMarket(ust10y=6.0))
    high = client.get("/api/v1/valuations/estimate", params={"noi": 100000}).json()
    re_high = next(e for e in high["estimates"] if e["asset_class"].startswith("Direct real estate"))

    monkeypatch.setattr(valuation_services, "MarketDataService", lambda: _FakeMarket(ust10y=3.0))
    low = client.get("/api/v1/valuations/estimate", params={"noi": 100000}).json()
    re_low = next(e for e in low["estimates"] if e["asset_class"].startswith("Direct real estate"))

    assert re_high["estimated_value"] < re_low["estimated_value"]


def test_pe_mark_reflects_proxy_move() -> None:
    body = client.get("/api/v1/valuations/estimate", params={"pe_committed": 1000000}).json()
    pe = next(e for e in body["estimates"] if e["asset_class"].startswith("Private equity"))
    # pe_change = -3.0% -> mark = 1,000,000 * 0.97 = 970,000
    assert pe["estimated_value"] == pytest.approx(970000, rel=1e-3)
