# JHI-SIG: 69M2705M | Newsletter visual-layer tests | JHI Research & Analytics Firm, Inc. (proprietary)
"""Tests for the additive newsletter "visual layer": the deterministic macro-regime
classifier (all four quadrants + graceful degradation), the matplotlib exhibits (regime
quadrant + signal heat map return PNG bytes), and the wiring into the Insider Briefs and
Economic Brief editions (hero + exhibits above the unchanged existing content), including
the reportlab PDF fallback. All network-free (quotes are injected)."""

from dataclasses import asdict
from datetime import datetime, timezone

from app import macro_regime as mr
from app import newsletter_charts as nc
from app.market_models import Quote
from app.newsletter_content import build_edition


def _q(symbol: str, name: str, price: float, unit: str = "%",
       asset_class: str = "macro", change: float | None = None) -> Quote:
    return Quote(symbol=symbol, name=name, asset_class=asset_class, price=price,
                 unit=unit, source="fred", change_percent=change,
                 observation_date="2026-06-01", as_of_label="Monthly · as of Jun 2026")


def _macro_quotes() -> list[Quote]:
    """A fixed, network-free quote set covering the visual-layer inputs (with a few feed
    changes so the heat-map momentum column is exercised)."""
    return [
        _q("INFLATION", "US CPI", 3.10),
        _q("FED_FUNDS", "Fed Funds", 4.50),
        _q("UST10Y", "10-Year Treasury", 4.20, change=0.8),
        _q("UNEMPLOYMENT", "Unemployment", 4.10),
        _q("RETAIL_SALES", "Retail Sales", 700.0, "USD bn"),
        _q("CONSUMER_SENTIMENT", "Consumer Sentiment", 65.0, "index"),
        _q("INDUSTRIAL_PRODUCTION", "Industrial Production", 102.0, "index"),
        _q("GDP", "GDP", 28000.0, "USD bn"),
        _q("SPX", "S&P 500", 5600.0, "index", "equity", change=1.2),
        _q("GOLD", "Gold", 2400.0, "USD/oz", "commodity", change=-0.6),
        _q("BTC", "Bitcoin", 65000.0, "USD", "crypto", change=3.4),
    ]


# ── The deterministic classifier ─────────────────────────────────────────────
def test_classify_regime_covers_all_four_quadrants() -> None:
    assert mr.classify_regime(0.5, 0.5).quadrant == "reflation"
    assert mr.classify_regime(0.5, -0.5).quadrant == "goldilocks"
    assert mr.classify_regime(-0.5, 0.5).quadrant == "stagflation"
    assert mr.classify_regime(-0.5, -0.5).quadrant == "deflation"


def test_classify_regime_labels_are_generic_not_proprietary() -> None:
    labels = {mr.classify_regime(g, i).label
              for g in (-1, 1) for i in (-1, 1)}
    assert labels == {"Reflation", "Goldilocks", "Stagflation", "Deflation / Slowdown"}


def test_classify_regime_boundary_is_accelerating_side() -> None:
    # Exactly-zero scores resolve to the accelerating side so a read is always defined.
    r = mr.classify_regime(0.0, 0.0)
    assert r.quadrant == "reflation"
    assert r.growth_state == "accelerating" and r.inflation_state == "accelerating"


def test_classify_regime_states_and_caption_are_consistent() -> None:
    r = mr.classify_regime(-0.3, 0.4)
    assert r.growth_state == "decelerating"
    assert r.inflation_state == "accelerating"
    assert "decelerating" in r.caption and "hot" in r.caption


# ── Axis derivation from synthetic quote maps (all quadrants) ────────────────
def _qmap(**prices: float) -> dict[str, Quote]:
    return {s: _q(s, s, p) for s, p in prices.items()}


def test_derive_axes_reflation() -> None:
    # Tight labor + strong sentiment ⇒ growth up; hot CPI ⇒ inflation up.
    m = _qmap(UNEMPLOYMENT=3.5, CONSUMER_SENTIMENT=90.0, INDUSTRIAL_PRODUCTION=106.0,
              INFLATION=4.0)
    a = mr.assess_regime(m)
    assert a.available and a.regime.quadrant == "reflation"
    assert a.growth.score > 0 and a.inflation.score > 0


def test_derive_axes_goldilocks() -> None:
    m = _qmap(UNEMPLOYMENT=3.5, CONSUMER_SENTIMENT=90.0, INFLATION=1.8)
    a = mr.assess_regime(m)
    assert a.available and a.regime.quadrant == "goldilocks"
    assert a.growth.score > 0 and a.inflation.score < 0


def test_derive_axes_stagflation() -> None:
    m = _qmap(UNEMPLOYMENT=6.0, CONSUMER_SENTIMENT=55.0, INFLATION=4.5)
    a = mr.assess_regime(m)
    assert a.available and a.regime.quadrant == "stagflation"
    assert a.growth.score < 0 and a.inflation.score > 0


