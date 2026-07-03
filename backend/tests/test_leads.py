# JHI-SIG: 69M2705M | Growth / Leads | John Henry Investments (proprietary)
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_capture_lead_and_count() -> None:
    before = client.get("/api/v1/leads/count").json()["count"]
    email = f"lead-{uuid4().hex[:8]}@example.com"
    resp = client.post(
        "/api/v1/leads",
        json={"email": email, "full_name": "Jordan Lee", "interest": "investor"},
    )
    assert resp.status_code == 201
    assert resp.json()["status"] == "captured"
    after = client.get("/api/v1/leads/count").json()["count"]
    assert after == before + 1


def test_duplicate_email_is_idempotent() -> None:
    email = f"dup-{uuid4().hex[:8]}@example.com"
    client.post("/api/v1/leads", json={"email": email})
    second = client.post("/api/v1/leads", json={"email": email})
    assert second.status_code == 201
    assert second.json()["status"] == "already_on_list"


def test_invalid_email_rejected() -> None:
    resp = client.post("/api/v1/leads", json={"email": "not-an-email"})
    assert resp.status_code == 400


def test_list_leads_requires_auth() -> None:
    assert client.get("/api/v1/leads").status_code == 401
