from uuid import uuid4

from fastapi.testclient import TestClient

from app import research_services
from app.main import app

client = TestClient(app)


def _trending_series(start: float, monthly_drift: float, n: int = 40) -> list[tuple[int, float]]:
    series = []
    price = start
    ts = 1_600_000_000
    for i in range(n):
        price *= 1 + monthly_drift
        series.append((ts + i * 2_592_000, price))
    return series


def test_score_backtest_with_predictive_synthetic_data(monkeypatch) -> None:
    # Construct a universe where higher momentum -> higher forward return, so a
    # momentum score should produce a positive information coefficient.
    drifts = {
        "AAPL": 0.03, "MSFT": 0.025, "GOOGL": 0.02, "AMZN": 0.015, "NVDA": 0.01,
        "JPM": 0.005, "XOM": 0.0, "JNJ": -0.005, "PG": -0.01, "KO": -0.015,
        "SPY": 0.012, "QQQ": 0.018, "GLD": 0.002, "TLT": -0.002, "VNQ": 0.004, "IEF": 0.001,
    }

    def fake_history(symbol, range_="3y", interval="1mo"):
        return _trending_series(100.0, drifts.get(symbol, 0.0))

    monkeypatch.setattr(research_services, "yahoo_chart_history", fake_history)

    response = client.get("/api/v1/research/score-backtest")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["n_assets"] >= 4
    assert body["n_periods"] > 0
    assert body["mean_information_coefficient"] is not None
    # Monotonic drift universe => momentum factor should be positively predictive.
    assert body["mean_information_coefficient"] > 0
    assert body["ic_hit_rate"] > 0.5


def test_score_backtest_handles_provider_outage(monkeypatch) -> None:
    def boom(symbol, range_="3y", interval="1mo"):
        raise RuntimeError("network down")

    monkeypatch.setattr(research_services, "yahoo_chart_history", boom)
    response = client.get("/api/v1/research/score-backtest")
    assert response.status_code == 200
    assert response.json()["status"] == "unavailable"


def test_acquisition_validation_reports_agreement() -> None:
    response = client.get("/api/v1/research/acquisition-validation")
    assert response.status_code == 200
    body = response.json()
    assert body["n_cases"] == 5
    assert 0.0 <= body["agreement_rate"] <= 1.0
    # The engine is tuned to the fixture; expect strong agreement.
    assert body["agreement_rate"] >= 0.8
    assert any("fixture" in d.lower() for d in body["deficiencies"])


def test_data_coverage_lists_live_and_deficient_categories() -> None:
    response = client.get("/api/v1/research/data-coverage")
    assert response.status_code == 200
    body = response.json()
    assert body["live_categories"] >= 6
    assert body["total_categories"] > body["live_categories"]
    categories = {row["category"]: row for row in body["rows"]}
    assert categories["Crypto"]["status"] == "live"
    assert categories["FX / currencies"]["status"] == "live"
    assert categories["Private businesses / SMB"]["status"] == "partial"
    # Every non-live row carries a concrete corrective action.
    for row in body["rows"]:
        if row["status"] != "live":
            assert row["corrective_action"]
    assert len(body["open_deficiencies"]) >= 4


def test_adoption_requires_auth_and_runs_on_real_db() -> None:
    assert client.get("/api/v1/research/adoption").status_code == 401

    unique = uuid4().hex[:10]
    registered = client.post(
        "/api/v1/auth/register",
        json={
            "organization_name": f"Adoption Org {unique}",
            "full_name": "Adoption Tester",
            "email": f"adopt-{unique}@example.com",
            "password": "SecurePass123",
            "plan": "professional",
        },
    ).json()
    headers = {"Authorization": f"Bearer {registered['access_token']}"}

    response = client.get("/api/v1/research/adoption", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["total_users"] >= 1
    assert body["total_organizations"] >= 1
    assert "NON-REPRESENTATIVE" in body["dataset_quality"]
    assert len(body["deficiencies"]) >= 1
