from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

PASSWORD = "SecurePass123"


def register_user() -> dict:
    unique = uuid4().hex[:10]
    response = client.post(
        "/api/v1/auth/register",
        json={
            "organization_name": f"Mobile Org {unique}",
            "full_name": "Mobile Tester",
            "email": f"mobile-{unique}@example.com",
            "password": PASSWORD,
            "plan": "consumer",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_password_login_without_2fa_authenticates_directly() -> None:
    user = register_user()
    response = client.post(
        "/api/v1/auth/login/initiate",
        json={"email": user["user"]["email"], "password": PASSWORD},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "authenticated"
    assert body["auth"]["access_token"]


def test_login_initiate_rejects_bad_password() -> None:
    user = register_user()
    response = client.post(
        "/api/v1/auth/login/initiate",
        json={"email": user["user"]["email"], "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_two_factor_enable_and_verify_flow() -> None:
    user = register_user()
    headers = {"Authorization": f"Bearer {user['access_token']}"}

    enable = client.post("/api/v1/auth/2fa/enable", headers=headers)
    assert enable.status_code == 200
    assert enable.json()["enabled"] is True
    assert enable.json()["otpauth_url"].startswith("otpauth://totp/")

    initiate = client.post(
        "/api/v1/auth/login/initiate",
        json={"email": user["user"]["email"], "password": PASSWORD},
    )
    assert initiate.status_code == 200
    body = initiate.json()
    assert body["status"] == "two_factor_required"
    assert body["challenge_token"]
    dev_code = body["dev_code"]
    assert dev_code

    verify = client.post(
        "/api/v1/auth/2fa/verify",
        json={"challenge_token": body["challenge_token"], "code": dev_code},
    )
    assert verify.status_code == 200
    assert verify.json()["access_token"]


def test_two_factor_verify_rejects_bad_code() -> None:
    user = register_user()
    headers = {"Authorization": f"Bearer {user['access_token']}"}
    client.post("/api/v1/auth/2fa/enable", headers=headers)
    initiate = client.post(
        "/api/v1/auth/login/initiate",
        json={"email": user["user"]["email"], "password": PASSWORD},
    ).json()

    verify = client.post(
        "/api/v1/auth/2fa/verify",
        json={"challenge_token": initiate["challenge_token"], "code": "000000"},
    )
    assert verify.status_code == 401


def test_biometric_register_challenge_and_assert_flow() -> None:
    user = register_user()
    email = user["user"]["email"]
    headers = {"Authorization": f"Bearer {user['access_token']}"}
    credential_id = f"cred-{uuid4().hex}"

    register = client.post(
        "/api/v1/auth/biometric/register",
        headers=headers,
        json={"credential_id": credential_id, "label": "iPhone 15"},
    )
    assert register.status_code == 200
    assert register.json()["registered"] is True

    challenge = client.post("/api/v1/auth/biometric/challenge", json={"email": email})
    assert challenge.status_code == 200
    challenge_body = challenge.json()
    assert challenge_body["has_credential"] is True
    assert credential_id in challenge_body["credential_ids"]

    assertion = client.post(
        "/api/v1/auth/biometric/assert",
        json={
            "challenge_token": challenge_body["challenge_token"],
            "credential_id": credential_id,
        },
    )
    assert assertion.status_code == 200
    assert assertion.json()["access_token"]


def test_biometric_challenge_without_device_reports_no_credential() -> None:
    user = register_user()
    challenge = client.post(
        "/api/v1/auth/biometric/challenge", json={"email": user["user"]["email"]}
    )
    assert challenge.status_code == 200
    assert challenge.json()["has_credential"] is False


def test_security_status_reflects_enabled_factors() -> None:
    user = register_user()
    headers = {"Authorization": f"Bearer {user['access_token']}"}
    client.post("/api/v1/auth/2fa/enable", headers=headers)
    client.post(
        "/api/v1/auth/biometric/register",
        headers=headers,
        json={"credential_id": f"cred-{uuid4().hex}", "label": "Pixel 9"},
    )

    status_response = client.get("/api/v1/auth/security/status", headers=headers)
    assert status_response.status_code == 200
    body = status_response.json()
    assert body["two_factor_enabled"] is True
    assert body["biometric_enabled"] is True
    assert body["device_count"] >= 1


def test_two_factor_challenge_token_cannot_be_used_as_bearer() -> None:
    user = register_user()
    headers = {"Authorization": f"Bearer {user['access_token']}"}
    client.post("/api/v1/auth/2fa/enable", headers=headers)
    initiate = client.post(
        "/api/v1/auth/login/initiate",
        json={"email": user["user"]["email"], "password": PASSWORD},
    ).json()

    leaked = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {initiate['challenge_token']}"},
    )
    assert leaked.status_code == 401
