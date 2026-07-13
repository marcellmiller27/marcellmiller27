"""Tests for the durable, Postgres/SQLAlchemy-backed integrations endpoints."""

from fastapi.testclient import TestClient

from app.integration_services import IntegrationService
from app.main import app

client = TestClient(app)

BASE = "/api/v1/integrations"


def _create_connection(connector_key: str = "plaid") -> dict:
    resp = client.post(
        f"{BASE}/connections",
        json={
            "connector_key": connector_key,
            "display_name": "Operating bank account",
            "credential_reference": "secret://plaid/item/jhi-operating",
        },
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


def test_connector_registry_includes_banking_vendor_and_office() -> None:
    connectors = {c["key"] for c in client.get(f"{BASE}/connectors").json()}
    assert {"plaid", "bill-com", "microsoft-365"} <= connectors


def test_create_connection_persists_and_lists() -> None:
    conn = _create_connection()
    listed = {c["id"] for c in client.get(f"{BASE}/connections").json()}
    assert conn["id"] in listed
    assert conn["status"] == "connected"


def test_create_sync_job_completes() -> None:
    conn = _create_connection("plaid")
    resp = client.post(
        f"{BASE}/sync-jobs",
        json={
            "connection_id": conn["id"],
            "object_type": "bank_transactions",
            "direction": "import",
            "requested_by": "test",
        },
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["status"] == "completed"
    assert "Plaid Banking" in body["message"]


def test_sync_job_unknown_connection_rejected() -> None:
    resp = client.post(
        f"{BASE}/sync-jobs",
        json={
            "connection_id": "00000000-0000-0000-0000-000000000000",
            "object_type": "bank_transactions",
            "direction": "import",
        },
    )
    assert resp.status_code == 400


def test_sync_job_unsupported_object_type_rejected() -> None:
    conn = _create_connection("plaid")  # banking connector
    resp = client.post(
        f"{BASE}/sync-jobs",
        json={
            "connection_id": conn["id"],
            "object_type": "journal_entries",  # not supported by Plaid
            "direction": "import",
        },
    )
    assert resp.status_code == 400


def test_import_banking_transaction_adds_accounting_suggestion() -> None:
    resp = client.post(
        f"{BASE}/banking/transactions",
        json={
            "transaction_date": "2026-06-23",
            "external_id": "txn_001",
            "account_name": "Operating Checking",
            "description": "OpenAI API usage",
            "amount": "-120.00",
            "counterparty": "OpenAI",
            "category": "AI",
        },
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["suggested_account_code"] == "5100"
    assert body["suggested_journal_memo"]
    # persisted
    assert any(t["external_id"] == "txn_001" for t in client.get(f"{BASE}/banking/transactions").json())


def test_banking_transaction_unknown_connection_rejected() -> None:
    resp = client.post(
        f"{BASE}/banking/transactions",
        json={
            "connection_id": "00000000-0000-0000-0000-000000000000",
            "transaction_date": "2026-06-23",
            "external_id": "txn_x",
            "account_name": "Checking",
            "description": "test",
            "amount": "-10.00",
        },
    )
    assert resp.status_code == 400


def test_import_vendor_bill_creates_balanced_journal_suggestion() -> None:
    resp = client.post(
        f"{BASE}/vendor/bills",
        json={
            "vendor_name": "Microsoft",
            "external_id": "bill_001",
            "bill_date": "2026-06-23",
            "lines": [
                {"description": "Microsoft 365 subscription", "account_code": "5000",
                 "amount": "320.00"}
            ],
        },
    )
    assert resp.status_code == 201, resp.text
    bill = resp.json()
    assert bill["total_amount"] == "320.00"
    debits = sum(float(line["debit"]) for line in bill["suggested_journal_entry"]["lines"])
    credits = sum(float(line["credit"]) for line in bill["suggested_journal_entry"]["lines"])
    assert debits == credits == 320.00
    # persisted + recomputed on read
    listed = client.get(f"{BASE}/vendor/bills").json()
    assert any(b["external_id"] == "bill_001" for b in listed)


def test_office_export_package_for_excel_financial_report() -> None:
    resp = client.post(
        f"{BASE}/office/export-package",
        json={
            "document_type": "excel_workbook",
            "template_name": "Monthly Financial Report",
            "source_report": "financial_report",
            "period_start": "2026-06-01",
            "period_end": "2026-06-30",
            "requested_by": "Marcellus Miller",
        },
    )
    assert resp.status_code == 200, resp.text
    package = resp.json()
    assert package["file_name"] == "monthly-financial-report.xlsx"
    assert "Income Statement" in package["sheets_or_sections"]


def test_connectors_pure_helper() -> None:
    # connectors() needs no DB
    keys = {c.key for c in IntegrationService().connectors()}
    assert "salesforce" in keys and "quickbooks" in keys
