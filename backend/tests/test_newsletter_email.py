# JHI-SIG: 69M2705M | Newsletter email (SES) tests | JHI Research & Analytics Firm, Inc. (proprietary)
"""Tests for the SES newsletter-email layer: Aegira-branded render, JHI legal footer,
safe dry-run when SES is unconfigured, and staff-gating on the send endpoint."""

from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.email_service import (
    email_send_enabled,
    newsletter_email_html,
    newsletter_email_subject,
    send_newsletter_email,
)
from app.main import app
from app.newsletter_content import build_edition

client = TestClient(app)


def _edition():
    return build_edition("economic-brief", [], datetime.now(timezone.utc), full=True)


def test_email_render_is_aegira_branded_with_jhi_legal() -> None:
    ed = _edition()
    subject = newsletter_email_subject(ed)
    html = newsletter_email_html(ed)
    assert "Aegira" in subject
    assert ed.title in html
    assert "By Ellery Vance, VP of Editorial, Aegira (AI)" in html
    # Legal/provenance retained in the footer.
    assert "JHI Research & Analytics Firm, Inc." in html
    assert "JHI-SIG: 69M2705M" in html
    assert html.strip().startswith("<!doctype html")


def test_send_defaults_to_dry_run_when_disabled(monkeypatch) -> None:
    monkeypatch.delenv("ENABLE_EMAIL_SEND", raising=False)
    monkeypatch.delenv("SES_SENDER", raising=False)
    assert email_send_enabled() is False
    res = send_newsletter_email(["founder@jhi.test"], _edition())
    assert res["status"] == "dry_run"
    assert res["provider"] == "none"
    assert res["recipients"] == ["founder@jhi.test"]
    assert "html" in res and _edition().title in res["html"]


def test_send_endpoint_requires_staff_auth() -> None:
    r = client.post("/api/v1/newsletters/economic-brief/send", json={})
    assert r.status_code in (401, 403)
