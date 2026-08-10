# JHI-SIG: 69M2705M | Newsletter free-subscriber capture (double opt-in stub) | JHI Research & Analytics Firm, Inc. (proprietary)
"""Minimal free-subscriber capture + list model with a **double opt-in stub**.

A prospective reader subscribes with their email and a cadence preference; the list holds
them as ``pending`` and mints a confirmation token. Confirming the token activates the
subscription. This is the standard double-opt-in shape — but it is a **stub**:

    • It does NOT send any confirmation email (safe by default — nothing goes live).
    • It stores state in-memory (per-process), so it is ideal for wiring the flow and for
      network-free tests.

TODO(persist+send): back this with a persisted table and send the confirmation link via the
existing SES path (``email_service``) once list-management/compliance review is complete.
Broadcasts only ever target CONFIRMED subscribers.
"""

from __future__ import annotations

import re
import secrets
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.newsletter_content import CADENCES

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

_LOCK = threading.Lock()


@dataclass
class Subscription:
    email: str
    cadence: str
    status: str = "pending"  # "pending" | "confirmed" | "unsubscribed"
    confirm_token: str = field(default_factory=lambda: secrets.token_urlsafe(16))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    confirmed_at: datetime | None = None


# In-memory list keyed by lower-cased email (stub — see module docstring).
_SUBS: dict[str, Subscription] = {}


def reset() -> None:
    """Clear the in-memory list (used by tests)."""
    with _LOCK:
        _SUBS.clear()


def _normalize_cadence(cadence: str | None) -> str:
    c = (cadence or "weekly-pulse").strip().lower()
    return c if c in CADENCES else "weekly-pulse"


def subscribe(email: str, cadence: str | None = "weekly-pulse") -> dict:
    """Capture a free subscriber as ``pending`` and mint a confirmation token.

    Never sends an email (stub). Returns a status dict including the ``confirm_token`` the
    caller would embed in a confirmation link. Idempotent for an existing pending/confirmed
    address.
    """
    normalized = email.strip().lower()
    if not _EMAIL_RE.match(normalized):
        return {"status": "invalid", "message": "Enter a valid email address."}
    cadence = _normalize_cadence(cadence)
    with _LOCK:
        existing = _SUBS.get(normalized)
        if existing and existing.status == "confirmed":
            return {"status": "already_confirmed", "email": normalized,
                    "message": "You're already confirmed on the list."}
        if existing and existing.status == "pending":
            return {"status": "pending", "email": normalized,
                    "confirm_token": existing.confirm_token,
                    "message": "Check your inbox to confirm (double opt-in). No email is sent in this stub."}
        sub = Subscription(email=normalized, cadence=cadence)
        _SUBS[normalized] = sub
        return {"status": "pending", "email": normalized, "confirm_token": sub.confirm_token,
                "message": "Almost there — confirm your subscription to finish (double opt-in). "
                           "No confirmation email is sent in this stub."}


def confirm(token: str) -> dict:
    """Activate a pending subscription by its confirmation token (double opt-in step)."""
    with _LOCK:
        for sub in _SUBS.values():
            if sub.confirm_token == token and sub.status == "pending":
                sub.status = "confirmed"
                sub.confirmed_at = datetime.now(timezone.utc)
                return {"status": "confirmed", "email": sub.email,
                        "message": "Subscription confirmed. Welcome to The Main Street Acquirer."}
    return {"status": "invalid", "message": "This confirmation link is invalid or already used."}


def unsubscribe(email: str) -> dict:
    with _LOCK:
        sub = _SUBS.get(email.strip().lower())
        if not sub:
            return {"status": "not_found", "message": "That address is not on the list."}
        sub.status = "unsubscribed"
        return {"status": "unsubscribed", "email": sub.email, "message": "You've been removed from the list."}


def confirmed_recipients(cadence: str | None = None) -> list[str]:
    """Confirmed subscriber emails, optionally filtered to a cadence (broadcast target)."""
    with _LOCK:
        return [
            s.email for s in _SUBS.values()
            if s.status == "confirmed" and (cadence is None or s.cadence == _normalize_cadence(cadence))
        ]


def stats() -> dict:
    with _LOCK:
        confirmed = sum(1 for s in _SUBS.values() if s.status == "confirmed")
        pending = sum(1 for s in _SUBS.values() if s.status == "pending")
    return {"confirmed": confirmed, "pending": pending, "total": confirmed + pending}
