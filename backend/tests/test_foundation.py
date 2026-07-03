# JHI-SIG: 69M2705M | Identity, Auth & Security | John Henry Investments (proprietary)
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def register_user(plan: str = "consumer") -> dict:
    unique = uuid4().hex[:10]
    response = client.post(
        "/api/v1/auth/register",
        json={
            "organization_name": f"John Henry Test Org {unique}",
            "full_name": "Marcellus Miller",
            "email": f"marcellus-{unique}@example.com",
            "password": "SecurePass123",
            "plan": plan,
        },
    )
    assert response.status_code == 201
    return response.json()


def test_register_login_and_me_flow() -> None:
    registered = register_user()
    token = registered["access_token"]

    me_response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert me_response.status_code == 200
    assert me_response.json()["user"]["email"] == registered["user"]["email"]
    assert me_response.json()["organization"]["id"] == registered["organization"]["id"]

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": registered["user"]["email"], "password": "SecurePass123"},
    )

    assert login_response.status_code == 200
    assert login_response.json()["access_token"]


def test_protected_auth_me_rejects_missing_token() -> None:
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_billing_plans_are_public() -> None:
    response = client.get("/api/v1/billing/plans")

    assert response.status_code == 200
    assert {plan["plan"] for plan in response.json()} == {"consumer", "professional", "enterprise"}


def test_checkout_webhook_and_audit_log_flow() -> None:
    registered = register_user("professional")
    token = registered["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    organization_id = registered["organization"]["id"]

    checkout_response = client.post(
        "/api/v1/billing/checkout-session",
        headers=headers,
        json={
            "plan": "enterprise",
            "success_url": "https://app.example.test/success",
            "cancel_url": "https://app.example.test/cancel",
        },
    )
    webhook_response = client.post(
        "/api/v1/billing/webhook",
        json={
            "event_type": "checkout.session.completed",
            "organization_id": organization_id,
            "plan": "enterprise",
            "status": "active",
            "provider_customer_id": "cus_test",
            "provider_subscription_id": "sub_test",
        },
    )
    subscription_response = client.get("/api/v1/billing/subscription", headers=headers)
    audit_response = client.get("/api/v1/billing/audit-logs", headers=headers)

    assert checkout_response.status_code == 200
    assert checkout_response.json()["plan"] == "enterprise"
    assert webhook_response.status_code == 200
    assert webhook_response.json()["status"] == "active"
    assert subscription_response.json()["subscription"]["status"] == "active"
    assert audit_response.status_code == 200
    assert any(log["action"] == "billing.checkout_requested" for log in audit_response.json())
