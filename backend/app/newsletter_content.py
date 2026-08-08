# JHI-SIG: 69M2705M | Newsletter content engine (server-side) | JHI Research & Analytics Firm, Inc. (proprietary)
"""Server-side generation of the editorial editions (The Economic Brief, Red Alerts,
Cross-Asset Opportunity Scan, Insider Briefs) from the live /market/quotes feed.

This is the single source of truth for the deterministic, threshold-based analysis the
front-end renders, so a downloaded PDF matches what the reader sees on screen. Making
the backend authoritative also lets the same content be reused for the SES email.

Depth (2026-08, Phase 1 — no new AWS): the editions carry an *analytical-facts* layer —
level-vs-history (against disclosed reference levels), vs-target/threshold, and cross-links
such as the real 10-year yield (10Y − CPI) and the term spread (10Y − Fed Funds). The
Economic Brief is structured as an analytical arc — executive thesis → analytical sections
→ cross-asset implications → forward watch. Every figure is deterministic and fact-locked
(shown as last released); commentary is interpretation, not a forecast.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.market_models import Quote

# The full indicator + market set the editions draw from (mirrors newsletter-format.ts).
NEWSLETTER_SYMBOLS: list[str] = [
    "GDP", "FED_FUNDS", "UNEMPLOYMENT", "RETAIL_SALES", "CONSUMER_SENTIMENT",
    "INDUSTRIAL_PRODUCTION", "INFLATION", "SPX", "GOLD", "UST10Y", "BTC",
]


@dataclass
class Item:
    label: str
    value: str = ""
    body: str = ""
    tags: list[str] = field(default_factory=list)
    source: str | None = None


@dataclass
class Chart:
    """A server-rendered institutional chart, embedded as a base64 ``data:`` URI.

    The image is the DERIVED figure only (levels/scores/contributions) — never a raw
    licensed row. The frontend shows it as an ``<img>`` and the headless-Chromium PDF
    captures it automatically (it prints the real page)."""

    label: str
    image: str          # a data:image/png;base64,... URI
    caption: str = ""
    source: str | None = None


@dataclass
class Group:
    heading: str
    blurb: str = ""
    items: list[Item] = field(default_factory=list)
    charts: list[Chart] = field(default_factory=list)


@dataclass
class Edition:
    slug: str
    title: str
    eyebrow: str
    dateline: str
    intro: str
    groups: list[Group]
    footer: str
    disclaimer: str
    methodology: str
    teaser: bool = False
    charts: list[Chart] = field(default_factory=list)


QuoteMap = dict[str, Quote]

EDITION_SLUGS = ("economic-brief", "red-alerts", "opportunity-scan", "insider-briefs")

# ── Disclosed reference levels for the level-vs-history / vs-target reads ─────
# These are stated in-copy so the analysis is transparent and auditable (not a
# black box). They are reference anchors, not forecasts.
_NEUTRAL_FUNDS = 2.5   # estimated longer-run neutral policy rate (r* + 2% target)
_CPI_TARGET = 2.0      # Federal Reserve inflation objective
_FULL_EMPLOYMENT = 4.0  # ~ natural rate of unemployment reference
_UST10Y_NORM = 4.0     # post-2000 nominal 10-year reference level

_DISCLAIMER = (
    "For research and educational purposes only. Not investment, legal, tax, or "
    "accounting advice. Written in Aegira's independent professional perspective."
)

# Methodology disclosure — the institutional standard from docs/EDITORIAL_STYLE_GUIDE.md (E1).
# Kept identical to the on-screen note so screen and PDF match verbatim.
METHODOLOGY = (
    "This edition is generated deterministically from Aegira's polled public-data feeds "
    "(Federal Reserve/FRED · U.S. Bureau of Labor Statistics · BEA · market feeds). "
    "Commentary is rule-based on disclosed thresholds; figures are shown as last released "
    "(see 'as of'). It is an independent professional read, not a forecast or advice."
)

# ── Attribution & governance disclaimers ─────────────────────────────────────
# Surfaced on SF1-derived content (the equity opportunity screen). Only the SOURCE
# is named and only DERIVED metrics are shown — never raw licensed rows (governance).
_SF1_ATTRIBUTION = "Data provided by Nasdaq Data Link / Sharadar."
_DERIVED_ONLY_NOTE = (
    "Fundamentals-derived figures (scores, factor contributions, margins, yields) are "
    "computed by Aegira from licensed point-in-time data and are surfaced as derived "
    "metrics only; no raw underlying data rows are shown or redistributed."
)
_BACKTEST_DISCLAIMER = (
    "Factor rankings reference Aegira's transparent, pre-registered, out-of-sample "
    "validated factor research. Any performance discussion is model-based and hypothetical; "
    "past or simulated performance does not guarantee future results."
)


def _methodology_for(slug: str) -> str:
    """Base methodology, plus the SF1 attribution / derived-only / back-test disclaimers
    on the SF1-derived edition (the opportunity scan) so attribution rides with the data."""
    if slug == "opportunity-scan":
        return " ".join([METHODOLOGY, _SF1_ATTRIBUTION, _DERIVED_ONLY_NOTE, _BACKTEST_DISCLAIMER])
    return METHODOLOGY


def edition_date(now: datetime) -> str:
    # e.g. "Wednesday, July 22, 2026"
    return now.strftime("%A, %B %d, %Y").replace(" 0", " ")


def fmt(q: Quote | None) -> str:
    """Mirror of newsletter-format.ts `fmt`."""
    if q is None or q.price is None:
        return "—"
    v = q.price
    unit = q.unit
    if unit == "%":
        return f"{v:.2f}%"
    if unit == "index":
        return f"{v:.1f}"
    if unit == "USD bn":
        return f"${v / 1000:.2f}T" if v >= 1000 else f"${v:.1f}B"
    if unit == "USD mn":
        return f"${v / 1000:.2f}B" if v >= 1000 else f"${v:.1f}M"
    if unit in ("USD/oz", "USD"):
        return f"${v:,.0f}"
    return f"{v:,.2f}"


def _price(m: QuoteMap, s: str) -> float | None:
    q = m.get(s)
    return q.price if q else None


# ── Analytical-facts layer (derived, fact-locked cross-links) ────────────────
def _real_rate(m: QuoteMap) -> float | None:
    """The real 10-year yield ≈ nominal 10Y − headline CPI. The single most
    important cross-asset number: the hurdle rate for every risk asset."""
    ten, cpi = _price(m, "UST10Y"), _price(m, "INFLATION")
    return None if ten is None or cpi is None else ten - cpi


def _term_spread(m: QuoteMap) -> float | None:
    """10Y minus the policy rate — a curve/term-premium proxy. Negative = inverted."""
    ten, ff = _price(m, "UST10Y"), _price(m, "FED_FUNDS")
    return None if ten is None or ff is None else ten - ff


def _gap_phrase(value: float, reference: float, unit: str = " points") -> str:
    """'0.9 points above' / '0.4 points below' / 'in line with' vs a reference."""
    gap = value - reference
    if abs(gap) < 0.05:
        return "in line with"
    return f"{abs(gap):.1f}{unit} {'above' if gap > 0 else 'below'}"


# ── The Economic Brief ──────────────────────────────────────────────────────
_SECTIONS: list[tuple[str, str, list[str]]] = [
    ("Monetary Policy & Rates",
     "The policy rate and the long end set the cost of capital for the whole economy. "
     "We read each against its own history — the policy rate versus a ~2.5% neutral "
     "estimate, the 10-year versus its ~4% post-2000 norm.",
     ["FED_FUNDS", "UST10Y"]),
    ("Inflation",
     "Price growth versus the Federal Reserve's 2% objective. The distance from target — "
     "not the level alone — is what governs the timing and pace of any easing.",
     ["INFLATION"]),
    ("Labor & the Consumer",
     "Employment slack and household demand — the engine of roughly two-thirds of output, "
     "and the swing factor for whether the expansion holds.",
     ["UNEMPLOYMENT", "RETAIL_SALES", "CONSUMER_SENTIMENT"]),
    ("Growth & Output", "Aggregate activity and the industrial base — the denominator for "
     "leverage, valuation, and deficit ratios.",
     ["GDP", "INDUSTRIAL_PRODUCTION"]),
    ("Markets", "The cross-asset read on risk appetite, safe-haven demand, and liquidity.",
     ["SPX", "GOLD", "BTC"]),
]


def _commentary(symbol: str, v: float | None) -> str:
    if v is None:
        return "Awaiting the next release."
    if symbol == "FED_FUNDS":
        vs = _gap_phrase(v, _NEUTRAL_FUNDS)
        anchor = f" — roughly {vs} our ~{_NEUTRAL_FUNDS:.1f}% neutral estimate" if vs != "in line with" \
            else " — about in line with our ~2.5% neutral estimate"
        if v >= 4:
            return (f"A restrictive stance{anchor}, continuing to weigh on rate-sensitive demand, "
                    "leverage-dependent deals, and refinancings.")
        if v >= 2.5:
            return f"A moderately restrictive stance{anchor}; policy is not yet neutral."
        return f"An accommodative stance{anchor}, supportive of credit and risk assets."
    if symbol == "UST10Y":
        vs = _gap_phrase(v, _UST10Y_NORM)
        anchor = (f" ({vs} its ~{_UST10Y_NORM:.1f}% post-2000 norm)"
                  if vs != "in line with" else " (near its ~4% post-2000 norm)")
        return (f"Long rates remain elevated{anchor}, keeping borrowing costs and discount rates high."
                if v >= 4.5 else
                f"Long rates are easing{anchor}, a tailwind for valuations and refinancing.")
    if symbol == "INFLATION":
        above = v - _CPI_TARGET
        vs = (f"{above:.1f} points above" if above >= 0.05
              else f"{abs(above):.1f} points below" if above <= -0.05 else "in line with")
        if v <= 2.5:
            return f"At {vs} the Fed's 2% target — consistent with an easing bias."
        if v <= 4:
            return (f"Running {vs} the 2% target; the last mile of disinflation is proving sticky "
                    "and is what keeps the Fed on hold.")
        return f"Elevated at {vs} target, constraining the path to rate cuts."
    if symbol == "UNEMPLOYMENT":
        vs = _gap_phrase(v, _FULL_EMPLOYMENT)
        anchor = (f" ({vs} the ~{_FULL_EMPLOYMENT:.1f}% full-employment reference)"
                  if vs != "in line with" else " (near the ~4% full-employment reference)")
        if v < 4.5:
            return f"The labor market remains firm{anchor}, underpinning consumer resilience."
        if v <= 5.5:
            return f"A softening labor market{anchor} that bears watching for demand risk."
        return f"A weak labor market{anchor}, signaling cyclical downside."
    if symbol == "RETAIL_SALES":
        return "Headline household spending — the clearest read on consumer demand."
    if symbol == "CONSUMER_SENTIMENT":
        return ("Subdued sentiment; households remain cautious despite steady spending."
                if v < 60 else "Improving sentiment supports the demand outlook.")
    if symbol == "GDP":
        return "Aggregate output; the denominator for leverage, valuation and deficit ratios."
    if symbol == "INDUSTRIAL_PRODUCTION":
        return "The industrial base — a cyclical tell for goods demand and capex."
    if symbol == "SPX":
        return "Broad equity risk appetite and the equity cost of capital."
    if symbol == "GOLD":
        return "Safe-haven demand and a hedge against real-rate and fiscal risk."
    if symbol == "BTC":
        return "A high-beta read on liquidity and speculative risk appetite."
    return ""


def _thesis(m: QuoteMap) -> str:
    """The executive thesis — a synthesized, fact-locked read that opens the arc.
    Each clause ties a level to its reference so the interpretation is transparent."""
    ff, cpi, un = _price(m, "FED_FUNDS"), _price(m, "INFLATION"), _price(m, "UNEMPLOYMENT")
    ten, rr, ts = _price(m, "UST10Y"), _real_rate(m), _term_spread(m)
    parts: list[str] = []

    if ff is not None:
        stance = ("restrictive" if ff >= 4 else "moderately restrictive" if ff >= 2.5
                  else "accommodative")
        parts.append(
            f"The federal funds rate at {ff:.2f}% sits {_gap_phrase(ff, _NEUTRAL_FUNDS)} our "
            f"~{_NEUTRAL_FUNDS:.1f}% neutral reference — a {stance} setting that keeps the cost of "
            "capital high across the economy.")
    if cpi is not None:
        if cpi > _CPI_TARGET:
            parts.append(
                f"Inflation at {cpi:.2f}% is still {cpi - _CPI_TARGET:.1f} points above the Fed's "
                "2% objective, so the last mile of disinflation — not growth — governs the timing "
                "of any cuts.")
        else:
            parts.append(
                f"Inflation at {cpi:.2f}% is at or below the 2% objective, opening room for an "
                "easing bias.")
    if rr is not None and ten is not None:
        parts.append(
            f"With the 10-year near {ten:.2f}%, the real 10-year yield is roughly {rr:.2f}% — "
            "positive real rates of this size discipline valuations and reward patient, "
            "cash-flowing capital.")
    if un is not None:
        parts.append(
            f"The labor market at {un:.2f}% unemployment is "
            f"{'still firm' if un < 4.5 else 'softening at the margin'}, the swing factor for "
            "whether the consumer keeps the expansion intact.")
    if ts is not None and ts < 0:
        parts.append(
            f"The 10-year below the policy rate (a {ts:.2f}-point spread) leaves the curve "
            "inverted — historically a late-cycle signal that rewards up-in-quality positioning.")
    parts.append(
        "The sections below read each pillar against its own history, then translate the macro "
        "into cross-asset implications for allocators and acquirers.")
    return " ".join(parts)


def _cross_asset_group(m: QuoteMap) -> Group:
    """Synthesis section: translate the macro read into cross-asset implications."""
    rr, ts = _real_rate(m), _term_spread(m)
    items: list[Item] = []
    if rr is not None:
        items.append(Item(
            label="Real rates", value=f"{rr:.2f}% (10Y − CPI)",
            body=(
                "Positive real yields near multi-decade highs raise the hurdle rate for every "
                "asset: they cap equity multiples, reward front-to-intermediate high-quality "
                "credit, and pressure long-duration and richly-valued growth. This is the single "
                "most important number for cross-asset positioning today."
                if rr >= 1 else
                "Real yields are only modestly positive — a less punishing backdrop for duration "
                "and long-duration equity, but not yet a green light for aggressive risk."),
            tags=["Rates", "Equities", "Fixed income"],
            source="Derived: 10-year Treasury − headline CPI (FRED)."))
    if ts is not None:
        items.append(Item(
            label="Yield curve", value=f"{ts:.2f} pts (10Y − Fed Funds)",
            body=(
                "Inverted: the market is pricing policy easing ahead. The historical playbook "
                "favors up-in-quality, shorter-duration credit and locking in yield before the "
                "curve normalizes."
                if ts < 0 else
                "Positively sloped: a normalizing curve that historically supports banks, "
                "cyclical risk, and a re-steepening carry trade."),
            tags=["Fixed income", "Equities"],
            source="Derived: 10-year Treasury − federal funds rate (FRED)."))
    spx, gold, btc = m.get("SPX"), m.get("GOLD"), m.get("BTC")
    haven_bits: list[str] = []
    if gold and gold.price is not None:
        haven_bits.append(
            f"Gold at {fmt(gold)} reflects fiscal- and real-rate-hedging demand; pair it with "
            "cash-flowing real assets repriced to the new rate regime.")
    if spx and spx.price is not None:
        haven_bits.append(
            f"Equities ({spx.name} {fmt(spx)}) still clear a high real-rate hurdle — favor "
            "quality compounders and free-cash-flow yield over long-duration growth.")
    if btc and btc.price is not None:
        haven_bits.append(
            f"{btc.name} at {fmt(btc)} is a high-beta read on liquidity — a satellite, not a core, "
            "until policy eases.")
    if haven_bits:
        items.append(Item(
            label="Risk vs. haven", value="positioning",
            body=" ".join(haven_bits), tags=["Equities", "Real assets", "Digital assets"]))
    return Group(
        heading="Cross-asset implications",
        blurb="How the macro read maps to positioning across asset classes — interpretation, "
              "not a forecast or advice.",
        items=items)


def _forward_watch_group(m: QuoteMap) -> Group:
    """What would change the read — the releases and levels the desk is watching next."""
    return Group(
        heading="Forward watch — what would change the read",
        blurb="The catalysts the desk is tracking, and the levels that would flip the balance "
              "of risk.",
        items=[
            Item(label="Inflation path", value=f"CPI {fmt(m.get('INFLATION'))} vs 2% target",
                 body="A print that resumes progress toward 2% is the clearest trigger for the "
                      "Fed to cut; a re-acceleration pushes cuts out and pressures duration."),
            Item(label="Labor market", value=f"Unemployment {fmt(m.get('UNEMPLOYMENT'))}",
                 body="A sustained move above the ~4.5–5% band would shift the balance of risk "
                      "from inflation to growth and likely accelerate the easing timeline."),
            Item(label="Policy rate", value=f"Fed Funds {fmt(m.get('FED_FUNDS'))}",
                 body="The first cut re-rates rate-sensitive sectors — watch the pace and the "
                      "dot-path, not just the first move."),
            Item(label="Long rates", value=f"10Y {fmt(m.get('UST10Y'))}",
                 body="A durable break in the 10-year resets discount rates across public and "
                      "private valuations and cap rates in real assets."),
        ])


# ── Chart/visual layer (server-rendered, resilient) ─────────────────────────
def _macro_chart(m: QuoteMap) -> list["Chart"]:
    """A current-vs-reference macro chart for the Economic Brief.

    We poll FRED for *current* levels only (no history feed), so — per governance —
    we render an honest current-vs-disclosed-reference bar rather than fabricating a
    time series. Built solely from released levels + the anchors stated in-copy."""
    cpi, ff, ten = _price(m, "INFLATION"), _price(m, "FED_FUNDS"), _price(m, "UST10Y")
    labels: list[str] = []
    current: list[float] = []
    reference: list[float] = []
    for level, label, anchor in (
        (cpi, "CPI", _CPI_TARGET),
        (ff, "Fed Funds", _NEUTRAL_FUNDS),
        (ten, "10Y UST", _UST10Y_NORM),
    ):
        if level is not None:
            labels.append(label)
            current.append(level)
            reference.append(anchor)
    if len(labels) < 2:
        return []
    try:
        from app import newsletter_charts as nc
        img = nc.reference_bar("Policy & inflation vs. reference anchors",
                               labels, current, reference, unit="%")
    except Exception:  # noqa: BLE001 - never break newsletter generation
        return []
    return [Chart(
        label="Current levels vs. reference anchors",
        image=img,
        caption="Released levels (as of the latest print) against Aegira's disclosed "
                "reference anchors — the 2.0% CPI target, ~2.5% neutral policy rate, and "
                "~4.0% post-2000 10-year norm. Levels only; no series is implied.",
        source="Derived from FRED releases · reference anchors disclosed in-copy.")]


def _insider_chart(m: QuoteMap, title: str) -> list["Chart"]:
    """A thematic rate/real-rate stack supporting the deep-dive."""
    ff, ten, cpi = _price(m, "FED_FUNDS"), _price(m, "UST10Y"), _price(m, "INFLATION")
    rr = _real_rate(m)
    labels: list[str] = []
    values: list[float] = []
    for level, label in ((ff, "Fed Funds"), (ten, "10Y UST"), (cpi, "CPI"), (rr, "Real 10Y")):
        if level is not None:
            labels.append(label)
            values.append(level)
    if len(labels) < 2:
        return []
    try:
        from app import newsletter_charts as nc
        img = nc.labeled_levels(f"The rate stack — {title}", labels, values, unit="%")
    except Exception:  # noqa: BLE001
        return []
    return [Chart(
        label="The rate stack",
        image=img,
        caption="The nominal policy rate and long end, headline inflation, and the derived "
                "real 10-year yield (10Y − CPI) — the after-inflation hurdle the brief turns on.",
        source="Derived from FRED releases (10Y − CPI).")]


def _economic_brief(m: QuoteMap, full: bool) -> tuple[str, list[Group]]:
    sections = _SECTIONS if full else _SECTIONS[:1]
    groups: list[Group] = []
    for heading, blurb, syms in sections:
        items: list[Item] = []
        for sym in syms:
            q = m.get(sym)
            if not q:
                continue
            items.append(Item(label=q.name, value=fmt(q), body=_commentary(sym, q.price),
                              source=q.note))
        groups.append(Group(heading=heading, blurb=blurb, items=items))
    if full:
        # Close the analytical arc: synthesis → forward watch.
        groups.append(_cross_asset_group(m))
        groups.append(_forward_watch_group(m))
    return _thesis(m), groups


# ── Red Alerts ──────────────────────────────────────────────────────────────
_SEV_RANK = {"High": 0, "Medium": 1, "Low": 2}


def _build_alerts(m: QuoteMap) -> list[Item]:
    alerts: list[tuple[str, str, str, list[str]]] = []  # (severity, title, detail, classes)

    cpi = _price(m, "INFLATION")
    if cpi is not None and cpi > 3:
        alerts.append((
            "High" if cpi > 4 else "Medium",
            f"Inflation elevated at {cpi:.2f}%",
            "Above the 3% line — the last mile of disinflation is stalling, constraining the "
            "Fed's room to cut and pressuring long-duration valuations.",
            ["Rates", "Equities", "Fixed income"]))

    ff = _price(m, "FED_FUNDS")
    if ff is not None and ff >= 4:
        alerts.append((
            "Medium", f"Policy restrictive — Fed Funds at {ff:.2f}%",
            "Financing costs stay high; rate-sensitive sectors, leverage-dependent deals, and "
            "refinancings remain under pressure.",
            ["Private markets", "Real assets", "Equities"]))

    ten = _price(m, "UST10Y")
    if ten is not None and ten >= 4.5:
        alerts.append((
            "Medium", f"Long rates elevated — 10Y at {ten:.2f}%",
            "Higher discount rates compress valuations and raise the bar for new capital; watch "
            "duration exposure and cap-rate expansion.",
            ["Fixed income", "Real assets", "Equities"]))

    un = _price(m, "UNEMPLOYMENT")
    if un is not None and un >= 4.5:
        alerts.append((
            "High" if un >= 5.5 else "Medium",
            f"Labor softening — unemployment at {un:.2f}%",
            "A rising jobless rate flags cyclical demand risk to consumer spending, credit "
            "performance, and small-business cash flows.",
            ["Equities", "Credit", "Private markets"]))

    sent = _price(m, "CONSUMER_SENTIMENT")
    if sent is not None and sent < 60:
        alerts.append((
            "Low", f"Subdued consumer sentiment ({sent:.1f})",
            "Cautious households can foreshadow softer discretionary demand even while headline "
            "spending holds.",
            ["Equities", "Consumer"]))

    for sym in ("SPX", "GOLD", "BTC", "UST10Y"):
        q = m.get(sym)
        chg = q.change_percent if q else None
        if q and chg is not None and abs(chg) >= 2:
            sign = "+" if chg > 0 else ""
            alerts.append((
                "High" if abs(chg) >= 4 else "Medium",
                f"{q.name} moved {sign}{chg:.1f}% on the session",
                f"A sharp {'advance' if chg > 0 else 'decline'} signals a shift in risk appetite "
                "worth monitoring for follow-through.",
                ["Markets"]))

    alerts.sort(key=lambda a: _SEV_RANK[a[0]])
    return [Item(label=sev, value=title, body=detail, tags=classes)
            for sev, title, detail, classes in alerts]


# ── Cross-Asset Opportunity Scan ────────────────────────────────────────────
def _build_scan(m: QuoteMap) -> list[Item]:
    ff = m.get("FED_FUNDS")
    return [
        Item(label="Fixed Income", value=f"10Y {fmt(m.get('UST10Y'))}",
             body="Real yields near multi-year highs — intermediate Treasuries and investment-grade "
                  "credit offer carry now and convexity if disinflation resumes. Ladder duration "
                  "rather than reaching for it."),
        Item(label="Equities", value=f"Fed Funds {fmt(ff)}",
             body="With policy restrictive, favor quality compounders and free-cash-flow yield over "
                  "long-duration, unprofitable growth until the cutting cycle is confirmed."),
        Item(label="Real Assets", value=f"Gold {fmt(m.get('GOLD'))}",
             body="Gold's strength reflects fiscal and real-rate hedging demand. Pair it with "
                  "cash-flowing real estate where cap rates have repriced to the new rate regime."),
        Item(label="Private Markets / SMB", value=f"Debt cost ~{fmt(ff)}+",
             body="Higher leverage costs pressure LBO math — the edge is in lower-leverage, "
                  "cash-flowing small businesses acquired at disciplined multiples (a disciplined "
                  "acquirer's core hunting ground)."),
        Item(label="Digital Assets", value=f"BTC {fmt(m.get('BTC'))}",
             body="A high-beta read on liquidity — size positions to volatility and treat as a "
                  "satellite, not a core holding, until policy eases."),
    ]


# ── Insider Briefs (rotating deep-dive on the most salient macro theme) ──────
_INSIDER_TITLES = {
    "real-cost-of-capital": "The Real Cost of Capital",
    "last-mile-disinflation": "The Last Mile of Disinflation",
    "labor-at-the-margin": "Labor at the Margin",
    "safe-haven-bid": "The Safe-Haven Bid",
}


def _insider_theme_key(m: QuoteMap) -> str:
    """Deterministically pick the most salient theme from the live data. Ordered
    candidates give a stable tie-break so the same data always yields the same brief."""
    rr = _real_rate(m)
    cpi, un = _price(m, "INFLATION"), _price(m, "UNEMPLOYMENT")
    gold = m.get("GOLD")
    gchg = abs(gold.change_percent) if gold and gold.change_percent is not None else 0.0
    candidates: list[tuple[str, float]] = [
        ("real-cost-of-capital", rr if rr is not None else 0.0),
        ("last-mile-disinflation", max(0.0, cpi - _CPI_TARGET) if cpi is not None else 0.0),
        ("labor-at-the-margin", max(0.0, un - _FULL_EMPLOYMENT) if un is not None else 0.0),
        ("safe-haven-bid", gchg),
    ]
    return max(candidates, key=lambda c: c[1])[0]


def _insider_setup_group(m: QuoteMap) -> Group:
    syms = ["FED_FUNDS", "UST10Y", "INFLATION", "UNEMPLOYMENT"]
    items: list[Item] = []
    for sym in syms:
        q = m.get(sym)
        if not q:
            continue
        items.append(Item(label=q.name, value=fmt(q), body=_commentary(sym, q.price),
                          source=q.note))
    rr = _real_rate(m)
    if rr is not None:
        items.append(Item(
            label="Real 10-year yield", value=f"{rr:.2f}%",
            body="The nominal 10-year minus headline CPI — the economy's true, after-inflation "
                 "hurdle rate and the anchor for cross-asset valuation.",
            source="Derived: 10-year Treasury − CPI (FRED)."))
    return Group(heading="The setup — where the data sits",
                 blurb="The levels this brief is built on, each shown as last released.",
                 items=items)


def _insider_theme_content(key: str, m: QuoteMap) -> tuple[str, list[Item], list[Item]]:
    """Return (thesis, why-it-matters items, the-Aegira-lens items) for a theme.
    All figures are pulled from the live data and shown as released (fact-locked)."""
    ff, cpi, un = fmt(m.get("FED_FUNDS")), fmt(m.get("INFLATION")), fmt(m.get("UNEMPLOYMENT"))
    ten = fmt(m.get("UST10Y"))
    rr, ts = _real_rate(m), _term_spread(m)
    rr_s = f"{rr:.2f}%" if rr is not None else "positive"

    if key == "last-mile-disinflation":
        thesis = (
            f"Disinflation is easy at first and hard at the end. With CPI at {cpi} against the "
            "Fed's 2% objective, the remaining gap is concentrated in the stickiest components — "
            "shelter and core services — where progress is measured in tenths, not points. That "
            f"is why the funds rate is still {ff}: the Fed is not fighting the level of inflation "
            "so much as its persistence. This brief examines why the last mile is the hardest, and "
            "what it means for the timing of relief.")
        why = [
            Item("Services inflation is structural, not transitory",
                 "measured in tenths",
                 "The goods disinflation that did the early work has largely run its course. "
                 "What remains is services and shelter, which move slowly and track wages — so the "
                 "path to 2% is a grind, not a step-change."),
            Item("The Fed's reaction function is asymmetric", f"Fed Funds {ff}",
                 "A central bank that has spent its credibility re-anchoring expectations will "
                 "wait for convincing evidence before cutting. That bias keeps policy restrictive "
                 "for longer than a purely mechanical rule would imply."),
            Item("Duration carries the risk", f"10Y {ten}",
                 "If the last mile stalls, the front end stays anchored and the long end reprices "
                 "higher — the pain lands on long-duration bonds and richly-valued growth equity."),
        ]
        lens = [
            Item("Positioning lens", "up-in-quality, laddered",
                 "Favor intermediate high-quality duration and free-cash-flow yield over "
                 "long-duration bets on imminent cuts. Let the data — not the calendar — set the "
                 "timeline. Research, not investment advice.")]
        return thesis, why, lens

    if key == "labor-at-the-margin":
        thesis = (
            f"The expansion lives or dies with the consumer, and the consumer lives or dies with "
            f"the job market. At {un} unemployment, the labor market is the pivot: firm enough to "
            "keep spending intact today, but the margin is where the cycle turns. This brief reads "
            "the labor signal for what it means to the consumer, to credit, and to the Fed's "
            "dual mandate.")
        why = [
            Item("The consumer is the transmission belt", f"Unemployment {un}",
                 "Roughly two-thirds of output is consumption. A rising jobless rate erodes income "
                 "growth, confidence, and the willingness to spend — the first domino in a "
                 "demand slowdown."),
            Item("Credit performance follows employment", f"Fed Funds {ff}",
                 "Consumer and small-business credit hold up while people are working. Softening "
                 "labor plus a high funds rate is the combination that lifts delinquencies and "
                 "tightens lending."),
            Item("The dual mandate shifts the Fed's hand", f"CPI {cpi}",
                 "As labor softens, the Fed's balance tilts from inflation toward employment — the "
                 "condition that historically pulls the first cut forward."),
        ]
        lens = [
            Item("Positioning lens", "defensive quality",
                 "Late-cycle labor softening rewards balance-sheet quality, defensive cash flows, "
                 "and caution on consumer-cyclical and lower-quality credit. Research, not advice.")]
        return thesis, why, lens

    if key == "safe-haven-bid":
        gold = fmt(m.get("GOLD"))
        thesis = (
            f"When gold rallies with real rates still positive, it is saying something. At {gold}, "
            "the safe-haven bid is not a bet on deflation — it is a hedge against fiscal risk, "
            "currency debasement, and the tail where the Fed is forced to ease into sticky "
            "inflation. This brief unpacks what the haven trade is pricing and how to hold it.")
        why = [
            Item("Gold vs. real rates is the tell", f"Real 10Y {rr_s}",
                 "Gold normally struggles when real yields are high. Strength despite positive "
                 "real rates points to demand for a hedge against fiscal and monetary tail risk, "
                 "not a simple rate trade."),
            Item("Fiscal arithmetic is the backdrop", f"10Y {ten}",
                 "Large deficits financed at a higher cost of debt raise the odds of financial "
                 "repression or debasement over time — precisely the regime that rewards real, "
                 "scarce assets."),
            Item("It is a hedge, not a core holding", f"Fed Funds {ff}",
                 "The haven trade earns its place as portfolio insurance. Size it to the risk it "
                 "hedges, and pair it with cash-flowing real assets rather than treating it as a "
                 "standalone return engine."),
        ]
        lens = [
            Item("Positioning lens", "insurance, sized",
                 "Treat the haven allocation as a hedge sized to fiscal and real-rate tail risk — "
                 "complemented by repriced, cash-flowing real assets. Research, not advice.")]
        return thesis, why, lens

    # default: real-cost-of-capital
    curve = (f"an inverted curve ({ts:.2f} pts, 10Y − Fed Funds)" if ts is not None and ts < 0
             else "a normalizing curve")
    thesis = (
        "The defining feature of this cycle is not the headline level of interest rates but their "
        f"real, after-inflation cost. With the 10-year at {ten} and CPI at {cpi}, the real "
        f"10-year yield is roughly {rr_s} — near the highest sustained level in more than a "
        f"decade, alongside {curve}. Positive real rates of this magnitude quietly reset the price "
        "of everything: they are the hurdle every investment, every deal, and every valuation must "
        "now clear. This brief traces how that hurdle reshapes capital allocation.")
    why = [
        Item("Every valuation carries a higher hurdle", f"Real 10Y {rr_s}",
             "Discounted cash flows are worth less when the discount rate is higher in real terms. "
             "The effect is largest for long-duration, back-end-loaded growth and smallest for "
             "near-term, cash-generative businesses."),
        Item("Leverage math has fundamentally changed", f"Fed Funds {ff}",
             "With financing near policy-rate levels, the levered-buyout arithmetic that worked in "
             "a zero-rate world no longer clears. The edge shifts to lower-leverage, cash-flowing "
             "acquisitions bought at disciplined multiples."),
        Item("Cash flow beats promises", f"10Y {ten}",
             "When capital is no longer free, investors are paid to prefer realized free cash flow "
             "over promised future growth. Quality, coverage, and pricing power are repriced up."),
    ]
    lens = [
        Item("Positioning lens", "patient, cash-flowing capital",
             "A positive-real-rate regime rewards discipline: quality compounders, front-to-"
             "intermediate high-grade credit, and cash-flowing real and private assets acquired "
             "at sensible multiples. Research, not investment advice.")]
    return thesis, why, lens


def _insider_brief(m: QuoteMap, now: datetime, full: bool) -> Edition:
    key = _insider_theme_key(m)
    title = _INSIDER_TITLES[key]
    thesis, why_items, lens_items = _insider_theme_content(key, m)
    dateline = f"Edition of {edition_date(now)}"

    groups: list[Group] = [_insider_setup_group(m)]
    if full:
        groups.append(Group(
            heading="Why it matters",
            blurb="The mechanism — how this theme transmits into the economy and markets.",
            items=why_items))
        groups.append(_cross_asset_group(m))
        groups.append(_forward_watch_group(m))
        groups.append(Group(
            heading="The Aegira lens",
            blurb="How the desk frames the theme for allocators and acquirers.",
            items=lens_items))

    return Edition(
        slug="insider-briefs", title=f"Insider Brief — {title}", eyebrow="Insider Briefs",
        dateline=dateline, intro=thesis, groups=groups,
        footer="A rotating deep-dive on the most salient macro theme, built from public data "
               "(FRED · BLS · SEC EDGAR · market feeds) and written in Aegira's independent "
               "professional perspective.",
        disclaimer=_DISCLAIMER, methodology=METHODOLOGY, teaser=not full,
        charts=_insider_chart(m, title) if full else [])


def build_edition(slug: str, quotes: list[Quote], now: datetime, full: bool) -> Edition:
    """Build a normalized Edition for the given slug. Raises KeyError for unknown slug."""
    if slug not in EDITION_SLUGS:
        raise KeyError(slug)
    m: QuoteMap = {q.symbol: q for q in quotes}
    dateline = f"Edition of {edition_date(now)}"

    if slug == "insider-briefs":
        return _insider_brief(m, now, full)

    if slug == "economic-brief":
        intro, groups = _economic_brief(m, full)
        return Edition(
            slug=slug, title="The Economic Brief", eyebrow="Economic Tracking",
            dateline=dateline, intro=intro, groups=groups,
            footer="Sourced from public data — Federal Reserve (FRED), U.S. Bureau of Labor "
                   "Statistics, and market feeds. Figures are as last released.",
            disclaimer=_DISCLAIMER, methodology=METHODOLOGY, teaser=not full,
            charts=_macro_chart(m) if full else [])

    if slug == "red-alerts":
        alerts = _build_alerts(m)
        shown = alerts if full else alerts[:1]
        intro = ("All clear — no red alerts. Tracked indicators are within normal bands."
                 if not alerts else
                 "Threshold-triggered alerts from the live feed, ordered by severity.")
        return Edition(
            slug=slug, title="Red Alerts", eyebrow="Red Alerts", dateline=dateline,
            intro=intro, groups=[Group(heading="Triggered alerts", items=shown)] if shown else [],
            footer="Triggered from public data (FRED · BLS · market feeds). Thresholds are "
                   "indicative, not trading signals.",
            disclaimer=_DISCLAIMER, methodology=METHODOLOGY, teaser=not full)

    # opportunity-scan
    ideas = _build_scan(m)
    shown = ideas if full else ideas[:2]
    groups = [Group(heading="Opportunities by asset class", items=shown)]
    # Full edition only: the discovery-driven equity screen (heavy EDGAR+price fetch,
    # cached). Teaser omits it (keeps the anonymous path fast + gates the screen to subscribers).
    if full:
        equity_group = _build_equity_group()
        if equity_group is not None:
            groups.append(equity_group)
    return Edition(
        slug=slug, title="Cross-Asset Opportunity Scan", eyebrow="Opportunity Scan",
        dateline=dateline,
        intro="Where the current regime — restrictive policy, above-target inflation, and a "
              "resilient but softening consumer — is creating opportunity across asset classes.",
        groups=groups,
        footer="Ideas are generated from public data (FRED · BLS · SEC EDGAR · market feeds) "
               "and Aegira's validated factor research; equity fundamentals are derived from "
               "licensed data (Nasdaq Data Link / Sharadar) and surfaced as derived metrics only. "
               "Written in Aegira's independent professional perspective.",
        disclaimer=_DISCLAIMER, methodology=_methodology_for(slug), teaser=not full)


def _equity_charts(picks: list) -> list["Chart"]:
    """Ranked-score bar + per-name Value/Quality/Growth/Momentum decomposition.

    Both charts plot only DERIVED figures (the 0-100 scores and the signed weighted-z
    factor contributions) — no raw licensed rows."""
    charts: list[Chart] = []
    try:
        from app import newsletter_charts as nc
        names = [p.ticker for p in picks]
        scores = [float(p.score) for p in picks]
        charts.append(Chart(
            label="Top opportunities by score",
            image=nc.ranked_scores("Top equity opportunities — Opportunity Score", names, scores),
            caption="Cross-sectional 0-100 Opportunity Score for the top picks from the "
                    "validated blended factor model. Derived scores only.",
            source="Derived: Aegira blended factor model (Value/Quality/Growth + 12-1 momentum)."))
        contributions = [p.contributions for p in picks if p.contributions]
        if contributions and len(contributions) == len(names):
            charts.append(Chart(
                label="Factor decomposition",
                image=nc.factor_decomposition(
                    "What drives each pick — factor contribution", names, contributions),
                caption="Signed weighted-z contribution of each factor family to the composite "
                        "score. Positive extends right; it shows which factors earn each name its "
                        "rank. Derived contributions only.",
                source="Derived: Aegira blended factor model · Nasdaq Data Link / Sharadar."))
    except Exception:  # noqa: BLE001 - charts are optional; never break generation
        return charts
    return charts


def _build_equity_group() -> "Group | None":
    """Top-5 equity opportunities from the validated blended factor model (data finds;
    Ellery writes). Lazy import (heavy deps + network); resilient — returns None on any
    failure. Surfaces the DERIVED score + per-name factor decomposition (governance)."""
    try:
        from app.equity_opportunity_scan import top_opportunities
        picks = top_opportunities(n=5)
    except Exception:  # noqa: BLE001 - never break newsletter generation
        return None
    if not picks:
        return None
    items = []
    for p in picks:
        body = p.insight
        decomp = p.decomposition_str
        if decomp:
            body = f"{body} {decomp}."
        items.append(Item(
            label=p.ticker,
            value=p.value_str,
            body=body,
            tags=["Equities", p.top_factor],
            source=f"Derived score/factors · {p.name} · Nasdaq Data Link / Sharadar (derived only)",
        ))
    return Group(
        heading="Top equity opportunities",
        blurb="Discovery-driven: Aegira's validated blended factor model — Value, Quality, "
              "Growth and a 12-1 momentum sleeve, sector/size-aware and pre-registered, "
              "out-of-sample tested — ranks large/mid-cap US equities by a cross-sectional "
              "Opportunity Score. Each name is shown with its factor decomposition so the "
              "read is transparent. Research, not investment advice.",
        items=items,
        charts=_equity_charts(picks),
    )
