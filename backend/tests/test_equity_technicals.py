# JHI-SIG: 69M2705M | Deterministic technicals engine tests | JHI Research & Analytics Firm, Inc. (proprietary)
"""Tests for the deterministic equity-technicals engine: weekly aggregation, indicators,
market structure, trade setups, and the options-context framework. All data is
synthetic — no network."""

import datetime as dt
import math

import pytest

from app import equity_technicals as t


def _synthetic_bars(n: int = 400, start: str = "2023-01-02", drift: float = 0.0008) -> list[dict]:
    """A deterministic, weekday-only OHLC series with a mild up-drift + cyclic noise."""
    bars: list[dict] = []
    base = dt.date.fromisoformat(start)
    p = 100.0
    i = 0
    d = base
    while len(bars) < n:
        if d.weekday() < 5:  # trading days only
            p = p * (1 + drift) + 2.0 * math.sin(i / 9.0)
            bars.append(
                {
                    "date": d.isoformat(),
                    "open": p * 0.999,
                    "high": p * 1.01 + abs(math.sin(i)) * 0.5,
                    "low": p * 0.99 - abs(math.cos(i)) * 0.5,
                    "close": p,
                    "volume": 1_000_000 + i,
                }
            )
            i += 1
        d += dt.timedelta(days=1)
    return bars


# ── Weekly aggregation correctness ───────────────────────────────────────────
def test_weekly_aggregation_ohlc_is_correct() -> None:
    # Two ISO weeks: Mon–Wed of week 1, Mon–Tue of week 2 (skip weekends).
    daily = t.to_bars(
        [
            {"date": "2024-01-01", "open": 10, "high": 12, "low": 9, "close": 11, "volume": 100},  # Mon
            {"date": "2024-01-02", "open": 11, "high": 15, "low": 10, "close": 14, "volume": 200},  # Tue
            {"date": "2024-01-03", "open": 14, "high": 14, "low": 8, "close": 9, "volume": 150},   # Wed
            {"date": "2024-01-08", "open": 9, "high": 20, "low": 9, "close": 18, "volume": 300},   # Mon w2
            {"date": "2024-01-09", "open": 18, "high": 19, "low": 16, "close": 17, "volume": 250}, # Tue w2
        ]
    )
    weekly = t.aggregate_weekly(daily)
    assert len(weekly) == 2
    w1, w2 = weekly
    # Week 1: open=first, high=max, low=min, close=last, vol=sum, dated on last day.
    assert (w1.open, w1.high, w1.low, w1.close) == (10, 15, 8, 9)
    assert w1.volume == 450
    assert w1.date == "2024-01-03"
    # Week 2.
    assert (w2.open, w2.high, w2.low, w2.close) == (9, 20, 9, 17)
    assert w2.volume == 550
    assert w2.date == "2024-01-09"


def test_weekly_has_fewer_bars_than_daily() -> None:
    daily = t.to_bars(_synthetic_bars(300))
    weekly = t.aggregate_weekly(daily)
    assert 0 < len(weekly) < len(daily)
    # A weekly high is never below the max daily high within its span (sanity).
    assert max(b.high for b in weekly) == pytest.approx(max(b.high for b in daily))


def test_aggregate_weekly_empty() -> None:
    assert t.aggregate_weekly([]) == []


# ── Indicators ───────────────────────────────────────────────────────────────
def test_sma_and_ema_basic() -> None:
    vals = [float(x) for x in range(1, 11)]  # 1..10
    assert t.sma(vals, 5) == pytest.approx(8.0)  # mean of 6..10
    assert t.sma(vals, 20) is None  # not enough data
    ema = t.ema(vals, 5)
    assert ema is not None and 6.0 < ema < 10.0


def test_rsi_all_gains_is_100() -> None:
    vals = [float(x) for x in range(1, 40)]  # strictly increasing
    assert t.rsi(vals) == pytest.approx(100.0)


