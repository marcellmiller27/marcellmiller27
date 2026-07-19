# JHI-SIG: 69M2705M | Financial Diligence Suite | JHI Research & Analytics Firm, Inc. (proprietary)
"""Tests for the Financial Diligence Suite engine + endpoints."""

from fastapi.testclient import TestClient

from app.financial_diligence import analyze, pricing_band, quote_engagement
from app.financial_diligence_models import DiligenceInput, EngagementRequest
from app.main import app

client = TestClient(app)


def _clean_deal(**overrides) -> DiligenceInput:
    base = dict(
        business_name="Clean Co.",
        industry="professional_services",
        revenue=4_000_000,
        reported_ebitda=1_000_000,
        addbacks_claimed=80_000,
        questionable_addbacks=0,
        one_time_items=0,
        bank_deposits=4_020_000,  # ties out within materiality
        accounts_receivable=300_000,
        inventory=0,
        accounts_payable=180_000,
        recurring_revenue_pct=70,
        customer_concentration_pct=10,
        debt_like_items=0,
    )
    base.update(overrides)
    return DiligenceInput(**base)


def _messy_deal(**overrides) -> DiligenceInput:
    base = dict(
        business_name="Messy Co.",
        revenue=2_000_000,
        reported_ebitda=600_000,
        addbacks_claimed=300_000,      # 50% of EBITDA
        questionable_addbacks=200_000,
        one_time_items=100_000,
        bank_deposits=1_700_000,       # deposits trail revenue 15% → overstatement flag
        accounts_receivable=500_000,
        inventory=400_000,
        accounts_payable=100_000,
        recurring_revenue_pct=0,
        customer_concentration_pct=70,
        debt_like_items=250_000,
    )
    base.update(overrides)
    return DiligenceInput(**base)


def test_ebitda_normalization_discounts_questionable_and_removes_one_time() -> None:
    r = analyze(_messy_deal())
    # 600k - 0.5*200k - 100k = 400k
    assert r.adjusted_ebitda == 400_000
    assert r.ebitda_adjustment == 200_000


def test_proof_of_cash_flags_revenue_overstatement() -> None:
    r = analyze(_messy_deal())
    assert r.proof_of_cash.checked is True
    assert r.proof_of_cash.variance_pct == -15.0
    assert "overstatement" in r.proof_of_cash.flag.lower()


def test_proof_of_cash_skipped_without_deposits() -> None:
    r = analyze(_clean_deal(bank_deposits=None))
    assert r.proof_of_cash.checked is False
    assert any("proof-of-cash" in f.lower() for f in r.red_flags)


def test_net_working_capital_math() -> None:
    r = analyze(_messy_deal())
    # 500k AR + 400k inv - 100k AP = 800k
    assert r.working_capital.net_working_capital == 800_000
    assert r.working_capital.nwc_pct_of_revenue == 40.0


def test_clean_deal_scores_high_messy_scores_low() -> None:
    clean = analyze(_clean_deal())
    messy = analyze(_messy_deal())
    assert clean.financial_integrity_score >= 75
    assert messy.financial_integrity_score < 55
    assert messy.recommended_tier in ("B", "C")


def test_messy_deal_surfaces_multiple_red_flags() -> None:
    r = analyze(_messy_deal())
    joined = " ".join(r.red_flags).lower()
    assert "concentration" in joined
    assert "debt-like" in joined
    assert len(r.red_flags) >= 3


def test_report_is_not_an_audit_opinion() -> None:
    r = analyze(_clean_deal())
    d = r.disclaimer.lower()
    assert "not an audit" in d
    assert "no assurance" in d


def test_pricing_bands_scale_with_ebitda() -> None:
    assert pricing_band(500_000).band.startswith("SBA")
    assert "1M" in pricing_band(2_000_000).band
    assert "3M" in pricing_band(6_000_000).band
    assert "10M" in pricing_band(15_000_000).band
    # platform price undercuts the manual market at every band
    for e in (500_000, 2_000_000, 6_000_000, 15_000_000):
        b = pricing_band(e)
        assert b.platform_high < b.manual_high


def test_engagement_quote_qoe_uses_platform_pricing() -> None:
    q = quote_engagement(EngagementRequest(
        business_name="Target LLC", tier="qoe", target_ebitda=2_000_000,
        state="PA", contact_email="buyer@example.com",
    ))
    assert q.reference.startswith("FDS-")
    assert q.tier_name.startswith("Quality of Earnings")
    assert q.estimated_price_low == 8_000
    assert q.partner_match_status == "pending_match"
    assert len(q.next_steps) >= 3


def test_endpoints_analyze_tiers_pricing_engagement() -> None:
    a = client.post("/api/v1/financial-diligence/analyze", json={
        "business_name": "Endpoint Co.", "revenue": 3_000_000, "reported_ebitda": 700_000,
        "bank_deposits": 3_010_000, "customer_concentration_pct": 15, "recurring_revenue_pct": 40,
    })
    assert a.status_code == 200, a.text
    assert 0 <= a.json()["financial_integrity_score"] <= 100

    t = client.get("/api/v1/financial-diligence/tiers")
    assert t.status_code == 200
    assert {row["tier"] for row in t.json()} == {"A", "B", "C"}

    p = client.get("/api/v1/financial-diligence/pricing")
    assert p.status_code == 200 and len(p.json()) == 4

    e = client.post("/api/v1/financial-diligence/engagement", json={
        "business_name": "Target LLC", "tier": "qoe", "target_ebitda": 6_000_000,
        "state": "GA", "contact_email": "buyer@example.com",
    })
    assert e.status_code == 200, e.text
    assert e.json()["reference"].startswith("FDS-")


def test_endpoint_rejects_invalid_input() -> None:
    resp = client.post("/api/v1/financial-diligence/analyze", json={"business_name": "X", "revenue": 0})
    assert resp.status_code == 422
