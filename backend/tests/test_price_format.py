# JHI-SIG: 69M2705M | Canonical price formatter tests | JHI Research & Analytics Firm, Inc. (proprietary)
"""Acceptance + boundary tests for the canonical price formatter.

The six founder-specified exact strings are asserted verbatim; keep the TypeScript twin
(``src/lib/format.test.ts``) in lock-step.
"""

from app.price_format import format_price


# --- The six founder exact strings (the acceptance test) --------------------- #
def test_gold_two_decimals_with_commas() -> None:
    assert format_price(4585.80, asset_class="commodity") == "$4,585.80"


def test_btc_two_decimals_with_commas() -> None:
    assert format_price(72909.88, asset_class="crypto") == "$72,909.88"


def test_sub_dollar_crypto_four_decimals() -> None:
    assert format_price(0.1811, asset_class="crypto") == "$0.1811"


def test_low_single_digit_three_decimals() -> None:
    assert format_price(1.264, asset_class="crypto") == "$1.264"


def test_forex_eurusd_four_decimals_no_dollar() -> None:
    assert format_price(1.1690, asset_class="fx") == "1.1690"
    assert format_price(1.1690, is_forex=True) == "1.1690"


def test_forex_usdjpy_four_decimals_regardless_of_magnitude() -> None:
    # ~159 but forex is ALWAYS 4dp with no ``$``.
    assert format_price(158.8840, asset_class="fx") == "158.8840"


# --- Magnitude band boundaries ---------------------------------------------- #
def test_band_boundary_just_under_100_is_three_decimals() -> None:
    assert format_price(99.999, asset_class="equity") == "$99.999"


def test_band_boundary_exactly_100_is_two_decimals() -> None:
    assert format_price(100.0, asset_class="equity") == "$100.00"
    assert format_price(100.00, asset_class="equity") == "$100.00"


def test_band_boundary_just_under_1_is_four_decimals() -> None:
    assert format_price(0.9999, asset_class="crypto") == "$0.9999"


def test_band_boundary_exactly_1_is_three_decimals() -> None:
    assert format_price(1.00, asset_class="crypto") == "$1.000"


# --- Sub-0.0001 significant-figure safeguard -------------------------------- #
def test_sub_ten_thousandth_uses_four_significant_figures() -> None:
    # Would render as $0.0000 under a flat 4dp rule; safeguard shows 4 sig figs.
    assert format_price(0.00001234, asset_class="crypto") == "$0.00001234"
    assert format_price(0.000009876, asset_class="crypto") == "$0.000009876"


def test_exactly_at_0_0001_stays_four_decimals() -> None:
    assert format_price(0.0001, asset_class="crypto") == "$0.0001"


# --- Forex is never dollar-signed even sub-1 -------------------------------- #
def test_forex_sub_one_still_four_decimals_no_dollar() -> None:
    assert format_price(0.6543, asset_class="fx") == "0.6543"


# --- Negative values -------------------------------------------------------- #
def test_negative_dollar_value() -> None:
    assert format_price(-4585.80, asset_class="commodity") == "-$4,585.80"


def test_negative_sub_dollar_value() -> None:
    assert format_price(-0.1811, asset_class="crypto") == "-$0.1811"


def test_negative_forex_value() -> None:
    assert format_price(-1.1690, is_forex=True) == "-1.1690"


# --- Robustness ------------------------------------------------------------- #
def test_none_and_nan_render_em_dash() -> None:
    assert format_price(None, asset_class="crypto") == "—"
    assert format_price(float("nan"), asset_class="crypto") == "—"


def test_zero_dollar_value() -> None:
    assert format_price(0.0, asset_class="crypto") == "$0.0000"


def test_asset_class_case_insensitive_forex() -> None:
    assert format_price(1.1690, asset_class="FX") == "1.1690"
