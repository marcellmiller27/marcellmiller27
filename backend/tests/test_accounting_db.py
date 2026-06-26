from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chart_of_accounts_seeded() -> None:
    rows = client.get("/api/v1/accounting/chart-of-accounts").json()
    codes = {a["code"] for a in rows}
    assert {"1000", "4000", "5000"}.issubset(codes)
    # IP capitalization + amortization accounts present.
    assert {"1500", "1510", "1600", "5300", "5400"}.issubset(codes)


def test_capitalize_and_amortize_ip_entries() -> None:
    # Capitalize dev cost.
    cap = client.post(
        "/api/v1/accounting/journal-entries",
        json={
            "entry_date": "2026-07-01",
            "memo": "Capitalize platform development (IP)",
            "lines": [
                {"account_code": "1500", "debit": "180000.00", "credit": "0.00"},
                {"account_code": "1000", "debit": "0.00", "credit": "180000.00"},
            ],
        },
    )
    assert cap.status_code == 201
    # Record one month of amortization.
    amort = client.post(
        "/api/v1/accounting/journal-entries",
        json={
            "entry_date": "2026-07-31",
            "memo": "Monthly IP amortization",
            "lines": [
                {"account_code": "5300", "debit": "5000.00", "credit": "0.00"},
                {"account_code": "1510", "debit": "0.00", "credit": "5000.00"},
            ],
        },
    )
    assert amort.status_code == 201


def test_seeded_trial_balance_is_balanced() -> None:
    body = client.get(
        "/api/v1/accounting/trial-balance",
        params={"period_start": "2026-06-01", "period_end": "2026-06-30"},
    ).json()
    assert body["is_balanced"] is True
    assert body["rows"]
    assert body["total_debits"] == body["total_credits"]


def test_create_balanced_journal_entry() -> None:
    resp = client.post(
        "/api/v1/accounting/journal-entries",
        json={
            "entry_date": "2026-06-24",
            "memo": "Professional subscription payment",
            "source_module": "billing",
            "created_by": "api-test",
            "lines": [
                {"account_code": "1000", "debit": "299.00", "credit": "0.00"},
                {"account_code": "4000", "debit": "0.00", "credit": "299.00"},
            ],
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["memo"] == "Professional subscription payment"
    assert len(body["lines"]) == 2
    assert body["lines"][0]["account_name"] == "Cash and Cash Equivalents"


def test_unknown_account_code_rejected() -> None:
    resp = client.post(
        "/api/v1/accounting/journal-entries",
        json={
            "entry_date": "2026-06-24",
            "memo": "Bad entry",
            "lines": [
                {"account_code": "9999", "debit": "10.00", "credit": "0.00"},
                {"account_code": "4000", "debit": "0.00", "credit": "10.00"},
            ],
        },
    )
    assert resp.status_code == 400


def test_unbalanced_entry_rejected_by_validation() -> None:
    resp = client.post(
        "/api/v1/accounting/journal-entries",
        json={
            "entry_date": "2026-06-24",
            "memo": "Unbalanced",
            "lines": [
                {"account_code": "1000", "debit": "10.00", "credit": "0.00"},
                {"account_code": "4000", "debit": "0.00", "credit": "5.00"},
            ],
        },
    )
    assert resp.status_code == 422


def test_journal_entry_persists_and_filters_by_period() -> None:
    client.post(
        "/api/v1/accounting/journal-entries",
        json={
            "entry_date": "2026-07-15",
            "memo": "July entry",
            "lines": [
                {"account_code": "1000", "debit": "100.00", "credit": "0.00"},
                {"account_code": "4000", "debit": "0.00", "credit": "100.00"},
            ],
        },
    )
    june = client.get(
        "/api/v1/accounting/journal-entries",
        params={"period_start": "2026-06-01", "period_end": "2026-06-30"},
    ).json()
    july = client.get(
        "/api/v1/accounting/journal-entries",
        params={"period_start": "2026-07-01", "period_end": "2026-07-31"},
    ).json()
    assert all(e["entry_date"].startswith("2026-06") for e in june)
    assert any(e["memo"] == "July entry" for e in july)
