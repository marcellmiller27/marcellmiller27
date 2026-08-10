# JHI-SIG: 69M2705M | Acquisition Intelligence Framework | JHI Research & Analytics Firm, Inc. (proprietary)
"""Network-free tests for the Acquisition Intelligence Framework."""

from uuid import uuid4

from fastapi.testclient import TestClient

from app.framework_models import RatioInputs
from app.framework_ratios import compute_ratios
from app.main import app

client = TestClient(app)


def test_elements_cover_all_ten_with_tool_links() -> None:
    data = client.get("/api/v1/framework/elements").json()
    ids = {e["id"] for e in data["elements"]}
    expected = {
        "research-target", "financial-analysis", "industry-analysis", "market-analysis",
        "company-analysis", "valuation-considerations", "risk-analysis", "due-diligence",
        "economic-environment", "key-financial-ratios",
    }
    assert expected <= ids
    # Every element carries an explainer, a tool link, and a non-empty checklist.
    for e in data["elements"]:
        assert e["explainer"]["how_to"]
        assert e["explainer"]["what_to_look_for"]
        assert e["explainer"]["why_it_matters"]
        assert e["tool"]["href"].startswith("/")
        assert len(e["checklist"]) >= 3
    assert "research, not investment" in data["disclaimer"].lower()


def test_tool_links_wire_to_existing_modules() -> None:
    data = client.get("/api/v1/framework/elements").json()
    hrefs = {e["tool"]["href"] for e in data["elements"]}
    for required in ("/deal-xray", "/diligence-suite", "/valuation", "/macro"):
        assert required in hrefs


def test_ratios_catalog_lists_required_ratios() -> None:
    data = client.get("/api/v1/framework/ratios/catalog").json()
    keys = {r["key"] for r in data["ratios"]}
    expected = {
        "sde_multiple", "ebitda_multiple", "dscr", "debt_to_ebitda", "gross_margin",
        "operating_margin", "net_margin", "current_ratio", "quick_ratio", "roe",
        "working_capital",
    }
    assert expected <= keys


def test_ratios_compute_values_and_bands() -> None:
    payload = {
        "revenue": 1_000_000,
        "cogs": 400_000,
        "operating_expenses": 400_000,
        "net_income": 120_000,
        "ebitda": 200_000,
        "sde": 250_000,
        "purchase_price": 1_000_000,
        "total_debt": 400_000,
        "total_equity": 600_000,
        "current_assets": 300_000,
        "current_liabilities": 150_000,
        "inventory": 100_000,
        "annual_debt_service": 100_000,
    }
    resp = client.post("/api/v1/framework/ratios/compute", json=payload)
    assert resp.status_code == 200
    by_key = {r["key"]: r for r in resp.json()["results"]}

    assert abs(by_key["gross_margin"]["value"] - 0.6) < 1e-6
    assert by_key["gross_margin"]["status"] == "strong"
    assert abs(by_key["current_ratio"]["value"] - 2.0) < 1e-6
    assert by_key["current_ratio"]["status"] == "strong"
    assert abs(by_key["quick_ratio"]["value"] - (200_000 / 150_000)) < 1e-3
    assert abs(by_key["debt_to_ebitda"]["value"] - 2.0) < 1e-6
    assert abs(by_key["dscr"]["value"] - 2.0) < 1e-6
    assert by_key["dscr"]["status"] == "strong"
    assert abs(by_key["sde_multiple"]["value"] - 4.0) < 1e-6
    assert by_key["working_capital"]["value"] == 150_000


def test_ratios_missing_inputs_are_not_computed() -> None:
    report = compute_ratios(RatioInputs(revenue=1_000_000))
    by_key = {r.key: r for r in report.results}
    # No COGS -> gross margin cannot be computed.
    assert by_key["gross_margin"].value is None
    assert by_key["gross_margin"].status == "n/a"
    # No division by zero anywhere.
    assert all(r.value is not None or r.status == "n/a" for r in report.results)


def test_weak_ratios_are_flagged_in_summary() -> None:
    report = compute_ratios(
        RatioInputs(
            revenue=1_000_000,
            cogs=950_000,  # 5% gross margin -> weak
            ebitda=100_000,
            total_debt=500_000,  # 5x debt/ebitda -> weak
            annual_debt_service=120_000,  # DSCR 0.83 -> weak
        )
    )
    assert "watch" in report.summary.lower()


def test_due_diligence_checklist_categories_and_total() -> None:
    data = client.get("/api/v1/framework/due-diligence").json()
    cat_ids = {c["id"] for c in data["categories"]}
    assert {"financial", "legal", "operational", "commercial", "hr", "it"} <= cat_ids
    total = sum(len(c["items"]) for c in data["categories"])
    assert total == data["total_items"]
    assert total >= 30


def test_industry_benchmarks_are_derived_only() -> None:
    data = client.get("/api/v1/framework/industry-benchmarks").json()
    assert len(data["sectors"]) >= 8
    assert "derived" in data["disclaimer"].lower()
    for s in data["sectors"]:
        assert 0 <= s["gross_margin_pct"] <= 100
        assert s["ev_ebitda_multiple"] > 0


def test_market_analysis_template_shape() -> None:
    data = client.get("/api/v1/framework/market-analysis").json()
    assert len(data["sections"]) >= 4
    assert len(data["five_forces"]) == 5
    assert any(f["key"] == "avg_annual_spend" for f in data["tam_worksheet"])


def test_toolkit_captures_lead_and_returns_resources() -> None:
    email = f"eta-{uuid4().hex[:8]}@example.com"
    before = client.get("/api/v1/framework/lead-count").json()["count"]
    resp = client.post("/api/v1/framework/toolkit", json={"email": email, "full_name": "Sam Searcher"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "captured"
    assert len(body["resources"]) >= 3
    assert body["cta_href"] == "/pricing"
    after = client.get("/api/v1/framework/lead-count").json()["count"]
    assert after == before + 1

    # Idempotent on repeat.
    again = client.post("/api/v1/framework/toolkit", json={"email": email})
    assert again.json()["status"] == "already_on_list"


def test_toolkit_rejects_invalid_email() -> None:
    resp = client.post("/api/v1/framework/toolkit", json={"email": "nope"})
    assert resp.status_code == 400


def test_due_diligence_deal_type_allowed_in_pipeline() -> None:
    resp = client.post(
        "/api/v1/pipeline/deals",
        json={
            "business_name": f"DD Target {uuid4().hex[:6]}",
            "deal_type": "due_diligence",
            "stage": "screen",
            "headline": "Diligence started from the framework",
        },
    )
    assert resp.status_code == 200
    assert resp.json()["deal_type"] == "due_diligence"
