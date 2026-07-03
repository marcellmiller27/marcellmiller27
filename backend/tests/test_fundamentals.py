"""Tests for point-in-time fundamental factor computation (no look-ahead)."""

from app.fundamentals import FUNDAMENTAL_FACTORS, pit_fundamental_factors


def _row(datekey, caldate, price, eps, equity, netinc, revenue, marketcap, pb=None):
    return {
        "ticker": "TST",
        "dimension": "ARQ",
        "datekey": datekey,
        "calendardate": caldate,
        "price": price,
        "eps": eps,
        "equity": equity,
        "netinc": netinc,
        "revenue": revenue,
        "marketcap": marketcap,
        "pb": pb,
    }


ROWS = [
    # ~1 year prior filing
    _row("2022-05-15", "2022-03-31", 100.0, 4.0, 500.0, 80.0, 800.0, 2000.0, pb=4.0),
    # current filing
    _row("2023-05-15", "2023-03-31", 120.0, 5.0, 600.0, 100.0, 1000.0, 2400.0, pb=4.0),
    # a FUTURE filing that must be ignored when as_of is before it
    _row("2024-05-15", "2024-03-31", 150.0, 6.0, 700.0, 130.0, 1300.0, 3000.0, pb=4.0),
]


def test_computes_all_factor_families() -> None:
    f = pit_fundamental_factors(ROWS, as_of="2023-06-01")
    assert f is not None
    # value: earnings yield = eps/price = 5/120
    assert abs(f["value_earnings_yield"] - (5.0 / 120.0)) < 1e-9
    # book-to-price from pb=4 -> 0.25
    assert abs(f["value_book_to_price"] - 0.25) < 1e-9
    # quality: net margin = netinc/revenue = 100/1000 (netmargin not provided)
    assert abs(f["quality_net_margin"] - 0.10) < 1e-9
    # quality: roe = netinc/equity = 100/600
    assert abs(f["quality_roe"] - (100.0 / 600.0)) < 1e-9
    # growth: revenue YoY = (1000-800)/800 = 0.25
    assert abs(f["growth_revenue_yoy"] - 0.25) < 1e-9
    # growth: eps YoY = (5-4)/4 = 0.25
    assert abs(f["growth_earnings_yoy"] - 0.25) < 1e-9


def test_no_look_ahead_uses_only_filed_rows() -> None:
    # As of 2023-06-01 the 2024 filing must NOT be used.
    f = pit_fundamental_factors(ROWS, as_of="2023-06-01")
    assert abs(f["value_earnings_yield"] - (5.0 / 120.0)) < 1e-9
    # As of 2024-06-01 the 2024 filing becomes the current one (eps 6 / price 150).
    f2 = pit_fundamental_factors(ROWS, as_of="2024-06-01")
    assert abs(f2["value_earnings_yield"] - (6.0 / 150.0)) < 1e-9


def test_returns_none_before_first_filing() -> None:
    assert pit_fundamental_factors(ROWS, as_of="2020-01-01") is None


def test_growth_absent_without_prior_year() -> None:
    only_first = [ROWS[0]]
    f = pit_fundamental_factors(only_first, as_of="2022-06-01")
    assert f is not None
    assert "growth_revenue_yoy" not in f  # no prior-year row available


def test_handles_missing_and_zero_denominators() -> None:
    row = _row("2023-05-15", "2023-03-31", 0.0, None, 0.0, None, 0.0, 0.0, pb=0.0)
    f = pit_fundamental_factors([row], as_of="2023-06-01")
    # No valid ratios computable -> None (not a crash).
    assert f is None


def test_factor_names_exported() -> None:
    assert set(FUNDAMENTAL_FACTORS) == {
        "value_earnings_yield", "value_book_to_price", "quality_roe",
        "quality_net_margin", "growth_revenue_yoy", "growth_earnings_yoy",
    }
