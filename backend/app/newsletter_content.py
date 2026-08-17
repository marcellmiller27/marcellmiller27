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
from datetime import datetime, timezone

from app import data_registry as dr
from app.market_models import Quote

# The full indicator + market set the editions draw from (mirrors newsletter-format.ts).
# Crypto majors (ETH/SOL/XRP/XLM) and M2 liquidity are pulled for the Crypto
# Intelligence edition; they degrade gracefully when a provider/key is unavailable.
NEWSLETTER_SYMBOLS: list[str] = [
    "GDP", "FED_FUNDS", "UNEMPLOYMENT", "RETAIL_SALES", "CONSUMER_SENTIMENT",
    "INDUSTRIAL_PRODUCTION", "INFLATION", "SPX", "GOLD", "UST10Y",
    "BTC", "ETH", "SOL", "XRP", "XLM", "M2",
]


@dataclass
class Item:
    label: str
    value: str = ""
    body: str = ""
    tags: list[str] = field(default_factory=list)
    source: str | None = None
    # Data Foundation (Phase 1): "Monthly · as of Jun 2026" cadence/as-of disclosure.
    as_of_label: str | None = None


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
class PersonaPath:
    """One reader-journey path in the editor's letter (the 42Macro "persona routing").

    ``label`` and ``href`` are structural (never LLM-elevated); ``blurb`` is prose and is
    eligible for fact-locked editorial elevation. ``gated`` marks a path that points at a
    subscriber-gated module so the renderer can show a subtle upgrade nudge (never hide it).
    """

    label: str
    blurb: str
    href: str
    gated: bool = False


@dataclass
class CTA:
    label: str
    href: str


@dataclass
class EditorLetter:
    """The 42Macro-style "editor's letter" (a.k.a. lede) — an ENHANCEMENT layer that leads
    the edition without replacing any charts/data below it.

    Structure: a branded greeting → a consensus-challenging narrative lede (2-3 sentences)
    → three sharp teaser questions grounded in tracked data/entities → a "process over
    prediction" philosophy line → two persona-routing paths → a single clear CTA. Assembled
    deterministically from the edition's already-computed real themes/data, then elevated
    (prose only, fact-locked) through the E2 editorial LLM in Ellery Vance's voice.
    """

    greeting: str
    narrative: str
    questions: list[str] = field(default_factory=list)
    philosophy: str = ""
    persona_paths: list[PersonaPath] = field(default_factory=list)
    cta: CTA | None = None


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
    cadence: str = "recurring"
    # Optional 42Macro-style editor's letter that LEADS the edition (additive; the groups,
    # charts, and data below are unchanged). Any edition can opt in — the flagship Insider
    # Briefs carries the full letter; the Economic Brief carries a lighter lede.
    editor_letter: EditorLetter | None = None


QuoteMap = dict[str, Quote]

EDITION_SLUGS = (
    "economic-brief",
    "red-alerts",
    "opportunity-scan",
    "insider-briefs",
    "main-street-acquirer",
    "crypto-intelligence",
    "dividend-opportunities",
)

# ── Distribution cadence metadata ────────────────────────────────────────────
# Two broadcast rhythms drive the scheduled-generation hook and SES broadcast:
#   • "weekly-pulse"      — a lighter, time-sensitive weekly send
#   • "monthly-deep-dive" — the full flagship edition
# The Main Street Acquirer ships both: a weekly pulse and a monthly deep-dive.
EDITION_CADENCE: dict[str, tuple[str, ...]] = {
    "economic-brief": ("weekly-pulse",),
    "red-alerts": ("weekly-pulse",),
    "opportunity-scan": ("monthly-deep-dive",),
    "insider-briefs": ("monthly-deep-dive",),
    "main-street-acquirer": ("weekly-pulse", "monthly-deep-dive"),
    # Crypto Intelligence is a lighter, time-sensitive biweekly read → weekly-pulse
    # bucket (there is no separate biweekly broadcast rhythm); Dividend Opportunities
    # is the monthly income flagship → monthly-deep-dive.
    "crypto-intelligence": ("weekly-pulse",),
    "dividend-opportunities": ("monthly-deep-dive",),
}

CADENCES = ("weekly-pulse", "monthly-deep-dive")


def editions_for_cadence(cadence: str) -> list[str]:
    """Return the edition slugs that broadcast on the given cadence."""
    return [slug for slug, cads in EDITION_CADENCE.items() if cadence in cads]


def cadence_for(slug: str) -> str:
    """The primary (first) cadence label for an edition — used as edition metadata."""
    cads = EDITION_CADENCE.get(slug, ("recurring",))
    return cads[0]

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

