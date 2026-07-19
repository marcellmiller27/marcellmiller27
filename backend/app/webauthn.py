# JHI-SIG: 69M2705M | Identity, Auth & Security | JHI Research & Analytics Firm, Inc. (proprietary)
"""Minimal, real WebAuthn assertion verification (ES256 / ECDSA P-256).

This verifies the cryptographic proof a real authenticator produces during
``navigator.credentials.get()``:

1. ``clientDataJSON`` is the challenge the server issued, with ``type ==
   "webauthn.get"``.
2. The signature over ``authenticatorData || SHA256(clientDataJSON)`` validates
   against the credential's stored public key.
3. The signature counter advances (anti-cloning).

Scope note: this implements the common **ES256** case with an SPKI/PEM public
key. Full COSE-key decoding and RS256/EdDSA are future work; the registration
flow should store an EC P-256 public key in PEM form.
"""

from __future__ import annotations

import base64
import hashlib
import json

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_pem_public_key


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _b64url_no_pad(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def verify_es256_assertion(
    public_key_pem: str,
    authenticator_data_b64: str,
    client_data_json_b64: str,
    signature_b64: str,
    expected_challenge: str,
    *,
    previous_sign_count: int = 0,
) -> int:
    """Verify a WebAuthn assertion and return the new signature counter.

    Raises ``ValueError`` on any verification failure.
    """
    try:
        authenticator_data = _b64url_decode(authenticator_data_b64)
        client_data_json = _b64url_decode(client_data_json_b64)
        signature = _b64url_decode(signature_b64)
    except (ValueError, TypeError) as exc:
        raise ValueError("Malformed assertion encoding.") from exc

    # 1) Client data: correct ceremony type and the exact challenge we issued.
    try:
        client_data = json.loads(client_data_json)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid clientDataJSON.") from exc
    if client_data.get("type") != "webauthn.get":
        raise ValueError("Unexpected clientData type.")
    expected_b64 = _b64url_no_pad(expected_challenge.encode("utf-8"))
    if client_data.get("challenge") != expected_b64:
        raise ValueError("Challenge mismatch.")

    # 2) Signature over authenticatorData || SHA256(clientDataJSON).
    if len(authenticator_data) < 37:
        raise ValueError("authenticatorData too short.")
    client_data_hash = hashlib.sha256(client_data_json).digest()
    signed_message = authenticator_data + client_data_hash
    try:
        public_key = load_pem_public_key(public_key_pem.encode("utf-8"))
    except ValueError as exc:
        raise ValueError("Invalid stored public key.") from exc
    if not isinstance(public_key, ec.EllipticCurvePublicKey):
        raise ValueError("Unsupported key type (expected EC P-256 / ES256).")
    try:
        public_key.verify(signature, signed_message, ec.ECDSA(hashes.SHA256()))
    except InvalidSignature as exc:
        raise ValueError("Assertion signature is invalid.") from exc

    # 3) Anti-cloning: the signature counter must advance (unless both are 0).
    new_count = int.from_bytes(authenticator_data[33:37], "big")
    if new_count != 0 or previous_sign_count != 0:
        if new_count <= previous_sign_count:
            raise ValueError("Signature counter did not increase (possible cloned key).")
    return new_count