def test_derive_axes_deflation() -> None:
    m = _qmap(UNEMPLOYMENT=6.5, CONSUMER_SENTIMENT=52.0, INFLATION=1.2)
    a = mr.assess_regime(m)
    assert a.available and a.regime.quadrant == "deflation"
    assert a.growth.score < 0 and a.inflation.score < 0


def test_axis_derivation_renormalizes_with_partial_growth_inputs() -> None:
    # Only unemployment present (sentiment/IP missing) — the growth axis still resolves.
    a = mr.derive_growth(_qmap(UNEMPLOYMENT=3.5))
    assert a.available and a.score is not None and a.score > 0
    assert len(a.components) == 1


# ── Graceful degradation ─────────────────────────────────────────────────────
def test_assess_regime_degrades_when_inflation_missing() -> None:
    a = mr.assess_regime(_qmap(UNEMPLOYMENT=3.8, CONSUMER_SENTIMENT=80.0))
    assert a.available is False
    assert a.regime is None
    assert a.inflation.available is False


def test_assess_regime_degrades_when_growth_missing() -> None:
    a = mr.assess_regime(_qmap(INFLATION=3.0))
    assert a.available is False
    assert a.regime is None
    assert a.growth.available is False


def test_unavailable_status_quotes_are_ignored() -> None:
    m = _qmap(UNEMPLOYMENT=3.5, CONSUMER_SENTIMENT=80.0, INFLATION=3.0)
    m["INFLATION"].status = "unavailable"
    m["INFLATION"].price = None
    a = mr.assess_regime(m)
    assert a.available is False


def test_assess_regime_trail_uses_real_history_only() -> None:
    current = _qmap(UNEMPLOYMENT=6.0, CONSUMER_SENTIMENT=55.0, INFLATION=4.5)
    prior1 = _qmap(UNEMPLOYMENT=5.0, CONSUMER_SENTIMENT=62.0, INFLATION=3.8)
    prior2 = _qmap(UNEMPLOYMENT=5.5, CONSUMER_SENTIMENT=58.0, INFLATION=4.2)
    a = mr.assess_regime(current, history=[prior1, prior2])
    # Two real priors + the current reading, current LAST.
    assert len(a.trail) == 3
    assert a.trail[-1] == (a.growth.score, a.inflation.score)


def test_assess_regime_trail_without_history_is_just_current() -> None:
    a = mr.assess_regime(_qmap(UNEMPLOYMENT=3.5, CONSUMER_SENTIMENT=80.0, INFLATION=3.0))
    assert a.trail == [(a.growth.score, a.inflation.score)]


# ── The matplotlib exhibits return PNG bytes ─────────────────────────────────
def test_regime_quadrant_chart_returns_png_data_uri() -> None:
    img = nc.regime_quadrant_chart(-0.3, 0.4, "Stagflation",
                                   trail=[(-0.1, 0.1), (-0.2, 0.3), (-0.3, 0.4)],
                                   as_of="Jun 2026", growth_caption="Unemployment 4.1%",
                                   inflation_caption="CPI 3.1%")
    assert img.startswith("data:image/png;base64,")
    assert len(img) > 2000


def test_regime_quadrant_chart_single_point_ok() -> None:
    # Graceful: with no trail, only the current marker is drawn (no fabricated series).
    img = nc.regime_quadrant_chart(0.2, -0.5, "Goldilocks")
    assert img.startswith("data:image/png;base64,")


def test_signal_heatmap_chart_returns_png_data_uri() -> None:
    rows = [
        {"label": "S&P 500", "cells": [{"text": "5600", "severity": 0.2},
                                       {"text": "+1.2%", "severity": 0.3},
                                       {"text": "Risk-on", "severity": 0.4}]},
        {"label": "CPI", "cells": [{"text": "3.10%", "severity": 0.5},
                                   {"text": "—", "severity": 0.0},
                                   {"text": "Above target", "severity": 0.8}]},
    ]
    img = nc.signal_heatmap_chart(rows, as_of="Jun 2026")
    assert img.startswith("data:image/png;base64,")
    assert len(img) > 2000


def test_charts_are_deterministic() -> None:
    a = nc.regime_quadrant_chart(-0.3, 0.4, "Stagflation", as_of="Jun 2026")
    b = nc.regime_quadrant_chart(-0.3, 0.4, "Stagflation", as_of="Jun 2026")
    assert a == b