# Digital assets carry outsized volatility/regulatory risk — the crypto edition adds
# an explicit risk note on top of the standing disclaimer.
_CRYPTO_DISCLAIMER = (
    "For research and educational purposes only. Not investment, legal, tax, or "
    "accounting advice. Digital assets are highly volatile and speculative and can "
    "lose value rapidly; size any exposure to that risk. Written in Aegira's "
    "independent professional perspective."
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


_SBA_ATTRIBUTION = (
    "SBA lending figures are derived from the U.S. Small Business Administration's public "
    "7(a)/504 FOIA loan-level data; only aggregated, derived metrics are shown — never a "
    "borrower-level row."
)
_INDUSTRY_ATTRIBUTION = (
    "Industry recession-resilience and boomer-succession scores are computed by Aegira from "
    "disclosed, weighted sub-factors grounded in public data (U.S. Bureau of Labor Statistics, "
    "U.S. Census Bureau, and BEA). Multiples and margins are derived reference ranges, not "
    "quotes, appraisals, or advice."
)


_CRYPTO_ATTRIBUTION = (
    "Crypto spot prices and 24-hour moves are from CoinGecko's public feed; the M2 "
    "money-supply liquidity read is from the Federal Reserve (FRED). Figures are shown "
    "as last released; no exchange order-book or fund-flow data is scraped."
)
_DIVIDEND_ATTRIBUTION = (
    "Dividend, income, and balance-sheet-quality figures are DERIVED by Aegira from "
    "point-in-time fundamentals (Sharadar SF1 primary · SEC EDGAR fallback) and public "
    "SEC EDGAR cash-flow filings, combined with live market price. Only derived metrics "
    "(yields, payout, coverage, margins, ROE) are shown — never raw licensed rows."
)


def _methodology_for(slug: str) -> str:
    """Base methodology, plus source-specific attribution / derived-only disclaimers so
    attribution always rides with the data on each data-derived edition."""
    if slug == "opportunity-scan":
        return " ".join([METHODOLOGY, _SF1_ATTRIBUTION, _DERIVED_ONLY_NOTE, _BACKTEST_DISCLAIMER])
    if slug == "main-street-acquirer":
        return " ".join([METHODOLOGY, _SBA_ATTRIBUTION, _INDUSTRY_ATTRIBUTION, _DERIVED_ONLY_NOTE])
    if slug == "crypto-intelligence":
        return " ".join([METHODOLOGY, _CRYPTO_ATTRIBUTION])
    if slug == "dividend-opportunities":
        return " ".join([METHODOLOGY, _DIVIDEND_ATTRIBUTION, _DERIVED_ONLY_NOTE])
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


def _as_of(q: Quote | None) -> str | None:
    """The value's cadence/as-of disclosure label ("Monthly · as of Jun 2026").

    Falls back to computing it from the registry cadence when the quote predates the
    Data Foundation fields, so older/cached quotes still disclose honestly."""
    if q is None:
        return None
    if q.as_of_label:
        return q.as_of_label
    return dr.as_of_label(q.cadence or dr.cadence_for(q.symbol), q.observation_date)


def _pending_label(symbol: str) -> str:
    """A never-fabricate placeholder for a genuinely missing series: discloses the
    cadence and that the value is pending the next release (rather than omitting it)."""
    return f"pending ({dr.cadence_label(dr.cadence_for(symbol))} · next release)"


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
    # Graceful degradation: render with whatever series ARE available; omit only the
    # missing bar. Never return [] just because one series (e.g. Fed Funds) is missing.
    if len(labels) < 1:
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
    # Partial-render: draw whatever levels are available rather than an empty exhibit.
    if len(labels) < 1:
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
            if q is None or q.price is None:
                # Never omit: disclose the indicator as pending its next release.
                spec = dr.get_series(sym)
                items.append(Item(label=spec.name if spec else sym, value=_pending_label(sym),
                                  body="Awaiting the next release.",
                                  as_of_label=_as_of(q)))
                continue
            items.append(Item(label=q.name, value=fmt(q), body=_commentary(sym, q.price),
                              source=q.note, as_of_label=_as_of(q)))
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
        if q is None or q.price is None:
            spec = dr.get_series(sym)
            items.append(Item(label=spec.name if spec else sym, value=_pending_label(sym),
                              body="Awaiting the next release.", as_of_label=_as_of(q)))
            continue
        items.append(Item(label=q.name, value=fmt(q), body=_commentary(sym, q.price),
                          source=q.note, as_of_label=_as_of(q)))
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


# ── The editor's letter (42Macro-style lede) — an additive enhancement layer ─────
# The narrative letter LEADS and threads the piece; the graphs, tables, ratios, factor
# screens and cross-asset data below still CARRY the body. Assembled here from the
# edition's ALREADY-COMPUTED real data so every teaser question references a series we
# actually track; the prose is then elevated (fact-locked) by the E2 editorial LLM.
_PHILOSOPHY = (
    "Markets will always hand you something to worry about; the edge is a repeatable "
    "process, not a prediction."
)

# The standing persona routing. Both paths render for every reader; the "Act on the
# Signals" path points at the gated modules (a subtle upgrade nudge for non-subscribers
# is added in the renderer — the path is never hidden).
_CORE_READ_BLURB = (
    "Know what's changing. Stay with the standing macro read and this month's thesis, "
    "then carry the through-line into every decision."
)
_ACT_SIGNALS_BLURB = (
    "Stay on offense. Take the read into the Cross-Asset Opportunity Scan and Aegira's "
    "Valuation signals to turn the macro call into positioning."
)


def _persona_paths() -> list[PersonaPath]:
    return [
        PersonaPath(label="The Core Read", blurb=_CORE_READ_BLURB, href="#news-summary"),
        PersonaPath(label="Act on the Signals", blurb=_ACT_SIGNALS_BLURB,
                    href="/opportunities", gated=True),
    ]


def _insider_editor_letter(key: str, m: QuoteMap) -> EditorLetter:
    """The FULL editor's letter for the flagship (Insider Briefs → "The Aegira Monthly").

    Greeting → consensus-challenging narrative → three teaser questions grounded in the
    series this edition tracks → philosophy → two persona paths → one CTA. Numbers are
    reused verbatim from the edition's own data, so the fact-lock whitelist covers them.
    """
    ff, cpi, un = fmt(m.get("FED_FUNDS")), fmt(m.get("INFLATION")), fmt(m.get("UNEMPLOYMENT"))
    rr = _real_rate(m)
    rr_s = f"{rr:.2f}%" if rr is not None else "positive"
    gold = fmt(m.get("GOLD"))

    lede_by_theme = {
        "real-cost-of-capital": (
            "This month the data pushed back on a few things the Street takes for granted. "
            f"With the real 10-year yield near {rr_s}, the after-inflation cost of capital — "
            "not the headline level of rates — is quietly resetting the price of every asset, "
            "deal, and valuation. The consensus is still trading the first cut; the structural "
            "shift is that positive real rates now pay you to prefer realized cash flow over "
            "promised growth."),
        "last-mile-disinflation": (
            "This month the data pushed back on the easy disinflation story. With CPI at "
            f"{cpi} against the 2% target and the funds rate still {ff}, the last mile is "
            "concentrated in the stickiest components — the part the market keeps assuming "
            "away. The structural read the Street may be under-pricing: persistence, not the "
            "level, is what keeps policy restrictive."),
        "labor-at-the-margin": (
            "This month the data pushed back on the soft-landing consensus. At "
            f"{un} unemployment the labor market is still the pivot, but the margin is where "
            "cycles turn — and it is the swing factor for the consumer, for credit, and for "
            "the Fed's hand. The shift worth watching is not the level of jobs but the "
            "direction of the marginal one."),
        "safe-haven-bid": (
            f"This month the data pushed back on a tidy narrative. Gold at {gold} is rallying "
            f"with real rates still near {rr_s} — a combination that usually does not happen, "
            "and one the Street tends to explain away. The structural signal underneath: a "
            "hedge against fiscal risk and debasement, not a bet on deflation."),
    }
    questions_by_theme = {
        "real-cost-of-capital": [
            (f"If the real 10-year yield holds near {rr_s}, which valuations still clear the "
             "hurdle — and which are living on borrowed time?"),
            (f"With Fed Funds at {ff}, is the levered-buyout math the market still underwrites "
             "even solvent?"),
            ("When capital is no longer free, does the tape pay up for realized cash flow "
             "before it pays for a promise?"),
        ],
        "last-mile-disinflation": [
            (f"Is the market pricing the last mile of disinflation, or the cut it wants at "
             f"CPI {cpi}?"),
            (f"With the funds rate at {ff}, how much patience is really left in the "
             "reaction function?"),
            ("If services and shelter stay sticky, where does the pain land first — duration "
             "or growth equity?"),
        ],
        "labor-at-the-margin": [
            f"At {un} unemployment, is the consumer still the engine or the risk?",
            "Does credit performance follow the marginal job before the headline turns?",
            ("When the dual mandate tilts toward employment, how far forward does the first "
             "cut really pull?"),
        ],
        "safe-haven-bid": [
            f"Why is gold bid at {gold} while real rates sit near {rr_s}?",
            "Is the haven trade pricing deflation, or fiscal debasement?",
            ("If the Fed is forced to ease into sticky inflation, what actually protects "
             "purchasing power?"),
        ],
    }
    narrative = lede_by_theme.get(key, lede_by_theme["real-cost-of-capital"])
    questions = questions_by_theme.get(key, questions_by_theme["real-cost-of-capital"])
    return EditorLetter(
        greeting="Welcome to The Aegira Monthly.",
        narrative=narrative,
        questions=questions,
        philosophy=_PHILOSOPHY,
        persona_paths=_persona_paths(),
        cta=CTA(label="Explore Aegira Research", href="/reports"),
    )


def _economic_editor_letter(m: QuoteMap) -> EditorLetter:
    """A LIGHTER lede for the Economic Brief: greeting + narrative + one teaser question +
    both persona paths + a CTA. Numbers are drawn from the brief's own thesis/data."""
    ff, cpi = fmt(m.get("FED_FUNDS")), fmt(m.get("INFLATION"))
    rr = _real_rate(m)
    rr_s = f"{rr:.2f}%" if rr is not None else "positive"

    parts = ["This week the data pushed back on the easy consensus."]
    if ff != "—" and cpi != "—":
        parts.append(
            f"With the policy rate at {ff} and inflation at {cpi} against the 2% target, the "
            "last mile of disinflation — not growth — still governs the timing of relief.")
    if rr is not None:
        parts.append(
            f"A real 10-year yield near {rr_s} keeps the hurdle high and rewards patience "
            "over hope.")
    narrative = " ".join(parts)

    return EditorLetter(
        greeting="Welcome to The Economic Brief.",
        narrative=narrative,
        questions=["Is the market pricing the last mile of disinflation, or the cut it wants?"],
        philosophy=_PHILOSOPHY,
        persona_paths=_persona_paths(),
        cta=CTA(label="Explore Aegira Research", href="/newsletters"),
    )


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
        footer="A rotating deep-dive on the most salient macro theme, built from public data: "
               "Sharadar SF1 (Nasdaq Data Link) — point-in-time fundamentals (primary) · SEC "
               "EDGAR (fallback) · FRED · BLS · market feeds. Written in Aegira's independent "
               "professional perspective.",
        disclaimer=_DISCLAIMER, methodology=METHODOLOGY, teaser=not full,
        charts=_insider_chart(m, title) if full else [],
        cadence=cadence_for("insider-briefs"),
        editor_letter=_insider_editor_letter(key, m))


