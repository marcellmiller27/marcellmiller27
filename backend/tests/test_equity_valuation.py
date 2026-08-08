# JHI-SIG: 69M2705M | Equity valuation engine tests | JHI Research & Analytics Firm, Inc. (proprietary)
"""Tests for the Cross-Asset Valuation & Action Engine (Phase 1, equities): DCF math,
IRR/expected-return consistency, action thresholds, workbook, and resilient degradation.
All data is injected — no network."""

import pytest

from app import equity_valuation as ev
from app.equity_valuation_workbook import equity_valuation_workbook
from app.fundamentals import SOURCE_EDGAR, EquityFundamentals, FundamentalsYear


def _install(monkeypatch, *, net_income=1_000_000_000.0, shares=100_000_000.0,
             rev_first=100.0, rev_last=144.0, name="Acme Corp.", source=SOURCE_EDGAR):
    """Inject a normalized fundamentals bundle at the provider boundary (network-free).

    Patching ``fundamentals.equity_fundamentals`` keeps the DCF tests independent of
    whether SF1 (NASDAQ_DATA_LINK_API_KEY) is configured in the environment.
    """
    bundle = EquityFundamentals(
        ticker="ACME",
        entity_name=name,
        source=source,
        net_income=net_income,
        revenue=rev_last,
        stockholders_equity=5_000_000_000.0,
        operating_margin=0.25,
        net_margin=0.20,
        shares_outstanding=shares,
        years=[
            FundamentalsYear(fiscal_year=2022, revenue=rev_first),
            FundamentalsYear(fiscal_year=2024, revenue=rev_last),
        ],
    )
    monkeypatch.setattr(ev.fundamentals, "equity_fundamentals", lambda t, max_years=5: bundle)


def test_dcf_structure_and_growth_cap(monkeypatch) -> None:
    _install(monkeypatch)
    v = ev.value_equity("ACME", price=50.0, risk_free=0.04)
    # Growth capped at 12% even though the CAGR is 20%.
    assert abs(v.growth_rate - ev.GROWTH_CAP) < 1e-9
    # Discount = risk-free + beta * ERP.
    assert abs(v.discount_rate - (0.04 + ev.DEFAULT_BETA * ev.DEFAULT_EQUITY_RISK_PREMIUM)) < 1e-9
    assert len(v.projected_fcf) == ev.PROJECTION_YEARS == len(v.present_values)
    # Projected FCF grows each year; intrinsic per share is positive.
    assert all(b > a for a, b in zip(v.projected_fcf, v.projected_fcf[1:]))
    assert v.intrinsic_per_share > 0
    assert v.sources and "SEC EDGAR" in v.sources[0]


def test_expected_return_equals_discount_when_price_is_intrinsic(monkeypatch) -> None:
    # If the market price equals intrinsic value, the implied IRR must equal the
    # discount rate used to derive that intrinsic value (internal consistency).
    _install(monkeypatch)
    base = ev.value_equity("ACME", price=50.0, risk_free=0.04)
    at_fair = ev.value_equity("ACME", price=base.intrinsic_per_share, risk_free=0.04)
    assert abs(at_fair.expected_return - at_fair.discount_rate) < 1e-3
    assert abs(at_fair.upside_pct) < 1e-6
    assert at_fair.signal == "Accumulate"


def test_action_signal_thresholds(monkeypatch) -> None:
    _install(monkeypatch)
    fair = ev.value_equity("ACME", price=50.0, risk_free=0.04).intrinsic_per_share
    cheap = ev.value_equity("ACME", price=fair * 0.5, risk_free=0.04)   # +100% upside
    rich = ev.value_equity("ACME", price=fair * 1.5, risk_free=0.04)    # -33% upside
    assert cheap.signal == "Enter" and cheap.upside_pct >= ev.ENTER_UPSIDE
    assert rich.signal == "Sideline" and rich.upside_pct <= ev.SIDELINE_UPSIDE
    # Higher price ⇒ lower expected return (monotonic).
    assert cheap.expected_return > rich.expected_return
    # The written call reflects the signal.
    assert "deploy" in cheap.rationale.lower()
    assert "sideline" in rich.rationale.lower()


def test_non_positive_earnings_raise(monkeypatch) -> None:
    _install(monkeypatch, net_income=-5_000_000.0)
    with pytest.raises(ValueError):
        ev.value_equity("ACME", price=50.0, risk_free=0.04)


def test_sources_reflect_fundamentals_provenance(monkeypatch) -> None:
    from app.fundamentals import SOURCE_SF1

    _install(monkeypatch, source=SOURCE_SF1)
    v = ev.value_equity("ACME", price=50.0, risk_free=0.04)
    assert "Sharadar SF1" in v.sources[0]

    _install(monkeypatch, source=SOURCE_EDGAR)
    v2 = ev.value_equity("ACME", price=50.0, risk_free=0.04)
    assert "SEC EDGAR" in v2.sources[0]


def test_workbook_is_valid_xlsx(monkeypatch) -> None:
    _install(monkeypatch)
    v = ev.value_equity("ACME", price=50.0, risk_free=0.04)
    data = equity_valuation_workbook(v)
    assert data[:2] == b"PK"  # xlsx is a zip archive
    assert len(data) > 2000
