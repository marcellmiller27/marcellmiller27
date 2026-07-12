from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

PERIOD = {"period_start": "2026-06-01", "period_end": "2026-06-30"}


def test_financial_report_from_durable_ledger() -> None:
    body = client.get("/api/v1/reports/financial", params=PERIOD).json()
    labels = {line["label"] for line in body["income_statement"]}
    assert "Net income" in labels
    assert body["balance_sheet"]
    assert "pipeline_coverage" in body["kpis"]


def test_audit_report_counts_entries() -> None:
    body = client.get("/api/v1/reports/audit", params=PERIOD).json()
    assert body["findings"]
    assert body["risk_score"] == 42
    assert any("posted entries reviewed" in f["finding"] for f in body["findings"])


def test_reports_reject_bad_period() -> None:
    bad = client.get(
        "/api/v1/reports/financial",
        params={"period_start": "2026-06-30", "period_end": "2026-06-01"},
    )
    assert bad.status_code == 400


def test_executive_dashboard_from_db() -> None:
    body = client.get("/api/v1/dashboards/executive").json()
    assert body["metrics"]
    labels = {m["label"] for m in body["metrics"]}
    assert {"Cash position", "Weighted CRM pipeline", "Accounting controls"}.issubset(labels)
    assert "cash_position" in body


def test_new_journal_entry_flows_into_financials() -> None:
    before = client.get("/api/v1/reports/financial", params=PERIOD).json()
    before_cash = next(
        line["amount"] for line in before["cash_flow_summary"]
        if line["label"] == "Ending cash position"
    )
    # Post a cash receipt within the period.
    client.post(
        "/api/v1/accounting/journal-entries",
        json={
            "entry_date": "2026-06-20",
            "memo": "Cash receipt for report flow",
            "lines": [
                {"account_code": "1010", "debit": "1234.00", "credit": "0.00"},
                {"account_code": "4000", "debit": "0.00", "credit": "1234.00"},
            ],
        },
    )
    after = client.get("/api/v1/reports/financial", params=PERIOD).json()
    after_cash = next(
        line["amount"] for line in after["cash_flow_summary"]
        if line["label"] == "Ending cash position"
    )
    # Durable ledger: the new entry changes the computed cash position.
    from decimal import Decimal

    assert Decimal(after_cash) == Decimal(before_cash) + Decimal("1234.00")
