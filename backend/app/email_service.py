# JHI-SIG: 69M2705M | Newsletter email (Amazon SES) | JHI Research & Analytics Firm, Inc. (proprietary)
"""Amazon SES delivery for the newsletters — the roadmap's "Step B send".

Design mirrors the editorial LLM layer: **flag-gated and safe by default**. Live send
requires `ENABLE_EMAIL_SEND=1`, a verified `SES_SENDER`, and AWS credentials in the
environment (IAM access key/role with `ses:SendEmail`). When any of those is missing the
service runs in **dry-run** mode: it renders the exact HTML it *would* send and returns a
preview, but calls no external API — so the endpoint and tests work with no AWS access.

Provider: Amazon SES via boto3, lazy-imported inside the send path (like `anthropic` /
`playwright`) so dry-run + tests need no extra dependency installed.
"""

from __future__ import annotations

import logging
import os
from html import escape

from app.newsletter_content import Edition

logger = logging.getLogger(__name__)

# Product brand on the presentation surface; JHI is the legal publisher (footer).
_BRAND = "Aegira"
_ENTITY = "JHI Research & Analytics Firm, Inc."
_SIG = "JHI-SIG: 69M2705M"
_NAVY = "#0C1F33"
_MUTED = "#5A6B7D"


def email_send_enabled() -> bool:
    """True only when live send is explicitly enabled AND a sender is configured.

    Credentials themselves are validated by boto3/SES at call time; this gate keeps the
    default behavior a no-op dry-run so nothing is ever emailed by accident.
    """
    on = os.getenv("ENABLE_EMAIL_SEND", "0").strip().lower() in ("1", "true", "yes", "on")
    return on and bool(os.getenv("SES_SENDER", "").strip())


def _sender() -> str:
    return os.getenv("SES_SENDER", "").strip()


def _region() -> str:
    return os.getenv("AWS_REGION", "").strip() or "us-east-1"


def newsletter_email_subject(edition: Edition) -> str:
    return f"{_BRAND} · {edition.title} — {edition.dateline}"


def newsletter_email_html(edition: Edition) -> str:
    """A self-contained, inline-styled HTML email (email clients ignore <style>/CSS files).

    Aegira masthead + byline on top; JHI legal publisher + JHI-SIG in the footer.
    """
    def p(text: str, size: str = "14px", color: str = _NAVY, weight: str = "400", mt: str = "0") -> str:
        return (
            f'<p style="margin:{mt} 0 8px;font-family:Georgia,\'Times New Roman\',serif;'
            f'font-size:{size};line-height:1.55;color:{color};font-weight:{weight};">{text}</p>'
        )

    rows: list[str] = []
    for g in edition.groups:
        rows.append(
            f'<tr><td style="padding:14px 0 4px;border-top:1px solid #E4E9F0;">'
            f'<span style="font-family:Georgia,serif;font-size:15px;font-weight:700;color:{_NAVY};">'
            f"{escape(g.heading)}</span></td></tr>"
        )
        if g.blurb:
            rows.append(f'<tr><td>{p(escape(g.blurb), size="12px", color=_MUTED)}</td></tr>')
        for it in g.items:
            val = f' <strong style="color:{_NAVY};">{escape(it.value)}</strong>' if it.value else ""
            body = f'<br><span style="color:{_MUTED};font-size:13px;">{escape(it.body)}</span>' if it.body else ""
            rows.append(
                f'<tr><td style="padding:4px 0;font-family:Georgia,serif;font-size:14px;color:{_NAVY};">'
                f"<span>{escape(it.label)}</span>{val}{body}</td></tr>"
            )

    intro = p(escape(edition.intro), size="15px") if edition.intro else ""
    teaser = (
        p(
            "You're reading the free preview. The full edition is included with an "
            f"{_BRAND} subscription.",
            size="12px",
            color=_MUTED,
        )
        if edition.teaser
        else ""
    )

    return f"""\
<!doctype html><html><body style="margin:0;background:#F4F6F9;padding:24px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"
  style="max-width:640px;margin:0 auto;background:#FFFFFF;border:1px solid #E4E9F0;border-radius:10px;">
  <tr><td style="padding:24px 28px;">
    <p style="margin:0 0 2px;font-family:Arial,sans-serif;font-size:11px;letter-spacing:0.12em;
      text-transform:uppercase;color:{_MUTED};">{_BRAND} &middot; {escape(edition.eyebrow)}</p>
    <h1 style="margin:0;font-family:Georgia,serif;font-size:24px;color:{_NAVY};">{escape(edition.title)}</h1>
    <p style="margin:2px 0 0;font-family:Arial,sans-serif;font-size:12px;color:{_MUTED};">
      {escape(edition.dateline)} &middot; By Ellery Vance, VP of Editorial, {_BRAND} (AI)</p>
    <div style="height:1px;background:{_NAVY};margin:14px 0;"></div>
    {intro}
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0">{''.join(rows)}</table>
    {teaser}
    <div style="height:1px;background:#E4E9F0;margin:16px 0;"></div>
    {p(escape(edition.methodology), size="11px", color=_MUTED)}
    {p(f"Prepared by {_ENTITY}. {escape(edition.footer)}", size="11px", color=_MUTED)}
    {p(escape(edition.disclaimer), size="11px", color=_MUTED)}
    <p style="margin:10px 0 0;font-family:Arial,sans-serif;font-size:10px;color:{_MUTED};">
      &copy; 2026 {_ENTITY} &middot; Confidential &mdash; not for redistribution &middot; {_SIG}</p>
  </td></tr>
</table></body></html>"""


