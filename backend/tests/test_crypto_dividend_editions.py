# JHI-SIG: 69M2705M | Crypto Intelligence + Dividend Opportunities edition tests | JHI Research & Analytics Firm, Inc. (proprietary)
"""Network-free tests for the two new editions (Crypto Intelligence, Dividend
Opportunities): slugs are registered, both editions assemble deterministically with
injected quotes / a mocked screen, carry charts + attribution, degrade gracefully,
and render to a valid PDF."""

from datetime import datetime, timezone

from app.market_models import Quote
from app.newsletter_content import (
    CADENCES,
    EDITION_CADENCE,
    EDITION_SLUGS,
    build_edition,
    cadence_for,
    editions_for_cadence,
)
from app.pdf_export import newsletter_pdf


def _q(symbol: str, name: str, price: float, unit: str = "%",
       asset_class: str = "macro", change: float | None = None) -> Quote:
    return Quote(symbol=symbol, name=name, asset_class=asset_class, price=price,
                 unit=unit, source="test", change_percent=change)


def _crypto_quotes() -> list[Quote]:
    """A fixed, network-free quote set covering the crypto edition inputs."""
    return [
        _q("INFLATION", "US CPI", 3.10),
        _q("FED_FUNDS", "Fed Funds", 4.50),
        _q("UST10Y", "10-Year Treasury", 4.20),
        _q("BTC", "Bitcoin", 112450.0, "USD", "crypto", 1.8),
        _q("ETH", "Ethereum", 3200.0, "USD", "crypto", -0.4),
        _q("SOL", "Solana", 180.0, "USD", "crypto", 3.2),
        _q("XRP", "XRP", 0.61, "USD", "crypto", 0.1),
        _q("XLM", "Stellar", 0.11, "USD", "crypto", None),
        _q("M2", "M2 Money Supply", 21000.0, "USD bn"),
    ]


class _FakeIdea:
    """Duck-typed stand-in for DividendIdea (what the assembly reads)."""

    def __init__(self, ticker, name, score, dy, cov, roe):
        self.ticker = ticker
        self.name = name
        self.score = score
        self.dividend_yield = dy
        self.coverage = cov
        self.roe = roe
        self.quality_tag = "Coverage"
        self.value_str = f"Score {score:.0f} · {dy * 100:.1f}% yield"
        self.insight = f"{name} scores {score:.0f}/100. Research, not advice."
        self.source_disclosure = "SEC EDGAR (fundamentals — public domain); derived metrics only"


def _fake_ideas():
    return [
        _FakeIdea("JNJ", "Johnson & Johnson", 100.0, 0.031, 1.8, 0.25),
        _FakeIdea("PG", "Procter & Gamble", 75.0, 0.025, 1.6, 0.30),
        _FakeIdea("KO", "Coca-Cola", 50.0, 0.030, 1.4, 0.40),
    ]


# ── Registration ─────────────────────────────────────────────────────────────
def test_new_slugs_are_registered() -> None:
    for slug in ("crypto-intelligence", "dividend-opportunities"):
        assert slug in EDITION_SLUGS
        assert slug in EDITION_CADENCE
        assert cadence_for(slug) in CADENCES
    # The scheduled-generation buckets now include the two new editions.
    assert "crypto-intelligence" in editions_for_cadence("weekly-pulse")
    assert "dividend-opportunities" in editions_for_cadence("monthly-deep-dive")


# ── Crypto Intelligence ──────────────────────────────────────────────────────
def test_crypto_intelligence_assembles() -> None:
    now = datetime.now(timezone.utc)
    full = build_edition("crypto-intelligence", _crypto_quotes(), now, full=True)
    teaser = build_edition("crypto-intelligence", _crypto_quotes(), now, full=False)

    assert full.slug == "crypto-intelligence"
    assert full.title == "Crypto Intelligence"
    assert full.intro  # a thesis
    assert "Bitcoin" in full.intro
    headings = [g.heading for g in full.groups]
    assert headings[0].startswith("Majors")
    assert any(h.startswith("Liquidity") for h in headings)
    assert "The Aegira lens" in headings
    # Full carries the derived 24h-move chart; teaser stays lightweight + gated.
    assert len(full.charts) >= 1
    assert full.charts[0].image.startswith("data:image/png;base64,")
    assert teaser.charts == []
    assert teaser.teaser is True and full.teaser is False
    assert len(full.groups) > len(teaser.groups)


