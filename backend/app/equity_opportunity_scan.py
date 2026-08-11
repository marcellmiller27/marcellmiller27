# JHI-SIG: 69M2705M | Equity Opportunity Scan (discovery-driven) | JHI Research & Analytics Firm, Inc. (proprietary)
"""Discovery-driven equity Opportunity Scan for the newsletter.

Formula: **data finds, Ellery writes.** A deterministic value/quality/growth screen
over a large/mid-cap US universe — grounded in point-in-time fundamentals (Sharadar
SF1 primary, SEC EDGAR fallback) + live market price — ranks names by a cross-sectional
Opportunity Score (0-100). Raw SF1 rows stay internal; only the DERIVED score/factors
are surfaced (governance). The top 5 are surfaced as newsletter items; the editorial
layer (E2) elevates the *prose* only, fact-locked (every number originates here). Not
investment advice.

Value/quality/growth factors (thesis-tilted to cash-flow, durable margins, and
disciplined multiples):
  - Quality (0.40): operating margin, net margin, ROE
  - Growth  (0.30): multi-year revenue CAGR
  - Value   (0.30): earnings yield (E/P), book yield (B/P)  [needs market cap]
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

from app import edgar_services, fundamentals
from app.market_services import MarketDataService
from app.opportunity_score import _zscore

logger = logging.getLogger(__name__)

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

# Per-factor weights. Grouped into the four validated factor families
# (Value / Quality / Growth + a 12-1 price Momentum sleeve) so each pick can be
# decomposed for the reader. Weights sum to 1.0.
FACTOR_WEIGHTS = {
    "operating_margin": 0.13,
    "net_margin": 0.09,
    "roe": 0.13,           # Quality subtotal 0.35
    "revenue_cagr": 0.20,  # Growth
    "earnings_yield": 0.17,
    "book_yield": 0.08,    # Value subtotal 0.25
    "momentum_12_1": 0.20,  # Momentum (12-1 price momentum, skip last month)
}

# Map each raw factor to its family for the per-name decomposition surfaced to readers.
FACTOR_FAMILY = {
    "operating_margin": "Quality",
    "net_margin": "Quality",
    "roe": "Quality",
    "revenue_cagr": "Growth",
    "earnings_yield": "Value",
    "book_yield": "Value",
    "momentum_12_1": "Momentum",
}
FACTOR_FAMILIES = ("Value", "Quality", "Growth", "Momentum")


def ticker_source_disclosure(source: str | None) -> str:
    """Human-readable per-ticker provenance for the newsletter disclosure.

    Names the ACTUAL source used for a ticker (Sharadar SF1 primary vs SEC EDGAR
    fallback); for a ticker with no fundamentals it names the ATTEMPTED source(s)
    plus "no data available". Safe to surface — it discloses the SOURCE only, never
    raw licensed rows (governance).

    NOTE: This SF1-primary provenance is for the DERIVED opportunity scan only. The
    raw-line-item EDGAR Fundamentals export and the Deal X-Ray public-comp benchmark
    intentionally stay on public-domain SEC EDGAR (Nasdaq license) and never use SF1.
    """
    if source == fundamentals.SOURCE_SF1:
        return "Sharadar SF1 (Nasdaq Data Link) — point-in-time fundamentals (primary); derived metrics only"
    if source == fundamentals.SOURCE_EDGAR:
        return "SEC EDGAR (fallback) — public-domain fundamentals; derived metrics only"
    attempted = ("Sharadar SF1 → SEC EDGAR" if fundamentals.nasdaq_data_link_api_key()
                 else "SEC EDGAR")
    return f"{attempted} — no data available"

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
    # Provider key for the source ACTUALLY used for THIS ticker's fundamentals
    # (``fundamentals.SOURCE_SF1`` / ``SOURCE_EDGAR``). Drives the per-ticker
    # provenance disclosure surfaced in the newsletter (SF1 primary vs EDGAR fallback).
    source: str = ""
    # Signed weighted-z contribution of each factor family to the composite
    # (Value / Quality / Growth / Momentum). Derived output only.
    contributions: dict[str, float] = field(default_factory=dict)
    momentum_12_1: float | None = None

    @property
    def source_disclosure(self) -> str:
        """Honest per-ticker provenance for THIS name (safe to surface — names the
        SOURCE, never raw licensed rows). Reflects the ACTUAL source used; for a
        ticker whose fundamentals could not be sourced it returns the attempted
        source + 'no data available'."""
        return ticker_source_disclosure(self.source)

    @property
    def value_str(self) -> str:
        return (
            f"Score {self.score:.0f} · Op margin {self.operating_margin * 100:.1f}% · "
            f"Rev growth {self.revenue_cagr * 100:.1f}% · Earnings yield {self.earnings_yield * 100:.1f}%"
        )

    @property
    def top_factor(self) -> str:
        """The factor family that contributes most to this name's ranking."""
        if not self.contributions:
            return "Quality"
        return max(self.contributions.items(), key=lambda kv: kv[1])[0]

    @property
    def decomposition_str(self) -> str:
        """A compact, fact-locked read of the factor contributions (derived numbers)."""
        if not self.contributions:
            return ""
        parts = [f"{fam} {self.contributions[fam]:+.2f}" for fam in FACTOR_FAMILIES
                 if fam in self.contributions]
        return "Factor contribution — " + " · ".join(parts)

    @property
    def insight(self) -> str:
        lead = self.top_factor.lower()
        mom = ""
        if self.momentum_12_1 is not None:
            mom = f" 12-1 price momentum of {self.momentum_12_1 * 100:.1f}% adds a trend tailwind."
        return (
            f"{self.name} scores {self.score:.0f}/100, led by its {lead} factor: durable "
            f"operating margins near {self.operating_margin * 100:.1f}% and "
            f"{self.revenue_cagr * 100:.1f}% revenue growth, offered at a "
            f"{self.earnings_yield * 100:.1f}% earnings yield — quality at a disciplined "
            f"multiple.{mom} Research, not advice."
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
    """Full value/quality/growth factor vector for one name, or None if incomplete.

    Only DERIVED factors (margins, ROE, CAGR, yields) leave this function and reach
    the score — raw Sharadar SF1 rows stay internal (governance)."""
    # Skip the (network) fundamentals fetch entirely when there is no live price:
    # the factor vector needs a market cap, so it would be discarded anyway.
    if not price:
        return None
    try:
        # Point-in-time fundamentals: Sharadar SF1 primary, SEC EDGAR fallback.
        fin = fundamentals.equity_fundamentals(ticker, max_years=5)
    except edgar_services.ProviderError:
        return None

    op = fin.operating_margin
    nm = fin.net_margin
    ni = fin.net_income
    eq = fin.stockholders_equity
    shares = fin.shares_outstanding
    cagr = _revenue_cagr(fin)
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
        # Actual source used for THIS ticker (SF1 vs EDGAR) — surfaced per-ticker.
        "_source": fin.source,
    }


