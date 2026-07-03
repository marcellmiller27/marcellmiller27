"""Tests for JWT access tokens and scoped challenge tokens (PyJWT-backed)."""

import pytest

from app.security import (
    create_access_token,
    create_scoped_token,
    decode_access_token,
    decode_scoped_token,
)


def _claims() -> dict:
    return {"sub": "user-1", "organization_id": "org-1", "role": "admin", "email": "a@b.com"}


def test_access_token_is_standard_jwt_and_round_trips() -> None:
    token = create_access_token(_claims())
    # Standard JWT = three dot-separated segments (header.payload.signature).
    assert token.count(".") == 2
    decoded = decode_access_token(token)
    assert decoded["sub"] == "user-1"
    assert decoded["email"] == "a@b.com"


def test_tampered_access_token_is_rejected() -> None:
    token = create_access_token(_claims())
    tampered = token[:-2] + ("aa" if not token.endswith("aa") else "bb")
    with pytest.raises(ValueError):
        decode_access_token(tampered)


def test_scoped_token_round_trips_with_matching_scope() -> None:
    token = create_scoped_token({"sub": "user-1"}, scope="2fa")
    decoded = decode_scoped_token(token, scope="2fa")
    assert decoded["sub"] == "user-1"
    assert decoded["scope"] == "2fa"


def test_scoped_token_rejected_under_wrong_scope() -> None:
    token = create_scoped_token({"sub": "user-1"}, scope="2fa")
    with pytest.raises(ValueError):
        decode_scoped_token(token, scope="biometric")


def test_scoped_token_cannot_be_used_as_access_token() -> None:
    token = create_scoped_token({"sub": "user-1"}, scope="2fa")
    with pytest.raises(ValueError):
        decode_access_token(token)


def test_access_token_cannot_be_used_as_scoped_token() -> None:
    token = create_access_token(_claims())
    with pytest.raises(ValueError):
        decode_scoped_token(token, scope="2fa")
