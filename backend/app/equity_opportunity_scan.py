# JHI-SIG: 69M2705M | Equity Opportunity Scan (discovery-driven) | JHI Research & Analytics Firm, Inc. (proprietary)
"""Discovery-driven equity Opportunity Scan for the newsletter.

Formula: **data finds, Ellery writes.** A deterministic value/quality/growth screen
over a large/mid-cap US universe — grounded in FREE, redistributable **SEC EDGAR**
fundamentals + live market price — ranks names by a cross-sectional Opportunity Score
(0-100). The top 5 are surfaced as newsletter items; the editorial layer (E2) elevates
the *prose* only, fact-locked (every number originates here). Not investment advice.

Value/quality/growth factors (thesis-tilted to cash-flow, durable margins, and
disciplined multiples):
  - Quality (0.40): operating margin, net margin, ROE
  - Growth  (0.30): multi-year revenue CAGR
  - Value   (0.30): earnings yield (E/P), book yield (B/P)  [needs market cap]
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from app import edgar_services
from app.market_services import MarketDataService
from app.opportunity_score import _zscore

# Large/mid-cap US equities across sectors (Phase 1 universe; expand later).
LARGE_MID_CAP_UNIVERSE: list[str] = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "AVGO", "ORCL", "ADBE", "CRM",
    "JPM", "BAC", "V", "MA", "GS", "AXP",
    "UNH", "JNJ", "LLY", "ABBV", "MRK", "PFE",
    "HD", "LOW", "COST", "WMT", "TGT", "NKE", "SBUX", "MCD",
    "CAT", "DE", "HON", "UPS", "GE",
    "XOM", "CVX", "COP",
    "PG", "KO", "PEP",
]

FACTOR_WEIGHTS = {
    "operating_margin": 0.15,
    "net_margin": 0.10,
    "roe": 0.15,           # quality subtotal 0.40
    "revenue_cagr": 0.30,  # growth
    "earnings_yield": 0.20,
    "book_yield": 0.10,    # value subtotal 0.30
}

_SCAN_TTL_SECONDS = 6 * 3600  # heavy (EDGAR + prices); cache the ranked result
_scan_cache: dict[str, tuple[float, list["EquityOpportunity"]]] = {}


@dataclass
class EquityOpportunity:
    ticker: str
    name: str
    score: float
    operating_margin: float
    net_margin: float
    roe: float
    revenue_cagr: float
    earnings_yield: float
    price: float
    market_cap: float

    @property
    def value_str(self) -> str:
        return (
            f"Score {self.score:.0f} · Op margin {self.operating_margin * 100:.1f}% · "
            f"Rev growth {self.revenue_cagr * 100:.1f}% · Earnings yield {self.earnings_yield * 100:.1f}%"
        )

    @property
    def insight(self) -> str:
        return (
            f"{self.name} pairs durable operating margins near {self.operating_margin * 100:.1f}% "
            f"with {self.revenue_cagr * 100:.1f}% revenue growth, offered at a "
            f"{self.earnings_yield * 100:.1f}% earnings yield — quality at a disciplined multiple. "
            "Research, not advice."
        )


def _revenue_cagr(hist) -> float | None:
    rows = [r for r in getattr(hist, "years", []) if r.revenue and r.revenue > 0]
    if len(rows) < 2:
        return None
    rows.sort(key=lambda r: r.fiscal_year)
    first, last = rows[0], rows[-1]
    span = last.fiscal_year - first.fiscal_year
    if span <= 0:
        return None
    try:
        return (last.revenue / first.revenue) ** (1.0 / span) - 1.0
    except (ZeroDivisionError, ValueError):
        return None


def _raw_factors(ticker: str, price: float | None) -> dict[str, float] | None:
    """Full value/quality/growth factor vector for one name, or None if incomplete."""
    try:
        fin = edgar_services.normalize(ticker)
        hist = edgar_services.history(ticker, max_years=5)
        shares = edgar_services.latest_shares_outstanding(ticker)
    except edgar_services.ProviderError:
        return None

    op = fin.operating_margin
    nm = fin.net_margin
    ni = fin.net_income
    eq = fin.stockholders_equity
    cagr = _revenue_cagr(hist)
    if None in (op, nm, ni, eq, cagr, price, shares) or not eq or eq <= 0 or not price:
        return None

    market_cap = price * shares
    if market_cap <= 0:
        return None

    return {
        "operating_margin": op,
        "net_margin": nm,
        "roe": ni / eq,
        "revenue_cagr": cagr,
        "earnings_yield": ni / market_cap,
        "book_yield": eq / market_cap,
        "_price": price,
        "_market_cap": market_cap,
        "_name": fin.entity_name,
    }


def _rank(rows: dict[str, dict[str, float]], n: int) -> list[EquityOpportunity]:
    tickers = list(rows.keys())
    composite = {t: 0.0 for t in tickers}
    for factor, weight in FACTOR_WEIGHTS.items():
        zs = _zscore([rows[t][factor] for t in tickers])
        for t, z in zip(tickers, zs):
            composite[t] += weight * z

    ordered = sorted(composite.items(), key=lambda kv: kv[1])
    denom = max(len(ordered) - 1, 1)
    score = {t: round(rank / denom * 100.0, 1) for rank, (t, _v) in enumerate(ordered)}

    top = sorted(tickers, key=lambda t: score[t], reverse=True)[:n]
    out: list[EquityOpportunity] = []
    for t in top:
        r = rows[t]
        out.append(EquityOpportunity(
            ticker=t, name=str(r["_name"]), score=score[t],
            operating_margin=r["operating_margin"], net_margin=r["net_margin"],
            roe=r["roe"], revenue_cagr=r["revenue_cagr"], earnings_yield=r["earnings_yield"],
            price=r["_price"], market_cap=r["_market_cap"],
        ))
    return out


def top_opportunities(n: int = 5, universe: list[str] | None = None, force: bool = False) -> list[EquityOpportunity]:
    """Ranked top-N equity opportunities from the screen (cached ~6h). Resilient:
    returns [] on data failure so the newsletter degrades gracefully."""
    uni = universe or LARGE_MID_CAP_UNIVERSE
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

        rows: dict[str, dict[str, float]] = {}
        for t in uni:
            factors = _raw_factors(t, prices.get(t.upper()))
            if factors is not None:
                rows[t] = factors

        result = _rank(rows, n) if len(rows) >= 5 else []
    except Exception:  # noqa: BLE001 - never break newsletter generation
        result = []

    _scan_cache[key] = (now + _SCAN_TTL_SECONDS, result)
    return result


def reset_cache() -> None:
    _scan_cache.clear()
