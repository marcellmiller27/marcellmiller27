# JHI-SIG: 69M2705M | Cross-Asset Valuation & Action Engine — Phase 1 (equities) | JHI Research & Analytics Firm, Inc. (proprietary)
"""Equity DCF + expected-return (IRR) + enter/sideline action engine.

Phase 1 of the Cross-Asset Valuation & Action Engine covers **equities**. It grounds
a transparent, disclosed-assumption discounted-cash-flow on **all our data-sets**:
point-in-time fundamentals (Sharadar SF1 primary, SEC EDGAR fallback — earnings,
equity, revenue history), the live market price, and the risk-free rate from the
market/FRED feed. Raw SF1 rows stay internal; only the derived DCF output is
surfaced (governance). It returns an intrinsic value, an
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

from app import edgar_services, fundamentals
from app.market_services import MarketDataService

logger = logging.getLogger(__name__)

# ── Disclosed model assumptions (Phase 1) ────────────────────────────────────
PROJECTION_YEARS = 5
DEFAULT_EQUITY_RISK_PREMIUM = 0.05  # long-run US equity risk premium
DEFAULT_BETA = 1.0                  # market beta (Phase 1: single-beta; per-name beta later)
TERMINAL_GROWTH = 0.025             # ~ long-run nominal GDP
GROWTH_CAP = 0.12                   # classic cap on projected growth (prudence)
GROWTH_FLOOR = 0.0
DEFAULT_GROWTH = 0.04               # used when revenue history is insufficient
DEFAULT_RISK_FREE = 0.045           # fallback if the 10Y is unavailable
MIN_DISCOUNT_SPREAD = 0.005         # keep discount rate above terminal growth

# Action thresholds (Founder-approved defaults) on margin of safety (upside).
ENTER_UPSIDE = 0.20
SIDELINE_UPSIDE = -0.10

# ── Valuation Framework 2.0 — disclosed assumptions (Phase 1) ─────────────────
# All parameters are fixed, deterministic, and disclosed in the output notes.
INNOVATOR_GROWTH_CAP = 0.18         # higher near-term cap for tech-enabled/innovator names
RND_AMORTIZATION_YEARS = 5          # straight-line life for capitalized R&D (Damodaran-style)
ROIC_FADE_SPREAD = 0.02            # min ROIC-over-cost-of-capital excess to extend high-growth fade
MAX_EXTRA_HIGH_GROWTH_YEARS = 5    # extra fade years granted to durable value creators
MAX_HIGH_GROWTH_YEARS = PROJECTION_YEARS + MAX_EXTRA_HIGH_GROWTH_YEARS  # hard cap (10y)
MOAT_MAX_PREMIUM = 0.15            # max margin-of-safety credit from a full (100) Moat score

# Archetype classification thresholds (R&D-intensity / gross-margin "tell").
RND_INTENSITY_INNOVATOR = 0.06     # R&D / revenue ≥ 6% ⇒ R&D-intensive innovator
RND_INTENSITY_TECH_ENABLED = 0.02  # ≥ 2% + rich gross margin ⇒ tech-enabled
GROSS_MARGIN_TECH = 0.50
GROSS_MARGIN_FRANCHISE = 0.60

_ARCH_INNOVATOR = "R&D-intensive innovator"
_ARCH_TECH_ENABLED = "Tech-enabled"
_ARCH_FRANCHISE = "High-margin franchise"
_ARCH_CLASSIC = "Classic (industry/value)"
_INNOVATOR_ARCHETYPES = frozenset({_ARCH_INNOVATOR, _ARCH_TECH_ENABLED, _ARCH_FRANCHISE})

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
    # ── Valuation Framework 2.0 (innovator-fair view; headline signal below) ──
    # R&D-as-investment
    adjusted_owner_earnings: float
    rnd_treatment: str
    rnd_amortization_years: int
    rnd_asset: float
    # ROIC- & reinvestment-driven growth
    roic: float | None
    cost_of_capital: float
    reinvestment_rate: float | None
    fundamental_growth: float | None
    high_growth_years: int
    growth_path: list[float]
    # Sector re-tagging & calibration
    archetype: str
    growth_cap_used: float
    # Innovation & Moat score (0–100, quantified)
    innovation_moat_score: float
    innovation_moat_components: dict[str, float]
    # Blended read
    composite_margin: float
    # Prior conservative (classic) view — disclosed component
    classic_base_fcf: float
    classic_growth_rate: float
    classic_intrinsic_per_share: float
    classic_upside_pct: float
    classic_signal: str
    # Action (headline = Valuation 2.0 blend)
    signal: str
    rationale: str
    notes: list[str]
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


def _project(base_fcf: float, growth_rates: list[float], g_t: float, r: float):
    """Discount a per-year growth schedule. Returns
    (intrinsic_equity, projected_fcf, present_values, terminal_value, pv_terminal).

    A flat schedule ``[g] * n`` reproduces the classic base * (1+g)**t DCF exactly."""
    projected: list[float] = []
    pvs: list[float] = []
    total = 0.0
    level = base_fcf
    for t, g in enumerate(growth_rates, start=1):
        level = level * (1.0 + g)
        pv = level / (1.0 + r) ** t
        projected.append(level)
        pvs.append(pv)
        total += pv
    n = len(growth_rates)
    terminal_value = level * (1.0 + g_t) / (r - g_t)
    pv_terminal = terminal_value / (1.0 + r) ** n
    return total + pv_terminal, projected, pvs, terminal_value, pv_terminal


def _flat(g: float, years: int = PROJECTION_YEARS) -> list[float]:
    return [g] * years


def _fade(g0: float, n: int, g_t: float) -> list[float]:
    """Linear high-growth fade from ``g0`` (year 1) to ``g_t`` by year ``n``."""
    if n <= 1:
        return [g0]
    return [g0 + (g_t - g0) * i / (n - 1) for i in range(n)]


def _solve_irr(base_fcf: float, growth_rates: list[float], g_t: float, market_cap: float) -> float:
    """Discount rate r that sets DCF value == market cap (equity IRR under the projected
    cash flows). Bisection; intrinsic is monotonically decreasing in r."""
    lo, hi = g_t + MIN_DISCOUNT_SPREAD, 0.60

    def value_at(r: float) -> float:
        return _project(base_fcf, growth_rates, g_t, r)[0]

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


# ── Valuation Framework 2.0 helpers ──────────────────────────────────────────
def _rnd_series(fin) -> list[float]:
    """R&D expense newest-first (index 0 = most recent year) from the year series."""
    rows = [r for r in getattr(fin, "years", []) if getattr(r, "rnd", None)]
    rows.sort(key=lambda r: r.fiscal_year, reverse=True)
    series = [float(r.rnd) for r in rows if r.rnd and r.rnd > 0]
    if not series and getattr(fin, "rnd", None):
        series = [float(fin.rnd)]
    return series


def _rnd_capitalization(rnd_newest_first: list[float], life: int) -> tuple[float, float, float]:
    """Damodaran-style R&D capitalization (deterministic).

    Treats R&D as a capital asset amortized straight-line over ``life`` years:
      - ``asset``        — unamortized R&D asset (Σ spend_k × (life−k)/life)
      - ``amortization`` — this year's amortization charge (Σ spend_k / life)
      - ``adjustment``   — current R&D expense − amortization, added back to net income

    Steady-state R&D ⇒ adjustment ≈ 0 (no free lunch); rising R&D ⇒ positive add-back,
    so heavy-R&D innovators are credited for the investment rather than penalized."""
    if not rnd_newest_first:
        return 0.0, 0.0, 0.0
    current = rnd_newest_first[0]
    asset = 0.0
    amortization = 0.0
    for k in range(min(len(rnd_newest_first), life)):
        spend = rnd_newest_first[k]
        asset += spend * (life - k) / life
        amortization += spend / life
    return asset, amortization, current - amortization


def _rnd_cagr(fin) -> float | None:
    series = _rnd_series(fin)  # newest-first
    if len(series) < 2:
        return None
    newest, oldest = series[0], series[-1]
    span = len(series) - 1
    if oldest <= 0 or newest <= 0:
        return None
    try:
        return (newest / oldest) ** (1.0 / span) - 1.0
    except (ZeroDivisionError, ValueError):
        return None


def _reinvestment_rate(fin) -> float | None:
    """Reinvestment = (capex + R&D) / net income (SF1 capex sign-agnostic)."""
    ni = getattr(fin, "net_income", None)
    if not ni or ni <= 0:
        return None
    capex = abs(getattr(fin, "capex", None) or 0.0)
    rnd = getattr(fin, "rnd", None) or 0.0
    if capex == 0.0 and rnd == 0.0:
        return None
    return (capex + rnd) / ni


def _archetype(rnd_intensity: float | None, gross_margin: float | None) -> str:
    gm = gross_margin or 0.0
    if rnd_intensity is not None and rnd_intensity >= RND_INTENSITY_INNOVATOR:
        return _ARCH_INNOVATOR
    if rnd_intensity is not None and rnd_intensity >= RND_INTENSITY_TECH_ENABLED and gm >= GROSS_MARGIN_TECH:
        return _ARCH_TECH_ENABLED
    if gm >= GROSS_MARGIN_FRANCHISE:
        return _ARCH_FRANCHISE
    return _ARCH_CLASSIC


def _norm(x: float | None, lo: float, hi: float) -> float:
    """Clamp x into [0,1] on the [lo,hi] scale; None ⇒ 0 (can't credit what we can't measure)."""
    if x is None or hi <= lo:
        return 0.0
    return max(0.0, min(1.0, (x - lo) / (hi - lo)))


def _moat_score(
    *,
    rnd_intensity: float | None,
    rnd_cagr: float | None,
    gross_margin: float | None,
    revenue_cagr: float | None,
    roic_excess: float | None,
) -> tuple[float, dict[str, float]]:
    """Quantified 0–100 Innovation & Moat score. Missing inputs score 0 (conservative)."""
    parts = {
        "rnd_intensity": 25.0 * _norm(rnd_intensity, 0.0, 0.15),
        "rnd_growth": 15.0 * _norm(rnd_cagr, 0.0, 0.25),
        "gross_margin_durability": 20.0 * _norm(gross_margin, 0.20, 0.70),
        "revenue_growth_durability": 20.0 * _norm(revenue_cagr, 0.0, 0.20),
        "reinvestment_efficiency": 20.0 * _norm(roic_excess, 0.0, 0.20),
    }
    score = round(sum(parts.values()), 1)
    return score, {k: round(v, 1) for k, v in parts.items()}


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
    archetype = v["archetype"]
    moat = v["innovation_moat_score"]
    classic_val = v["classic_intrinsic_per_share"]
    classic_up = v["classic_upside_pct"]
    composite = v["composite_margin"]
    high_years = v["high_growth_years"]
    lead = (
        f"Valuation 2.0 tags {name} ({ticker}) as a {archetype.lower()} (Innovation & Moat "
        f"{moat:.0f}/100) and puts its intrinsic value at {_fmt_usd(intrinsic)}/share versus a "
        f"market price of {_fmt_usd(price)} — a {_fmt_pct(upside)} margin of safety "
        f"({_fmt_pct(composite)} after the moat credit). We start from R&D-adjusted owner-earnings, "
        f"fade a {_fmt_pct(g)} growth path over {high_years} years at a {_fmt_pct(r)} cost of "
        f"capital to a {_fmt_pct(TERMINAL_GROWTH)} terminal, implying an expected return of about "
        f"{_fmt_pct(er)}. The prior conservative (classic) DCF valued it at "
        f"{_fmt_usd(classic_val)}/share ({_fmt_pct(classic_up)} margin) — shown as a disclosed "
        f"lower-bound component."
    )
    if signal == "Enter":
        action = (
            " With the blended margin of safety above our 20% threshold, this clears the bar to "
            "deploy — an attractive entry to accumulate, sized to conviction. The edge is the "
            "gap between price and disclosed intrinsic value, not a forecast of the next print."
        )
    elif signal == "Sideline":
        action = (
            " Priced at or beyond intrinsic value even after the moat credit, the margin of "
            "safety is negative — the disciplined call is to stay on the sideline and keep dry "
            "powder. Revisit on a pullback, an earnings reset, or a lower cost of capital."
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
    # Point-in-time fundamentals: Sharadar SF1 primary, SEC EDGAR fallback. Only the
    # DERIVED DCF output below is surfaced — raw SF1 rows stay internal (governance).
    fin = fundamentals.equity_fundamentals(ticker, max_years=5)
    hist = fin  # `.years` is duck-compatible with the CAGR helper
    shares = fin.shares_outstanding

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

    net_income = base_fcf  # positive owner-earnings proxy (validated above)

    rf = risk_free if risk_free is not None else risk_free_rate()
    discount = rf + DEFAULT_BETA * DEFAULT_EQUITY_RISK_PREMIUM
    discount = max(discount, TERMINAL_GROWTH + MIN_DISCOUNT_SPREAD)

    cagr = _revenue_cagr(hist)
    market_cap = price * shares

    # ── Prior conservative (classic) DCF: net income, flat capped growth (unchanged) ──
    classic_g = DEFAULT_GROWTH if cagr is None else max(GROWTH_FLOOR, min(cagr, GROWTH_CAP))
    classic_intrinsic, _, _, _, _ = _project(net_income, _flat(classic_g), TERMINAL_GROWTH, discount)
    classic_per_share = classic_intrinsic / shares
    classic_upside = classic_per_share / price - 1.0
    classic_signal = _signal(classic_upside)

    # ── Valuation 2.0 ─────────────────────────────────────────────────────────
    # 1) R&D-as-investment: capitalize/amortize R&D into adjusted owner-earnings.
    rnd_hist = _rnd_series(fin)
    rnd_asset, rnd_amort, rnd_adj = _rnd_capitalization(rnd_hist, RND_AMORTIZATION_YEARS)
    adjusted_owner_earnings = net_income + rnd_adj
    if adjusted_owner_earnings <= 0:
        adjusted_owner_earnings = net_income  # never let the add-back invert the sign
    if rnd_hist:
        rnd_treatment = (
            f"Capitalized R&D over {RND_AMORTIZATION_YEARS}y (Damodaran): owner-earnings = net "
            f"income + current R&D {_fmt_usd(rnd_hist[0])} − amortization {_fmt_usd(rnd_amort)}."
        )
    else:
        rnd_treatment = "No R&D reported — owner-earnings = net income (no adjustment)."

    # 2) Sector re-tag & calibration from the R&D-intensity / gross-margin tell.
    revenue = getattr(fin, "revenue", None)
    rnd_latest = getattr(fin, "rnd", None) or (rnd_hist[0] if rnd_hist else None)
    rnd_intensity = (rnd_latest / revenue) if (rnd_latest and revenue and revenue > 0) else None
    archetype = _archetype(rnd_intensity, getattr(fin, "gross_margin", None))
    growth_cap = INNOVATOR_GROWTH_CAP if archetype in _INNOVATOR_ARCHETYPES else GROWTH_CAP

    # 3) ROIC- & reinvestment-driven growth.
    roic = getattr(fin, "roic", None)
    roic_excess = (roic - discount) if roic is not None else None
    reinvestment = _reinvestment_rate(fin)
    fundamental_growth = (reinvestment * roic) if (reinvestment is not None and roic is not None) else None

    if cagr is not None:
        g0 = max(GROWTH_FLOOR, min(cagr, growth_cap))
    elif fundamental_growth is not None:
        g0 = max(GROWTH_FLOOR, min(fundamental_growth, growth_cap))
    else:
        g0 = DEFAULT_GROWTH

    # 4) Innovation & Moat score (needs revenue CAGR + roic excess).
    moat_score, moat_parts = _moat_score(
        rnd_intensity=rnd_intensity,
        rnd_cagr=_rnd_cagr(fin),
        gross_margin=getattr(fin, "gross_margin", None),
        revenue_cagr=cagr,
        roic_excess=roic_excess,
    )

    # Longer high-growth fade for durable value creators (ROIC > cost of capital).
    high_years = PROJECTION_YEARS
    if roic_excess is not None and roic_excess >= ROIC_FADE_SPREAD:
        extra = round(roic_excess / 0.05) + round(moat_score / 50.0)
        high_years = min(MAX_HIGH_GROWTH_YEARS, PROJECTION_YEARS + min(MAX_EXTRA_HIGH_GROWTH_YEARS, extra))

    if high_years > PROJECTION_YEARS:
        growth_path = _fade(g0, high_years, TERMINAL_GROWTH)
    else:
        growth_path = _flat(g0, PROJECTION_YEARS)  # reduces to classic when no durability evidence

    intrinsic, projected, pvs, tv, pv_tv = _project(
        adjusted_owner_earnings, growth_path, TERMINAL_GROWTH, discount
    )
    per_share = intrinsic / shares
    upside = per_share / price - 1.0
    expected_return = _solve_irr(adjusted_owner_earnings, growth_path, TERMINAL_GROWTH, market_cap)

    # 5) Blend: intrinsic margin of safety + Innovation/Moat credit → the call.
    composite_margin = upside + MOAT_MAX_PREMIUM * (moat_score / 100.0)
    signal = _signal(composite_margin)

    notes = [
        f"Archetype (calibration): {archetype}; growth cap {_fmt_pct(growth_cap)} "
        f"(R&D-intensity {_fmt_pct(rnd_intensity) if rnd_intensity is not None else 'n/a'}, "
        f"gross margin {_fmt_pct(fin.gross_margin) if getattr(fin, 'gross_margin', None) is not None else 'n/a'}).",
        rnd_treatment,
        (
            f"Growth: year-1 {_fmt_pct(g0)} fading to terminal {_fmt_pct(TERMINAL_GROWTH)} over "
            f"{high_years} years. ROIC {_fmt_pct(roic) if roic is not None else 'n/a'} vs cost of "
            f"capital {_fmt_pct(discount)} "
            + (
                f"(excess {_fmt_pct(roic_excess)} extends the high-growth fade)."
                if roic_excess is not None and roic_excess >= ROIC_FADE_SPREAD
                else "(no fade extension)."
            )
        ),
        (
            f"Reinvestment rate {_fmt_pct(reinvestment) if reinvestment is not None else 'n/a'} × ROIC ⇒ "
            f"fundamental growth {_fmt_pct(fundamental_growth) if fundamental_growth is not None else 'n/a'}."
        ),
        (
            f"Innovation & Moat {moat_score:.0f}/100 = "
            + ", ".join(f"{k} {val:.0f}" for k, val in moat_parts.items())
            + f"; moat credit {_fmt_pct(MOAT_MAX_PREMIUM * moat_score / 100.0)} added to the "
            f"{_fmt_pct(upside)} raw margin ⇒ {_fmt_pct(composite_margin)} blended."
        ),
        (
            f"Signals: classic {classic_signal} ({_fmt_pct(classic_upside)}) vs "
            f"Valuation 2.0 {signal} ({_fmt_pct(composite_margin)})."
        ),
        "Deterministic and fact-locked; all figures derived from disclosed inputs. Research, not investment advice.",
    ]

    payload = {
        "ticker": ticker,
        "name": fin.entity_name,
        "price": price,
        "intrinsic_per_share": per_share,
        "upside_pct": upside,
        "expected_return": expected_return,
        "discount_rate": discount,
        "growth_rate": g0,
        "signal": signal,
        "archetype": archetype,
        "innovation_moat_score": moat_score,
        "classic_intrinsic_per_share": classic_per_share,
        "classic_upside_pct": classic_upside,
        "composite_margin": composite_margin,
        "high_growth_years": high_years,
    }
    return EquityValuation(
        ticker=ticker,
        name=fin.entity_name,
        as_of=datetime.now(UTC),
        price=price,
        shares_outstanding=shares,
        market_cap=market_cap,
        base_fcf=adjusted_owner_earnings,
        fcf_basis="R&D-adjusted owner-earnings (net income + capitalized/amortized R&D).",
        growth_rate=g0,
        terminal_growth=TERMINAL_GROWTH,
        risk_free=rf,
        equity_risk_premium=DEFAULT_EQUITY_RISK_PREMIUM,
        beta=DEFAULT_BETA,
        discount_rate=discount,
        projection_years=len(growth_path),
        projected_fcf=projected,
        present_values=pvs,
        terminal_value=tv,
        pv_terminal_value=pv_tv,
        intrinsic_equity_value=intrinsic,
        intrinsic_per_share=per_share,
        upside_pct=upside,
        expected_return=expected_return,
        # Valuation 2.0
        adjusted_owner_earnings=adjusted_owner_earnings,
        rnd_treatment=rnd_treatment,
        rnd_amortization_years=RND_AMORTIZATION_YEARS,
        rnd_asset=rnd_asset,
        roic=roic,
        cost_of_capital=discount,
        reinvestment_rate=reinvestment,
        fundamental_growth=fundamental_growth,
        high_growth_years=high_years,
        growth_path=growth_path,
        archetype=archetype,
        growth_cap_used=growth_cap,
        innovation_moat_score=moat_score,
        innovation_moat_components=moat_parts,
        composite_margin=composite_margin,
        classic_base_fcf=net_income,
        classic_growth_rate=classic_g,
        classic_intrinsic_per_share=classic_per_share,
        classic_upside_pct=classic_upside,
        classic_signal=classic_signal,
        signal=signal,
        rationale=_rationale(payload),
        notes=notes,
        sources=[
            fundamentals.source_label(fin.source),
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
