# JHI-SIG: 69M2705M | Tests for the H5 EXPANDED SF1 back-test (network-free)
"""Network-free unit tests for the expanded, survivorship-free SF1 validation harness.

These exercise the pure math (quarter bucketing, TTM revenue CAGR, momentum, PIT factor
vector, fundamental composite, blend, size/sector neutralization, observation building
with the no-look-ahead forward-return window, and the metric/verdict machinery) with
deterministic synthetic panels — no Sharadar SF1 or TICKERS calls are made.
"""

from __future__ import annotations

import math

from app.sf1_expanded_backtest import (
    FUND_BLEND_WEIGHT,
    FUND_FACTOR_WEIGHTS,
    MOM_BLEND_WEIGHT,
    _Observation,
    _ols_residualize,
    _sector_neutralize,
    _segment_metrics,
    assemble_periods,
    blend_scores,
    build_observations,
    fundamental_composite,
    fundamental_vector,
    neutralize,
    price_momentum,
    quarter_bucket,
    summarize,
    ttm_revenue_cagr,
)


def _art_row(datekey: str, reportperiod: str, revenue: float, netinc: float, price: float) -> dict:
    return {
        "datekey": datekey,
        "reportperiod": reportperiod,
        "revenue": revenue,
        "netinc": netinc,
        "equity": revenue * 0.5,
        "opinc": netinc * 1.3,
        "fcf": netinc * 0.9,
        "sharesbas": 1_000_000,
        "price": price,
    }


def _series(ticker_seed: float, n: int = 10) -> list[dict]:
    """A ticker's ascending ART rows spanning ~n years (one filing per year)."""
    rows = []
    for i in range(n):
        year = 2010 + i
        rows.append(
            _art_row(
                datekey=f"{year}-03-01",
                reportperiod=f"{year - 1}-12-31",
                revenue=100.0 + 10.0 * i + ticker_seed,
                netinc=10.0 + i + ticker_seed,
                price=10.0 + i + ticker_seed,
            )
        )
    return rows


# --------------------------------------------------------------------------- #
# Pre-registered constants                                                     #
# --------------------------------------------------------------------------- #
def test_pre_registered_weights_and_blend() -> None:
    assert abs(sum(FUND_FACTOR_WEIGHTS.values()) - 1.0) < 1e-9
    value = (
        FUND_FACTOR_WEIGHTS["earnings_yield"]
        + FUND_FACTOR_WEIGHTS["book_yield"]
        + FUND_FACTOR_WEIGHTS["fcf_yield"]
    )
    quality = (
        FUND_FACTOR_WEIGHTS["roe"]
        + FUND_FACTOR_WEIGHTS["operating_margin"]
        + FUND_FACTOR_WEIGHTS["net_margin"]
    )
    assert abs(value - 0.40) < 1e-9
    assert abs(quality - 0.35) < 1e-9
    assert abs(FUND_FACTOR_WEIGHTS["revenue_cagr"] - 0.25) < 1e-9
    assert abs(FUND_BLEND_WEIGHT + MOM_BLEND_WEIGHT - 1.0) < 1e-9


def test_quarter_bucket() -> None:
    assert quarter_bucket("2014-01-15") == "2014-Q1"
    assert quarter_bucket("2014-03-31") == "2014-Q1"
    assert quarter_bucket("2014-04-01") == "2014-Q2"
    assert quarter_bucket("2014-08-20") == "2014-Q3"
    assert quarter_bucket("2014-12-31") == "2014-Q4"


# --------------------------------------------------------------------------- #
# Factor math                                                                  #
# --------------------------------------------------------------------------- #
def test_ttm_revenue_cagr_pit() -> None:
    rows = [
        _art_row("2018-03-01", "2017-12-31", 100.0, 10.0, 10.0),
        _art_row("2019-03-01", "2018-12-31", 110.0, 11.0, 11.0),
        _art_row("2021-03-01", "2020-12-31", 121.0, 12.0, 12.0),
    ]
    # From idx 2 (2020) back to the earliest within 3y -> 2017 (100 -> 121 over 3y).
    assert abs(ttm_revenue_cagr(rows, 2) - ((121.0 / 100.0) ** (1 / 3) - 1.0)) < 1e-9
    # idx 0 has no earlier row -> None.
    assert ttm_revenue_cagr(rows, 0) is None


def test_price_momentum_uses_only_past_prices() -> None:
    rows = _series(0.0, n=8)  # prices 10,11,...,17
    # idx 5 (price 15) vs idx 1 (price 11) over 4 quarters lookback.
    assert abs(price_momentum(rows, 5) - (15.0 / 11.0 - 1.0)) < 1e-9
    # Not enough history for a 4-back lookback.
    assert price_momentum(rows, 3) is None


