# JHI-SIG: 69M2705M | Cross-Asset Valuation & Action Engine — Phase 1 (equities) | JHI Research & Analytics Firm, Inc. (proprietary)
"""Equity DCF + expected-return (IRR) + enter/sideline action engine.

Phase 1 of the Cross-Asset Valuation & Action Engine covers **equities**. It grounds
a transparent, disclosed-assumption discounted-cash-flow on **all our data-sets**:
free SEC EDGAR fundamentals (earnings, equity, revenue history), the live market price,
and the risk-free rate from the market/FRED feed. It returns an intrinsic value, an
implied expected return (IRR), and a fact-locked **Enter / Accumulate / Sideline**
action write-up for allocators deciding whether to deploy or keep dry powder.

Every figure is deterministic and reproducible; assumptions are disclosed in-copy and
in the Excel workbook. Research, not investment advice. (Commodities, crypto, and FX
use method-specific engines in later phases.)
"""

from __future__ import annotations

import logging
import time
from datetime import UTC, datetime

from pydantic import BaseModel

from app import edgar_services
from app.market_services import MarketDataService

logger = logging.getLogger(__name__)

# ── Disclosed model assumptions (Phase 1) ────────────────────────────────────
PROJECTION_YEARS = 5
DEFAULT_EQUITY_RISK_PREMIUM = 0.05  # long-run US equity risk premium
DEFAULT_BETA = 1.0                  # market beta (Phase 1: single-beta; per-name beta later)
TERMINAL_GROWTH = 0.025             # ~ long-run nominal GDP
GROWTH_CAP = 0.12                   # cap projected growth for prudence
GROWTH_FLOOR = 0.0
DEFAULT_GROWTH = 0.04               # used when revenue history is insufficient
DEFAULT_RISK_FREE = 0.045           # fallback if the 10Y is unavailable
MIN_DISCOUNT_SPREAD = 0.005         # keep discount rate above terminal growth

# Action thresholds (Founder-approved defaults) on margin of safety (upside).
ENTER_UPSIDE = 0.20
SIDELINE_UPSIDE = -0.10

_UNIVERSE_TTL_SECONDS = 6 * 3600
_universe_cache: dict[str, tuple[float, list[EquityValuation]]] = {}


class EquityValuation(BaseModel):
    ticker: str
    name: str
    as_of: datetime
    # Inputs / market
    price: float
    shares_outstanding: float
    market_cap: float
    # DCF assumptions (disclosed)
    base_fcf: float
    fcf_basis: str
    growth_rate: float
    terminal_growth: float
    risk_free: float
    equity_risk_premium: float
    beta: float
    discount_rate: float
    projection_years: int
    # DCF outputs
    projected_fcf: list[float]
    present_values: list[float]
    terminal_value: float
    pv_terminal_value: float
    intrinsic_equity_value: float
    intrinsic_per_share: float
    upside_pct: float
    expected_return: float
    # Action
    signal: str
    rationale: str
    sources: list[str]
    disclaimer: str = (
        "For research and educational purposes only. Not investment advice. Intrinsic value "
        "is model output under disclosed assumptions, not a price target."
    )


def _fmt_pct(x: float) -> str:
    return f"{x * 100:.1f}%"


def _fmt_usd(x: float) -> str:
    if abs(x) >= 1e12:
        return f"${x / 1e12:.2f}T"
    if abs(x) >= 1e9:
        return f"${x / 1e9:.2f}B"
    if abs(x) >= 1e6:
        return f"${x / 1e6:.1f}M"
    return f"${x:,.2f}"


def risk_free_rate() -> float:
    """Risk-free = live 10-year Treasury yield (decimal). Falls back to a default."""
    try:
        resp = MarketDataService().quotes(["UST10Y"])
        for q in resp.quotes:
            if q.symbol.upper() == "UST10Y" and q.price is not None:
                return float(q.price) / 100.0
    except Exception:
        logger.debug("Falling back to default risk-free rate.", exc_info=True)
    return DEFAULT_RISK_FREE


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


