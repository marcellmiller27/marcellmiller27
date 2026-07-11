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


def test_integration_connector_and_office_export_endpoints() -> None:
    connectors_response = client.get("/api/v1/integrations/connectors")
    export_response = client.post(
        "/api/v1/integrations/office/export-package",
        json={
            "document_type": "word_document",
            "template_name": "Audit Summary",
            "source_report": "audit_report",
            "period_start": "2026-06-01",
            "period_end": "2026-06-30",
            "requested_by": "api-test",
        },
    )

    assert connectors_response.status_code == 200
    assert export_response.status_code == 200
    assert any(connector["key"] == "microsoft-365" for connector in connectors_response.json())
    assert export_response.json()["file_name"] == "audit-summary.docx"


def test_integration_connection_sync_and_import_endpoints() -> None:
    connection_response = client.post(
        "/api/v1/integrations/connections",
        json={
            "connector_key": "bill-com",
            "display_name": "Bill.com AP workspace",
            "credential_reference": "secret://bill-com/jhi",
            "enabled": True,
        },
    )
    connection_id = connection_response.json()["id"]

    sync_response = client.post(
        "/api/v1/integrations/sync-jobs",
        json={
            "connection_id": connection_id,
            "object_type": "bills",
            "direction": "import",
            "requested_by": "api-test",
        },
    )
    vendor_bill_response = client.post(
        "/api/v1/integrations/vendor/bills",
        json={
            "connection_id": connection_id,
            "vendor_name": "Vercel",
            "external_id": "bill_api_001",
            "bill_date": "2026-06-23",
            "currency": "USD",
            "lines": [
                {
                    "description": "Application hosting",
                    "account_code": "5000",
                    "amount": "250.00",
                }
            ],
        },
    )

    assert connection_response.status_code == 201
    assert sync_response.status_code == 201
    assert sync_response.json()["status"] == "completed"
    assert vendor_bill_response.status_code == 201
    assert vendor_bill_response.json()["total_amount"] == "250.00"