def test_fundamental_vector_derives_expected_ratios() -> None:
    rows = [
        _art_row("2018-03-01", "2017-12-31", 100.0, 10.0, 5.0),
        _art_row("2019-03-01", "2018-12-31", 200.0, 20.0, 5.0),
    ]
    vec = fundamental_vector(rows, 1)
    market_cap = 5.0 * 1_000_000
    assert abs(vec["earnings_yield"] - 20.0 / market_cap) < 1e-9
    assert abs(vec["book_yield"] - 100.0 / market_cap) < 1e-9
    assert abs(vec["fcf_yield"] - 18.0 / market_cap) < 1e-9
    assert abs(vec["roe"] - 20.0 / 100.0) < 1e-9
    assert abs(vec["operating_margin"] - 26.0 / 200.0) < 1e-9
    assert abs(vec["net_margin"] - 20.0 / 200.0) < 1e-9
    assert set(vec) == set(FUND_FACTOR_WEIGHTS)


def test_fundamental_vector_none_when_incomplete() -> None:
    incomplete = [{"datekey": "2019-03-01", "reportperiod": "2018-12-31", "revenue": 100.0}]
    assert fundamental_vector(incomplete, 0) is None
    bad_price = [
        _art_row("2018-03-01", "2017-12-31", 100.0, 10.0, 10.0),
        _art_row("2019-03-01", "2018-12-31", 110.0, 11.0, 0.0),
    ]
    assert fundamental_vector(bad_price, 1) is None


def test_composite_ranks_by_factor_strength() -> None:
    strong = {f: 2.0 for f in FUND_FACTOR_WEIGHTS}
    weak = {f: 1.0 for f in FUND_FACTOR_WEIGHTS}
    comp = fundamental_composite({"STRONG": strong, "WEAK": weak})
    assert comp["STRONG"] > comp["WEAK"]


def test_blend_weights_and_leg_isolation() -> None:
    fund = {"A": -1.0, "B": 1.0}
    mom = {"A": 1.0, "B": -1.0}
    blended = blend_scores(fund, mom)
    # 0.6*z(fund) + 0.4*z(mom); fund and mom point opposite, fund wins (0.6 > 0.4).
    assert blended["B"] > blended["A"]
    fund_only = blend_scores(fund, mom, fund_w=1.0, mom_w=0.0)
    assert fund_only["B"] > fund_only["A"]
    mom_only = blend_scores(fund, mom, fund_w=0.0, mom_w=1.0)
    assert mom_only["A"] > mom_only["B"]


# --------------------------------------------------------------------------- #
# Neutralization                                                               #
# --------------------------------------------------------------------------- #
def test_ols_residualize_removes_linear_size_tilt() -> None:
    # y is an exact linear function of x -> residuals are ~0.
    x = {t: float(i) for i, t in enumerate("ABCDE")}
    y = {t: 3.0 + 2.0 * x[t] for t in x}
    resid = _ols_residualize(y, x)
    assert all(abs(v) < 1e-9 for v in resid.values())


def test_sector_neutralize_zero_mean_unit_sd_within_sector() -> None:
    scores = {"A": 1.0, "B": 3.0, "C": 10.0, "D": 20.0}
    sectors = {"A": "T", "B": "T", "C": "F", "D": "F"}
    out = _sector_neutralize(scores, sectors)
    # Within each 2-name sector, standardized values are symmetric +/-1.
    assert abs(out["A"] + out["B"]) < 1e-9
    assert abs(out["C"] + out["D"]) < 1e-9
    assert out["B"] > out["A"] and out["D"] > out["C"]


def test_neutralize_kills_pure_size_and_sector_signal() -> None:
    # A score that is purely log(size) should neutralize to ~0 everywhere.
    caps = {"A": 1e8, "B": 1e9, "C": 1e10, "D": 1e11, "E": 1e12}
    scores = {t: math.log(c) for t, c in caps.items()}
    sectors = {"A": "T", "B": "T", "C": "F", "D": "F", "E": "F"}
    out = neutralize(scores, sectors, caps)
    assert all(abs(v) < 1e-6 for v in out.values())


