from datetime import datetime, timezone
from uuid import uuid4

from fastapi.testclient import TestClient

from app.equity_opportunity_scan import EquityOpportunity, _rank
from app.fundamentals import SOURCE_EDGAR, SOURCE_SF1
from app.main import app
from app.market_models import Quote
from app.market_services import MarketDataService
from app.newsletter_content import EDITION_SLUGS, NEWSLETTER_SYMBOLS, build_edition

client = TestClient(app)


def _q(symbol: str, name: str, price: float, unit: str = "%", asset_class: str = "macro") -> Quote:
    return Quote(symbol=symbol, name=name, asset_class=asset_class, price=price,
                 unit=unit, source="fred")


def _macro_quotes() -> list[Quote]:
    """A fixed, network-free quote set covering the newsletter indicators."""
    return [
        _q("INFLATION", "US CPI", 3.10),
        _q("FED_FUNDS", "Fed Funds", 4.50),
        _q("UST10Y", "10-Year Treasury", 4.20),
        _q("UNEMPLOYMENT", "Unemployment", 4.10),
        _q("RETAIL_SALES", "Retail Sales", 700.0, "USD bn"),
        _q("CONSUMER_SENTIMENT", "Consumer Sentiment", 65.0, "index"),
        _q("INDUSTRIAL_PRODUCTION", "Industrial Production", 102.0, "index"),
        _q("GDP", "GDP", 28000.0, "USD bn"),
        _q("SPX", "S&P 500", 5600.0, "index", "equity"),
        _q("GOLD", "Gold", 2400.0, "USD/oz", "commodity"),
        _q("BTC", "Bitcoin", 65000.0, "USD", "crypto"),
    ]


def _fake_picks() -> list[EquityOpportunity]:
    # Mix of actual sources so the per-ticker provenance disclosure is exercised:
    # SF1 primary for the first three, EDGAR fallback for the last two.
    sources = [SOURCE_SF1, SOURCE_SF1, SOURCE_SF1, SOURCE_EDGAR, SOURCE_EDGAR]
    picks: list[EquityOpportunity] = []
    for i, t in enumerate(["NVDA", "AAPL", "MSFT", "HD", "COST"]):
        picks.append(EquityOpportunity(
            ticker=t, name=f"{t} Inc", score=90.0 - i * 8,
            operating_margin=0.30 - i * 0.02, net_margin=0.22, roe=0.40,
            revenue_cagr=0.15 - i * 0.01, earnings_yield=0.05, price=100.0, market_cap=2e12,
            source=sources[i],
            contributions={"Value": 0.20 - i * 0.04, "Quality": 0.50 - i * 0.05,
                           "Growth": 0.30 - i * 0.04, "Momentum": 0.25 - i * 0.06},
            momentum_12_1=0.30 - i * 0.05,
        ))
    return picks


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


# ── Phase 2: charts / factor decomposition / disclaimers (network-free) ───────
def test_economic_brief_carries_a_server_rendered_chart() -> None:
    now = datetime.now(timezone.utc)
    full = build_edition("economic-brief", _macro_quotes(), now, full=True)
    assert len(full.charts) >= 1
    chart = full.charts[0]
    # Embedded as a base64 PNG data-URI so the frontend <img> + PDF both capture it.
    assert chart.image.startswith("data:image/png;base64,")
    assert len(chart.image) > 1000
    assert chart.caption and chart.source
    # Teaser stays lightweight (no heavy exhibits, gates the anonymous path).
    teaser = build_edition("economic-brief", _macro_quotes(), now, full=False)
    assert teaser.charts == []


def test_charts_are_deterministic() -> None:
    now = datetime.now(timezone.utc)
    a = build_edition("economic-brief", _macro_quotes(), now, full=True)
    b = build_edition("economic-brief", _macro_quotes(), now, full=True)
    assert a.charts[0].image == b.charts[0].image


def test_insider_brief_has_thematic_chart() -> None:
    full = build_edition("insider-briefs", _macro_quotes(), datetime.now(timezone.utc), full=True)
    assert len(full.charts) >= 1
    assert full.charts[0].image.startswith("data:image/png;base64,")