# ── The Main Street Acquirer ─────────────────────────────────────────────────
# A newsletter for SMB / search-fund / ETA acquirers. Every figure is DERIVED from
# public data (FRED macro · SBA 7(a) FOIA · BLS/Census/BEA industry) and fact-locked.
# Engines are imported lazily and wrapped so a data gap never breaks generation.

_MSA_PLAYBOOKS: list[tuple[str, str, list[tuple[str, str]]]] = [
    (
        "Sourcing off-market deals",
        "The best main-street deals rarely hit a marketplace. A disciplined acquirer builds "
        "proprietary flow rather than bidding against a crowd on brokered listings.",
        [
            ("Direct-to-owner outreach", "Target owners aged 55+ in resilient trades (the "
             "succession wave) with a respectful, specific thesis — not a generic mailer."),
            ("Intermediary relationships", "Cultivate accountants, wealth advisors, and "
             "trade-association contacts who meet retiring owners first."),
            ("Buy-box discipline", "Write a one-page buy box (industry, size, geography, "
             "owner-transition profile) and disqualify fast to protect your time."),
        ],
    ),
    (
        "Reading a CIM without getting fooled",
        "A confident-looking CIM is a sales document. The acquirer's job is to separate "
        "durable, transferable cash flow from owner-dependent, one-time, or dressed-up EBITDA.",
        [
            ("Normalize the add-backs", "Discount aggressive add-backs and re-underwrite to "
             "a defensible SDE/EBITDA before you anchor on a price."),
            ("Test owner-dependence", "If the owner is the top rainmaker or master "
             "technician, price and structure for a real transition, not a clean handoff."),
            ("Insist on a QoE", "For anything financeable, a quality-of-earnings review pays "
             "for itself by catching the numbers that don't reconcile to the bank statements."),
        ],
    ),
    (
        "Structuring the transition",
        "The deal doesn't end at close — the first 100 days determine whether the cash flow "
        "you underwrote actually shows up. Structure the transition into the deal.",
        [
            ("Seller note + earnout", "Align the seller through a note and a modest earnout so "
             "incentives survive the handoff — and DSCR has a cushion."),
            ("Retain the bench", "Identify and lock in the key employees before close; their "
             "relationships are often the real asset."),
            ("Transition services", "Negotiate a paid, time-boxed consulting period so "
             "customer and vendor relationships transfer deliberately."),
        ],
    ),
    (
        "Underwriting to DSCR, not to a multiple",
        "In a positive-real-rate world, the multiple is downstream of the debt math. The "
        "binding constraint on a leveraged main-street deal is debt-service coverage.",
        [
            ("Solve for coverage first", "Back into the price that keeps DSCR comfortably "
             "above the lender's floor after a realistic capex and owner-salary load."),
            ("Stress the downside", "Underwrite a revenue-decline scenario; if coverage "
             "breaks below 1.0x in a mild downturn, the structure is too tight."),
            ("Right-size the equity", "More equity or a larger seller note strengthens DSCR "
             "and lender appetite — and buys negotiating room on price."),
        ],
    ),
]


def _usd(value: float | None) -> str:
    if value is None:
        return "—"
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:.0f}K"
    return f"${value:,.0f}"


# Map an industry-resilience key to the Deal X-Ray industry vocabulary.
_MSA_INDUSTRY_MAP = {
    "hvac": "hvac", "electrical": "electrical", "landscaping": "landscaping",
    "restaurant": "restaurant", "healthcare_services": "healthcare_services",
    "professional_services": "professional_services", "logistics": "logistics",
    "auto_repair": "general",
}


def _msa_thesis(m: QuoteMap) -> str:
    """Acquirer-framed executive thesis — the macro read through the SBA/DSCR lens."""
    ff, rr = _price(m, "FED_FUNDS"), _real_rate(m)
    ten = _price(m, "UST10Y")
    parts = [
        "For the main-street acquirer, the macro backdrop is not an abstraction — it sets the "
        "cost of the debt that funds the deal and the discipline the multiple must respect."
    ]
    if ff is not None:
        prime = ff + 3.0  # prime ≈ policy rate + ~3 points
        parts.append(
            f"With the federal funds rate at {ff:.2f}%, prime sits near {prime:.2f}% and a "
            "typical SBA 7(a) acquisition loan (prime + a spread) is expensive — so debt-service "
            "coverage, not the headline multiple, is the binding constraint on every offer.")
    if rr is not None and ten is not None:
        parts.append(
            f"A real 10-year yield around {rr:.2f}% (10Y {ten:.2f}% − CPI) rewards patient buyers "
            "of cash-flowing businesses bought at disciplined multiples over levered bets on "
            "multiple expansion.")
    parts.append(
        "This edition pairs that macro read with the SBA lending picture, a recession-resilient "
        "industry in the succession wave, a working acquisition playbook, and a fact-locked deal "
        "teardown — all from public data, all derived, none of it advice.")
    return " ".join(parts)


