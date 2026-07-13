# JHI-SIG: 69M2705M | Gatekeeper P0 tests | John Henry Investments (proprietary)
"""Tests for the System Administrator gatekeeper: RBAC permission checks, admin
user-management endpoints, audit trail, and the ENFORCE_AUTH enforcement flag."""

import os
import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _register(role_label: str = "admin") -> tuple[str, dict]:
    email = f"{role_label}-{uuid.uuid4().hex[:8]}@example.test"
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "organization_name": f"Org {uuid.uuid4().hex[:6]}",
            "full_name": "Test User",
            "email": email,
            "password": "supersecret123",
        },
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    return body["access_token"], body


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_admin_endpoints_require_token() -> None:
    # No token -> 401 even with ENFORCE_AUTH off (admin router is always guarded).
    assert client.get("/api/v1/admin/overview").status_code == 401


def test_admin_overview_and_users() -> None:
    token, _ = _register()
    r = client.get("/api/v1/admin/overview", headers=_auth(token))
    assert r.status_code == 200, r.text
    assert r.json()["total_users"] >= 1
    users = client.get("/api/v1/admin/users", headers=_auth(token))
    assert users.status_code == 200
    assert len(users.json()) >= 1


def test_create_change_role_deactivate_and_audit() -> None:
    token, _ = _register()
    # Create a member user in the admin's org.
    email = f"member-{uuid.uuid4().hex[:8]}@example.test"
    created = client.post(
        "/api/v1/admin/users",
        headers=_auth(token),
        json={"email": email, "full_name": "Member", "role": "investor", "password": "memberpass123"},
    )
    assert created.status_code == 201, created.text
    uid = created.json()["id"]
    assert created.json()["role"] == "investor"

    # Change role.
    changed = client.patch(f"/api/v1/admin/users/{uid}/role", headers=_auth(token), json={"role": "cpa"})
    assert changed.status_code == 200
    assert changed.json()["role"] == "cpa"

    # Deactivate.
    deact = client.patch(f"/api/v1/admin/users/{uid}/active", headers=_auth(token), json={"is_active": False})
    assert deact.status_code == 200
    assert deact.json()["is_active"] is False

    # Reset MFA (no-op but audited).
    assert client.post(f"/api/v1/admin/users/{uid}/reset-mfa", headers=_auth(token)).status_code == 200

    # Audit trail captured admin actions.
    logs = client.get("/api/v1/admin/audit-logs", headers=_auth(token)).json()
    actions = {x["action"] for x in logs}
    assert {"admin.user.created", "admin.user.role_changed", "admin.user.active_changed"}.issubset(actions)


def test_cannot_deactivate_or_demote_self() -> None:
    token, body = _register()
    me_id = body["user"]["id"]
    # Deactivate self -> 400.
    r1 = client.patch(f"/api/v1/admin/users/{me_id}/active", headers=_auth(token), json={"is_active": False})
    assert r1.status_code == 400
    # Demote self from admin -> 400.
    r2 = client.patch(f"/api/v1/admin/users/{me_id}/role", headers=_auth(token), json={"role": "investor"})
    assert r2.status_code == 400


def test_non_admin_is_forbidden() -> None:
    admin_token, _ = _register()
    email = f"inv-{uuid.uuid4().hex[:8]}@example.test"
    client.post(
        "/api/v1/admin/users",
        headers=_auth(admin_token),
        json={"email": email, "full_name": "Investor", "role": "investor", "password": "investorpass1"},
    )
    inv = client.post("/api/v1/auth/login", json={"email": email, "password": "investorpass1"})
    inv_token = inv.json()["access_token"]
    # Investor lacks admin:access -> 403.
    assert client.get("/api/v1/admin/overview", headers=_auth(inv_token)).status_code == 403
    # But has product read permissions in the roles matrix.
    roles = client.get("/api/v1/admin/roles", headers=_auth(admin_token)).json()
    admin_entry = next(x for x in roles if x["role"] == "admin")
    inv_entry = next(x for x in roles if x["role"] == "investor")
    assert "admin:access" in admin_entry["permissions"]
    assert "admin:access" not in inv_entry["permissions"]


def test_enforce_auth_flag_gates_product_endpoints() -> None:
    token, _ = _register()
    os.environ["ENFORCE_AUTH"] = "true"
    try:
        # Product endpoint without token -> 401 when enforced.
        assert client.get("/api/v1/accounting/chart-of-accounts").status_code == 401
        # With a valid token -> allowed through the gate.
        assert client.get("/api/v1/accounting/chart-of-accounts", headers=_auth(token)).status_code == 200
        # Public allowlist (login) still open without a token.
        assert client.post("/api/v1/auth/login", json={"email": "x@y.z", "password": "nope"}).status_code in (401, 400)
    finally:
        os.environ.pop("ENFORCE_AUTH", None)
