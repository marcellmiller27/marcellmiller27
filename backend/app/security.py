import base64
import hashlib
import hmac
import json
import os
import time
from datetime import datetime, timedelta, timezone
from secrets import token_bytes
from typing import Any

TOKEN_SECRET = os.getenv("AUTH_JWT_SECRET", "development-only-change-me")
TOKEN_TTL_MINUTES = int(os.getenv("AUTH_TOKEN_TTL_MINUTES", "120"))
TOTP_PERIOD_SECONDS = 30
TOTP_DIGITS = 6


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def token_bytes_urlsafe(num_bytes: int = 24) -> str:
    """Return a URL-safe random string for use as a one-time challenge nonce."""
    return _b64encode(token_bytes(num_bytes))


def hash_password(password: str) -> str:
    salt = token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 210_000)
    return f"pbkdf2_sha256${_b64encode(salt)}${_b64encode(digest)}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, salt_value, digest_value = password_hash.split("$", 2)
    except ValueError:
        return False
    if algorithm != "pbkdf2_sha256":
        return False
    salt = _b64decode(salt_value)
    expected = _b64decode(digest_value)
    actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 210_000)
    return hmac.compare_digest(actual, expected)


def create_access_token(payload: dict[str, Any]) -> str:
    token_payload = {
        **payload,
        "exp": int((datetime.now(timezone.utc) + timedelta(minutes=TOKEN_TTL_MINUTES)).timestamp()),
    }
    body = _b64encode(json.dumps(token_payload, separators=(",", ":")).encode("utf-8"))
    signature = hmac.new(TOKEN_SECRET.encode("utf-8"), body.encode("ascii"), hashlib.sha256).digest()
    return f"{body}.{_b64encode(signature)}"


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        body, signature = token.split(".", 1)
    except ValueError as exc:
        raise ValueError("Invalid token format.") from exc

    expected_signature = hmac.new(
        TOKEN_SECRET.encode("utf-8"),
        body.encode("ascii"),
        hashlib.sha256,
    ).digest()
    if not hmac.compare_digest(_b64decode(signature), expected_signature):
        raise ValueError("Invalid token signature.")

    payload = json.loads(_b64decode(body))
    if int(payload["exp"]) < int(datetime.now(timezone.utc).timestamp()):
        raise ValueError("Token expired.")
    return payload


def create_scoped_token(payload: dict[str, Any], scope: str, ttl_minutes: int = 5) -> str:
    """Short-lived token namespaced by ``scope`` (for example "2fa" or "biometric").

    Signing with a scope-specific key means these tokens cannot be replayed as a
    normal access token, and an access token cannot satisfy a scoped challenge.
    """
    secret = f"{TOKEN_SECRET}:{scope}"
    token_payload = {
        **payload,
        "scope": scope,
        "exp": int((datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)).timestamp()),
    }
    body = _b64encode(json.dumps(token_payload, separators=(",", ":")).encode("utf-8"))
    signature = hmac.new(secret.encode("utf-8"), body.encode("ascii"), hashlib.sha256).digest()
    return f"{body}.{_b64encode(signature)}"


def decode_scoped_token(token: str, scope: str) -> dict[str, Any]:
    secret = f"{TOKEN_SECRET}:{scope}"
    try:
        body, signature = token.split(".", 1)
    except ValueError as exc:
        raise ValueError("Invalid token format.") from exc

    expected_signature = hmac.new(
        secret.encode("utf-8"),
        body.encode("ascii"),
        hashlib.sha256,
    ).digest()
    if not hmac.compare_digest(_b64decode(signature), expected_signature):
        raise ValueError("Invalid token signature.")

    payload = json.loads(_b64decode(body))
    if payload.get("scope") != scope:
        raise ValueError("Token scope mismatch.")
    if int(payload["exp"]) < int(datetime.now(timezone.utc).timestamp()):
        raise ValueError("Token expired.")
    return payload


def generate_totp_secret() -> str:
    """Return a base32 TOTP shared secret (RFC 4648 alphabet, no padding)."""
    return base64.b32encode(token_bytes(20)).decode("ascii").rstrip("=")


def _hotp(secret_b32: str, counter: int) -> str:
    padding = "=" * (-len(secret_b32) % 8)
    key = base64.b32decode(secret_b32 + padding, casefold=True)
    digest = hmac.new(key, counter.to_bytes(8, "big"), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    binary = int.from_bytes(digest[offset : offset + 4], "big") & 0x7FFFFFFF
    return str(binary % (10**TOTP_DIGITS)).zfill(TOTP_DIGITS)


def totp_now(secret_b32: str) -> str:
    """Current RFC 6238 TOTP code for the shared secret."""
    return _hotp(secret_b32, int(time.time() // TOTP_PERIOD_SECONDS))


def verify_totp(secret_b32: str, code: str, window: int = 1) -> bool:
    """Validate a TOTP code, tolerating ``window`` steps of clock drift."""
    if not code or not code.strip().isdigit():
        return False
    candidate = code.strip().zfill(TOTP_DIGITS)
    counter = int(time.time() // TOTP_PERIOD_SECONDS)
    return any(
        hmac.compare_digest(_hotp(secret_b32, counter + offset), candidate)
        for offset in range(-window, window + 1)
    )


def totp_provisioning_uri(secret_b32: str, account_name: str, issuer: str) -> str:
    from urllib.parse import quote, urlencode

    label = quote(f"{issuer}:{account_name}")
    query = urlencode(
        {
            "secret": secret_b32,
            "issuer": issuer,
            "digits": TOTP_DIGITS,
            "period": TOTP_PERIOD_SECONDS,
        }
    )
    return f"otpauth://totp/{label}?{query}"
