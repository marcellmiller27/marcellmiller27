# JHI-SIG: 69M2705M | CRM | John Henry Investments (proprietary)
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _new_contact() -> dict:
    resp = client.post(
        "/api/v1/crm/contacts",
        json={
            "full_name": "Jordan Lee",
            "organization": "Lee Capital",
            "email": f"jordan-{uuid4().hex[:6]}@example.com",
            "role": "Principal",
        },
    )
    assert resp.status_code == 201
    return resp.json()


def test_summary_has_seed_data() -> None:
    body = client.get("/api/v1/crm/summary").json()
    assert body["total_contacts"] >= 1


def test_create_contact_persists_and_lists() -> None:
    contact = _new_contact()
    listed = client.get("/api/v1/crm/contacts").json()
    assert any(c["id"] == contact["id"] for c in listed)


def test_create_deal_requires_existing_contact() -> None:
    contact = _new_contact()
    ok = client.post(
        "/api/v1/crm/deals",
        json={
            "contact_id": contact["id"],
            "name": "Advisory retainer",
            "stage": "qualified",
            "expected_value": "12000.00",
            "probability": 50,
            "next_step": "Schedule intro call",
        },
    )
    assert ok.status_code == 201
    assert ok.json()["contact_id"] == contact["id"]

    bad = client.post(
        "/api/v1/crm/deals",
        json={"contact_id": str(uuid4()), "name": "Ghost deal"},
    )
    assert bad.status_code == 400


def test_create_activity_validates_contact_and_deal() -> None:
    contact = _new_contact()
    deal = client.post(
        "/api/v1/crm/deals",
        json={"contact_id": contact["id"], "name": "Deal", "expected_value": "5000.00"},
    ).json()

    ok = client.post(
        "/api/v1/crm/activities",
        json={
            "contact_id": contact["id"],
            "deal_id": deal["id"],
            "activity_type": "call",
            "summary": "Discovery call",
        },
    )
    assert ok.status_code == 201

    bad_deal = client.post(
        "/api/v1/crm/activities",
        json={
            "contact_id": contact["id"],
            "deal_id": str(uuid4()),
            "activity_type": "call",
            "summary": "x",
        },
    )
    assert bad_deal.status_code == 400


def test_summary_reflects_new_active_deal() -> None:
    before = client.get("/api/v1/crm/summary").json()
    contact = _new_contact()
    client.post(
        "/api/v1/crm/deals",
        json={
            "contact_id": contact["id"],
            "name": "Pipeline deal",
            "stage": "proposal",
            "expected_value": "10000.00",
            "probability": 40,
            "next_step": "Send proposal",
        },
    )
    after = client.get("/api/v1/crm/summary").json()
    assert after["total_contacts"] == before["total_contacts"] + 1
    assert after["active_deals"] >= before["active_deals"] + 1
    assert "Send proposal" in after["next_actions"]