def _msa_sba_group(full: bool) -> tuple["Group | None", list["Chart"]]:
    """SBA Lending Intelligence — derived funding/lender/trend reads + charts."""
    try:
        from app import sba_intelligence as sba
        intel = sba.intelligence(top_n=8)
    except Exception:  # noqa: BLE001 - never break generation
        return None, []

    fy = intel.fiscal_years
    span = f"FY{fy[0]}–FY{fy[-1]}" if fy else "recent fiscal years"
    items: list[Item] = []
    latest = intel.yearly_trends[-1] if intel.yearly_trends else None
    if latest:
        items.append(Item(
            label=f"7(a) volume, {span}", value=f"{intel.loan_count:,} loans · {_usd(intel.total_gross_approval)}",
            body=(f"Across the tracked main-street trades, FY{latest.fiscal_year} saw {latest.loan_count:,} "
                  f"approvals averaging {_usd(latest.avg_gross_approval)} — the acquisition-financing "
                  "pipeline SMB buyers actually draw on."),
            source=intel.source))
    top = intel.by_industry[0] if intel.by_industry else None
    if top:
        items.append(Item(
            label="Best-funded trade", value=f"{top.naics_description}",
            body=(f"{top.loan_count:,} loans totalling {_usd(top.total_gross_approval)}; median deal "
                  f"{_usd(top.median_gross_approval)}, with {top.change_of_ownership_pct:.0f}% financing a "
                  "change of ownership — a direct read on where SBA capital backs acquisitions."),
            tags=["SBA 7(a)", f"NAICS {top.naics_code}"]))
    if intel.active_lenders:
        top_lenders = ", ".join(f"{le.bank_name} ({le.loan_count})" for le in intel.active_lenders[:3])
        items.append(Item(
            label="Most active lenders", value=f"{len(intel.active_lenders)} banks",
            body=f"By approval count in the sample: {top_lenders}. These are the desks that "
                 "understand main-street acquisition credit and move fastest.",
            source="Derived from SBA 7(a) FOIA (aggregated by lender)."))
    for note in intel.notes:
        items.append(Item(label="Data note", value="", body=note))

    charts: list[Chart] = []
    if full:
        charts = _msa_sba_charts(intel)
    group = Group(
        heading="SBA Lending Intelligence",
        blurb="Where SBA 7(a) capital is actually flowing across main-street trades — funding "
              "volume, typical deal sizes, the most active lenders, and the acquisition "
              "(change-of-ownership) share. Derived from the SBA's public FOIA loan-level data.",
        items=items, charts=charts)
    return group, charts


def _msa_sba_charts(intel) -> list["Chart"]:
    charts: list[Chart] = []
    try:
        from app import newsletter_charts as nc
        if intel.yearly_trends:
            years = [f"FY{t.fiscal_year}" for t in intel.yearly_trends]
            totals = [t.total_gross_approval for t in intel.yearly_trends]
            charts.append(Chart(
                label="SBA 7(a) volume by fiscal year",
                image=nc.labeled_levels("SBA 7(a) gross approval by fiscal year ($M)",
                                        years, [v / 1_000_000 for v in totals], unit="M"),
                caption="Total SBA 7(a) gross loan approvals across the tracked main-street trades, "
                        "by fiscal year. Derived aggregate of public FOIA loan-level records.",
                source=intel.source))
        top = intel.by_industry[:6]
        if top:
            labels = [i.naics_description[:28] for i in top]
            meds = [i.median_gross_approval for i in top]
            charts.append(Chart(
                label="Median SBA loan by trade",
                image=nc.horizontal_bars("Median SBA 7(a) loan by trade ($K)", labels, meds,
                                         value_suffix="K", xlabel="Median gross approval ($K)",
                                         scale=1_000.0),
                caption="Median SBA 7(a) gross approval per loan by trade — a proxy for typical "
                        "financeable deal size. Derived medians only.",
                source=intel.source))
    except Exception:  # noqa: BLE001
        return charts
    return charts


def _msa_industry_group(profile, snap, full: bool) -> Group:
    """Recession-Resilient Industry Spotlight — one industry per issue."""
    from app import industry_resilience as ir  # local import for weights disclosure
    items: list[Item] = [
        Item(label="Recession resilience", value=f"{profile.recession_resilience:.0f}/100",
             body="Composite of essential-service demand, BLS employment stability through "
                  "downturns, and recurring-revenue tendency (disclosed weights "
                  f"{int(ir.RESILIENCE_WEIGHTS['essential_service']*100)}/"
                  f"{int(ir.RESILIENCE_WEIGHTS['demand_stability']*100)}/"
                  f"{int(ir.RESILIENCE_WEIGHTS['recurring_contract']*100)}).",
             tags=["Resilience"]),
        Item(label="Succession opportunity", value=f"{profile.succession_opportunity:.0f}/100",
             body="Composite of the owner-age-55+ share (the succession wave), market "
                  "fragmentation, and SBA financeability — how deep and bankable the acquisition "
                  "pool is.",
             tags=["Succession"]),
        Item(label="Typical valuation range",
             value=f"{profile.typical_multiple_low:.1f}–{profile.typical_multiple_high:.1f}x SDE/EBITDA",
             body=f"Derived reference range (base ~{profile.typical_multiple_base:.1f}x) with a "
                  f"typical EBITDA margin near {profile.typical_ebitda_margin*100:.0f}%. Reference "
                  "only — not a quote or appraisal.",
             tags=["Valuation"]),
    ]
    if profile.pros:
        items.append(Item(label="Why acquirers like it", value="",
                          body=" ".join(f"• {p}" for p in profile.pros)))
    if profile.cons:
        items.append(Item(label="What to watch", value="",
                          body=" ".join(f"• {c}" for c in profile.cons)))
    if profile.red_flags:
        items.append(Item(label="Red flags", value="",
                          body=" ".join(f"• {r}" for r in profile.red_flags)))
    if snap is not None:
        items.append(Item(
            label="SBA financing read", value=_usd(snap.median_gross_approval) + " median loan",
            body=(f"In the SBA data, this trade shows {snap.loan_count:,} loans with a "
                  f"{snap.change_of_ownership_pct:.0f}% change-of-ownership share and an average "
                  f"term near {snap.avg_term_months/12:.0f} years — a financeable, acquisition-"
                  "active corner of main street."),
            source="Derived from SBA 7(a) FOIA (aggregated for this trade)."))

    charts: list[Chart] = []
    if full:
        try:
            from app import newsletter_charts as nc
            charts.append(Chart(
                label="Resilience vs. succession",
                image=nc.labeled_levels(
                    f"{profile.name} — acquirer score",
                    ["Recession resilience", "Succession opportunity"],
                    [profile.recession_resilience, profile.succession_opportunity],
                    unit=""),
                caption="Aegira's derived composite scores for the spotlight industry, from "
                        "disclosed, weighted public-data sub-factors. Scores only.",
                source="Derived: Aegira industry-resilience model (BLS · Census · BEA)."))
        except Exception:  # noqa: BLE001
            charts = []
    return Group(
        heading=f"Recession-Resilient Industry Spotlight — {profile.name}",
        blurb="One industry per issue, scored for recession resilience and boomer-succession "
              "opportunity, with derived multiples/margins, the acquirer's pros and cons, and the "
              "red flags to underwrite against.",
        items=items, charts=charts)


def _msa_playbook_group(now: datetime) -> Group:
    """Rotating Acquisition Playbook — one tactical chapter per issue."""
    idx = (int(now.strftime("%U")) + now.year * 53) % len(_MSA_PLAYBOOKS)
    title, blurb, plays = _MSA_PLAYBOOKS[idx]
    return Group(
        heading=f"Acquisition Playbook — {title}",
        blurb=blurb,
        items=[Item(label=label, value="", body=body) for label, body in plays])


