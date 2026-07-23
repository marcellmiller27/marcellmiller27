# JHI-SIG: 69M2705M | Newsletter content engine (server-side) | JHI Research & Analytics Firm, Inc. (proprietary)
"""Server-side generation of the editorial editions (The Economic Brief, Red Alerts,
Cross-Asset Opportunity Scan) from the live /market/quotes feed.

This is a faithful Python port of the deterministic, threshold-based logic that the
front-end components render, so a downloaded PDF matches what the reader sees on
screen. Making the backend the source of truth also lets the same content be reused
for the Step-B email attachment (no browser required).
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
class Group:
    heading: str
    blurb: str = ""
    items: list[Item] = field(default_factory=list)


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
    teaser: bool = False


QuoteMap = dict[str, Quote]

EDITION_SLUGS = ("economic-brief", "red-alerts", "opportunity-scan")

_DISCLAIMER = (
    "For research and educational purposes only. Not investment, legal, tax, or "
    "accounting advice. Written in JHI's independent professional perspective."
)


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


# ── The Economic Brief ──────────────────────────────────────────────────────
_SECTIONS: list[tuple[str, str, list[str]]] = [
    ("Monetary Policy & Rates",
     "The policy rate and the long end frame the cost of capital across the economy.",
     ["FED_FUNDS", "UST10Y"]),
    ("Inflation",
     "The pace of price growth relative to the Federal Reserve's 2% objective.",
     ["INFLATION"]),
    ("Labor & the Consumer",
     "Employment slack and household demand — the engine of two-thirds of output.",
     ["UNEMPLOYMENT", "RETAIL_SALES", "CONSUMER_SENTIMENT"]),
    ("Growth & Output", "Aggregate activity and the industrial base.",
     ["GDP", "INDUSTRIAL_PRODUCTION"]),
    ("Markets", "Cross-asset read on risk appetite and safe-haven demand.",
     ["SPX", "GOLD", "BTC"]),
]


def _commentary(symbol: str, v: float | None) -> str:
    if v is None:
        return "Awaiting the next release."
    if symbol == "FED_FUNDS":
        if v >= 4:
            return "A restrictive stance that continues to weigh on rate-sensitive demand."
        if v >= 2.5:
            return "A moderately restrictive stance; policy is not yet neutral."
        return "An accommodative stance supportive of credit and risk assets."
    if symbol == "UST10Y":
        return ("Long rates remain elevated, keeping borrowing costs and discount rates high."
                if v >= 4.5 else
                "Long rates are easing, a tailwind for valuations and refinancing.")
    if symbol == "INFLATION":
        if v <= 2.5:
            return "At or near the Fed's 2% target — consistent with an easing bias."
        if v <= 4:
            return "Running above the 2% target; the last mile of disinflation is proving sticky."
        return "Elevated and above target, constraining the path to rate cuts."
    if symbol == "UNEMPLOYMENT":
        if v < 4.5:
            return "The labor market remains firm, underpinning consumer resilience."
        if v <= 5.5:
            return "A softening labor market that bears watching for demand risk."
        return "A weak labor market signaling cyclical downside."
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


def _headline(m: QuoteMap) -> str:
    ff = _price(m, "FED_FUNDS")
    cpi = _price(m, "INFLATION")
    un = _price(m, "UNEMPLOYMENT")
    stance = "current" if ff is None else (
        "restrictive" if ff >= 4 else "moderately restrictive" if ff >= 2.5 else "accommodative")
    infl = "" if cpi is None else (
        "with inflation back near target" if cpi <= 2.5
        else f"with inflation at {cpi:.1f}%, still above the 2% target")
    labor = "" if un is None else (
        "and the labor market holding firm" if un < 4.5 else "as the labor market softens")
    return (f"Policy remains {stance} {infl} {labor}. The picture below balances a resilient "
            "consumer against still-elevated financing costs — the central tension for allocators "
            "and acquirers this cycle.").replace("  ", " ")


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
    return _headline(m), groups


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
                  "cash-flowing small businesses acquired at disciplined multiples (JHI's core "
                  "hunting ground)."),
        Item(label="Digital Assets", value=f"BTC {fmt(m.get('BTC'))}",
             body="A high-beta read on liquidity — size positions to volatility and treat as a "
                  "satellite, not a core holding, until policy eases."),
    ]


def build_edition(slug: str, quotes: list[Quote], now: datetime, full: bool) -> Edition:
    """Build a normalized Edition for the given slug. Raises KeyError for unknown slug."""
    if slug not in EDITION_SLUGS:
        raise KeyError(slug)
    m: QuoteMap = {q.symbol: q for q in quotes}
    dateline = f"Edition of {edition_date(now)}"

    if slug == "economic-brief":
        intro, groups = _economic_brief(m, full)
        return Edition(
            slug=slug, title="The Economic Brief", eyebrow="Economic Tracking",
            dateline=dateline, intro=intro, groups=groups,
            footer="Sourced from public data — Federal Reserve (FRED), U.S. Bureau of Labor "
                   "Statistics, and market feeds. Figures are as last released.",
            disclaimer=_DISCLAIMER, teaser=not full)

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
            disclaimer=_DISCLAIMER, teaser=not full)

    # opportunity-scan
    ideas = _build_scan(m)
    shown = ideas if full else ideas[:2]
    return Edition(
        slug=slug, title="Cross-Asset Opportunity Scan", eyebrow="Opportunity Scan",
        dateline=dateline,
        intro="Where the current regime — restrictive policy, above-target inflation, and a "
              "resilient but softening consumer — is creating opportunity across asset classes.",
        groups=[Group(heading="Opportunities by asset class", items=shown)],
        footer="Ideas are generated from public data (FRED · BLS · market feeds), written in "
               "JHI's independent professional perspective.",
        disclaimer=_DISCLAIMER, teaser=not full)