# --------------------------------------------------------------------------- #
# Observation building — PIT / no look-ahead / forward-gap                     #
# --------------------------------------------------------------------------- #
def test_build_observations_no_lookahead_and_forward_window() -> None:
    rows = _series(0.0, n=8)  # datekeys 2010..2017, prices 10..17
    meta = {"T": {"sector": "Tech", "isdelisted": "N"}}
    obs = build_observations({"T": rows}, meta, forward_gap=0)
    # Every observation's forward return is next-filing/this-filing - 1 (report-to-report).
    o = obs[0]
    assert o.sector == "Tech"
    # idx 4 is the first with enough momentum history (>=4 back); forward uses idx5/idx4.
    idx4 = next(x for x in obs if abs(x.momentum - (14.0 / 10.0 - 1.0)) < 1e-9)
    assert abs(idx4.forward - (15.0 / 14.0 - 1.0)) < 1e-9


def test_forward_gap_shifts_return_window_without_touching_signal() -> None:
    rows = _series(0.0, n=8)
    meta = {"T": {"sector": "Tech", "isdelisted": "N"}}
    o0 = build_observations({"T": rows}, meta, forward_gap=0)
    o1 = build_observations({"T": rows}, meta, forward_gap=1)
    # Same signal formation date (bucket) but the gap=1 return is one filing later.
    b0 = {o.bucket: o for o in o0}
    b1 = {o.bucket: o for o in o1}
    shared = set(b0) & set(b1)
    assert shared
    for bucket in shared:
        # Identical momentum (signal unchanged) but different realized forward return.
        assert abs(b0[bucket].momentum - b1[bucket].momentum) < 1e-9
        assert abs(b0[bucket].forward - b1[bucket].forward) > 1e-12


def test_delisted_name_contributes_only_between_filings() -> None:
    # A name that stops filing after 6 rows yields no observation past its last pair.
    rows = _series(0.0, n=6)
    meta = {"D": {"sector": "Energy", "isdelisted": "Y"}}
    obs = build_observations({"D": rows}, meta, forward_gap=0)
    # Last observation's forward uses the final available filing; nothing fabricated after.
    last_buckets = sorted(o.bucket for o in obs)
    assert last_buckets[-1] == quarter_bucket(rows[-2]["datekey"])


# --------------------------------------------------------------------------- #
# Panel assembly + metrics + verdict                                           #
# --------------------------------------------------------------------------- #
def _signal_observations(n_periods: int = 24, n_assets: int = 40) -> list[_Observation]:
    """Panels where the neutralized blended score predicts the forward return."""
    obs: list[_Observation] = []
    sectors = ["Tech", "Energy", "Health", "Financials"]
    for p in range(n_periods):
        for i in range(n_assets):
            strength = float(i)
            fwd = strength * 0.001
            # A couple of adjacent swaps per period -> finite (non-degenerate) IC series.
            if i % 10 == p % 10 and i + 1 < n_assets:
                fwd = (strength + 1) * 0.001
            obs.append(
                _Observation(
                    ticker=f"A{i}",
                    bucket=f"{2000 + p}-Q1",
                    fundamental={f: strength for f in FUND_FACTOR_WEIGHTS},
                    momentum=strength,
                    forward=fwd,
                    market_cap=1e9 * (1 + i),
                    sector=sectors[i % len(sectors)],
                )
            )
    return obs


def test_assemble_periods_respects_min_names() -> None:
    obs = _signal_observations(n_periods=4, n_assets=40)
    periods = assemble_periods(obs, min_names=30)
    assert len(periods) == 4
    for period in periods:
        assert set(period.composite) == set(period.forward)
    # Too-high a threshold drops everything.
    assert assemble_periods(obs, min_names=100) == []


def test_segment_metrics_detects_real_signal() -> None:
    periods = assemble_periods(_signal_observations(), min_names=30)
    m = _segment_metrics("signal", periods)
    assert m.mean_ic is not None and m.mean_ic > 0.0
    assert m.hit_rate is not None and m.hit_rate > 0.55


def test_summarize_pass_on_signal_and_sets_5h_flag() -> None:
    meta = {f"A{i}": {"sector": "Tech", "isdelisted": "N"} for i in range(40)}
    result = summarize(_signal_observations(), meta, min_names=30)
    assert result.out_of_sample.n_periods > 0
    assert result.h5_pass is True
    assert result.oos_verdict == "PASS"
    assert result.line_item_5h_validated is True
    assert result.dimension == "ART"


def test_summarize_empty_is_unavailable_and_fail() -> None:
    result = summarize([], {"AAA": {"sector": "Tech", "isdelisted": "N"}}, min_names=30)
    assert result.status == "unavailable"
    assert result.h5_pass is False
    assert result.oos_verdict == "FAIL"
    assert result.line_item_5h_validated is False
