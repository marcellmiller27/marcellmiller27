# JHI-SIG: 69M2705M | Billing & Subscriptions | John Henry Investments (proprietary)
"""Stripe webhook verification + mapping to the internal billing event shape.

Security: when ``STRIPE_WEBHOOK_SECRET`` is configured, incoming webhooks MUST
carry a valid ``Stripe-Signature`` header, verified with the Stripe SDK. This
prevents forged billing events (e.g. someone POSTing a fake "subscription
active"). When no secret is set (local dev / tests), we fall back to trusting the
internal JSON shape so the mock flow keeps working.
"""

from __future__ import annotations

import json
import os

import stripe

from app.foundation_models import BillingWebhookEvent, SubscriptionPlan, SubscriptionStatus

# Stripe subscription status -> our internal status.
_STRIPE_STATUS_MAP: dict[str, SubscriptionStatus] = {
    "active": SubscriptionStatus.ACTIVE,
    "trialing": SubscriptionStatus.TRIALING,
    "past_due": SubscriptionStatus.PAST_DUE,
    "unpaid": SubscriptionStatus.PAST_DUE,
    "canceled": SubscriptionStatus.CANCELED,
    "incomplete": SubscriptionStatus.INCOMPLETE,
    "incomplete_expired": SubscriptionStatus.CANCELED,
}

# Default status implied by the event type when the object has no status field.
_EVENT_STATUS_DEFAULT: dict[str, SubscriptionStatus] = {
    "checkout.session.completed": SubscriptionStatus.ACTIVE,
    "customer.subscription.deleted": SubscriptionStatus.CANCELED,
    "invoice.payment_failed": SubscriptionStatus.PAST_DUE,
}


def stripe_webhook_secret() -> str | None:
    secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    return secret or None


def verify_and_parse(raw_body: bytes, signature_header: str | None) -> BillingWebhookEvent:
    """Return a validated billing event, verifying the Stripe signature if configured.

    Raises ``ValueError`` on a missing/invalid signature or malformed payload so
    the caller can return HTTP 400.
    """
    secret = stripe_webhook_secret()
    if secret:
        if not signature_header:
            raise ValueError("Missing Stripe-Signature header.")
        try:
            stripe.Webhook.construct_event(raw_body, signature_header, secret)
        except Exception as exc:  # noqa: BLE001 - any failure => reject as 400
            raise ValueError(f"Invalid Stripe webhook signature or payload: {exc}") from exc
        # Signature verified above, so the raw body is authentic; parse it as plain
        # JSON for stable, dict-based access (avoids StripeObject quirks).
        return _map_stripe_event(json.loads(raw_body))

    # Dev / no-secret fallback: trust the internal JSON contract (mock flow).
    try:
        data = json.loads(raw_body or b"{}")
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON body.") from exc
    try:
        return BillingWebhookEvent.model_validate(data)
    except Exception as exc:  # noqa: BLE001 - pydantic validation error => 400
        raise ValueError(f"Invalid webhook body: {exc}") from exc


def _map_stripe_event(event: dict) -> BillingWebhookEvent:
    """Map a verified Stripe Event (as a plain dict) into ``BillingWebhookEvent``.

    We rely on ``metadata.organization_id`` (and optional ``metadata.plan``) being
    set on the Stripe object at checkout time to tie the event back to a tenant.
    """
    event_type = event["type"]
    obj = event.get("data", {}).get("object", {})
    metadata = obj.get("metadata") or {}

    organization_id = metadata.get("organization_id")
    if not organization_id:
        raise ValueError("Stripe event is missing metadata.organization_id.")

    plan: SubscriptionPlan | None = None
    if metadata.get("plan"):
        try:
            plan = SubscriptionPlan(metadata["plan"])
        except ValueError:
            plan = None

    status: SubscriptionStatus | None = None
    obj_status = obj.get("status")
    if obj_status in _STRIPE_STATUS_MAP:
        status = _STRIPE_STATUS_MAP[obj_status]
    else:
        status = _EVENT_STATUS_DEFAULT.get(event_type)

    provider_subscription_id = obj.get("subscription")
    if not provider_subscription_id and event_type.startswith("customer.subscription"):
        provider_subscription_id = obj.get("id")

    return BillingWebhookEvent(
        event_type=event_type,
        organization_id=organization_id,
        plan=plan,
        status=status,
        provider_customer_id=obj.get("customer"),
        provider_subscription_id=provider_subscription_id,
    )