def test_opportunity_scan_surfaces_factor_decomposition(monkeypatch) -> None:
    # Mock the (network) screen so this test is network-free but exercises the real
    # chart/decomposition wiring in build_edition (which imports top_opportunities lazily).
    import app.equity_opportunity_scan as eos
    monkeypatch.setattr(eos, "top_opportunities", lambda n=5, **kw: _fake_picks())

    ed = build_edition("opportunity-scan", _macro_quotes(), datetime.now(timezone.utc), full=True)
    equity = next(g for g in ed.groups if g.heading == "Top equity opportunities")

    # Two derived charts: ranked scores + factor decomposition.
    labels = {c.label for c in equity.charts}
    assert "Top opportunities by score" in labels
    assert "Factor decomposition" in labels
    for c in equity.charts:
        assert c.image.startswith("data:image/png;base64,")

    # Each pick carries a fact-locked factor decomposition + its leading factor tag.
    first = equity.items[0]
    assert "Factor contribution —" in first.body
    assert any(fam in first.tags for fam in ("Value", "Quality", "Growth", "Momentum"))
    # Per-ticker provenance reflects the ACTUAL source used for THAT name (SF1 vs
    # EDGAR), read from the fundamentals provider — governance names the SOURCE only.
    assert "Sharadar SF1 (Nasdaq Data Link)" in (first.source or "")
    assert "primary" in (first.source or "")
    # A ticker sourced from the EDGAR fallback discloses SEC EDGAR (fallback), not SF1.
    edgar_item = next(it for it in equity.items if it.label == "HD")
    assert "SEC EDGAR (fallback)" in (edgar_item.source or "")
    assert "Sharadar SF1" not in (edgar_item.source or "")


_SOURCE_ATTRIBUTION = (
    "Sharadar SF1 (Nasdaq Data Link) — point-in-time fundamentals (primary) · "
    "SEC EDGAR (fallback) · FRED · BLS · market feeds."
)


def test_opportunity_scan_footer_leads_with_sf1_attribution() -> None:
    # SF1 is now the PRIMARY fundamentals source; the footer must say so (not "SEC EDGAR").
    ed = build_edition("opportunity-scan", _macro_quotes(), datetime.now(timezone.utc), full=True)
    assert _SOURCE_ATTRIBUTION in ed.footer


def test_insider_brief_footer_leads_with_sf1_attribution() -> None:
    ed = build_edition("insider-briefs", _macro_quotes(), datetime.now(timezone.utc), full=True)
    assert _SOURCE_ATTRIBUTION in ed.footer


def test_opportunity_scan_methodology_has_attribution_and_disclaimers() -> None:
    ed = build_edition("opportunity-scan", _macro_quotes(), datetime.now(timezone.utc), full=True)
    method = ed.methodology
    assert "Data provided by Nasdaq Data Link / Sharadar." in method
    assert "derived metrics only" in method
    assert "past or simulated performance does not guarantee future results" in method
    assert "pre-registered" in method and "out-of-sample" in method


def test_factor_decomposition_sums_and_families() -> None:
    # _rank is pure (no network): verify the four-family decomposition is exposed and
    # that momentum is neutralized-and-active when supplied for the cohort.
    rows = {}
    for i, t in enumerate(["A", "B", "C", "D", "E", "F"]):
        rows[t] = {
            "operating_margin": 0.1 + i * 0.03, "net_margin": 0.08 + i * 0.02,
            "roe": 0.15 + i * 0.05, "revenue_cagr": 0.05 + i * 0.03,
            "earnings_yield": 0.03 + i * 0.005, "book_yield": 0.02 + i * 0.004,
            "_price": 100.0 + i, "_market_cap": 1e11, "_name": f"{t} Inc",
        }
    momentum = {"A": 0.2, "B": 0.15, "C": 0.5, "D": 0.1, "E": -0.05, "F": 0.0}
    ranked = _rank(rows, 5, momentum=momentum)
    assert ranked and ranked[0].score == 100.0
    for r in ranked:
        assert set(r.contributions) == {"Value", "Quality", "Growth", "Momentum"}
    # With momentum active for the cohort, at least one pick has a non-zero momentum sleeve.
    assert any(abs(r.contributions["Momentum"]) > 0 for r in ranked)


def test_factor_decomposition_degrades_without_momentum() -> None:
    rows = {}
    for i, t in enumerate(["A", "B", "C", "D", "E"]):
        rows[t] = {
            "operating_margin": 0.1 + i * 0.03, "net_margin": 0.08 + i * 0.02,
            "roe": 0.15 + i * 0.05, "revenue_cagr": 0.05 + i * 0.03,
            "earnings_yield": 0.03 + i * 0.005, "book_yield": 0.02 + i * 0.004,
            "_price": 100.0 + i, "_market_cap": 1e11, "_name": f"{t} Inc",
        }
    ranked = _rank(rows, 5, momentum={})  # no momentum history at all
    # Momentum sleeve is inactive → contribution is zero, but the family is still present.
    for r in ranked:
        assert r.contributions["Momentum"] == 0.0
        assert r.momentum_12_1 is None
