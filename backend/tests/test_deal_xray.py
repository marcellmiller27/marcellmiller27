# JHI-SIG: 69M2705M | Acquisition / Deal X-Ray | JHI Research & Analytics Firm, Inc. (proprietary)
"""Tests for the Deal X-Ray CIM analyzer engine + endpoint."""

from fastapi.testclient import TestClient

from app.deal_xray import analyze
from app.deal_xray_models import DealInput
from app.main import app

client = TestClient(app)


def _strong_deal(**overrides) -> DealInput:
    base = dict(
        business_name="Reliable HVAC Co.",
        industry="hvac",
        year_founded=2005,
        revenue=3_000_000,
        revenue_prior=2_600_000,
        reported_ebitda=600_000,
        addbacks=60_000,
        annual_capex=90_000,
        employees=12,
        owner_involvement="semi_absentee",
        equipment_age_years=5,
        customer_concentration_pct=8,
        recurring_revenue_pct=30,
        asking_price=1_800_000,
        down_payment_pct=10,
        seller_note_pct=10,
        loan_rate_pct=11.5,
        loan_term_years=10,
    )
    base.update(overrides)
    return DealInput(**base)


def _weak_deal(**overrides) -> DealInput:
    base = dict(
        business_name="Corner Diner LLC",
        industry="restaurant",
        revenue=1_000_000,
        reported_ebitda=300_000,   # 30% margin — high for a restaurant
        addbacks=180_000,          # 60% of EBITDA — aggressive
        employees=25,
        owner_involvement="owner_critical",
        equipment_age_years=12,
        customer_concentration_pct=40,
        recurring_revenue_pct=0,
        asking_price=1_500_000,    # 5x — rich
        down_payment_pct=5,
        seller_note_pct=0,
    )
    base.update(overrides)
    return DealInput(**base)


def test_strong_deal_scores_well_and_recommends_buy() -> None:
    r = analyze(_strong_deal())
    assert r.deal_score >= 70
    assert r.recommendation == "Buy"
    assert r.ethic_rating >= 80
    assert len(r.segments) == 6  # 6 scored segments + the separate ethic rating
    assert len(r.financing_options) == 3
    best = max(f.dscr for f in r.financing_options if f.dscr is not None)
    assert best >= 1.25


def test_weak_deal_flags_ethics_and_avoids_buy() -> None:
    r = analyze(_weak_deal())
    assert r.ethic_rating < 60
    assert "add-back" in r.ethic_note.lower()
    assert r.recommendation in ("Watch", "Pass")
    # normalization must discount aggressive add-backs below reported EBITDA
    assert r.valuation.normalized_ebitda < 300_000


def test_valuation_verdict_undervalued_and_overvalued() -> None:
    assert analyze(_strong_deal(asking_price=500_000)).valuation.verdict == "undervalued"
    assert analyze(_strong_deal(asking_price=6_000_000)).valuation.verdict == "overvalued"


def test_unfinanceable_deal_is_pass() -> None:
    # Tiny cash flow vs. a rich price → DSCR < 1.0 → Pass
    r = analyze(_weak_deal(reported_ebitda=120_000, addbacks=0, asking_price=2_000_000))
    assert r.recommendation == "Pass"


def test_segments_have_findings_and_weights_sum_to_one() -> None:
    r = analyze(_strong_deal())
    assert all(s.findings for s in r.segments)
    assert abs(sum(s.weight for s in r.segments) - 1.0) < 1e-9


def test_endpoint_analyze_returns_report() -> None:
    payload = {
        "business_name": "Test Plumbing",
        "industry": "plumbing",
        "revenue": 2_000_000,
        "revenue_prior": 1_800_000,
        "reported_ebitda": 400_000,
        "addbacks": 40_000,
        "employees": 10,
        "owner_involvement": "semi_absentee",
        "customer_concentration_pct": 10,
        "recurring_revenue_pct": 20,
        "asking_price": 1_300_000,
    }
    resp = client.post("/api/v1/deal-xray/analyze", json=payload)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert 0 <= body["deal_score"] <= 100
    assert body["recommendation"] in ("Buy", "Watch", "Pass")
    assert body["valuation"]["dcf_enterprise_value"] > 0
    assert len(body["diligence_questions"]) >= 1


def test_endpoint_rejects_invalid_input() -> None:
    resp = client.post("/api/v1/deal-xray/analyze", json={"business_name": "X", "revenue": -5})
    assert resp.status_code == 422


def _cdb_deal(**overrides) -> DealInput:
    """The real Carrollton Design Build CIM — a peak-year, concentrated, volatile deal."""
    base = dict(
        business_name="Carrollton Design Build",
        industry="construction_management",
        year_founded=1984,
        revenue=12_962_195,
        revenue_prior=11_701_091,
        reported_ebitda=2_381_009,
        addbacks=58_745,
        annual_depreciation=56_362,
        earnings_history=[2_381_009, 1_612_599, 827_662, 866_690, 1_345_480],
        employees=14,
        owner_involvement="owner_operated",
        customer_concentration_pct=64,
        recurring_revenue_pct=15,
        asking_price=6_200_000,
        down_payment_pct=10,
        seller_note_pct=0,
    )
    base.update(overrides)
    return DealInput(**base)


def test_valuation_basis_blends_recent_years_not_peak() -> None:
    r = analyze(_cdb_deal())
    # 2-yr average (2,381,009 & 1,612,599) = 1,996,804 — well below the 2025 peak.
    assert 1_990_000 <= r.valuation.normalized_ebitda <= 2_000_000
    assert "2-yr average" in r.valuation.basis_note
    # Priced at ~3.1x the blended basis → fairly priced, NOT undervalued off the peak year.
    assert r.valuation.verdict == "fairly priced"


def test_concentration_and_volatility_dock_the_ethic_rating() -> None:
    r = analyze(_cdb_deal())
    assert r.ethic_rating < 75  # no longer a false "100 / looks credible"
    note = r.ethic_note.lower()
    assert "concentration" in note
    assert "volatil" in note


def test_dcf_is_curbed_not_a_fantasy() -> None:
    r = analyze(_cdb_deal())
    # DCF is bounded to the multiple range (<= high multiple value), never a runaway EV.
    assert r.valuation.dcf_enterprise_value <= r.valuation.multiple_value_high
    # Growth used in the DCF is curbed for concentration + non-recurring revenue.
    assert r.valuation.dcf_assumptions["growth"] <= 0.04
    assert r.valuation.dcf_assumptions["discount_rate_wacc"] >= 0.20


def test_depreciation_used_as_capex_proxy_for_asset_light() -> None:
    # No capex given, but depreciation is → engine uses it instead of a heavy industry estimate.
    r = analyze(_cdb_deal())
    assert r.valuation.dcf_assumptions["capex"] == 56_362
    r_estimate = analyze(_cdb_deal(annual_depreciation=None))
    # Industry estimate would be far larger than the depreciation proxy.
    assert r_estimate.valuation.dcf_assumptions["capex"] > 56_362


def test_construction_management_industry_is_recognized() -> None:
    r = analyze(_cdb_deal())
    # Resilience 50/100 for construction management surfaces in the market segment.
    market = next(s for s in r.segments if s.segment == "Market & durability")
    assert "50/100" in " ".join(market.findings)