def _intrinsic(base_fcf: float, g: float, g_t: float, r: float, years: int):
    """Return (intrinsic_equity, projected_fcf, present_values, terminal_value, pv_terminal)."""
    projected: list[float] = []
    pvs: list[float] = []
    total = 0.0
    for t in range(1, years + 1):
        fcf_t = base_fcf * (1.0 + g) ** t
        pv = fcf_t / (1.0 + r) ** t
        projected.append(fcf_t)
        pvs.append(pv)
        total += pv
    fcf_terminal = base_fcf * (1.0 + g) ** years
    terminal_value = fcf_terminal * (1.0 + g_t) / (r - g_t)
    pv_terminal = terminal_value / (1.0 + r) ** years
    return total + pv_terminal, projected, pvs, terminal_value, pv_terminal


def _expected_return(base_fcf: float, g: float, g_t: float, market_cap: float, years: int) -> float:
    """Solve for the discount rate r that sets DCF value == market cap (equity IRR under
    the projected cash flows). Bisection; intrinsic is monotonically decreasing in r."""
    lo, hi = g_t + MIN_DISCOUNT_SPREAD, 0.60

    def value_at(r: float) -> float:
        return _intrinsic(base_fcf, g, g_t, r, years)[0]

    if value_at(lo) < market_cap:
        return lo  # richly valued even at the minimum discount rate
    if value_at(hi) > market_cap:
        return hi  # deeply cheap even at a very high discount rate
    for _ in range(64):
        mid = (lo + hi) / 2.0
        if value_at(mid) > market_cap:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def _signal(upside: float) -> str:
    if upside >= ENTER_UPSIDE:
        return "Enter"
    if upside <= SIDELINE_UPSIDE:
        return "Sideline"
    return "Accumulate"


def _rationale(v: dict) -> str:
    name, ticker = v["name"], v["ticker"]
    upside, er, r = v["upside_pct"], v["expected_return"], v["discount_rate"]
    intrinsic, price = v["intrinsic_per_share"], v["price"]
    g = v["growth_rate"]
    signal = v["signal"]
    lead = (
        f"Our discounted-cash-flow puts {name} ({ticker}) at an intrinsic value of "
        f"{_fmt_usd(intrinsic)}/share versus a market price of {_fmt_usd(price)} — a margin of "
        f"safety of {_fmt_pct(upside)}. We discount a {_fmt_pct(g)} growth path at a "
        f"{_fmt_pct(r)} cost of equity to a {_fmt_pct(TERMINAL_GROWTH)} terminal rate; at today's "
        f"price the market is implying an expected return of about {_fmt_pct(er)}."
    )
    if signal == "Enter":
        action = (
            " With a margin of safety above our 20% threshold, this clears the bar to "
            "deploy — an attractive entry to accumulate, sized to conviction. The edge is the "
            "gap between price and disclosed intrinsic value, not a forecast of the next print."
        )
    elif signal == "Sideline":
        action = (
            " Priced at or beyond intrinsic value, the margin of safety is negative — the "
            "disciplined call is to stay on the sideline and keep dry powder. Revisit on a "
            "pullback, an earnings reset, or a lower cost of capital."
        )
    else:
        action = (
            " Trading near intrinsic value, the risk/reward is balanced — accumulate "
            "opportunistically on weakness rather than paying up here. No urgency either way."
        )
    return (lead + action + " Research, not investment advice.").replace("  ", " ")