def _momentum_by_ticker(tickers: list[str]) -> dict[str, float]:
    """Best-effort 12-1 monthly price momentum (skip the most recent month) per name.

    Cross-sectional trend sleeve for the blend. Network best-effort: any name whose
    history is missing is simply omitted (the caller neutralizes it), and a total
    failure degrades the blend to Value/Quality/Growth."""
    from app.market_services import yahoo_chart_history

    out: dict[str, float] = {}
    for t in tickers:
        try:
            hist = yahoo_chart_history(t, range_="2y", interval="1mo")
        except Exception:  # noqa: BLE001 - momentum is best-effort, never fatal
            continue
        closes = [c for _ts, c in hist if c and c > 0]
        if len(closes) < 13:
            continue
        try:
            out[t] = closes[-2] / closes[-13] - 1.0  # t-1 over t-12 (skip last month)
        except (ZeroDivisionError, ValueError):
            continue
    return out


def _rank(rows: dict[str, dict[str, float]], n: int,
          momentum: dict[str, float] | None = None) -> list[EquityOpportunity]:
    tickers = list(rows.keys())
    momentum = momentum or {}

    # Momentum sleeve is active only if at least a few names carry real history; else
    # its weight is redistributed proportionally across the fundamentals factors.
    mom_active = len(momentum) >= max(3, len(tickers) // 2)
    weights = dict(FACTOR_WEIGHTS)
    if mom_active:
        mom_mean = sum(momentum.values()) / len(momentum)
        for t in tickers:
            rows[t]["momentum_12_1"] = momentum.get(t, mom_mean)  # neutralize missing
    else:
        mom_w = weights.pop("momentum_12_1")
        scale = 1.0 / (1.0 - mom_w)
        weights = {k: v * scale for k, v in weights.items()}

    composite = {t: 0.0 for t in tickers}
    contrib: dict[str, dict[str, float]] = {
        t: {fam: 0.0 for fam in FACTOR_FAMILIES} for t in tickers
    }
    for factor, weight in weights.items():
        zs = _zscore([rows[t][factor] for t in tickers])
        family = FACTOR_FAMILY[factor]
        for t, z in zip(tickers, zs):
            composite[t] += weight * z
            contrib[t][family] += weight * z

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
            source=str(r.get("_source", "")),
            contributions={fam: round(contrib[t][fam], 4) for fam in FACTOR_FAMILIES},
            momentum_12_1=(round(momentum[t], 4) if t in momentum else None),
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

        if len(rows) >= 5:
            # Momentum only for the ranked candidate set (bounds the extra network).
            momentum = _momentum_by_ticker(list(rows.keys()))
            result = _rank(rows, n, momentum=momentum)
        else:
            result = []
    except Exception:  # noqa: BLE001 - never break newsletter generation
        result = []

    _scan_cache[key] = (now + _SCAN_TTL_SECONDS, result)
    return result


def reset_cache() -> None:
    _scan_cache.clear()
