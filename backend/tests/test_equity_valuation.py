# JHI-SIG: 69M2705M | Equity valuation engine tests | JHI Research & Analytics Firm, Inc. (proprietary)
"""Tests for the Cross-Asset Valuation & Action Engine (Phase 1, equities): DCF math,
IRR/expected-return consistency, action thresholds, workbook, and resilient degradation.
All data is injected — no network."""

import pytest

from app import equity_valuation as ev
from app.equity_valuation_workbook import equity_valuation_workbook
from app.fundamentals import SOURCE_EDGAR, EquityFundamentals, FundamentalsYear


def _install(monkeypatch, *, net_income=1_000_000_000.0, shares=100_000_000.0,
             rev_first=100.0, rev_last=144.0, name="Acme Corp.", source=SOURCE_EDGAR,
             revenue=None, gross_margin=None, rnd=None, roic=None, capex=None,
             rnd_first=None, rnd_last=None, years=None):
    """Inject a normalized fundamentals bundle at the provider boundary (network-free).

    Patching ``fundamentals.equity_fundamentals`` keeps the DCF tests independent of
    whether SF1 (NASDAQ_DATA_LINK_API_KEY) is configured in the environment. The
    Valuation 2.0 knobs (``rnd``/``roic``/``gross_margin``/…) default to ``None`` so
    the classic-reduction behaviour of the legacy tests is preserved.
    """
    if years is None:
        years = [
            FundamentalsYear(fiscal_year=2022, revenue=rev_first,
                             rnd=rnd_first, gross_margin=gross_margin),
            FundamentalsYear(fiscal_year=2024, revenue=rev_last,
                             rnd=rnd_last if rnd_last is not None else rnd,
                             gross_margin=gross_margin),
        ]
    bundle = EquityFundamentals(
        ticker="ACME",
        entity_name=name,
        source=source,
        net_income=net_income,
        revenue=revenue if revenue is not None else rev_last,
        stockholders_equity=5_000_000_000.0,
        gross_margin=gross_margin,
        operating_margin=0.25,
        net_margin=0.20,
        shares_outstanding=shares,
        rnd=rnd,
        capex=capex,
        roic=roic,
        years=years,
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


# ── Valuation Framework 2.0 ──────────────────────────────────────────────────
def test_reduces_to_classic_without_innovation_data(monkeypatch) -> None:
    # No R&D and no ROIC ⇒ the 2.0 path must collapse EXACTLY onto the classic DCF.
    _install(monkeypatch)
    v = ev.value_equity("ACME", price=50.0, risk_free=0.04)
    assert v.roic is None
    assert v.high_growth_years == ev.PROJECTION_YEARS
    assert len(v.growth_path) == ev.PROJECTION_YEARS
    assert all(abs(g - v.growth_path[0]) < 1e-12 for g in v.growth_path)  # flat
    assert v.adjusted_owner_earnings == v.base_fcf == v.classic_base_fcf  # net income
    assert abs(v.intrinsic_per_share - v.classic_intrinsic_per_share) < 1e-6
    assert v.archetype == "Classic (industry/value)"
    assert v.growth_cap_used == ev.GROWTH_CAP


def test_rnd_capitalized_lifts_owner_earnings(monkeypatch) -> None:
    # Rising R&D ⇒ positive add-back ⇒ adjusted owner-earnings above raw net income,
    # so a heavy-R&D innovator is not penalized for expensing its investment.
    _install(monkeypatch, net_income=1_000_000_000.0,
             rnd=400_000_000.0, rnd_first=150_000_000.0, rnd_last=400_000_000.0,
             revenue=4_000_000_000.0, gross_margin=0.6, roic=0.25, capex=200_000_000.0)
    v = ev.value_equity("ACME", price=50.0, risk_free=0.04)
    assert v.adjusted_owner_earnings > v.classic_base_fcf
    assert v.rnd_asset > 0
    assert "Capitalized R&D" in v.rnd_treatment
    # Owner-earnings uplift lifts the 2.0 intrinsic above the classic value.
    assert v.intrinsic_per_share > v.classic_intrinsic_per_share


def test_flat_rnd_is_roughly_neutral_on_earnings(monkeypatch) -> None:
    # Steady-state R&D over a full amortization life ⇒ add-back ≈ 0 (no free lunch
    # from capitalization alone; the current spend equals the amortization charge).
    flat = [
        FundamentalsYear(fiscal_year=y, revenue=5_000_000_000.0, rnd=300_000_000.0)
        for y in range(2020, 2025)
    ]
    _install(monkeypatch, net_income=1_000_000_000.0, rnd=300_000_000.0,
             revenue=5_000_000_000.0, years=flat)
    v = ev.value_equity("ACME", price=50.0, risk_free=0.04)
    assert abs(v.adjusted_owner_earnings - v.classic_base_fcf) < 1e-6


def test_roic_above_cost_of_capital_extends_fade(monkeypatch) -> None:
    high = ev.value_equity  # alias for readability
    _install(monkeypatch, roic=0.30, revenue=5_000_000_000.0)
    v = high("ACME", price=50.0, risk_free=0.04)
    assert v.roic == 0.30
    assert v.roic > v.cost_of_capital
    assert v.high_growth_years > ev.PROJECTION_YEARS
    assert len(v.growth_path) == v.high_growth_years
    # Fade is monotonically decreasing toward the terminal rate.
    assert all(a >= b for a, b in zip(v.growth_path, v.growth_path[1:]))
    assert abs(v.growth_path[-1] - ev.TERMINAL_GROWTH) < 1e-9


def test_low_roic_does_not_extend_fade(monkeypatch) -> None:
    _install(monkeypatch, roic=0.05)  # ~ at/below cost of capital
    v = ev.value_equity("ACME", price=50.0, risk_free=0.04)
    assert v.high_growth_years == ev.PROJECTION_YEARS


def test_archetype_and_growth_cap(monkeypatch) -> None:
    _install(monkeypatch, rnd=800_000_000.0, revenue=5_000_000_000.0, gross_margin=0.65)
    innovator = ev.value_equity("ACME", price=50.0, risk_free=0.04)
    assert innovator.archetype == "R&D-intensive innovator"
    assert innovator.growth_cap_used == ev.INNOVATOR_GROWTH_CAP

    _install(monkeypatch, rnd=None, gross_margin=0.30)
    classic = ev.value_equity("ACME", price=50.0, risk_free=0.04)
    assert classic.archetype == "Classic (industry/value)"
    assert classic.growth_cap_used == ev.GROWTH_CAP


def test_moat_score_bounds_and_components(monkeypatch) -> None:
    _install(monkeypatch, net_income=1_000_000_000.0,
             rnd=900_000_000.0, rnd_first=300_000_000.0, rnd_last=900_000_000.0,
             revenue=5_000_000_000.0, gross_margin=0.70, roic=0.35, capex=300_000_000.0)
    v = ev.value_equity("ACME", price=50.0, risk_free=0.04)
    assert 0.0 <= v.innovation_moat_score <= 100.0
    assert v.innovation_moat_score > 50.0  # strong innovator on every lens
    expected_keys = {
        "rnd_intensity", "rnd_growth", "gross_margin_durability",
        "revenue_growth_durability", "reinvestment_efficiency",
    }
    assert set(v.innovation_moat_components) == expected_keys
    assert abs(sum(v.innovation_moat_components.values()) - v.innovation_moat_score) < 0.5


def test_blend_gives_innovator_a_fairer_read(monkeypatch) -> None:
    # A high-moat innovator whose raw upside sits just under the Enter bar gets the
    # moat credit that tips the blended call to Enter — while the classic view is
    # kept as a disclosed component (both shown).
    _install(monkeypatch, net_income=1_000_000_000.0,
             rnd=900_000_000.0, rnd_first=300_000_000.0, rnd_last=900_000_000.0,
             revenue=5_000_000_000.0, gross_margin=0.70, roic=0.35, capex=300_000_000.0)
    fair = ev.value_equity("ACME", price=50.0, risk_free=0.04)
    # Price the name so raw upside is just below +20% but the moat credit clears it.
    price = fair.intrinsic_per_share / (1.0 + (ev.ENTER_UPSIDE - 0.05))
    v = ev.value_equity("ACME", price=price, risk_free=0.04)
    assert v.upside_pct < ev.ENTER_UPSIDE                      # raw margin below bar
    assert v.composite_margin >= ev.ENTER_UPSIDE              # moat credit clears it
    assert v.signal == "Enter"
    assert v.classic_signal in {"Enter", "Accumulate", "Sideline"}  # disclosed component present
    assert v.composite_margin > v.upside_pct                  # credit is additive


def test_notes_and_sources_disclose_assumptions(monkeypatch) -> None:
    _install(monkeypatch, rnd=800_000_000.0, revenue=5_000_000_000.0,
             gross_margin=0.65, roic=0.30, capex=200_000_000.0)
    v = ev.value_equity("ACME", price=50.0, risk_free=0.04)
    blob = " ".join(v.notes).lower()
    assert "archetype" in blob
    assert "r&d" in blob
    assert "moat" in blob
    assert "roic" in blob
    assert any("research, not investment advice" in n.lower() for n in v.notes)
    assert v.sources and "SEC EDGAR" in v.sources[0]
