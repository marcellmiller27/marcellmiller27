# JHI-SIG: 69M2705M | Tests for the H5 SF1 fundamental-factor back-test (network-free)
"""Network-free unit tests for the point-in-time SF1 factor validation harness.

These exercise the pure math (PIT gating, revenue CAGR, factor vector, cross-sectional
composite) and the metric/verdict machinery with deterministic synthetic panels — no
Sharadar SF1 or Yahoo calls are made.
"""

from __future__ import annotations

from app.sf1_factor_backtest import (
    FACTOR_WEIGHTS,
    _Period,
    _segment_metrics,
    build_periods,
    composite_scores,
    factor_vector,
    pit_rows,
    revenue_cagr,
    summarize,
)


def _sf1_row(datekey: str, reportperiod: str, revenue: float, netinc: float) -> dict:
    return {
        "datekey": datekey,
        "reportperiod": reportperiod,
        "revenue": revenue,
        "netinc": netinc,
        "equity": revenue * 0.5,
        "opinc": netinc * 1.3,
        "fcf": netinc * 0.9,
        "sharesbas": 1_000_000,
    }


def test_pre_registered_weights_sum_to_one() -> None:
    assert abs(sum(FACTOR_WEIGHTS.values()) - 1.0) < 1e-9
    # Value 0.40 / Quality 0.35 / Growth 0.25 blocks.
    value = FACTOR_WEIGHTS["earnings_yield"] + FACTOR_WEIGHTS["book_yield"] + FACTOR_WEIGHTS["fcf_yield"]
    quality = FACTOR_WEIGHTS["roe"] + FACTOR_WEIGHTS["operating_margin"] + FACTOR_WEIGHTS["net_margin"]
    assert abs(value - 0.40) < 1e-9
    assert abs(quality - 0.35) < 1e-9
    assert abs(FACTOR_WEIGHTS["revenue_cagr"] - 0.25) < 1e-9


def test_pit_rows_gate_by_datekey() -> None:
    rows = [
        _sf1_row("2019-03-01", "2018-12-31", 100.0, 10.0),
        _sf1_row("2020-03-01", "2019-12-31", 110.0, 12.0),
        _sf1_row("2021-03-01", "2020-12-31", 130.0, 15.0),
    ]
    # As of mid-2020 only the first two filings were public.
    known = pit_rows(rows, "2020-06-30")
    assert [r["reportperiod"] for r in known] == ["2018-12-31", "2019-12-31"]
    # Before any filing -> nothing.
    assert pit_rows(rows, "2018-01-01") == []


def test_revenue_cagr_pit() -> None:
    rows = [
        _sf1_row("2019-03-01", "2018-12-31", 100.0, 10.0),
        _sf1_row("2021-03-01", "2020-12-31", 121.0, 15.0),
    ]
    # 100 -> 121 over 2 fiscal years == 10% CAGR.
    assert abs(revenue_cagr(rows) - 0.10) < 1e-6
    # Needs at least two positive-revenue rows.
    assert revenue_cagr(rows[:1]) is None


def test_factor_vector_derives_expected_ratios() -> None:
    rows = [
        _sf1_row("2019-03-01", "2018-12-31", 100.0, 10.0),
        _sf1_row("2020-03-01", "2019-12-31", 200.0, 20.0),
    ]
    vec = factor_vector(rows, "2021-01-01", price=1.0)
    # Latest known row: revenue 200, netinc 20, equity 100, opinc 26, fcf 18, shares 1e6.
    market_cap = 1.0 * 1_000_000
    assert abs(vec["earnings_yield"] - 20.0 / market_cap) < 1e-9
    assert abs(vec["book_yield"] - 100.0 / market_cap) < 1e-9
    assert abs(vec["fcf_yield"] - 18.0 / market_cap) < 1e-9
    assert abs(vec["roe"] - 20.0 / 100.0) < 1e-9
    assert abs(vec["operating_margin"] - 26.0 / 200.0) < 1e-9
    assert abs(vec["net_margin"] - 20.0 / 200.0) < 1e-9
    assert set(vec) == set(FACTOR_WEIGHTS)


def test_factor_vector_no_lookahead() -> None:
    """A filing dated in the future must never be used at an earlier rebalance date."""
    rows = [
        _sf1_row("2019-03-01", "2018-12-31", 100.0, 10.0),
        _sf1_row("2020-03-01", "2019-12-31", 110.0, 12.0),
        _sf1_row("2999-01-01", "2998-12-31", 9_999.0, 9_999.0),  # not yet public
    ]
    vec = factor_vector(rows, "2021-01-01", price=1.0)
    # Uses 2019 fiscal year (netinc 12), NOT the absurd future row.
    assert abs(vec["net_margin"] - 12.0 / 110.0) < 1e-9


