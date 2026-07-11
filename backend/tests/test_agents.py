from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _route(message: str) -> dict:
    resp = client.post("/api/v1/agents/message", json={"message": message})
    assert resp.status_code == 200
    return resp.json()


def test_roster_has_five_agents_with_profiles() -> None:
    body = client.get("/api/v1/agents").json()
    assert body["count"] == 5
    names = {a["name"].split()[0] for a in body["agents"]}
    assert {"Ava", "Max", "Sage", "Quinn", "Tess"}.issubset(names)
    for a in body["agents"]:
        assert a["avatar"].startswith("/team/")
        assert a["expertise"] and a["background"]


def test_billing_question_routes_to_max() -> None:
    reply = _route("what subscription plans and pricing do you offer?")
    assert reply["agent_name"].startswith("Max")
    assert reply["escalated"] is False


def test_security_question_routes_to_sage() -> None:
    reply = _route("how do I enable two-factor authentication on my account?")
    assert reply["agent_name"].startswith("Sage")


def test_onboarding_question_routes_to_ava() -> None:
    reply = _route("what is John Henry Investments and how do I get started?")
    assert reply["agent_name"].startswith("Ava")


def test_issue_routes_to_tess_and_escalates_to_founder() -> None:
    reply = _route("the dashboard is broken and not working, I'm getting an error")
    assert reply["agent_name"].startswith("Tess")
    assert reply["escalated"] is True
    assert reply["ticket_id"]
    assert "founder" in reply["answer"].lower()


def test_escalated_ticket_visible_to_founder() -> None:
    # Create an escalation
    client.post(
        "/api/v1/agents/message",
        json={"message": "the app crashed and won't load", "user_email": "user@example.test"},
    )
    # Founder (any authenticated user here) can list tickets
    unique = uuid4().hex[:10]
    token = client.post(
        "/api/v1/auth/register",
        json={
            "organization_name": f"Founder Org {unique}",
            "full_name": "Founder",
            "email": f"founder-{unique}@example.com",
            "password": "SecurePass123",
            "plan": "enterprise",
        },
    ).json()["access_token"]

    assert client.get("/api/v1/agents/tickets").status_code == 401
    tickets = client.get(
        "/api/v1/agents/tickets", headers={"Authorization": f"Bearer {token}"}
    )
    assert tickets.status_code == 200
    assert any(t["assigned_to"] == "founder" for t in tickets.json())
