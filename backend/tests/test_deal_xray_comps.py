import pytest
from fastapi.testclient import TestClient

from app import edgar_services
from app.deal_xray import analyze, build_comp_benchmark
from app.deal_xray_models import CompanyComp, DealInput
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def _clear_cache():
    edgar_services.reset_cache()
    yield
    edgar_services.reset_cache()


def _deal(**over):
    base = dict(
        business_name="Test SMB",
        industry="general",
        revenue=1_000_000.0,
        reported_ebitda=400_000.0,  # 40% EBITDA margin (high)
        asking_price=1_500_000.0,
    )
    base.update(over)
    return DealInput(**base)


def test_build_comp_benchmark_medians_and_high_margin_flag():
    comps = [
        CompanyComp(ticker="A", entity_name="A Inc", operating_margin=0.10, gross_margin=0.30, net_margin=0.08),
        CompanyComp(ticker="B", entity_name="B Inc", operating_margin=0.20, gross_margin=0.40, net_margin=0.12),
    ]
    bm = build_comp_benchmark(0.40, comps)
    assert bm.median_operating_margin == pytest.approx(0.15)
    assert bm.median_gross_margin == pytest.approx(0.35)
    assert "well above" in bm.comparison  # 0.40 > 0.15 * 1.5


def test_build_comp_benchmark_in_line():
    comps = [CompanyComp(ticker="A", entity_name="A Inc", operating_margin=0.30)]
    bm = build_comp_benchmark(0.25, comps)
    assert "in line" in bm.comparison


def test_analyze_attaches_benchmark_and_flags_high_margin():
    comps = [CompanyComp(ticker="LOW", entity_name="Low Inc", operating_margin=0.10)]
    bm = build_comp_benchmark(0.40, comps)
    report = analyze(_deal(), comp_benchmark=bm)
    assert report.comp_benchmark is not None
    assert report.comp_benchmark.median_operating_margin == pytest.approx(0.10)
    # Financial-quality segment gets a public-comps finding
    assert any("Public comps" in f for f in report.segments[0].findings)
    # Ethic note flags margins far above peers
    assert "public peers" in report.ethic_note


def test_analyze_without_benchmark_is_unchanged():
    report = analyze(_deal())
    assert report.comp_benchmark is None


def _fake_tickers():
    return {
        "0": {"cik_str": 60871, "ticker": "LOW", "title": "Lowes Companies Inc"},
    }


def _fake_facts(_cik):
    def a(val):
        return {"end": "2023-12-31", "val": val, "fy": 2023, "fp": "FY", "form": "10-K"}

    return {
        "entityName": "Lowes Companies Inc",
        "facts": {
            "us-gaap": {
                "Revenues": {"units": {"USD": [a(1000)]}},
                "OperatingIncomeLoss": {"units": {"USD": [a(100)]}},  # 10% op margin
                "NetIncomeLoss": {"units": {"USD": [a(70)]}},
            }
        },
    }


def test_endpoint_with_comp_tickers(monkeypatch):
    monkeypatch.setattr(edgar_services, "company_tickers", _fake_tickers)
    monkeypatch.setattr(edgar_services, "company_facts", _fake_facts)
    payload = _deal().model_dump()
    payload["comp_tickers"] = ["LOW"]
    resp = client.post("/api/v1/deal-xray/analyze", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["comp_benchmark"] is not None
    assert body["comp_benchmark"]["comps"][0]["ticker"] == "LOW"
    assert body["comp_benchmark"]["median_operating_margin"] == pytest.approx(0.10)


def test_endpoint_unknown_comp_ticker_is_listed_unavailable(monkeypatch):
    monkeypatch.setattr(edgar_services, "company_tickers", _fake_tickers)
    monkeypatch.setattr(edgar_services, "company_facts", _fake_facts)
    payload = _deal().model_dump()
    payload["comp_tickers"] = ["NOPE"]
    resp = client.post("/api/v1/deal-xray/analyze", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert "NOPE" in body["comp_benchmark"]["unavailable"]
