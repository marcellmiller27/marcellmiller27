from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_trial_balance_endpoint() -> None:
    response = client.get(
        "/api/v1/accounting/trial-balance",
        params={"period_start": "2026-06-01", "period_end": "2026-06-30"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["is_balanced"] is True
    assert payload["rows"]


def test_create_journal_entry_endpoint() -> None:
    response = client.post(
        "/api/v1/accounting/journal-entries",
        json={
            "entry_date": "2026-06-23",
            "memo": "Consumer subscription payment",
            "source_module": "billing",
            "created_by": "api-test",
            "lines": [
                {"account_code": "1000", "debit": "50.00", "credit": "0.00"},
                {"account_code": "4000", "debit": "0.00", "credit": "50.00"},
            ],
        },
    )

    assert response.status_code == 201
    assert response.json()["memo"] == "Consumer subscription payment"


def test_dashboard_and_crm_summary_endpoints() -> None:
    dashboard_response = client.get("/api/v1/dashboards/executive")
    crm_response = client.get("/api/v1/crm/summary")

    assert dashboard_response.status_code == 200
    assert crm_response.status_code == 200
    assert dashboard_response.json()["metrics"]
    assert crm_response.json()["total_contacts"] >= 1