# ── Edition wiring (both editions build with the visual block) ───────────────
def test_insider_brief_carries_full_visual_layer() -> None:
    ed = build_edition("insider-briefs", _macro_quotes(), datetime.now(timezone.utc), full=True)
    vl = ed.visual_layer
    assert vl is not None and vl.hero is not None
    assert vl.hero.wordmark == "The Aegira Monthly"
    assert vl.hero.variant == "full"
    assert vl.hero.regime_label  # a classified regime badge
    assert vl.hero.thesis  # a one-line thesis reused from the letter
    # Both exhibits present, embedded as base64 PNGs (so <img> + PDF both capture them).
    labels = [c.label for c in vl.charts]
    assert labels == ["Macro Regime Quadrant", "Cross-Asset Signal Heat Map"]
    for c in vl.charts:
        assert c.image.startswith("data:image/png;base64,")
    # ADDITIVE: the existing groups/editor-letter/charts are all still present.
    assert ed.editor_letter is not None
    assert len(ed.groups) >= 1 and ed.groups[0].heading.startswith("The setup")
    assert len(ed.charts) >= 1


def test_economic_brief_carries_lighter_visual_layer() -> None:
    ed = build_edition("economic-brief", _macro_quotes(), datetime.now(timezone.utc), full=True)
    vl = ed.visual_layer
    assert vl is not None and vl.hero is not None
    assert vl.hero.wordmark == "The Economic Brief"
    assert vl.hero.variant == "light"
    assert [c.label for c in vl.charts] == ["Macro Regime Quadrant", "Cross-Asset Signal Heat Map"]
    # The full analytical arc below is untouched (5 sections + cross-asset + forward watch).
    assert len(ed.groups) == 7
    assert len(ed.charts) >= 1


def test_hero_thesis_is_reused_from_editor_letter() -> None:
    # The hero's one-line thesis is the first sentence of the letter's narrative, so it
    # inherits the letter's fact-lock whitelist (never a fabricated number).
    ed = build_edition("insider-briefs", _macro_quotes(), datetime.now(timezone.utc), full=True)
    narrative = ed.editor_letter.narrative
    assert ed.visual_layer.hero.thesis
    assert ed.visual_layer.hero.thesis in narrative


def test_visual_layer_hero_labels_are_as_of_dated() -> None:
    ed = build_edition("economic-brief", _macro_quotes(), datetime.now(timezone.utc), full=True)
    assert ed.visual_layer.hero.as_of  # a real as-of disclosure


def test_teaser_keeps_hero_but_drops_exhibits() -> None:
    # Mirrors the existing chart gating: the hero (lightweight) stays; the heavy exhibits
    # are omitted on the teaser to keep the anonymous path lean.
    for slug in ("insider-briefs", "economic-brief"):
        ed = build_edition(slug, _macro_quotes(), datetime.now(timezone.utc), full=False)
        assert ed.visual_layer is not None and ed.visual_layer.hero is not None
        assert ed.visual_layer.charts == []


def test_visual_layer_is_opt_in_per_edition() -> None:
    # Only the two opted-in editions carry a visual layer for now; others stay unchanged.
    now = datetime.now(timezone.utc)
    for slug in ("red-alerts", "crypto-intelligence", "dividend-opportunities"):
        ed = build_edition(slug, _macro_quotes(), now, full=True)
        assert ed.visual_layer is None, slug


def test_visual_layer_serializes_via_asdict() -> None:
    # The router returns asdict(edition); the nested dataclasses must serialize cleanly.
    ed = build_edition("insider-briefs", _macro_quotes(), datetime.now(timezone.utc), full=True)
    d = asdict(ed)
    assert d["visual_layer"]["hero"]["wordmark"] == "The Aegira Monthly"
    assert len(d["visual_layer"]["charts"]) == 2
    assert d["visual_layer"]["charts"][0]["image"].startswith("data:image/png;base64,")


def test_visual_layer_is_deterministic() -> None:
    now = datetime.now(timezone.utc)
    a = build_edition("insider-briefs", _macro_quotes(), now, full=True)
    b = build_edition("insider-briefs", _macro_quotes(), now, full=True)
    assert a.visual_layer == b.visual_layer


def test_heatmap_rows_drop_unavailable_series() -> None:
    from app.newsletter_content import _heatmap_rows

    m = {q.symbol: q for q in _macro_quotes()}
    full_rows = _heatmap_rows(m)
    labels = {r["label"] for r in full_rows}
    assert "S&P 500" in labels and "Gold" in labels
    # Drop a series → its row disappears (graceful degradation, never a blank/fabricated row).
    m.pop("SPX")
    assert len(_heatmap_rows(m)) == len(full_rows) - 1


# ── The reportlab PDF fallback carries the visual layer ──────────────────────
def test_reportlab_pdf_includes_visual_layer() -> None:
    from app.pdf_export import _chart_flowables, _hero_flowables, newsletter_pdf

    for slug in ("insider-briefs", "economic-brief"):
        ed = build_edition(slug, _macro_quotes(), datetime.now(timezone.utc), full=True)
        # The hero + the two exhibits produce flowables for the fallback path.
        assert _hero_flowables(ed)  # non-empty
        assert len(_chart_flowables(ed.visual_layer.charts)) >= 2
        pdf = newsletter_pdf(ed)
        assert pdf[:4] == b"%PDF", slug
        assert len(pdf) > 1000, slug
