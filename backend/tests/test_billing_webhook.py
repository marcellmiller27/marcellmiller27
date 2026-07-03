"""Tests for Stripe webhook signature verification on the billing webhook."""

import hashlib
import hmac
import json
import time
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

WEBHOOK_SECRET = "whsec_test_secret_value"


def _register(plan: str = "professional") -> dict:
    unique = uuid4().hex[:10]
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "organization_name": f"WH Org {unique}",
            "full_name": "WH Tester",
            "email": f"wh-{unique}@example.com",
            "password": "SecurePass123",
            "plan": plan,
        },
    )
    assert resp.status_code == 201
    return resp.json()


def _stripe_signature(payload: bytes, secret: str, *, timestamp: int | None = None) -> str:
    ts = timestamp if timestamp is not None else int(time.time())
    signed = f"{ts}.".encode() + payload
    digest = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
    return f"t={ts},v1={digest}"


def _event_payload(organization_id: str, plan: str = "enterprise") -> bytes:
    event = {
        "id": "evt_test_123",
        "object": "event",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "metadata": {"organization_id": organization_id, "plan": plan},
                "customer": "cus_test_123",
                "subscription": "sub_test_123",
            }
        },
    }
    return json.dumps(event).encode("utf-8")


def test_valid_signature_is_accepted_and_applied(monkeypatch) -> None:
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", WEBHOOK_SECRET)
    registered = _register()
    org_id = registered["organization"]["id"]
    payload = _event_payload(org_id, plan="enterprise")
    sig = _stripe_signature(payload, WEBHOOK_SECRET)

    resp = client.post(
        "/api/v1/billing/webhook",
        content=payload,
        headers={"stripe-signature": sig, "content-type": "application/json"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "active"
    assert body["plan"] == "enterprise"


def test_forged_signature_is_rejected(monkeypatch) -> None:
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", WEBHOOK_SECRET)
    registered = _register()
    payload = _event_payload(registered["organization"]["id"])
    bad_sig = _stripe_signature(payload, "whsec_wrong_secret")

    resp = client.post(
        "/api/v1/billing/webhook",
        content=payload,
        headers={"stripe-signature": bad_sig, "content-type": "application/json"},
    )
    assert resp.status_code == 400


def test_missing_signature_header_is_rejected(monkeypatch) -> None:
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", WEBHOOK_SECRET)
    registered = _register()
    payload = _event_payload(registered["organization"]["id"])

    resp = client.post(
        "/api/v1/billing/webhook",
        content=payload,
        headers={"content-type": "application/json"},
    )
    assert resp.status_code == 400


def test_dev_fallback_without_secret_uses_internal_shape(monkeypatch) -> None:
    monkeypatch.delenv("STRIPE_WEBHOOK_SECRET", raising=False)
    registered = _register()
    resp = client.post(
        "/api/v1/billing/webhook",
        json={
            "event_type": "checkout.session.completed",
            "organization_id": registered["organization"]["id"],
            "plan": "professional",
            "status": "active",
        },
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "active"