def test_crypto_intelligence_is_deterministic() -> None:
    now = datetime.now(timezone.utc)
    a = build_edition("crypto-intelligence", _crypto_quotes(), now, full=True)
    b = build_edition("crypto-intelligence", _crypto_quotes(), now, full=True)
    assert a.charts[0].image == b.charts[0].image
    assert a.intro == b.intro


def test_crypto_intelligence_degrades_when_crypto_feed_missing() -> None:
    # Only macro quotes — the crypto feed is unavailable. Never omit: the majors are
    # disclosed as pending, and the edition still ships.
    now = datetime.now(timezone.utc)
    macro_only = [_q("INFLATION", "US CPI", 3.10), _q("FED_FUNDS", "Fed Funds", 4.50),
                  _q("UST10Y", "10Y", 4.20)]
    ed = build_edition("crypto-intelligence", macro_only, now, full=True)
    majors = ed.groups[0]
    assert majors.heading.startswith("Majors")
    assert all(it.value.startswith("pending") for it in majors.items)
    # No fabricated chart when there are no released % changes.
    assert ed.charts == []


def test_crypto_methodology_and_disclaimer() -> None:
    ed = build_edition("crypto-intelligence", _crypto_quotes(), datetime.now(timezone.utc), full=True)
    assert "CoinGecko" in ed.methodology
    assert "volatile" in ed.disclaimer.lower()


def test_crypto_intelligence_renders_to_pdf() -> None:
    ed = build_edition("crypto-intelligence", _crypto_quotes(), datetime.now(timezone.utc), full=True)
    pdf = newsletter_pdf(ed)
    assert pdf[:4] == b"%PDF"
    assert len(pdf) > 1000


# ── Dividend Opportunities ───────────────────────────────────────────────────
def _macro_quotes() -> list[Quote]:
    return [_q("INFLATION", "US CPI", 3.10), _q("FED_FUNDS", "Fed Funds", 4.50),
            _q("UST10Y", "10-Year Treasury", 4.20)]


def test_dividend_opportunities_assembles_with_screen(monkeypatch) -> None:
    # Mock the (network) screen so the test is network-free but exercises the real
    # assembly wiring (build_edition imports top_dividend_ideas lazily).
    import app.dividend_opportunities as do
    monkeypatch.setattr(do, "top_dividend_ideas", lambda n=6: _fake_ideas())

    now = datetime.now(timezone.utc)
    full = build_edition("dividend-opportunities", _macro_quotes(), now, full=True)
    teaser = build_edition("dividend-opportunities", _macro_quotes(), now, full=False)

    assert full.slug == "dividend-opportunities"
    assert full.title == "Dividend Opportunities"
    income = next(g for g in full.groups if g.heading.startswith("Income ideas"))
    assert {it.label for it in income.items} == {"JNJ", "PG", "KO"}
    assert all("Dividends" in it.tags for it in income.items)
    # Derived charts on the full edition (yield + income-quality score).
    chart_labels = {c.label for c in income.charts}
    assert "Income-quality score" in chart_labels
    for c in income.charts:
        assert c.image.startswith("data:image/png;base64,")
    # Teaser omits the heavy charts but still gates + ships.
    teaser_income = next((g for g in teaser.groups if g.heading.startswith("Income ideas")), None)
    if teaser_income is not None:
        assert teaser_income.charts == []
    assert teaser.teaser is True and full.teaser is False