def _msa_teardown_group(profile, snap) -> tuple["Group | None", "object | None"]:
    """Deal Teardown — run the Deal X-Ray + valuation lens on a representative deal
    sized to the SBA data and the spotlight industry's derived economics."""
    try:
        from app.deal_xray import analyze
        from app.deal_xray_models import DealInput
    except Exception:  # noqa: BLE001
        return None, None

    median_loan = (snap.median_gross_approval if snap else 900_000.0) or 900_000.0
    asking = round(median_loan / 0.85)  # SBA loan ≈ 85% of price → implied enterprise value
    ebitda = asking / max(profile.typical_multiple_base, 0.5)
    margin = max(profile.typical_ebitda_margin, 0.05)
    revenue = ebitda / margin
    industry_key = _MSA_INDUSTRY_MAP.get(profile.key, "general")

    deal = DealInput(
        business_name=f"Representative {profile.name} target",
        industry=industry_key,
        revenue=round(revenue),
        revenue_prior=round(revenue * 0.94),
        reported_ebitda=round(ebitda * 1.12),  # seller-presented (with add-backs)
        addbacks=round(ebitda * 0.18),
        earnings_history=[round(ebitda * 1.12), round(ebitda * 1.02), round(ebitda * 0.95)],
        employees=max(8, int(revenue / 200_000)),
        owner_involvement="owner_operated",
        customer_concentration_pct=18.0,
        recurring_revenue_pct=40.0,
        asking_price=asking,
        down_payment_pct=10.0,
        seller_note_pct=10.0,
        loan_term_years=10,
    )
    try:
        report = analyze(deal)
    except Exception:  # noqa: BLE001
        return None, None

    val = report.valuation
    items = [
        Item(label="Representative target",
             value=f"{_usd(deal.revenue)} rev · {_usd(deal.reported_ebitda)} EBITDA (as presented)",
             body=(f"A representative {profile.name.lower()} deal, sized to the SBA median loan and "
                   f"the trade's ~{profile.typical_multiple_base:.1f}x reference multiple. Illustrative "
                   "and derived — not a real listing.")),
        Item(label="Deal X-Ray score",
             value=f"{report.deal_score}/100 · {report.recommendation}",
             body=f"Credibility/ethic rating {report.ethic_rating}/100. {report.ethic_note}",
             tags=["Deal X-Ray"]),
        Item(label="Valuation lens",
             value=f"{_usd(val.multiple_value_low)}–{_usd(val.multiple_value_high)} (fair ~{_usd(val.multiple_value_base)})",
             body=(f"On a normalized {_usd(val.normalized_ebitda)} basis at "
                   f"{val.industry_multiple_low:.1f}–{val.industry_multiple_high:.1f}x, cross-checked "
                   f"by a curbed DCF ({_usd(val.dcf_enterprise_value)}). Asking {_usd(val.asking_price)} "
                   f"reads {val.verdict}."),
             tags=["Valuation"]),
    ]
    qoe_flags = [q for q in report.diligence_questions if "quality-of-earnings" in q.lower() or "add-back" in q.lower()]
    items.append(Item(
        label="Quality-of-earnings watch",
        value=f"add-backs {report.key_metrics.get('Add-back ratio', 'n/a')}",
        body=(qoe_flags[0] if qoe_flags else "Re-underwrite the seller-presented EBITDA to a "
              "defensible basis and confirm each add-back against source documents before anchoring "
              "on price."),
        tags=["QoE"]))
    return Group(
        heading="Deal Teardown",
        blurb="The Deal X-Ray engine, a quality-of-earnings lens, and Aegira's valuation view "
              "applied to a representative, fact-locked deal — how a disciplined acquirer would "
              "read it.",
        items=items), report


def _msa_financing_group(report) -> Group:
    """Financing Corner — SBA/DSCR structures from the teardown's financing options."""
    items: list[Item] = []
    if report is not None:
        for opt in report.financing_options:
            dscr = f"DSCR {opt.dscr:.2f}" if opt.dscr is not None else "DSCR n/a"
            fit = " · SBA-fit" if opt.sba_fit else ""
            items.append(Item(
                label=opt.label, value=f"{dscr}{fit}",
                body=(f"Equity {_usd(opt.equity_required)}, seller note {_usd(opt.seller_note)}, "
                      f"loan {_usd(opt.loan_amount)}; annual debt service {_usd(opt.annual_debt_service)}. "
                      f"{opt.note}"),
                tags=["Financing"]))
    items.append(Item(
        label="The rule of thumb", value="target DSCR ≥ 1.25x",
        body="Lenders want debt-service coverage comfortably above 1.0x; 1.25x+ after a realistic "
             "owner salary and maintenance capex is the durable target. Solve for the price that "
             "holds coverage in a downturn, then negotiate."))
    return Group(
        heading="Financing Corner — SBA & DSCR structures",
        blurb="How the same deal pencils under different capital structures — the SBA 7(a) 90/10 "
              "with a seller note versus a more conservative down payment — read through debt-"
              "service coverage. Derived from the teardown; not a financing offer.",
        items=items)


def _msa_metric_group(now: datetime, m: QuoteMap, profile, snap) -> Group:
    """Metric of the issue — a single rotating, fact-locked number worth internalizing."""
    rr = _real_rate(m)
    candidates: list[tuple[str, str, str]] = []
    if snap is not None:
        candidates.append((
            "Change-of-ownership share of SBA lending",
            f"{snap.change_of_ownership_pct:.0f}%",
            f"Of SBA 7(a) loans in {profile.name.lower()} (in the sample), this share financed an "
            "acquisition rather than expansion — a direct gauge of how bankable buying this "
            "business is."))
        candidates.append((
            "Median SBA acquisition loan",
            _usd(snap.median_gross_approval),
            f"The median SBA 7(a) loan in {profile.name.lower()} — a practical anchor for the "
            "financeable size of a main-street deal in this trade."))
    candidates.append((
        f"Recession-resilience score — {profile.name}",
        f"{profile.recession_resilience:.0f}/100",
        "Aegira's derived composite of essential-service demand, employment stability, and "
        "recurring revenue for the spotlight industry."))
    if rr is not None:
        candidates.append((
            "The real cost of capital",
            f"{rr:.2f}%",
            "The real 10-year yield (10Y − CPI) — the after-inflation hurdle every acquisition "
            "must clear. When capital isn't free, price discipline is the edge."))
    idx = (int(now.strftime("%U")) + now.year * 53) % len(candidates)
    label, value, body = candidates[idx]
    return Group(
        heading="Metric of the Issue",
        blurb="One number, fact-locked, worth carrying into your next conversation with a "
              "seller or a lender.",
        items=[Item(label=label, value=value, body=body)])


