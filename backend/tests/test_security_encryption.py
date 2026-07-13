# JHI-SIG: 69M2705M | At-rest encryption tests | John Henry Investments (proprietary)
"""Tests for at-rest encryption of sensitive fields (TOTP secret)."""

from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select

from app.database import SessionLocal
from app.db_models import UserDB, UserSecurityDB
from app.main import app
from app.security import decrypt_secret, encrypt_secret

client = TestClient(app)

PASSWORD = "SecurePass123"


def _register() -> dict:
    unique = uuid4().hex[:10]
    response = client.post(
        "/api/v1/auth/register",
        json={
            "organization_name": f"Enc Org {unique}",
            "full_name": "Enc Tester",
            "email": f"enc-{unique}@example.com",
            "password": PASSWORD,
            "plan": "consumer",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_encrypt_round_trips() -> None:
    plaintext = "JBSWY3DPEHPK3PXP"
    ciphertext = encrypt_secret(plaintext)
    assert ciphertext != plaintext
    assert ciphertext.startswith("enc:v1:")
    assert decrypt_secret(ciphertext) == plaintext


def test_encrypt_is_non_deterministic() -> None:
    # Fernet embeds a random IV, so two encryptions differ but both decrypt back.
    a = encrypt_secret("same-value")
    b = encrypt_secret("same-value")
    assert a != b
    assert decrypt_secret(a) == decrypt_secret(b) == "same-value"


def test_decrypt_passes_through_legacy_plaintext() -> None:
    # Rows written before this change have no prefix; they must keep working.
    assert decrypt_secret("LEGACYPLAINTEXTSECRET") == "LEGACYPLAINTEXTSECRET"


def test_totp_secret_is_encrypted_at_rest() -> None:
    user = _register()
    headers = {"Authorization": f"Bearer {user['access_token']}"}
    enable = client.post("/api/v1/auth/2fa/enable", headers=headers)
    assert enable.status_code == 200
    plaintext_secret = enable.json()["secret"]

    with SessionLocal() as session:
        db_user = session.scalar(select(UserDB).where(UserDB.email == user["user"]["email"]))
        assert db_user is not None
        row = session.scalar(
            select(UserSecurityDB).where(UserSecurityDB.user_id == db_user.id)
        )
        assert row is not None
        # Stored value must NOT be the raw secret, and must be our encrypted form.
        assert row.totp_secret != plaintext_secret
        assert row.totp_secret.startswith("enc:v1:")
        # It must decrypt back to the secret the user was shown.
        assert decrypt_secret(row.totp_secret) == plaintext_secret


def test_legacy_plaintext_secret_still_verifies() -> None:
    """A pre-existing plaintext secret in the DB must still pass 2FA."""
    from app.security import totp_now

    user = _register()
    headers = {"Authorization": f"Bearer {user['access_token']}"}
    client.post("/api/v1/auth/2fa/enable", headers=headers)

    # Simulate a legacy row by overwriting with a raw (unprefixed) secret.
    legacy_secret = "JBSWY3DPEHPK3PXP"
    with SessionLocal() as session:
        db_user = session.scalar(select(UserDB).where(UserDB.email == user["user"]["email"]))
        row = session.scalar(
            select(UserSecurityDB).where(UserSecurityDB.user_id == db_user.id)
        )
        row.totp_secret = legacy_secret  # no enc:v1: prefix
        session.commit()

    initiate = client.post(
        "/api/v1/auth/login/initiate",
        json={"email": user["user"]["email"], "password": PASSWORD},
    ).json()
    verify = client.post(
        "/api/v1/auth/2fa/verify",
        json={"challenge_token": initiate["challenge_token"], "code": totp_now(legacy_secret)},
    )
    assert verify.status_code == 200
    assert verify.json()["access_token"]
