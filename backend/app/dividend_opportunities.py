# JHI-SIG: 69M2705M | Dividend Opportunities screen (derived income + quality) | JHI Research & Analytics Firm, Inc. (proprietary)
"""Derived dividend-income screen for the Dividend Opportunities newsletter.

Formula: **data finds, Ellery writes.** A deterministic income + quality screen over
a curated universe of established dividend payers — grounded in point-in-time
fundamentals (Sharadar SF1 primary, SEC EDGAR fallback), public SEC EDGAR cash-flow
filings (dividends paid), and live market price. Names are ranked by a cross-sectional
0-100 dividend-quality score that blends yield, payout coverage, and balance-sheet
quality. Only DERIVED metrics are surfaced (yield, payout, coverage, margins, ROE) —
raw licensed SF1 rows stay internal (governance). Not investment advice.

Screen factors (thesis-tilted to *covered, growing* income over headline yield):
  - Income   : trailing dividend yield (DPS ÷ price)
  - Coverage : how well cash flow / earnings cover the dividend (payout headroom)
  - Quality  : ROE, net margin (durable, cycle-through payers)
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

from app import edgar_services, fundamentals
from app.equity_opportunity_scan import _revenue_cagr
from app.market_services import MarketDataService
from app.opportunity_score import _zscore

logger = logging.getLogger(__name__)

# Curated universe of established dividend payers across sectors (Phase 1; expand
# later). Chosen for broad, cycle-through dividend records — the screen still ranks
# them purely on the derived, point-in-time figures.
DIVIDEND_UNIVERSE: list[str] = [
    "JNJ", "PG", "KO", "PEP", "MCD", "WMT", "COST", "HD", "LOW",
    "ABBV", "MRK", "PFE", "AMGN",
    "JPM", "BAC", "AXP",
    "XOM", "CVX", "COP",
    "CAT", "HON", "MMM", "UPS",
    "TXN", "AVGO", "IBM", "CSCO", "VZ",
]

# Blend weights for the dividend-quality composite (sum to 1.0). Coverage and quality
# are weighted above raw yield on purpose — a covered, quality dividend beats a high
# but fragile one.
FACTOR_WEIGHTS = {
    "dividend_yield": 0.30,
    "coverage": 0.35,
    "roe": 0.20,
    "net_margin": 0.15,
}

_SCAN_TTL_SECONDS = 6 * 3600  # heavy (EDGAR + prices); cache the ranked result
_scan_cache: dict[str, tuple[float, list["DividendIdea"]]] = {}


@dataclass
class DividendIdea:
    ticker: str
    name: str
    score: float
    price: float
    dividend_yield: float | None            # trailing DPS / price
    payout_ratio: float | None              # dividends / net income
    coverage: float | None                  # cash flow (or earnings) / dividends
    coverage_basis: str                     # "free cash flow" or "earnings"
    roe: float
    net_margin: float
    revenue_cagr: float | None
    # Provider key for the source ACTUALLY used for THIS ticker's fundamentals
    # (``fundamentals.SOURCE_SF1`` / ``SOURCE_EDGAR``). Dividends themselves are always
    # from public-domain SEC EDGAR.
    source: str = ""
    contributions: dict[str, float] = field(default_factory=dict)

    @property
    def source_disclosure(self) -> str:
        """Honest per-ticker provenance (names the SOURCE only, never raw rows)."""
        base = fundamentals.source_label(self.source) if self.source else "point-in-time fundamentals"
        return f"{base} + SEC EDGAR dividends (public domain); derived metrics only"

    @property
    def quality_tag(self) -> str:
        """The leading dimension for this name's rank (for the reader's tag)."""
        if not self.contributions:
            return "Quality"
        family = max(self.contributions.items(), key=lambda kv: kv[1])[0]
        return {
            "dividend_yield": "Yield",
            "coverage": "Coverage",
            "roe": "Quality",
            "net_margin": "Quality",
        }.get(family, "Quality")

    @property
    def value_str(self) -> str:
        yld = f"{self.dividend_yield * 100:.1f}% yield" if self.dividend_yield is not None else "yield n/a"
        cov = f"{self.coverage:.1f}x cover" if self.coverage is not None else "cover n/a"
        return f"Score {self.score:.0f} · {yld} · {cov} · ROE {self.roe * 100:.0f}%"

    @property
    def insight(self) -> str:
        yld = (f"a trailing dividend yield near {self.dividend_yield * 100:.1f}%"
               if self.dividend_yield is not None else "an established dividend")
        cov = (f"covered {self.coverage:.1f}x by {self.coverage_basis}"
               if self.coverage is not None else "a payout backed by cash flow")
        growth = (f" Revenue has compounded near {self.revenue_cagr * 100:.1f}% a year, "
                  "supporting dividend growth." if self.revenue_cagr is not None else "")
        return (
            f"{self.name} scores {self.score:.0f}/100 on the income-quality blend: {yld}, "
            f"{cov}, on {self.net_margin * 100:.0f}% net margins and a {self.roe * 100:.0f}% "
            f"return on equity.{growth} Research, not advice."
        )


def _dividend_factors(ticker: str, price: float | None) -> dict[str, float] | None:
    """Derived income + quality factor vector for one name, or None if incomplete.

    Only DERIVED figures (yield, coverage, margins, ROE) leave this function — raw
    Sharadar SF1 rows stay internal (governance)."""
    if not price:
        return None
    try:
        fin = fundamentals.equity_fundamentals(ticker, max_years=5)
    except edgar_services.ProviderError:
        return None

    ni = fin.net_income
    eq = fin.stockholders_equity
    nm = fin.net_margin
    shares = fin.shares_outstanding
    if None in (ni, eq, nm, shares) or not eq or eq <= 0 or not shares or shares <= 0:
        return None

    # Dividends paid (public-domain SEC EDGAR cash-flow filing). A non-payer / missing
    # concept degrades gracefully: the name is dropped from the income screen.
    try:
        dividends_paid = edgar_services.latest_annual_dividends_paid(ticker)
    except edgar_services.ProviderError:
        dividends_paid = None
    if not dividends_paid or dividends_paid <= 0:
        return None

    dps = dividends_paid / shares
    dividend_yield = dps / price
    payout_ratio = dividends_paid / ni if ni and ni > 0 else None

    # Coverage: prefer free cash flow (SF1-rich) over earnings, both vs. the dividend.
    fcf = fin.free_cash_flow
    if fcf is not None and fcf > 0:
        coverage = fcf / dividends_paid
        coverage_basis = "free cash flow"
    elif ni and ni > 0:
        coverage = ni / dividends_paid
        coverage_basis = "earnings"
    else:
        coverage = None
        coverage_basis = "earnings"

    # A plausible-yield guard: filings-derived DPS occasionally misparses; cap the
    # yield we will trust at 20% (anything above is a data artifact, not an idea).
    if dividend_yield <= 0 or dividend_yield > 0.20:
        return None

    return {
        "dividend_yield": dividend_yield,
        "coverage": coverage if coverage is not None else 0.0,
        "roe": ni / eq,
        "net_margin": nm,
        "_payout_ratio": payout_ratio if payout_ratio is not None else -1.0,
        "_coverage_basis": coverage_basis,  # type: ignore[dict-item]
        "_has_coverage": 1.0 if coverage is not None else 0.0,
        "_revenue_cagr": _revenue_cagr(fin) if _revenue_cagr(fin) is not None else -99.0,
        "_price": price,
        "_name": fin.entity_name,  # type: ignore[dict-item]
        "_source": fin.source,  # type: ignore[dict-item]
    }


def _rank(rows: dict[str, dict], n: int) -> list[DividendIdea]:
    tickers = list(rows.keys())
    composite = {t: 0.0 for t in tickers}
    contrib: dict[str, dict[str, float]] = {t: {} for t in tickers}
    for factor, weight in FACTOR_WEIGHTS.items():
        zs = _zscore([rows[t][factor] for t in tickers])
        for t, z in zip(tickers, zs):
            composite[t] += weight * z
            contrib[t][factor] = weight * z

    ordered = sorted(composite.items(), key=lambda kv: kv[1])
    denom = max(len(ordered) - 1, 1)
    score = {t: round(rank / denom * 100.0, 1) for rank, (t, _v) in enumerate(ordered)}

    top = sorted(tickers, key=lambda t: score[t], reverse=True)[:n]
    out: list[DividendIdea] = []
    for t in top:
        r = rows[t]
        out.append(DividendIdea(
            ticker=t, name=str(r["_name"]), score=score[t], price=r["_price"],
            dividend_yield=r["dividend_yield"],
            payout_ratio=(r["_payout_ratio"] if r["_payout_ratio"] >= 0 else None),
            coverage=(r["coverage"] if r["_has_coverage"] else None),
            coverage_basis=str(r["_coverage_basis"]),
            roe=r["roe"], net_margin=r["net_margin"],
            revenue_cagr=(r["_revenue_cagr"] if r["_revenue_cagr"] > -90 else None),
            source=str(r.get("_source", "")),
            contributions={k: round(contrib[t][k], 4) for k in FACTOR_WEIGHTS},
        ))
    return out


def top_dividend_ideas(
    n: int = 6, universe: list[str] | None = None, force: bool = False
) -> list[DividendIdea]:
    """Ranked top-N dividend ideas from the screen (cached ~6h). Resilient: returns []
    on data failure so the newsletter degrades gracefully (Always-Deliver)."""
    uni = universe or DIVIDEND_UNIVERSE
    key = f"{n}:{','.join(uni)}"
    now = time.time()
    if not force:
        hit = _scan_cache.get(key)
        if hit and hit[0] > now:
            return hit[1]

    try:
        prices: dict[str, float] = {}
        try:
            resp = MarketDataService().quotes(uni)
            for q in resp.quotes:
                if getattr(q, "price", None) is not None and getattr(q, "status", "") == "ok":
                    prices[q.symbol.upper()] = float(q.price)
        except Exception:  # noqa: BLE001 - price feed best-effort
            prices = {}

        rows: dict[str, dict] = {}
        for t in uni:
            factors = _dividend_factors(t, prices.get(t.upper()))
            if factors is not None:
                rows[t] = factors

        result = _rank(rows, n) if len(rows) >= 3 else []
    except Exception:  # noqa: BLE001 - never break newsletter generation
        result = []

    _scan_cache[key] = (now + _SCAN_TTL_SECONDS, result)
    return result


def reset_cache() -> None:
    _scan_cache.clear()
