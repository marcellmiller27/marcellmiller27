# JHI-SIG: 69M2705M | Research & Opportunity Score | John Henry Investments (proprietary)
"""Point-in-time (PIT) fundamental factor computation from Sharadar SF1 rows.

Pure functions (no I/O) so they are deterministically unit-testable. The live SF1
history is fetched by ``market_services.sharadar_sf1_history`` and passed in here.

CRITICAL PIT rule: only rows whose filing date (``datekey``) is on/before the
as-of date are used — this is what prevents look-ahead bias. Use the As-Reported
dimensions (ARQ/ART/ARY), never the restated MRQ/MRT/MRY.
"""

from __future__ import annotations

from typing import Any

# Factor names produced by this module (higher = more attractive, pre-normalization).
FUNDAMENTAL_FACTORS = [
    "value_earnings_yield",   # earnings / price  (cheap = high)
    "value_book_to_price",    # book / price      (cheap = high)
    "quality_roe",            # return on equity
    "quality_net_margin",     # net income / revenue
    "growth_revenue_yoy",     # YoY revenue growth
    "growth_earnings_yoy",    # YoY EPS growth
]


def _f(row: dict[str, Any], key: str) -> float | None:
    """Return a numeric field as float, or None if missing/unparseable."""
    val = row.get(key)
    if val is None:
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def _safe_ratio(num: float | None, den: float | None) -> float | None:
    if num is None or den is None or den == 0:
        return None
    return num / den


def _prior_year_row(rows: list[dict[str, Any]], as_of_row: dict[str, Any]) -> dict[str, Any] | None:
    """Find the row ~1 year (>= 300 days) before the as-of row's calendardate/datekey."""
    ref = as_of_row.get("calendardate") or as_of_row.get("datekey")
    if not ref:
        return None
    ref_year = int(str(ref)[:4])
    candidates = [
        r for r in rows
        if (r.get("calendardate") or r.get("datekey"))
        and int(str(r.get("calendardate") or r.get("datekey"))[:4]) <= ref_year - 1
    ]
    return candidates[-1] if candidates else None


def pit_fundamental_factors(
    rows: list[dict[str, Any]], as_of: str
) -> dict[str, float] | None:
    """Compute PIT fundamental factors as of ``as_of`` (YYYY-MM-DD).

    ``rows`` must be SF1 records sorted ascending by ``datekey``. Only rows filed
    on/before ``as_of`` are used (no look-ahead). Returns a factor->value dict, or
    ``None`` if there is no usable filing as of that date.
    """
    visible = [r for r in rows if (r.get("datekey") or "") <= as_of]
    if not visible:
        return None
    cur = visible[-1]  # most recent filing known as of `as_of`

    price = _f(cur, "price")
    eps = _f(cur, "eps")
    equity = _f(cur, "equity")
    netinc = _f(cur, "netinc")
    revenue = _f(cur, "revenue")
    marketcap = _f(cur, "marketcap")
    shares = _f(cur, "sharesbas") or _f(cur, "shareswa")

    factors: dict[str, float] = {}

    # --- Value ---
    ey = _safe_ratio(eps, price)
    if ey is None:
        ey = _safe_ratio(netinc, marketcap)
    if ey is not None:
        factors["value_earnings_yield"] = ey

    # book-to-price: prefer 1/pb; else equity/marketcap; else book-per-share/price
    pb = _f(cur, "pb")
    bp = (1.0 / pb) if (pb and pb != 0) else _safe_ratio(equity, marketcap)
    if bp is None and shares and price:
        bp = _safe_ratio(equity, shares * price)
    if bp is not None:
        factors["value_book_to_price"] = bp

    # --- Quality ---
    roe = _f(cur, "roe")
    if roe is None:
        roe = _safe_ratio(netinc, equity)
    if roe is not None:
        factors["quality_roe"] = roe

    nm = _f(cur, "netmargin")
    if nm is None:
        nm = _safe_ratio(netinc, revenue)
    if nm is not None:
        factors["quality_net_margin"] = nm

    # --- Growth (needs a ~1-year-prior filing) ---
    prior = _prior_year_row(visible, cur)
    if prior is not None:
        rev0 = _f(prior, "revenue")
        if revenue is not None and rev0 not in (None, 0):
            factors["growth_revenue_yoy"] = (revenue - rev0) / abs(rev0)
        eps0 = _f(prior, "eps")
        if eps is not None and eps0 not in (None, 0):
            factors["growth_earnings_yoy"] = (eps - eps0) / abs(eps0)

    return factors or None
