# JHI-SIG: 69M2705M | Fundamentals provider tests (SF1 primary, EDGAR fallback) | JHI Research & Analytics Firm, Inc. (proprietary)
"""Unit tests for the point-in-time fundamentals provider.

All network I/O is mocked at the module boundary — no live Sharadar SF1 or SEC EDGAR
calls — so these run identically whether or not NASDAQ_DATA_LINK_API_KEY is set.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app import edgar_services, fundamentals
from app.fundamentals import SOURCE_EDGAR, SOURCE_SF1


# A representative Sharadar SF1 annual (ARY) row (subset of the ~150 real columns).
def _sf1_row(reportperiod: str, *, revenue, netinc, equity, opinc, gp, sharesbas, name="Acme Inc."):
    return {
        "ticker": "ACME",
        "dimension": "ARY",
        "name": name,
        "reportperiod": reportperiod,
        "calendardate": reportperiod,
        "datekey": reportperiod,
        "revenue": revenue,
        "netinc": netinc,
        "equity": equity,
        "opinc": opinc,
        "gp": gp,
        "sharesbas": sharesbas,
    }


def _edgar_fin(name="Edgar Co."):
    return SimpleNamespace(
        entity_name=name, fiscal_year=2024, period_end="2024-12-31",
        revenue=200.0, operating_income=40.0, net_income=30.0,
        stockholders_equity=150.0, gross_margin=0.5, operating_margin=0.2, net_margin=0.15,
    )


def _edgar_hist():
    return SimpleNamespace(years=[
        SimpleNamespace(fiscal_year=2022, revenue=160.0, net_income=20.0,
                        operating_income=30.0, stockholders_equity=120.0),
        SimpleNamespace(fiscal_year=2024, revenue=200.0, net_income=30.0,
                        operating_income=40.0, stockholders_equity=150.0),
    ])


def _install_edgar(monkeypatch, *, fin=None, hist=None, shares=50.0):
    monkeypatch.setattr(fundamentals.edgar_services, "normalize", lambda t: fin or _edgar_fin())
    monkeypatch.setattr(fundamentals.edgar_services, "history", lambda t, max_years=5: hist or _edgar_hist())
    monkeypatch.setattr(fundamentals.edgar_services, "latest_shares_outstanding", lambda t: shares)


def test_sf1_primary_when_key_set_and_field_mapping(monkeypatch) -> None:
    monkeypatch.setattr(fundamentals, "nasdaq_data_link_api_key", lambda: "key")
    rows = [
        _sf1_row("2024-12-31", revenue=1000.0, netinc=200.0, equity=500.0, opinc=300.0, gp=600.0, sharesbas=100.0),
        _sf1_row("2022-12-31", revenue=810.0, netinc=150.0, equity=400.0, opinc=240.0, gp=500.0, sharesbas=110.0),
    ]
    monkeypatch.setattr(fundamentals, "sharadar_sf1_annual", lambda t, limit=6: rows)
    # EDGAR should NOT be needed; make it explode if touched.
    monkeypatch.setattr(fundamentals.edgar_services, "normalize",
                        lambda t: (_ for _ in ()).throw(AssertionError("EDGAR should not be called")))

    f = fundamentals.equity_fundamentals("ACME")
    assert f.source == SOURCE_SF1
    assert f.net_income == 200.0
    assert f.revenue == 1000.0
    assert f.stockholders_equity == 500.0
    assert f.shares_outstanding == 100.0
    # Derived margins: opinc/revenue and netinc/revenue.
    assert f.operating_margin == pytest.approx(0.3)
    assert f.net_margin == pytest.approx(0.2)
    assert f.gross_margin == pytest.approx(0.6)
    # Multi-year series available for CAGR (newest first is fine; helper re-sorts).
    assert {y.fiscal_year for y in f.years} == {2024, 2022}


def test_edgar_fallback_when_no_key(monkeypatch) -> None:
    monkeypatch.setattr(fundamentals, "nasdaq_data_link_api_key", lambda: None)
    # SF1 fetch must never be attempted without a key.
    monkeypatch.setattr(fundamentals, "sharadar_sf1_annual",
                        lambda t, limit=6: (_ for _ in ()).throw(AssertionError("no SF1 without key")))
    _install_edgar(monkeypatch)

    f = fundamentals.equity_fundamentals("ACME")
    assert f.source == SOURCE_EDGAR
    assert f.net_income == 30.0
    assert f.shares_outstanding == 50.0
    assert len(f.years) == 2


def test_edgar_fallback_when_sf1_raises(monkeypatch) -> None:
    monkeypatch.setattr(fundamentals, "nasdaq_data_link_api_key", lambda: "key")
    monkeypatch.setattr(fundamentals, "sharadar_sf1_annual",
                        lambda t, limit=6: (_ for _ in ()).throw(RuntimeError("SF1 down")))
    _install_edgar(monkeypatch)

    f = fundamentals.equity_fundamentals("ACME")
    assert f.source == SOURCE_EDGAR  # resilient: never crashes the caller


def test_edgar_fallback_when_sf1_missing_essential_field(monkeypatch) -> None:
    monkeypatch.setattr(fundamentals, "nasdaq_data_link_api_key", lambda: "key")
    # revenue missing -> SF1 considered unusable -> EDGAR fallback.
    rows = [_sf1_row("2024-12-31", revenue=None, netinc=200.0, equity=500.0, opinc=300.0, gp=600.0, sharesbas=100.0)]
    monkeypatch.setattr(fundamentals, "sharadar_sf1_annual", lambda t, limit=6: rows)
    _install_edgar(monkeypatch)

    f = fundamentals.equity_fundamentals("ACME")
    assert f.source == SOURCE_EDGAR


def test_raises_when_edgar_fallback_also_fails(monkeypatch) -> None:
    monkeypatch.setattr(fundamentals, "nasdaq_data_link_api_key", lambda: None)
    monkeypatch.setattr(fundamentals.edgar_services, "normalize",
                        lambda t: (_ for _ in ()).throw(edgar_services.ProviderError("no EDGAR")))
    with pytest.raises(edgar_services.ProviderError):
        fundamentals.equity_fundamentals("ACME")
