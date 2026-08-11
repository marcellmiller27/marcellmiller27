# JHI-SIG: 69M2705M | Equity Opportunity Scan tests | JHI Research & Analytics Firm, Inc. (proprietary)
"""Tests for the discovery-driven equity Opportunity Scan: scoring/ranking (pure, no
network), CAGR, graceful degradation, and newsletter integration + fact-lock shape."""

from datetime import datetime, timezone
from types import SimpleNamespace

from app import equity_opportunity_scan as scan
from app.fundamentals import SOURCE_EDGAR, SOURCE_SF1
from app.newsletter_content import build_edition


def _factors(op, nm, roe, cagr, ey, by, name, price=100.0, mcap=1e12):
    return {
        "operating_margin": op, "net_margin": nm, "roe": roe, "revenue_cagr": cagr,
        "earnings_yield": ey, "book_yield": by, "_price": price, "_market_cap": mcap, "_name": name,
    }


def test_rank_scores_and_orders_best_first() -> None:
    rows = {
        "STRONG": _factors(0.35, 0.28, 0.40, 0.20, 0.06, 0.10, "Strong Co"),
        "GOOD": _factors(0.25, 0.18, 0.25, 0.12, 0.05, 0.08, "Good Co"),
        "MID": _factors(0.15, 0.10, 0.15, 0.07, 0.04, 0.06, "Mid Co"),
        "WEAK": _factors(0.08, 0.04, 0.08, 0.02, 0.03, 0.04, "Weak Co"),
        "POOR": _factors(0.03, 0.01, 0.03, -0.01, 0.02, 0.03, "Poor Co"),
    }
    out = scan._rank(rows, n=3)
    assert len(out) == 3
    assert out[0].ticker == "STRONG"  # highest across every factor
    assert 0.0 <= out[-1].score <= 100.0 and out[0].score >= out[1].score
    # value string carries the numbers (fact-lock lives in `value`, not prose)
    assert "Score" in out[0].value_str and "%" in out[0].value_str


def test_rank_propagates_actual_per_ticker_source() -> None:
    rows = {
        "SF1CO": {**_factors(0.35, 0.28, 0.40, 0.20, 0.06, 0.10, "SF1 Co"), "_source": SOURCE_SF1},
        "EDGARCO": {**_factors(0.15, 0.10, 0.15, 0.07, 0.04, 0.06, "Edgar Co"), "_source": SOURCE_EDGAR},
        "NASRC": {**_factors(0.08, 0.04, 0.08, 0.02, 0.03, 0.04, "No Src Co")},  # no _source
    }
    out = {o.ticker: o for o in scan._rank(rows, n=3)}
    assert out["SF1CO"].source == SOURCE_SF1
    assert out["EDGARCO"].source == SOURCE_EDGAR
    assert out["NASRC"].source == ""


def test_ticker_source_disclosure_reflects_actual_source(monkeypatch) -> None:
    # SF1 -> primary; EDGAR -> fallback; neither -> attempted source + "no data available".
    sf1 = scan.ticker_source_disclosure(SOURCE_SF1)
    assert "Sharadar SF1 (Nasdaq Data Link)" in sf1 and "primary" in sf1
    edgar = scan.ticker_source_disclosure(SOURCE_EDGAR)
    assert "SEC EDGAR (fallback)" in edgar and "Sharadar SF1" not in edgar

    # No data, key present -> attempted SF1 then EDGAR.
    monkeypatch.setattr(scan.fundamentals, "nasdaq_data_link_api_key", lambda: "key")
    no_data = scan.ticker_source_disclosure("")
    assert no_data == "Sharadar SF1 → SEC EDGAR — no data available"
    # No data, no key -> only EDGAR was attempted.
    monkeypatch.setattr(scan.fundamentals, "nasdaq_data_link_api_key", lambda: None)
    assert scan.ticker_source_disclosure(None) == "SEC EDGAR — no data available"


def test_revenue_cagr() -> None:
    hist = SimpleNamespace(years=[
        SimpleNamespace(fiscal_year=2022, revenue=100.0),
        SimpleNamespace(fiscal_year=2024, revenue=144.0),
    ])
    cagr = scan._revenue_cagr(hist)
    assert cagr is not None and abs(cagr - 0.20) < 1e-6  # 100 -> 144 over 2 yrs = 20%/yr
    assert scan._revenue_cagr(SimpleNamespace(years=[])) is None


def test_top_opportunities_is_resilient(monkeypatch) -> None:
    scan.reset_cache()
    # Force the price feed to blow up; screen must degrade to [] (never break the letter).
    monkeypatch.setattr(scan, "MarketDataService", lambda: (_ for _ in ()).throw(RuntimeError("no net")))
    assert scan.top_opportunities(n=5, universe=["AAPL", "MSFT"], force=True) == []


def test_newsletter_includes_equity_group_when_full(monkeypatch) -> None:
    picks = [
        scan.EquityOpportunity("AAPL", "Apple Inc.", 92.0, 0.30, 0.25, 0.45, 0.09, 0.05, 200.0, 3e12),
        scan.EquityOpportunity("MSFT", "Microsoft Corp.", 88.0, 0.42, 0.35, 0.40, 0.07, 0.04, 400.0, 3e12),
    ]
    monkeypatch.setattr("app.equity_opportunity_scan.top_opportunities", lambda n=5: picks)
    now = datetime.now(timezone.utc)

    full = build_edition("opportunity-scan", [], now, full=True)
    headings = [g.heading for g in full.groups]
    assert "Top equity opportunities" in headings
    eq = next(g for g in full.groups if g.heading == "Top equity opportunities")
    assert [i.label for i in eq.items] == ["AAPL", "MSFT"]

    teaser = build_edition("opportunity-scan", [], now, full=False)
    assert "Top equity opportunities" not in [g.heading for g in teaser.groups]