def _main_street_acquirer(m: QuoteMap, now: datetime, full: bool) -> Edition:
    dateline = f"Edition of {edition_date(now)}"
    intro = _msa_thesis(m)

    groups: list[Group] = []

    # Charts live at the group level (the "brief" renderer shows both edition- and
    # group-level charts, so keeping them per-group avoids double-rendering).
    sba_group, _ = _msa_sba_group(full)
    if sba_group is not None:
        groups.append(sba_group)

    # Spotlight industry + its SBA snapshot (deterministic per-week rotation).
    profile = None
    snap = None
    try:
        from app import industry_resilience as ir
        profile = ir.spotlight_for(now)
    except Exception:  # noqa: BLE001
        profile = None
    if profile is not None:
        try:
            from app import sba_intelligence as sba
            snap = sba.industry_snapshot(sba.intelligence(top_n=20), profile.naics_prefixes)
        except Exception:  # noqa: BLE001
            snap = None
        groups.append(_msa_industry_group(profile, snap, full))

    report = None
    if full:
        groups.append(_msa_playbook_group(now))
        if profile is not None:
            teardown_group, report = _msa_teardown_group(profile, snap)
            if teardown_group is not None:
                groups.append(teardown_group)
            groups.append(_msa_financing_group(report))
        groups.append(_msa_metric_group(now, m, profile, snap) if profile is not None
                      else Group(heading="Metric of the Issue", items=[]))

    return Edition(
        slug="main-street-acquirer", title="The Main Street Acquirer",
        eyebrow="Main Street Acquirer",
        dateline=dateline, intro=intro, groups=groups,
        footer="Built for SMB, search-fund, and ETA acquirers from public data — Federal Reserve "
               "(FRED), the SBA's 7(a)/504 FOIA loan-level data, and BLS/Census/BEA industry "
               "series. Figures are derived and shown as last released; no marketplace data is "
               "scraped or used.",
        disclaimer=_DISCLAIMER, methodology=_methodology_for("main-street-acquirer"),
        teaser=not full, charts=[],
        cadence=cadence_for("main-street-acquirer"))


# ── Crypto Intelligence ──────────────────────────────────────────────────────
# A biweekly digital-asset read: the Bitcoin/crypto cycle, price action across the
# majors, and the liquidity & adoption backdrop (M2 money supply + the real-rate
# regime). Built from the existing crypto quote adapter (CoinGecko) + FRED — no new
# vendor. Every figure is shown as last released; nothing is fabricated.
_CRYPTO_MAJORS: list[str] = ["BTC", "ETH", "SOL", "XRP", "XLM"]


def _crypto_commentary(symbol: str, q: Quote) -> str:
    chg = q.change_percent
    trend = ""
    if chg is not None:
        if abs(chg) < 0.5:
            trend = " Little changed over the session — consolidating."
        else:
            trend = (f" {'Up' if chg > 0 else 'Down'} {abs(chg):.1f}% on the session, a "
                     f"{'risk-on' if chg > 0 else 'risk-off'} tell.")
    base = {
        "BTC": "The reserve asset of the space and the anchor of the cycle — a high-beta "
               "read on global liquidity and institutional adoption.",
        "ETH": "The largest smart-contract network — a proxy for on-chain activity, "
               "staking demand, and the app/L2 economy.",
        "SOL": "A high-throughput L1 — a beta-on-beta read on speculative appetite and "
               "developer/retail flows.",
        "XRP": "A payments-focused token — sensitive to regulatory clarity and "
               "cross-border settlement adoption.",
        "XLM": "A payments/settlement network — a small-cap read on the adoption theme.",
    }.get(symbol, "A digital-asset read on liquidity and risk appetite.")
    return base + trend


def _crypto_majors_group(m: QuoteMap) -> Group:
    items: list[Item] = []
    for sym in _CRYPTO_MAJORS:
        q = m.get(sym)
        if q is None or q.price is None:
            spec = dr.get_series(sym)
            items.append(Item(label=spec.name if spec else sym, value=_pending_label(sym),
                              body="Awaiting the next quote from the crypto feed.",
                              as_of_label=_as_of(q)))
            continue
        items.append(Item(label=q.name, value=fmt(q), body=_crypto_commentary(sym, q),
                          source=q.note, as_of_label=_as_of(q)))
    return Group(
        heading="Majors — price & 24-hour action",
        blurb="Spot price and the 24-hour move across the majors — Bitcoin as the cycle "
              "anchor, then the large-cap alts. Levels are shown as last released.",
        items=items)


def _crypto_liquidity_group(m: QuoteMap) -> Group:
    """Liquidity & adoption signals: M2 money supply (the liquidity tide crypto rides),
    the policy/real-rate backdrop, and the ETF/price-action read (proxied honestly by
    spot action + liquidity — no fabricated fund-flow numbers)."""
    items: list[Item] = []
    m2 = m.get("M2")
    if m2 is not None and m2.price is not None:
        items.append(Item(
            label="M2 money supply", value=fmt(m2),
            body="The broad-money tide crypto has historically ridden: expanding liquidity "
                 "is a tailwind for scarce, high-beta assets; contracting liquidity is a "
                 "headwind. This is the single most important macro input for the cycle.",
            source=m2.note, as_of_label=_as_of(m2)))
    else:
        items.append(Item(
            label="M2 money supply", value=_pending_label("M2"),
            body="Liquidity read pending the next FRED release (set FRED_API_KEY to "
                 "activate the live series).", as_of_label=_as_of(m2)))
    rr = _real_rate(m)
    if rr is not None:
        items.append(Item(
            label="Real rates backdrop", value=f"{rr:.2f}% (10Y − CPI)",
            body=("Positive real yields are a headwind for non-yielding assets like crypto — "
                  "the opportunity cost of holding is real."
                  if rr >= 1 else
                  "Only modestly positive real yields lower the opportunity cost of holding "
                  "non-yielding assets — a less punishing backdrop for crypto."),
            source="Derived: 10-year Treasury − headline CPI (FRED)."))
    ff = m.get("FED_FUNDS")
    if ff is not None and ff.price is not None:
        items.append(Item(
            label="Policy stance", value=fmt(ff),
            body="Restrictive policy drains liquidity and caps speculative risk appetite; the "
                 "first cuts historically re-open the risk window for digital assets.",
            source=ff.note, as_of_label=_as_of(ff)))
    btc = m.get("BTC")
    if btc is not None and btc.price is not None:
        items.append(Item(
            label="ETF / price-action read", value="spot-led",
            body=(f"With Bitcoin at {fmt(btc)}, the desk reads adoption and spot-ETF demand "
                  "through price action and liquidity rather than any single fund-flow print — "
                  "sustained strength above prior ranges is the cleanest tell that institutional "
                  "demand is absorbing supply."),
            tags=["Adoption", "ETF"]))
    return Group(
        heading="Liquidity & adoption signals",
        blurb="What actually drives the cycle: the money-supply tide (M2), the real-rate "
              "opportunity cost, the policy stance, and the spot/ETF adoption read.",
        items=items)


def _crypto_lens_group(m: QuoteMap) -> Group:
    """Positioning lens — how the desk frames digital assets for allocators."""
    return Group(
        heading="The Aegira lens",
        blurb="How the desk frames digital assets — interpretation, not a forecast or advice.",
        items=[
            Item(label="Position sizing", value="satellite, sized to volatility",
                 body="Treat crypto as a high-beta satellite, not a core holding, until policy "
                      "eases and liquidity turns. Size to the drawdown you can tolerate, not the "
                      "upside you hope for."),
            Item(label="Quality within the space", value="BTC/ETH core",
                 body="Concentration in the two largest, most liquid networks (Bitcoin, "
                      "Ethereum) carries less idiosyncratic risk than the long tail of alts; "
                      "treat small-caps as speculative options."),
            Item(label="The cycle trigger", value="liquidity inflection",
                 body="The clearest catalyst is a liquidity inflection — a durable M2 "
                      "re-expansion and/or the start of the cutting cycle. Watch the tide, not "
                      "the headlines."),
        ])


