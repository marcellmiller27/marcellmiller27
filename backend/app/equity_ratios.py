# JHI-SIG: 69M2705M | Deterministic fundamental-ratio breakdown | JHI Research & Analytics Firm, Inc. (proprietary)
"""Derive a full, labeled fundamental-ratio breakdown from normalized point-in-time
fundamentals (Sharadar SF1 primary, SEC EDGAR fallback).

Every ratio is a DERIVED output computed from the normalized inputs the provider
exposes — raw licensed SF1 rows are never surfaced (governance). Each metric degrades
gracefully to ``None`` when an input is missing (Data Foundation doctrine: no
fabricated numbers), and the whole bundle is tagged with source + fiscal period +
as-of for provenance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app import fundamentals as fnd
from app.fundamentals import EquityFundamentals

# Number-format hints consumed by the workbook renderer.
FMT_PCT = "pct"
FMT_RATIO = "ratio"
FMT_USD = "usd"
FMT_MULT = "mult"
FMT_EPS = "eps"


@dataclass
class RatioMetric:
    label: str
    value: float | None
    fmt: str
    note: str = ""


@dataclass
class RatioSection:
    title: str
    metrics: list[RatioMetric] = field(default_factory=list)


@dataclass
class TrendRow:
    fiscal_year: int
    revenue: float | None = None
    revenue_yoy: float | None = None
    net_income: float | None = None
    eps: float | None = None
    gross_margin: float | None = None
    operating_margin: float | None = None
    net_margin: float | None = None


@dataclass
class FundamentalRatios:
    ticker: str
    name: str
    source_label: str
    fiscal_period: str
    as_of: datetime
    sections: list[RatioSection] = field(default_factory=list)
    trend: list[TrendRow] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def _ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator is None or denominator == 0:
        return None
    return numerator / denominator


def _revenue_yoy(fin: EquityFundamentals) -> float | None:
    rows = sorted(
        [y for y in fin.years if y.revenue and y.revenue > 0], key=lambda y: y.fiscal_year
    )
    if len(rows) < 2:
        return None
    prev, last = rows[-2].revenue, rows[-1].revenue
    return (last / prev - 1.0) if prev else None


def _revenue_cagr(fin: EquityFundamentals) -> float | None:
    rows = sorted(
        [y for y in fin.years if y.revenue and y.revenue > 0], key=lambda y: y.fiscal_year
    )
    if len(rows) < 2:
        return None
    span = rows[-1].fiscal_year - rows[0].fiscal_year
    if span <= 0 or not rows[0].revenue:
        return None
    try:
        return (rows[-1].revenue / rows[0].revenue) ** (1.0 / span) - 1.0
    except (ZeroDivisionError, ValueError):
        return None


def compute_ratios(fin: EquityFundamentals, price: float | None = None) -> FundamentalRatios:
    """Compute the full ratio breakdown from a normalized fundamentals bundle."""
    rev = fin.revenue
    ni = fin.net_income
    equity = fin.stockholders_equity
    shares = fin.shares_outstanding

    # ── Profitability & margins ──────────────────────────────────────────────
    gross_margin = fin.gross_margin if fin.gross_margin is not None else _ratio(fin.gross_profit, rev)
    op_margin = fin.operating_margin if fin.operating_margin is not None else _ratio(
        fin.operating_income, rev
    )
    net_margin = fin.net_margin if fin.net_margin is not None else _ratio(ni, rev)
    ebitda_margin = _ratio(fin.ebitda, rev)
    fcf = fin.free_cash_flow
    fcf_margin = _ratio(fcf, rev)
    roe = fin.roe if fin.roe is not None else _ratio(ni, equity)
    roa = _ratio(ni, fin.total_assets)
    roic = fin.roic

    # ── Per-share / earnings ─────────────────────────────────────────────────
    eps = fin.eps if fin.eps is not None else (_ratio(ni, shares))
    eps_basic = fin.eps_basic if fin.eps_basic is not None else (_ratio(ni, shares))
    fcf_per_share = _ratio(fcf, shares)

    # ── Leverage & solvency ──────────────────────────────────────────────────
    debt = fin.total_debt
    if debt is None and fin.total_liabilities is not None:
        debt = fin.total_liabilities  # conservative D/E proxy when only total liabilities known
    debt_to_equity = _ratio(debt, equity)
    debt_note = (
        "Total debt / equity" if fin.total_debt is not None else "Total liabilities / equity (proxy)"
    )
    interest_coverage = _ratio(
        fin.ebit if fin.ebit is not None else fin.operating_income,
        abs(fin.interest_expense) if fin.interest_expense else None,
    )

    # ── Liquidity ────────────────────────────────────────────────────────────
    current_ratio = _ratio(fin.current_assets, fin.current_liabilities)
    quick_ratio = _ratio(
        (fin.current_assets - fin.inventory)
        if (fin.current_assets is not None and fin.inventory is not None)
        else fin.current_assets,
        fin.current_liabilities,
    )
    cash_ratio = _ratio(fin.cash_and_equivalents, fin.current_liabilities)

    # ── Valuation multiples (need a live price) ──────────────────────────────
    pe = _ratio(price, eps) if (price is not None and eps and eps > 0) else None
    market_cap = (price * shares) if (price is not None and shares) else None
    ps = _ratio(market_cap, rev)
    pb = _ratio(market_cap, equity)

    # ── Shareholder returns ──────────────────────────────────────────────────
    dps = fin.dividends_per_share
    dividend_yield = _ratio(dps, price) if (price is not None and dps) else None
    payout_ratio = _ratio(dps, eps) if (dps and eps and eps > 0) else None

    src = fnd.source_label(fin.source)
    period = fin.period_end or (str(fin.fiscal_year) if fin.fiscal_year else "latest")

    sections = [
        RatioSection(
            "Profitability & returns",
            [
                RatioMetric("Gross margin", gross_margin, FMT_PCT, "Gross profit / revenue"),
                RatioMetric("Operating margin", op_margin, FMT_PCT, "Operating income / revenue"),
                RatioMetric("Net margin", net_margin, FMT_PCT, "Net income / revenue"),
                RatioMetric("EBITDA margin", ebitda_margin, FMT_PCT, "EBITDA / revenue"),
                RatioMetric("Return on equity (ROE)", roe, FMT_PCT, "Net income / equity"),
                RatioMetric("Return on assets (ROA)", roa, FMT_PCT, "Net income / total assets"),
                RatioMetric("Return on invested capital (ROIC)", roic, FMT_PCT, "Source metric"),
            ],
        ),
        RatioSection(
            "Growth & cash generation",
            [
                RatioMetric("Revenue (latest)", rev, FMT_USD, f"Fiscal {period}"),
                RatioMetric("Revenue growth (YoY)", _revenue_yoy(fin), FMT_PCT, "Latest vs. prior year"),
                RatioMetric("Revenue CAGR (period)", _revenue_cagr(fin), FMT_PCT, "Across available years"),
                RatioMetric("Free cash flow (FCF)", fcf, FMT_USD, "Cash-flow-statement based"),
                RatioMetric("FCF margin", fcf_margin, FMT_PCT, "FCF / revenue"),
                RatioMetric("FCF per share", fcf_per_share, FMT_USD, "FCF / shares outstanding"),
            ],
        ),
        RatioSection(
            "Per-share earnings",
            [
                RatioMetric("EPS (diluted)", eps, FMT_EPS, "Diluted earnings per share"),
                RatioMetric("EPS (basic)", eps_basic, FMT_EPS, "Basic earnings per share"),
                RatioMetric("Net income", ni, FMT_USD, f"Fiscal {period}"),
                RatioMetric("Shares outstanding", shares, FMT_USD, "Period-end basic shares"),
            ],
        ),
        RatioSection(
            "Leverage & solvency",
            [
                RatioMetric("Debt-to-equity", debt_to_equity, FMT_RATIO, debt_note),
                RatioMetric("Interest coverage", interest_coverage, FMT_MULT, "EBIT / interest expense"),
                RatioMetric("Total debt", debt, FMT_USD, debt_note),
                RatioMetric("Stockholders' equity", equity, FMT_USD, f"Fiscal {period}"),
            ],
        ),
        RatioSection(
            "Liquidity",
            [
                RatioMetric("Current ratio", current_ratio, FMT_RATIO, "Current assets / current liabilities"),
                RatioMetric("Quick ratio", quick_ratio, FMT_RATIO, "(Current assets − inventory) / current liabilities"),
                RatioMetric("Cash ratio", cash_ratio, FMT_RATIO, "Cash & equivalents / current liabilities"),
            ],
        ),
        RatioSection(
            "Valuation multiples",
            [
                RatioMetric("Price / earnings (P/E)", pe, FMT_MULT, "Price / diluted EPS"),
                RatioMetric("Price / sales (P/S)", ps, FMT_MULT, "Market cap / revenue"),
                RatioMetric("Price / book (P/B)", pb, FMT_MULT, "Market cap / equity"),
                RatioMetric("Market capitalization", market_cap, FMT_USD, "Price × shares"),
            ],
        ),
        RatioSection(
            "Shareholder returns",
            [
                RatioMetric("Dividend per share", dps, FMT_EPS, "Declared DPS"),
                RatioMetric("Dividend yield", dividend_yield, FMT_PCT, "DPS / price"),
                RatioMetric("Payout ratio", payout_ratio, FMT_PCT, "DPS / EPS"),
            ],
        ),
    ]

    # ── Multi-period trend (where available) ─────────────────────────────────
    year_rows = sorted([y for y in fin.years if y.fiscal_year], key=lambda y: y.fiscal_year)
    trend: list[TrendRow] = []
    prev_rev: float | None = None
    for y in year_rows:
        yoy = (y.revenue / prev_rev - 1.0) if (prev_rev and y.revenue) else None
        trend.append(
            TrendRow(
                fiscal_year=y.fiscal_year,
                revenue=y.revenue,
                revenue_yoy=yoy,
                net_income=y.net_income,
                eps=y.eps,
                gross_margin=y.gross_margin,
                operating_margin=y.operating_margin,
                net_margin=y.net_margin,
            )
        )
        if y.revenue:
            prev_rev = y.revenue

    notes = [
        f"Source: {src}. Fiscal period {period}. All ratios are derived outputs; missing "
        "inputs are shown as n/a (no fabricated values).",
        "Research and educational output — not investment advice, not an audit or CPA opinion.",
    ]
    return FundamentalRatios(
        ticker=fin.ticker,
        name=fin.entity_name,
        source_label=src,
        fiscal_period=str(period),
        as_of=datetime.now(UTC),
        sections=sections,
        trend=trend,
        notes=notes,
    )
