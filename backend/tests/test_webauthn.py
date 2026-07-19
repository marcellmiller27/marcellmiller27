# JHI-SIG: 69M2705M | WebAuthn tests | JHI Research & Analytics Firm, Inc. (proprietary)
"""Tests for real WebAuthn (ES256) biometric assertion verification."""

import base64
import hashlib
import json
import os
from uuid import uuid4

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

PASSWORD = "SecurePass123"


def _b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _register_user() -> dict:
    unique = uuid4().hex[:10]
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "organization_name": f"WA Org {unique}",
            "full_name": "WA Tester",
            "email": f"wa-{unique}@example.com",
            "password": PASSWORD,
            "plan": "consumer",
        },
    )
    assert resp.status_code == 201
    return resp.json()


def _new_keypair():
    private_key = ec.generate_private_key(ec.SECP256R1())
    pem = private_key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii")
    return private_key, pem


def _make_assertion(private_key, nonce: str, *, sign_count: int):
    client_data = {
        "type": "webauthn.get",
        "challenge": _b64url(nonce.encode("utf-8")),
        "origin": "https://app.johnhenry.test",
    }
    client_data_json = json.dumps(client_data).encode("utf-8")
    authenticator_data = b"\x00" * 32 + b"\x01" + sign_count.to_bytes(4, "big")
    signed = authenticator_data + hashlib.sha256(client_data_json).digest()
    signature = private_key.sign(signed, ec.ECDSA(hashes.SHA256()))
    return {
        "authenticator_data": _b64url(authenticator_data),
        "client_data_json": _b64url(client_data_json),
        "signature": _b64url(signature),
    }


def _register_credential(headers, public_key_pem: str) -> str:
    credential_id = f"cred-{uuid4().hex}"
    resp = client.post(
        "/api/v1/auth/biometric/register",
        headers=headers,
        json={"credential_id": credential_id, "public_key": public_key_pem, "label": "iPhone"},
    )
    assert resp.status_code == 200
    return credential_id


def _challenge(email: str) -> dict:
    resp = client.post("/api/v1/auth/biometric/challenge", json={"email": email})
    assert resp.status_code == 200
    return resp.json()


def test_valid_es256_assertion_authenticates() -> None:
    user = _register_user()
    email = user["user"]["email"]
    headers = {"Authorization": f"Bearer {user['access_token']}"}
    private_key, pem = _new_keypair()
    credential_id = _register_credential(headers, pem)

    ch = _challenge(email)
    assertion = _make_assertion(private_key, ch["challenge"], sign_count=1)
    resp = client.post(
        "/api/v1/auth/biometric/assert",
        json={"challenge_token": ch["challenge_token"], "credential_id": credential_id, **assertion},
    )
    assert resp.status_code == 200
    assert resp.json()["access_token"]


def test_tampered_signature_is_rejected() -> None:
    user = _register_user()
    email = user["user"]["email"]
    headers = {"Authorization": f"Bearer {user['access_token']}"}
    private_key, pem = _new_keypair()
    credential_id = _register_credential(headers, pem)

    ch = _challenge(email)
    assertion = _make_assertion(private_key, ch["challenge"], sign_count=1)
    # Flip a byte in the signature.
    bad = bytearray(base64.urlsafe_b64decode(assertion["signature"] + "=="))
    bad[10] ^= 0x01
    assertion["signature"] = _b64url(bytes(bad))
    resp = client.post(
        "/api/v1/auth/biometric/assert",
        json={"challenge_token": ch["challenge_token"], "credential_id": credential_id, **assertion},
    )
    assert resp.status_code == 401


def test_wrong_key_is_rejected() -> None:
    user = _register_user()
    email = user["user"]["email"]
    headers = {"Authorization": f"Bearer {user['access_token']}"}
    _, pem = _new_keypair()
    credential_id = _register_credential(headers, pem)
    attacker_key, _ = _new_keypair()  # signs with a different key

    ch = _challenge(email)
    assertion = _make_assertion(attacker_key, ch["challenge"], sign_count=1)
    resp = client.post(
        "/api/v1/auth/biometric/assert",
        json={"challenge_token": ch["challenge_token"], "credential_id": credential_id, **assertion},
    )
    assert resp.status_code == 401


def test_counter_regression_is_rejected() -> None:
    user = _register_user()
    email = user["user"]["email"]
    headers = {"Authorization": f"Bearer {user['access_token']}"}
    private_key, pem = _new_keypair()
    credential_id = _register_credential(headers, pem)

    # First assertion advances the stored counter to 5.
    ch1 = _challenge(email)
    a1 = _make_assertion(private_key, ch1["challenge"], sign_count=5)
    ok = client.post(
        "/api/v1/auth/biometric/assert",
        json={"challenge_token": ch1["challenge_token"], "credential_id": credential_id, **a1},
    )
    assert ok.status_code == 200

    # Replay with the same (non-increasing) counter must fail.
    ch2 = _challenge(email)
    a2 = _make_assertion(private_key, ch2["challenge"], sign_count=5)
    replay = client.post(
        "/api/v1/auth/biometric/assert",
        json={"challenge_token": ch2["challenge_token"], "credential_id": credential_id, **a2},
    )
    assert replay.status_code == 401


def test_challenge_mismatch_is_rejected() -> None:
    user = _register_user()
    email = user["user"]["email"]
    headers = {"Authorization": f"Bearer {user['access_token']}"}
    private_key, pem = _new_keypair()
    credential_id = _register_credential(headers, pem)

    ch = _challenge(email)
    # Sign a different challenge than the one bound to the token.
    assertion = _make_assertion(private_key, "some-other-nonce", sign_count=1)
    resp = client.post(
        "/api/v1/auth/biometric/assert",
        json={"challenge_token": ch["challenge_token"], "credential_id": credential_id, **assertion},
    )
    assert resp.status_code == 401


def test_presence_only_rejected_in_production(monkeypatch) -> None:
    user = _register_user()
    email = user["user"]["email"]
    headers = {"Authorization": f"Bearer {user['access_token']}"}
    _, pem = _new_keypair()
    credential_id = _register_credential(headers, pem)
    ch = _challenge(email)

    monkeypatch.setenv("APP_ENV", "production")
    resp = client.post(
        "/api/v1/auth/biometric/assert",
        json={"challenge_token": ch["challenge_token"], "credential_id": credential_id},
    )
    assert resp.status_code == 401


def test_presence_only_allowed_in_dev() -> None:
    # Existing demo path: no assertion fields, dev mode -> still authenticates.
    assert os.getenv("APP_ENV", "development") != "production"
    user = _register_user()
    email = user["user"]["email"]
    headers = {"Authorization": f"Bearer {user['access_token']}"}
    credential_id = f"cred-{uuid4().hex}"
    client.post(
        "/api/v1/auth/biometric/register",
        headers=headers,
        json={"credential_id": credential_id, "label": "Pixel"},
    )
    ch = _challenge(email)
    resp = client.post(
        "/api/v1/auth/biometric/assert",
        json={"challenge_token": ch["challenge_token"], "credential_id": credential_id},
    )
    assert resp.status_code == 200