def _crypto_chart(m: QuoteMap) -> list["Chart"]:
    """A 24-hour move bar across the majors — plotted only from released % changes."""
    labels: list[str] = []
    values: list[float] = []
    for sym in _CRYPTO_MAJORS:
        q = m.get(sym)
        if q is not None and q.change_percent is not None:
            labels.append(sym)
            values.append(q.change_percent)
    if len(labels) < 1:
        return []
    try:
        from app import newsletter_charts as nc
        img = nc.labeled_levels("Crypto majors — 24-hour move", labels, values, unit="%")
    except Exception:  # noqa: BLE001 - never break newsletter generation
        return []
    return [Chart(
        label="Crypto majors — 24-hour move",
        image=img,
        caption="The session move across the crypto majors, as last released by the spot "
                "feed. Levels only; no series is implied.",
        source="Derived from CoinGecko spot 24-hour changes.")]


def _crypto_intelligence(m: QuoteMap, now: datetime, full: bool) -> Edition:
    dateline = f"Edition of {edition_date(now)}"

    btc, eth = m.get("BTC"), m.get("ETH")
    m2 = _price(m, "M2")
    rr = _real_rate(m)
    parts: list[str] = []
    if btc is not None and btc.price is not None:
        move = ""
        if btc.change_percent is not None:
            move = (f", {'up' if btc.change_percent > 0 else 'down'} "
                    f"{abs(btc.change_percent):.1f}% on the session")
        parts.append(
            f"Bitcoin trades at {fmt(btc)}{move} — the anchor of the digital-asset cycle "
            "and a high-beta read on global liquidity and institutional adoption.")
    if eth is not None and eth.price is not None:
        parts.append(
            f"Ethereum at {fmt(eth)} tracks on-chain activity and the app/L2 economy, the "
            "second read on whether risk appetite is broadening beyond Bitcoin.")
    if m2 is not None:
        parts.append(
            "The cycle ultimately rides the liquidity tide: crypto has historically "
            "advanced when broad money (M2) is expanding and struggled when it contracts.")
    if rr is not None:
        parts.append(
            f"With the real 10-year yield near {rr:.2f}%, the opportunity cost of holding a "
            "non-yielding asset is "
            f"{'real — a headwind that keeps crypto a satellite' if rr >= 1 else 'modest — a less punishing backdrop'} "
            "until policy eases.")
    parts.append(
        "This edition reads the majors, the liquidity and adoption backdrop, and how the "
        "desk frames position sizing — interpretation from public data, not advice.")
    intro = " ".join(parts)

    groups: list[Group] = [_crypto_majors_group(m), _crypto_liquidity_group(m)]
    if full:
        groups.append(_crypto_lens_group(m))

    return Edition(
        slug="crypto-intelligence", title="Crypto Intelligence", eyebrow="Crypto Intelligence",
        dateline=dateline, intro=intro, groups=groups,
        footer="Built from public data — CoinGecko spot prices (Bitcoin, Ethereum, and the "
               "large-cap alts) and the Federal Reserve's M2 money-supply series (FRED). "
               "Figures are derived and shown as last released; no exchange order-book or "
               "fund-flow data is scraped or redistributed.",
        disclaimer=_CRYPTO_DISCLAIMER, methodology=_methodology_for("crypto-intelligence"),
        teaser=not full, charts=_crypto_chart(m) if full else [],
        cadence=cadence_for("crypto-intelligence"))


# ── Dividend Opportunities ───────────────────────────────────────────────────
# A monthly income read: dividend growth + balance-sheet quality + income ideas,
# DERIVED from point-in-time fundamentals (SF1 primary · EDGAR fallback) and public
# SEC EDGAR cash-flow filings, combined with live price. Only derived metrics are
# surfaced (yields, payout, coverage, margins, ROE) — never raw licensed rows.
def _dividend_income_group(full: bool) -> tuple["Group | None", list["Chart"]]:
    """The screened income ideas — dividend yield, payout, coverage, and quality.

    Lazy import (heavy: EDGAR + prices) and resilient — returns (None, []) on any
    failure so the edition still ships (Always-Deliver)."""
    try:
        from app.dividend_opportunities import top_dividend_ideas
        ideas = top_dividend_ideas(n=6)
    except Exception:  # noqa: BLE001 - never break newsletter generation
        return None, []
    if not ideas:
        return None, []

    items: list[Item] = []
    for idea in ideas:
        items.append(Item(
            label=idea.ticker, value=idea.value_str, body=idea.insight,
            tags=["Dividends", idea.quality_tag],
            source=f"Derived income/quality · {idea.name} · {idea.source_disclosure}"))

    charts: list[Chart] = []
    if full:
        try:
            from app import newsletter_charts as nc
            names = [i.ticker for i in ideas]
            yields = [i.dividend_yield * 100 for i in ideas if i.dividend_yield is not None]
            if len(yields) == len(names) and names:
                charts.append(Chart(
                    label="Dividend yield by idea",
                    image=nc.horizontal_bars("Dividend yield by income idea (%)", names,
                                             [i.dividend_yield * 100 for i in ideas],
                                             value_suffix="%", xlabel="Trailing dividend yield (%)"),
                    caption="Derived trailing dividend yield (dividends paid ÷ shares ÷ price) "
                            "for the screened income ideas. Derived metrics only.",
                    source="Derived from SEC EDGAR dividends + live price."))
            scores = [float(i.score) for i in ideas]
            charts.append(Chart(
                label="Income-quality score",
                image=nc.ranked_scores("Income ideas — dividend-quality score", names, scores),
                caption="Cross-sectional 0–100 dividend-quality score blending yield, payout "
                        "coverage, and balance-sheet quality. Derived scores only.",
                source="Derived: Aegira dividend-quality screen (fundamentals + price)."))
        except Exception:  # noqa: BLE001 - charts are optional
            charts = []

    group = Group(
        heading="Income ideas — dividend growth & quality",
        blurb="A derived screen of dividend payers ranked by a blend of yield, payout "
              "coverage, and balance-sheet quality — dividends that are covered by cash "
              "flow and backed by durable margins. Research, not investment advice.",
        items=items, charts=charts)
    return group, charts


