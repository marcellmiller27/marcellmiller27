from datetime import datetime, timezone
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from app.market_services import MarketDataService
from app.newsletter_content import EDITION_SLUGS, NEWSLETTER_SYMBOLS, build_edition

client = TestClient(app)


def _auth_token() -> str:
    unique = uuid4().hex[:10]
    response = client.post(
        "/api/v1/auth/register",
        json={
            "organization_name": f"Newsletter Test Org {unique}",
            "full_name": "Reader One",
            "email": f"reader-{unique}@example.com",
            "password": "SecurePass123",
        },
    )
    assert response.status_code == 201
    return response.json()["access_token"]


def test_every_edition_returns_a_pdf_download() -> None:
    for slug in EDITION_SLUGS:
        response = client.get(f"/api/v1/newsletters/{slug}/pdf")
        assert response.status_code == 200, slug
        assert response.headers["content-type"] == "application/pdf"
        assert response.headers["content-disposition"].startswith("attachment;")
        assert f"aegira-{slug}-" in response.headers["content-disposition"]
        # Valid PDF magic bytes — proves reportlab produced a real document.
        assert response.content[:4] == b"%PDF", slug


def test_unknown_edition_is_404() -> None:
    response = client.get("/api/v1/newsletters/not-a-real-edition/pdf")
    assert response.status_code == 404


def test_edition_json_endpoint() -> None:
    # The content API that drives on-screen render + PDF + email.
    for slug in EDITION_SLUGS:
        r = client.get(f"/api/v1/newsletters/{slug}")
        assert r.status_code == 200, slug
        body = r.json()
        assert body["edition"]["slug"] == slug
        assert body["edition"]["title"]
        assert isinstance(body["edition"]["groups"], list)
        assert body["as_of"]
        assert body["editorial"] in ("deterministic", "llm") or body["editorial"].startswith(
            "deterministic:"
        )
    assert client.get("/api/v1/newsletters/not-a-real-edition").status_code == 404


def test_pdf_download_is_role_aware() -> None:
    # Anonymous readers get the teaser; an authenticated reader gets the full edition.
    anon = client.get("/api/v1/newsletters/economic-brief/pdf")
    token = _auth_token()
    full = client.get(
        "/api/v1/newsletters/economic-brief/pdf",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert anon.status_code == 200 and full.status_code == 200
    assert anon.content[:4] == b"%PDF" and full.content[:4] == b"%PDF"
    # The full edition (5 sections) is materially larger than the teaser (1 section).
    assert len(full.content) > len(anon.content)


def test_full_edition_has_more_content_than_teaser() -> None:
    quotes = MarketDataService().quotes(NEWSLETTER_SYMBOLS).quotes
    now = datetime.now(timezone.utc)

    full = build_edition("economic-brief", quotes, now, full=True)
    teaser = build_edition("economic-brief", quotes, now, full=False)
    # Analytical arc: 5 sections + cross-asset implications + forward watch.
    assert len(full.groups) == 7
    assert [g.heading for g in full.groups][-2:] == [
        "Cross-asset implications",
        "Forward watch — what would change the read",
    ]
    assert len(teaser.groups) == 1
    assert teaser.teaser is True and full.teaser is False

    scan_full = build_edition("opportunity-scan", quotes, now, full=True)
    scan_teaser = build_edition("opportunity-scan", quotes, now, full=False)
    assert len(scan_full.groups[0].items) == 5
    assert len(scan_teaser.groups[0].items) == 2


def test_economic_brief_thesis_carries_fact_locked_analytics() -> None:
    # The executive thesis should synthesize the read with the derived real-rate cross-link,
    # and every number in it must trace to a released figure or a disclosed reference.
    quotes = MarketDataService().quotes(NEWSLETTER_SYMBOLS).quotes
    ed = build_edition("economic-brief", quotes, datetime.now(timezone.utc), full=True)
    assert "real 10-year yield" in ed.intro.lower()
    # The cross-asset section exposes the derived real-rate and curve facts.
    xa = next(g for g in ed.groups if g.heading == "Cross-asset implications")
    labels = {it.label for it in xa.items}
    assert "Real rates" in labels


def test_insider_brief_is_a_themed_deepdive() -> None:
    quotes = MarketDataService().quotes(NEWSLETTER_SYMBOLS).quotes
    now = datetime.now(timezone.utc)

    full = build_edition("insider-briefs", quotes, now, full=True)
    teaser = build_edition("insider-briefs", quotes, now, full=False)

    assert full.slug == "insider-briefs"
    assert full.title.startswith("Insider Brief —")
    assert full.intro  # a thesis
    headings = [g.heading for g in full.groups]
    assert headings[0].startswith("The setup")
    assert "Why it matters" in headings
    assert "The Aegira lens" in headings
    # Teaser is materially thinner and gated.
    assert len(teaser.groups) == 1 and teaser.teaser is True
    assert len(full.groups) > len(teaser.groups)


def test_insider_brief_theme_selection_is_deterministic() -> None:
    # Same data → same brief (stable theme selection + tie-break).
    quotes = MarketDataService().quotes(NEWSLETTER_SYMBOLS).quotes
    now = datetime.now(timezone.utc)
    a = build_edition("insider-briefs", quotes, now, full=True)
    b = build_edition("insider-briefs", quotes, now, full=True)
    assert a.title == b.title
