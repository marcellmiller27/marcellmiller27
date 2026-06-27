import base64
import hashlib
import hmac
import os
import time
from datetime import datetime, timedelta, timezone
from secrets import token_bytes
from typing import Any

import jwt
from cryptography.fernet import Fernet, InvalidToken

TOKEN_SECRET = os.getenv("AUTH_JWT_SECRET", "development-only-change-me")
TOKEN_TTL_MINUTES = int(os.getenv("AUTH_TOKEN_TTL_MINUTES", "120"))
TOTP_PERIOD_SECONDS = 30
TOTP_DIGITS = 6

# Prefix marking a value that has been encrypted at rest by ``encrypt_secret``.
# Legacy (plaintext) values lack this prefix and are returned as-is on decrypt,
# so existing rows keep working and get upgraded on the next write.
_ENC_PREFIX = "enc:v1:"


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def token_bytes_urlsafe(num_bytes: int = 24) -> str:
    """Return a URL-safe random string for use as a one-time challenge nonce."""
    return _b64encode(token_bytes(num_bytes))


def _fernet() -> Fernet:
    """Build the symmetric cipher used to encrypt sensitive fields at rest.

    Uses ``APP_ENCRYPTION_KEY`` (a urlsafe-base64 32-byte Fernet key) when set;
    otherwise deterministically derives a key from ``AUTH_JWT_SECRET`` so the
    feature works out of the box in dev/test. In production, set a dedicated
    ``APP_ENCRYPTION_KEY`` and rotate it independently of the signing secret.
    """
    configured = os.getenv("APP_ENCRYPTION_KEY")
    if configured:
        key = configured.encode("ascii")
    else:
        derived = hashlib.sha256(f"fieldenc:{TOKEN_SECRET}".encode("utf-8")).digest()
        key = base64.urlsafe_b64encode(derived)
    return Fernet(key)


def encrypt_secret(plaintext: str) -> str:
    """Encrypt a sensitive value for storage at rest (authenticated, AES-128)."""
    token = _fernet().encrypt(plaintext.encode("utf-8")).decode("ascii")
    return f"{_ENC_PREFIX}{token}"


def decrypt_secret(stored: str) -> str:
    """Return the plaintext for a stored value.

    Backward-compatible: values without the ``enc:v1:`` prefix are treated as
    legacy plaintext and returned unchanged. Raises ``ValueError`` if an
    encrypted value cannot be authenticated (tampering or wrong key).
    """
    if not stored.startswith(_ENC_PREFIX):
        return stored
    token = stored[len(_ENC_PREFIX) :].encode("ascii")
    try:
        return _fernet().decrypt(token).decode("utf-8")
    except InvalidToken as exc:
        raise ValueError("Could not decrypt stored secret.") from exc


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
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_TTL_MINUTES),
    }
    return jwt.encode(token_payload, TOKEN_SECRET, algorithm="HS256")


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, TOKEN_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError as exc:
        raise ValueError(f"Invalid token: {exc}") from exc
    # Reject scoped (2fa/biometric) tokens from being used as access tokens.
    if payload.get("scope") is not None:
        raise ValueError("Scoped token cannot be used as an access token.")
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
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes),
    }
    return jwt.encode(token_payload, secret, algorithm="HS256")


def decode_scoped_token(token: str, scope: str) -> dict[str, Any]:
    secret = f"{TOKEN_SECRET}:{scope}"
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.PyJWTError as exc:
        raise ValueError(f"Invalid token: {exc}") from exc
    if payload.get("scope") != scope:
        raise ValueError("Token scope mismatch.")
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