def test_rsi_bounds() -> None:
    vals = _synthetic_close_series()
    r = t.rsi(vals)
    assert r is not None and 0.0 <= r <= 100.0


def test_macd_shape() -> None:
    vals = _synthetic_close_series()
    m = t.macd(vals)
    assert m is not None
    macd_line, signal, hist = m
    assert hist == pytest.approx(macd_line - signal)


def test_atr_positive() -> None:
    bars = t.to_bars(_synthetic_bars(120))
    a = t.atr(bars)
    assert a is not None and a > 0


def test_realized_vol_positive() -> None:
    vals = _synthetic_close_series()
    v = t.realized_volatility(vals)
    assert v is not None and v > 0


def _synthetic_close_series() -> list[float]:
    return [b.close for b in t.to_bars(_synthetic_bars(200))]


# ── Structure + full read ────────────────────────────────────────────────────
def test_uptrend_structure_detected() -> None:
    bars = _synthetic_bars(300, drift=0.002)  # strong up-drift
    read = t.compute_technicals(bars, "UP", "Daily")
    assert read.trend == "Uptrend"
    assert read.range_high >= read.price >= 0
    assert read.range_low <= read.range_high
    assert read.sma20 is not None


def test_downtrend_structure_detected() -> None:
    bars = _synthetic_bars(300, drift=-0.002)  # down-drift
    read = t.compute_technicals(bars, "DN", "Daily")
    assert read.trend in ("Downtrend", "Range / transition")


def test_compute_requires_two_bars() -> None:
    with pytest.raises(ValueError):
        t.compute_technicals([{"date": "2024-01-01", "open": 1, "high": 1, "low": 1, "close": 1}], "X")


def test_daily_and_weekly_both_build_and_have_setups() -> None:
    bars = _synthetic_bars(400, drift=0.0015)
    db = t.to_bars(bars)
    daily = t.compute_technicals(db, "SYN", "Daily", window=252)
    weekly = t.compute_technicals(t.aggregate_weekly(db), "SYN", "Weekly", window=52)
    assert daily.timeframe == "Daily" and weekly.timeframe == "Weekly"
    assert daily.setups and weekly.setups
    # Every populated setup with a defined trigger/stop has a coherent R:R.
    for s in daily.setups + weekly.setups:
        if s.trigger is not None and s.stop is not None and s.risk_reward is not None:
            assert s.risk_reward > 0
    # Weekly setups are labeled as position/swing style.
    assert any("Position" in s.style or "Swing" in s.style for s in weekly.setups)


def test_setup_levels_are_derived_from_computed_levels() -> None:
    bars = _synthetic_bars(300, drift=0.0015)
    read = t.compute_technicals(bars, "SYN", "Daily")
    long_setups = [s for s in read.setups if s.bias == "Long" and s.trigger is not None]
    if long_setups:
        s = long_setups[0]
        # Long setup: stop below trigger, target above trigger (coherent geometry).
        assert s.stop is not None and s.stop < s.trigger
        if s.target is not None:
            assert s.target > s.trigger


# ── Options context ──────────────────────────────────────────────────────────
def test_options_context_expected_move_scales_with_horizon() -> None:
    bars = _synthetic_bars(300, drift=0.0015)
    db = t.to_bars(bars)
    daily = t.compute_technicals(db, "SYN", "Daily")
    weekly = t.compute_technicals(t.aggregate_weekly(db), "SYN", "Weekly", window=52)
    oc = t.options_context(daily, weekly)
    assert oc.expected_move_1w is not None and oc.expected_move_1m is not None
    # 1-month move (√21) is larger than 1-week move (√5).
    assert oc.expected_move_1m > oc.expected_move_1w
    assert oc.vol_regime in ("Elevated", "Moderate", "Subdued", "Unknown")
    assert oc.strategies  # at least one archetype
    assert any("not a recommendation" in n.lower() for n in oc.notes)
