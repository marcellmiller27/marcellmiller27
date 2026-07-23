from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.main import app
from app.market_services import MarketDataService
from app.newsletter_content import EDITION_SLUGS, NEWSLETTER_SYMBOLS, build_edition

client = TestClient(app)


def test_every_edition_returns_a_pdf_download() -> None:
    for slug in EDITION_SLUGS:
        response = client.get(f"/api/v1/newsletters/{slug}/pdf")
        assert response.status_code == 200, slug
        assert response.headers["content-type"] == "application/pdf"
        assert response.headers["content-disposition"].startswith("attachment;")
        assert f"jhi-{slug}-" in response.headers["content-disposition"]
        # Valid PDF magic bytes — proves reportlab produced a real document.
        assert response.content[:4] == b"%PDF", slug


def test_unknown_edition_is_404() -> None:
    response = client.get("/api/v1/newsletters/not-a-real-edition/pdf")
    assert response.status_code == 404


def test_full_edition_has_more_content_than_teaser() -> None:
    quotes = MarketDataService().quotes(NEWSLETTER_SYMBOLS).quotes
    now = datetime.now(timezone.utc)

    full = build_edition("economic-brief", quotes, now, full=True)
    teaser = build_edition("economic-brief", quotes, now, full=False)
    assert len(full.groups) == 5
    assert len(teaser.groups) == 1
    assert teaser.teaser is True and full.teaser is False

    scan_full = build_edition("opportunity-scan", quotes, now, full=True)
    scan_teaser = build_edition("opportunity-scan", quotes, now, full=False)
    assert len(scan_full.groups[0].items) == 5
    assert len(scan_teaser.groups[0].items) == 2
