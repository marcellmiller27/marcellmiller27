# JHI-SIG: 69M2705M | Acquisition / Deal X-Ray | John Henry Investments (proprietary)
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
    assert r.opportunity_score >= 70
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
    assert 0 <= body["opportunity_score"] <= 100
    assert body["recommendation"] in ("Buy", "Watch", "Pass")
    assert body["valuation"]["dcf_enterprise_value"] > 0
    assert len(body["diligence_questions"]) >= 1


def test_endpoint_rejects_invalid_input() -> None:
    resp = client.post("/api/v1/deal-xray/analyze", json={"business_name": "X", "revenue": -5})
    assert resp.status_code == 422