def test_factor_vector_none_when_incomplete() -> None:
    incomplete = [{"datekey": "2020-03-01", "reportperiod": "2019-12-31", "revenue": 100.0}]
    assert factor_vector(incomplete, "2021-01-01", price=1.0) is None
    assert factor_vector([], "2021-01-01", price=1.0) is None
    assert factor_vector([_sf1_row("2020-03-01", "2019-12-31", 100.0, 10.0)], "2021-01-01", price=0.0) is None


def test_composite_ranks_by_factor_strength() -> None:
    # Two names identical except one has strictly higher raw factors -> higher composite.
    strong = {f: 2.0 for f in FACTOR_WEIGHTS}
    weak = {f: 1.0 for f in FACTOR_WEIGHTS}
    comp = composite_scores({"STRONG": strong, "WEAK": weak})
    assert comp["STRONG"] > comp["WEAK"]


def _perfect_signal_periods(n_periods: int = 24, n_assets: int = 10) -> list[_Period]:
    """Panels where the composite strongly (but not perfectly) predicts forward return."""
    periods: list[_Period] = []
    for p in range(n_periods):
        composite = {f"A{i}": float(i) for i in range(n_assets)}
        forward = {f"A{i}": float(i) * 0.01 for i in range(n_assets)}
        # Introduce a period-VARYING number of adjacent swaps so the IC series has
        # non-zero variance (finite t-stat) while staying strongly positive.
        n_swaps = 1 + (p % 3)
        for s in range(n_swaps):
            a, b = 2 * s, 2 * s + 1
            if b < n_assets:
                forward[f"A{a}"], forward[f"A{b}"] = forward[f"A{b}"], forward[f"A{a}"]
        periods.append(_Period(date=f"20{p:02d}-01-01", composite=composite, forward=forward))
    return periods


def _no_signal_periods(n_periods: int = 24, n_assets: int = 10) -> list[_Period]:
    periods: list[_Period] = []
    for p in range(n_periods):
        composite = {f"A{i}": float(i) for i in range(n_assets)}
        # Deterministic pseudo-shuffle uncorrelated with composite order.
        forward = {f"A{i}": float((i * 7 + p * 3) % n_assets) * 0.01 for i in range(n_assets)}
        periods.append(_Period(date=f"20{p:02d}-01-01", composite=composite, forward=forward))
    return periods


def test_segment_metrics_pass_on_real_signal() -> None:
    m = _segment_metrics("signal", _perfect_signal_periods())
    assert m.mean_ic is not None and m.mean_ic > 0.5
    assert m.ic_t_stat is not None and abs(m.ic_t_stat) >= 2.0
    assert m.hit_rate == 1.0
    assert m.passes is True


def test_segment_metrics_fail_on_no_signal() -> None:
    m = _segment_metrics("noise", _no_signal_periods())
    assert m.mean_ic is not None and abs(m.mean_ic) < 0.2
    assert m.passes is False


def test_summarize_empty_is_unavailable_and_fail() -> None:
    result = summarize(["AAA", "BBB"], [])
    assert result.status == "unavailable"
    assert result.h5_pass is False
    assert result.oos_verdict == "FAIL"


def test_summarize_splits_and_reports_pass_on_signal() -> None:
    result = summarize([f"A{i}" for i in range(10)], _perfect_signal_periods())
    assert result.out_of_sample.n_periods > 0
    assert result.in_sample.n_periods > 0
    assert result.h5_pass is True
    assert result.oos_verdict == "PASS"


def test_build_periods_pit_and_min_names() -> None:
    n_assets = 12
    sf1_by_ticker: dict[str, list[dict]] = {}
    prices_by_ticker: dict[str, list[tuple[str, float]]] = {}
    dates = [f"2021-{month:02d}-01" for month in range(1, 9)]
    for i in range(n_assets):
        sf1_by_ticker[f"A{i}"] = [
            _sf1_row("2020-03-01", "2019-12-31", 100.0 + i, 10.0 + i),
            _sf1_row("2021-03-01", "2020-12-31", 120.0 + i, 12.0 + i),
        ]
        prices_by_ticker[f"A{i}"] = [(d, 100.0 + i + t) for t, d in enumerate(dates)]

    periods = build_periods(sf1_by_ticker, prices_by_ticker, min_names=10)
    assert periods, "expected evaluable periods"
    for period in periods:
        assert len(period.composite) == n_assets
        assert set(period.composite) == set(period.forward)

    # With fewer than min_names available names, no period qualifies.
    few = build_periods(
        {k: sf1_by_ticker[k] for k in ("A0", "A1", "A2")},
        {k: prices_by_ticker[k] for k in ("A0", "A1", "A2")},
        min_names=10,
    )
    assert few == []