def broadcast_editions(recipients: list[str], editions: list[Edition]) -> list[dict]:
    """Send (or dry-run) a batch of editions to the same recipient list.

    Used by the cadence broadcast: each edition is sent independently so one failure
    (or a dry-run) doesn't block the others. Dry-run remains the default when SES is
    unconfigured — nothing is emailed by accident.
    """
    return [send_newsletter_email(recipients, edition) for edition in editions]


def broadcast_by_cadence(
    cadence: str,
    recipients: list[str] | None = None,
    now=None,
    quotes=None,
) -> dict:
    """Generate every edition on a cadence and broadcast it to confirmed subscribers.

    ``recipients`` defaults to the confirmed subscriber list for the cadence. ``quotes`` may
    be injected to keep callers/tests network-free. Live send still requires the SES gate;
    otherwise each edition returns a dry-run preview.
    """
    from app.newsletter_content import generate_scheduled_editions  # lazy: avoid import cycle

    if recipients is None:
        from app.newsletter_subscriptions import confirmed_recipients
        recipients = confirmed_recipients(cadence)

    editions = generate_scheduled_editions(cadence, now=now, quotes=quotes, full=True)
    sends = broadcast_editions(recipients, editions) if recipients else []
    return {
        "cadence": cadence,
        "editions": [e.slug for e in editions],
        "recipient_count": len(recipients),
        "live": email_send_enabled(),
        "results": [{k: v for k, v in s.items() if k != "html"} for s in sends],
        "note": (
            "No confirmed recipients on this cadence — generated editions only."
            if not recipients else
            ("Broadcast sent via SES." if email_send_enabled()
             else "Dry-run: SES not configured, so no email was sent.")
        ),
    }


def send_newsletter_email(recipients: list[str], edition: Edition) -> dict:
    """Send (or dry-run) an edition to recipients. Never raises to the caller on a
    config gap — returns a status dict. Real SES errors propagate so callers see them."""
    subject = newsletter_email_subject(edition)
    html = newsletter_email_html(edition)

    if not email_send_enabled():
        logger.info("Email dry-run (ENABLE_EMAIL_SEND/SES_SENDER not set): %d recipient(s).", len(recipients))
        return {
            "status": "dry_run",
            "provider": "none",
            "recipients": recipients,
            "subject": subject,
            "html": html,
            "reason": "ENABLE_EMAIL_SEND off or SES_SENDER unset — no email was sent.",
        }

    import boto3  # lazy: only needed for a live send

    client = boto3.client("ses", region_name=_region())
    resp = client.send_email(
        Source=_sender(),
        Destination={"ToAddresses": recipients},
        Message={
            "Subject": {"Data": subject, "Charset": "UTF-8"},
            "Body": {"Html": {"Data": html, "Charset": "UTF-8"}},
        },
    )
    return {
        "status": "sent",
        "provider": "ses",
        "recipients": recipients,
        "subject": subject,
        "message_id": resp.get("MessageId"),
    }