def _dividend_context_group(m: QuoteMap) -> Group:
    """Why income now — the macro case for dividends against the rate backdrop."""
    items: list[Item] = []
    ten = m.get("UST10Y")
    if ten is not None and ten.price is not None:
        items.append(Item(
            label="The bond alternative", value=f"10Y {fmt(ten)}",
            body="Income investing competes with the risk-free rate. A high 10-year sets a "
                 "high bar: an equity income idea must offer growth and coverage the bond "
                 "cannot, not just a comparable headline yield.",
            source=ten.note, as_of_label=_as_of(ten)))
    rr = _real_rate(m)
    if rr is not None:
        items.append(Item(
            label="Real rates & payout discipline", value=f"{rr:.2f}% (10Y − CPI)",
            body="Positive real rates reward realized cash flow over promised growth — "
                 "precisely the regime that favors covered, growing dividends from "
                 "quality balance sheets over high-yield 'value traps.'",
            source="Derived: 10-year Treasury − headline CPI (FRED)."))
    items.append(Item(
        label="What we screen for", value="covered growth, not headline yield",
        body="The trap in income investing is a high yield that is not covered by cash flow. "
             "The screen prioritizes payout coverage (cash flow vs. the dividend), "
             "balance-sheet quality (ROE, margins), and dividend-supporting growth over the "
             "highest nominal yield."))
    return Group(
        heading="Why income now — the rate backdrop",
        blurb="The macro case for a disciplined income sleeve in a positive-real-rate world.",
        items=items)


def _dividend_lens_group() -> Group:
    return Group(
        heading="The Aegira lens",
        blurb="How the desk frames a durable income sleeve — interpretation, not advice.",
        items=[
            Item(label="Coverage before yield", value="cash flow first",
                 body="Underwrite the payout: a dividend covered by free cash flow with room "
                      "to grow beats a higher yield that is one bad quarter from a cut."),
            Item(label="Quality compounders", value="ROE + margins",
                 body="Durable operating margins and high returns on equity are what let a "
                      "company raise the dividend through a cycle — the difference between "
                      "income and a melting ice cube."),
            Item(label="Diversify the sleeve", value="across sectors",
                 body="Spread income ideas across sectors so a single-industry shock (energy, "
                      "banks, staples) does not take the whole payout with it."),
        ])


def _dividend_opportunities(m: QuoteMap, now: datetime, full: bool) -> Edition:
    dateline = f"Edition of {edition_date(now)}"
    ten = _price(m, "UST10Y")
    rr = _real_rate(m)
    parts = [
        "For the income investor, the job is not to chase the highest headline yield — it is "
        "to own dividends that are covered by cash flow, backed by durable margins, and able "
        "to grow through a cycle."
    ]
    if ten is not None:
        parts.append(
            f"With the 10-year Treasury near {ten:.2f}%, an equity income idea has to clear a "
            "higher bar than it did in the zero-rate era: it must offer coverage and growth the "
            "risk-free rate cannot.")
    if rr is not None:
        parts.append(
            f"A real 10-year yield around {rr:.2f}% rewards realized cash flow over promised "
            "growth — the regime that favors quality, covered, growing dividends.")
    parts.append(
        "This edition screens dividend payers on a derived blend of yield, payout coverage, "
        "and balance-sheet quality, then frames the macro case — all from public data, all "
        "derived, none of it advice.")
    intro = " ".join(parts)

    groups: list[Group] = []
    income_group, _ = _dividend_income_group(full)
    if income_group is not None:
        groups.append(income_group)
    groups.append(_dividend_context_group(m))
    if full:
        groups.append(_dividend_lens_group())

    return Edition(
        slug="dividend-opportunities", title="Dividend Opportunities",
        eyebrow="Dividend Opportunities",
        dateline=dateline, intro=intro, groups=groups,
        footer="Built from public data — point-in-time fundamentals (Sharadar SF1 primary · "
               "SEC EDGAR fallback), public SEC EDGAR cash-flow filings for dividends, and live "
               "market price. Yields, payout, coverage, margins, and ROE are DERIVED and shown "
               "as last released; no raw licensed rows are surfaced or redistributed.",
        disclaimer=_DISCLAIMER, methodology=_methodology_for("dividend-opportunities"),
        teaser=not full, charts=[], cadence=cadence_for("dividend-opportunities"))


def generate_scheduled_editions(
    cadence: str,
    now: datetime | None = None,
    quotes: list[Quote] | None = None,
    full: bool = True,
) -> list[Edition]:
    """Scheduled-generation hook: build every edition on a given cadence.

    Callable from a scheduler/cron (weekly-pulse vs. monthly-deep-dive). ``quotes`` may be
    injected to keep callers/tests network-free; otherwise the live market feed is polled.
    Resilient: a single edition failure never aborts the batch.
    """
    now = now or datetime.now(timezone.utc)
    slugs = editions_for_cadence(cadence)
    if quotes is None:
        from app.market_services import MarketDataService  # lazy: avoid import at module load
        quotes = MarketDataService().quotes(NEWSLETTER_SYMBOLS).quotes
    editions: list[Edition] = []
    for slug in slugs:
        try:
            editions.append(build_edition(slug, quotes, now, full=full))
        except Exception:  # noqa: BLE001 - never let one edition abort the scheduled batch
            continue
    return editions


def build_edition(slug: str, quotes: list[Quote], now: datetime, full: bool) -> Edition:
    """Build a normalized Edition for the given slug. Raises KeyError for unknown slug."""
    if slug not in EDITION_SLUGS:
        raise KeyError(slug)
    m: QuoteMap = {q.symbol: q for q in quotes}
    dateline = f"Edition of {edition_date(now)}"

    if slug == "main-street-acquirer":
        return _main_street_acquirer(m, now, full)

    if slug == "insider-briefs":
        return _insider_brief(m, now, full)

    if slug == "crypto-intelligence":
        return _crypto_intelligence(m, now, full)

    if slug == "dividend-opportunities":
        return _dividend_opportunities(m, now, full)

    if slug == "economic-brief":
        intro, groups = _economic_brief(m, full)
        return Edition(
            slug=slug, title="The Economic Brief", eyebrow="Economic Tracking",
            dateline=dateline, intro=intro, groups=groups,
            footer="Sourced from public data — Federal Reserve (FRED), U.S. Bureau of Labor "
                   "Statistics, and market feeds. Figures are as last released.",
            disclaimer=_DISCLAIMER, methodology=METHODOLOGY, teaser=not full,
            charts=_macro_chart(m) if full else [],
            cadence=cadence_for(slug),
            editor_letter=_economic_editor_letter(m))

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
            disclaimer=_DISCLAIMER, methodology=METHODOLOGY, teaser=not full,
            cadence=cadence_for(slug))

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
        footer="Ideas are generated from Sharadar SF1 (Nasdaq Data Link) — point-in-time "
               "fundamentals (primary) · SEC EDGAR (fallback) · FRED · BLS · market feeds. "
               "Combined with Aegira's validated factor research; equity fundamentals are "
               "surfaced as derived metrics only (raw licensed rows stay internal). "
               "Written in Aegira's independent professional perspective.",
        disclaimer=_DISCLAIMER, methodology=_methodology_for(slug), teaser=not full,
        cadence=cadence_for(slug))


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
        # Per-ticker provenance reflects the ACTUAL source used for THAT name
        # (Sharadar SF1 primary vs SEC EDGAR fallback), read from the fundamentals
        # provider. NOTE: the raw-line-item EDGAR Fundamentals export and the Deal
        # X-Ray public-comp benchmark intentionally stay on public-domain SEC EDGAR
        # (Nasdaq license) — only this DERIVED scan uses the SF1-primary source.
        items.append(Item(
            label=p.ticker,
            value=p.value_str,
            body=body,
            tags=["Equities", p.top_factor],
            source=f"Derived score/factors · {p.name} · {p.source_disclosure}",
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