def value_equity(
    ticker: str,
    price: float | None = None,
    risk_free: float | None = None,
) -> EquityValuation:
    """Value one equity via DCF. Raises edgar_services.ProviderError on data-fetch failure
    and ValueError when the inputs can't support a meaningful DCF (e.g., non-positive
    earnings, missing shares/price)."""
    ticker = ticker.strip().upper()
    fin = edgar_services.normalize(ticker)
    hist = edgar_services.history(ticker, max_years=5)
    shares = edgar_services.latest_shares_outstanding(ticker)

    base_fcf = fin.net_income
    if base_fcf is None or base_fcf <= 0:
        raise ValueError(
            f"{ticker}: DCF needs positive earnings; reported net income is non-positive or missing."
        )
    if not shares or shares <= 0:
        raise ValueError(f"{ticker}: shares outstanding unavailable — cannot derive per-share value.")

    if price is None:
        try:
            resp = MarketDataService().quotes([ticker])
            price = next(
                (float(q.price) for q in resp.quotes
                 if q.symbol.upper() == ticker and q.price is not None), None
            )
        except Exception:  # noqa: BLE001
            price = None
    if not price or price <= 0:
        raise ValueError(f"{ticker}: live market price unavailable — cannot compute upside.")

    rf = risk_free if risk_free is not None else risk_free_rate()
    discount = rf + DEFAULT_BETA * DEFAULT_EQUITY_RISK_PREMIUM
    discount = max(discount, TERMINAL_GROWTH + MIN_DISCOUNT_SPREAD)

    cagr = _revenue_cagr(hist)
    g = DEFAULT_GROWTH if cagr is None else max(GROWTH_FLOOR, min(cagr, GROWTH_CAP))

    intrinsic, projected, pvs, tv, pv_tv = _intrinsic(
        base_fcf, g, TERMINAL_GROWTH, discount, PROJECTION_YEARS
    )
    per_share = intrinsic / shares
    market_cap = price * shares
    upside = per_share / price - 1.0
    expected_return = _expected_return(base_fcf, g, TERMINAL_GROWTH, market_cap, PROJECTION_YEARS)
    signal = _signal(upside)

    payload = {
        "ticker": ticker,
        "name": fin.entity_name,
        "price": price,
        "intrinsic_per_share": per_share,
        "upside_pct": upside,
        "expected_return": expected_return,
        "discount_rate": discount,
        "growth_rate": g,
        "signal": signal,
    }
    return EquityValuation(
        ticker=ticker,
        name=fin.entity_name,
        as_of=datetime.now(UTC),
        price=price,
        shares_outstanding=shares,
        market_cap=market_cap,
        base_fcf=base_fcf,
        fcf_basis="Net income (owner-earnings proxy; Phase 2 adds cash-flow-statement FCF).",
        growth_rate=g,
        terminal_growth=TERMINAL_GROWTH,
        risk_free=rf,
        equity_risk_premium=DEFAULT_EQUITY_RISK_PREMIUM,
        beta=DEFAULT_BETA,
        discount_rate=discount,
        projection_years=PROJECTION_YEARS,
        projected_fcf=projected,
        present_values=pvs,
        terminal_value=tv,
        pv_terminal_value=pv_tv,
        intrinsic_equity_value=intrinsic,
        intrinsic_per_share=per_share,
        upside_pct=upside,
        expected_return=expected_return,
        signal=signal,
        rationale=_rationale(payload),
        sources=[
            "SEC EDGAR (fundamentals — public domain)",
            "Market price feed",
            "10-year Treasury yield (risk-free, FRED/market feed)",
        ],
    )


def value_universe(n: int = 8, universe: list[str] | None = None, force: bool = False) -> list[EquityValuation]:
    """Value the large/mid-cap universe and return the top-N by margin of safety (upside).
    Cached ~6h; resilient — names that fail to value are skipped."""
    from app.equity_opportunity_scan import LARGE_MID_CAP_UNIVERSE

    uni = universe or LARGE_MID_CAP_UNIVERSE
    key = f"{n}:{','.join(uni)}"
    now = time.time()
    if not force:
        hit = _universe_cache.get(key)
        if hit and hit[0] > now:
            return hit[1]

    prices: dict[str, float] = {}
    try:
        resp = MarketDataService().quotes(uni)
        for q in resp.quotes:
            if getattr(q, "price", None) is not None and getattr(q, "status", "") == "ok":
                prices[q.symbol.upper()] = float(q.price)
    except Exception:  # noqa: BLE001
        prices = {}

    rf = risk_free_rate()
    valued: list[EquityValuation] = []
    for t in uni:
        try:
            valued.append(value_equity(t, price=prices.get(t.upper()), risk_free=rf))
        except (edgar_services.ProviderError, ValueError):
            continue
        except Exception:
            logger.debug("Skipping unexpected valuation failure for %s.", t, exc_info=True)
            continue

    valued.sort(key=lambda v: v.upside_pct, reverse=True)
    result = valued[:n]
    _universe_cache[key] = (now + _UNIVERSE_TTL_SECONDS, result)
    return result


def reset_cache() -> None:
    _universe_cache.clear()
