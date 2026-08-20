# JHI-SIG: 69M2705M | Canonical price formatter (magnitude-aware) | JHI Research & Analytics Firm, Inc. (proprietary)
"""One canonical, magnitude-aware price-formatting standard for the whole platform.

This is the single source of truth on the backend for how an asset price renders as
text. The TypeScript twin in ``src/lib/format.ts`` implements the identical rule so a
price looks the same in a newsletter PDF, an Excel workbook label, and the live UI.

THE STANDARD
------------
Forex pairs / FX rates (EUR/USD, USD/JPY, GBP/USD, ...):
    4 decimal places, NO ``$`` symbol, shown as the rate — ALWAYS 4dp regardless of
    magnitude (USD/JPY is ~159 but still 4dp).

Dollar-priced assets (crypto, commodities, equities, indices, ETFs):
    ``$`` prefix + thousands comma separators, decimals BY MAGNITUDE of the absolute
    value:
      abs >= 100          -> 2 decimals  ($4,585.80, $72,909.88)
      1 <= abs < 100      -> 3 decimals  ($1.264)
      0.0001 <= abs < 1   -> 4 decimals  ($0.1811)
      abs < 0.0001        -> 4 significant figures (safeguard so a tiny value is not
                              shown as ``$0.0000``); never changes any of the above.

This is DISPLAY formatting only — it never mutates the stored/computed numeric value.
"""

from __future__ import annotations

import math
from typing import Any, Protocol

# Asset classes whose price renders as a dollar amount (``$`` + magnitude rule).
DOLLAR_PRICE_CLASSES: frozenset[str] = frozenset(
    {
        "crypto",
        "commodity",
        "equity",
        "index",
        "reit",
        "etf",
        "bond_proxy",
        "pe_proxy",
        "smb_proxy",
    }
)

# Asset classes that are forex rates (4dp, no ``$``).
FOREX_CLASSES: frozenset[str] = frozenset({"fx", "forex"})

EM_DASH = "—"


def _is_forex(asset_class: str | None, is_forex: bool | None) -> bool:
    if is_forex is not None:
        return is_forex
    if asset_class is not None:
        return asset_class.strip().lower() in FOREX_CLASSES
    return False


def _dollar_decimals(abs_value: float) -> int:
    """Decimal places for a dollar-priced value, by magnitude of its absolute value."""
    if abs_value >= 100:
        return 2
    if abs_value >= 1:
        return 3
    if abs_value >= 0.0001:
        return 4
    if abs_value == 0:
        return 4
    # Safeguard: sub-0.0001 -> 4 significant figures so it isn't shown as $0.0000.
    return max(4, 3 - math.floor(math.log10(abs_value)))


def format_price(
    value: float | int | None,
    *,
    asset_class: str | None = None,
    is_forex: bool | None = None,
) -> str:
    """Render ``value`` as a price string per the canonical standard.

    Pass ``is_forex=True`` (or an ``asset_class`` of ``"fx"``/``"forex"``) for FX rates
    (4dp, no ``$``); otherwise the value is treated as a dollar-priced asset and rendered
    with a ``$`` prefix, thousands separators, and magnitude-based decimals.
    """
    if value is None:
        return EM_DASH
    try:
        v = float(value)
    except (TypeError, ValueError):
        return EM_DASH
    if math.isnan(v) or math.isinf(v):
        return EM_DASH

    if _is_forex(asset_class, is_forex):
        # Forex: always 4dp, no ``$``, shown as the rate (no thousands separator).
        return f"{v:.4f}"

    sign = "-" if v < 0 else ""
    abs_v = abs(v)
    decimals = _dollar_decimals(abs_v)
    return f"{sign}${abs_v:,.{decimals}f}"


class _QuoteLike(Protocol):
    price: float | None
    unit: str
    asset_class: str


def format_quote(quote: _QuoteLike | Any | None) -> str:
    """Format a market quote for display, dispatching on its asset class / unit.

    Prices (forex + dollar-priced asset classes) route through :func:`format_price`;
    non-price readings (rates as ``%``, macro index levels, aggregate money-supply
    figures) keep their established, purpose-built formatting since the price standard
    does not apply to them. Twin of ``formatQuoteValue`` in ``src/lib/format.ts``.
    """
    if quote is None:
        return EM_DASH
    price = getattr(quote, "price", None)
    if price is None:
        return EM_DASH
    v = float(price)
    asset_class = (getattr(quote, "asset_class", None) or "").strip().lower()
    unit = getattr(quote, "unit", "") or ""

    if asset_class in FOREX_CLASSES:
        return format_price(v, is_forex=True)
    if asset_class in DOLLAR_PRICE_CLASSES:
        return format_price(v, asset_class=asset_class)

    # Non-price readings — preserve the existing, unit-appropriate rendering.
    if unit == "%":
        return f"{v:.2f}%"
    if unit == "index":
        return f"{v:.1f}"
    if unit == "USD bn":
        return f"${v / 1000:.2f}T" if v >= 1000 else f"${v:.1f}B"
    if unit == "USD mn":
        return f"${v / 1000:.2f}B" if v >= 1000 else f"${v:.1f}M"
    if unit in ("USD/oz", "USD"):
        return format_price(v, asset_class=asset_class)
    return f"{v:,.2f}"