def test_dividend_opportunities_degrades_when_screen_empty(monkeypatch) -> None:
    # Screen returns nothing (data gap). Always-Deliver: the edition still ships with
    # the macro context + lens, just without the income-ideas group.
    import app.dividend_opportunities as do
    monkeypatch.setattr(do, "top_dividend_ideas", lambda n=6: [])

    ed = build_edition("dividend-opportunities", _macro_quotes(), datetime.now(timezone.utc), full=True)
    headings = [g.heading for g in ed.groups]
    assert not any(h.startswith("Income ideas") for h in headings)
    assert any(h.startswith("Why income now") for h in headings)
    assert "The Aegira lens" in headings


def test_dividend_opportunities_never_breaks_on_screen_error(monkeypatch) -> None:
    # A screen exception must not abort generation (resilient by contract).
    import app.dividend_opportunities as do

    def _boom(n=6):
        raise RuntimeError("screen exploded")

    monkeypatch.setattr(do, "top_dividend_ideas", _boom)
    ed = build_edition("dividend-opportunities", _macro_quotes(), datetime.now(timezone.utc), full=True)
    assert ed.slug == "dividend-opportunities"
    assert ed.groups  # macro context + lens still present


def test_dividend_methodology_carries_attribution() -> None:
    ed = build_edition("dividend-opportunities", _macro_quotes(), datetime.now(timezone.utc), full=True)
    assert "SEC EDGAR" in ed.methodology
    assert "derived metrics only" in ed.methodology


def test_dividend_opportunities_renders_to_pdf(monkeypatch) -> None:
    import app.dividend_opportunities as do
    monkeypatch.setattr(do, "top_dividend_ideas", lambda n=6: _fake_ideas())
    ed = build_edition("dividend-opportunities", _macro_quotes(), datetime.now(timezone.utc), full=True)
    pdf = newsletter_pdf(ed)
    assert pdf[:4] == b"%PDF"
    assert len(pdf) > 1000


# ── Dividend screen logic (pure, network-free) ───────────────────────────────
def test_dividend_screen_rank_is_pure_and_ordered() -> None:
    from app.dividend_opportunities import _rank

    rows = {}
    for i, t in enumerate(["A", "B", "C", "D", "E"]):
        rows[t] = {
            "dividend_yield": 0.02 + i * 0.005,
            "coverage": 1.2 + i * 0.3,
            "roe": 0.10 + i * 0.05,
            "net_margin": 0.08 + i * 0.02,
            "_payout_ratio": 0.5,
            "_coverage_basis": "free cash flow",
            "_has_coverage": 1.0,
            "_revenue_cagr": 0.05 + i * 0.01,
            "_price": 100.0 + i,
            "_name": f"{t} Inc",
            "_source": "sec_edgar",
        }
    ranked = _rank(rows, 3)
    assert len(ranked) == 3
    assert ranked[0].score == 100.0
    # Scores are monotonically non-increasing down the ranked list.
    assert ranked[0].score >= ranked[1].score >= ranked[2].score
    for idea in ranked:
        assert set(idea.contributions) == set(
            ("dividend_yield", "coverage", "roe", "net_margin")
        )


def test_edgar_dividends_reader_parses_cashflow_tag(monkeypatch) -> None:
    # The additive EDGAR reader normalizes the cash-outflow sign to a positive
    # magnitude and returns None for a non-payer.
    from app import edgar_services

    monkeypatch.setattr(edgar_services, "ticker_to_cik", lambda t: ("0000000001", "Payer Inc"))
    facts = {
        "facts": {
            "us-gaap": {
                "PaymentsOfDividendsCommonStock": {
                    "units": {
                        "USD": [
                            {"form": "10-K", "end": "2025-12-31", "fy": 2025, "val": -1_200_000.0},
                            {"form": "10-K", "end": "2024-12-31", "fy": 2024, "val": -1_000_000.0},
                        ]
                    }
                }
            }
        }
    }
    monkeypatch.setattr(edgar_services, "company_facts", lambda cik10: facts)
    edgar_services.reset_cache()
    assert edgar_services.latest_annual_dividends_paid("PAYER") == 1_200_000.0

    monkeypatch.setattr(edgar_services, "company_facts", lambda cik10: {"facts": {"us-gaap": {}}})
    edgar_services.reset_cache()
    assert edgar_services.latest_annual_dividends_paid("NONPAYER") is None
