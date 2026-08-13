# JHI-SIG: 69M2705M | Deterministic equity technicals engine | JHI Research & Analytics Firm, Inc. (proprietary)
"""Deterministic, reproducible technical-analysis engine for a single equity.

Given a series of OHLC bars it computes — with **no randomness and no fabricated
numbers** — the market-structure and momentum read an institutional desk expects:

  * Trend structure via swing pivots — higher-highs / higher-lows (HH/HL),
    lower-highs / lower-lows (LH/LL), plus **BOS** (break of structure, trend
    continuation) and **CHoCH** (change of character, first counter-trend break).
  * Moving averages — SMA & EMA (20 / 50 / 200 and the 12 / 26 MACD pair).
  * Momentum — RSI(14), MACD(12,26,9).
  * Volatility — ATR(14) and realized/annualized return volatility.
  * Support / resistance from recent swing highs / lows.
  * 52-week (window) high / low and position within the range.
  * A **trade-setup** block (trigger, invalidation/stop, measured target, R:R)
    derived STRICTLY from the computed levels — never a forecast.

The engine runs on any timeframe: pass daily bars for the daily read, or aggregate
daily→weekly with :func:`aggregate_weekly` for the higher-timeframe read. All inputs
are the OHLC bars fetched from the shared Yahoo chart adapter (no new vendor).

Research and educational output — not investment advice.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import date, datetime

# ── Bar model ────────────────────────────────────────────────────────────────


@dataclass
class Bar:
    """One OHLC(V) candle. ``date`` is an ISO ``YYYY-MM-DD`` string."""

    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0


def _to_bar(row: dict | Bar) -> Bar:
    if isinstance(row, Bar):
        return row
    return Bar(
        date=str(row.get("date") or ""),
        open=float(row["open"]),
        high=float(row["high"]),
        low=float(row["low"]),
        close=float(row["close"]),
        volume=float(row.get("volume") or 0.0),
    )


def to_bars(rows: list[dict | Bar]) -> list[Bar]:
    """Normalize raw OHLC dicts (e.g. from ``market_services.yahoo_chart_ohlc``) to Bars,
    sorted oldest→newest by date."""
    bars = [_to_bar(r) for r in rows]
    bars.sort(key=lambda b: b.date)
    return bars


# ── Weekly aggregation ───────────────────────────────────────────────────────


def _iso_week_key(iso_date: str) -> tuple[int, int]:
    """(ISO-year, ISO-week) for an ``YYYY-MM-DD`` string. Groups trading days into the
    calendar week they belong to (Mon–Sun), which is the desk convention for weekly
    candles."""
    d = date.fromisoformat(iso_date)
    iso = d.isocalendar()
    return (iso[0], iso[1])


def aggregate_weekly(daily: list[Bar]) -> list[Bar]:
    """Aggregate daily bars into weekly OHLC bars (deterministic).

    Within each ISO week: open = first day's open, high = max high, low = min low,
    close = last day's close, volume = sum. The weekly bar is dated on its last
    trading day so the series stays chronologically comparable to the daily read.
    """
    if not daily:
        return []
    ordered = sorted(daily, key=lambda b: b.date)
    groups: dict[tuple[int, int], list[Bar]] = {}
    order: list[tuple[int, int]] = []
    for b in ordered:
        if not b.date:
            continue
        key = _iso_week_key(b.date)
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(b)
    weekly: list[Bar] = []
    for key in order:
        wk = groups[key]
        weekly.append(
            Bar(
                date=wk[-1].date,
                open=wk[0].open,
                high=max(b.high for b in wk),
                low=min(b.low for b in wk),
                close=wk[-1].close,
                volume=sum(b.volume for b in wk),
            )
        )
    return weekly


# ── Indicators (pure Python, deterministic) ──────────────────────────────────


def sma(values: list[float], period: int) -> float | None:
    if period <= 0 or len(values) < period:
        return None
    return sum(values[-period:]) / period


def ema_series(values: list[float], period: int) -> list[float]:
    """Full EMA series (same length as trailing window). Seeded with the SMA of the
    first ``period`` values — the standard, reproducible seed."""
    if period <= 0 or len(values) < period:
        return []
    k = 2.0 / (period + 1.0)
    seed = sum(values[:period]) / period
    out = [seed]
    for v in values[period:]:
        out.append(v * k + out[-1] * (1.0 - k))
    return out


def ema(values: list[float], period: int) -> float | None:
    series = ema_series(values, period)
    return series[-1] if series else None


def rsi(values: list[float], period: int = 14) -> float | None:
    """Wilder's RSI. Returns None until there are enough bars."""
    if len(values) < period + 1:
        return None
    gains = 0.0
    losses = 0.0
    for i in range(1, period + 1):
        change = values[i] - values[i - 1]
        if change >= 0:
            gains += change
        else:
            losses -= change
    avg_gain = gains / period
    avg_loss = losses / period
    for i in range(period + 1, len(values)):
        change = values[i] - values[i - 1]
        gain = change if change > 0 else 0.0
        loss = -change if change < 0 else 0.0
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


def macd(
    values: list[float], fast: int = 12, slow: int = 26, signal: int = 9
) -> tuple[float, float, float] | None:
    """MACD line, signal line, histogram (deterministic). None until enough bars."""
    if len(values) < slow + signal:
        return None
    fast_series = ema_series(values, fast)
    slow_series = ema_series(values, slow)
    # Align the two EMA series on their common tail (slow starts later).
    offset = (slow - fast)
    fast_aligned = fast_series[offset:]
    n = min(len(fast_aligned), len(slow_series))
    macd_line = [fast_aligned[-n + i] - slow_series[-n + i] for i in range(n)]
    if len(macd_line) < signal:
        return None
    signal_series = ema_series(macd_line, signal)
    if not signal_series:
        return None
    macd_val = macd_line[-1]
    signal_val = signal_series[-1]
    return (macd_val, signal_val, macd_val - signal_val)


def atr(bars: list[Bar], period: int = 14) -> float | None:
    """Average True Range (Wilder). None until there are enough bars."""
    if len(bars) < period + 1:
        return None
    trs: list[float] = []
    for i in range(1, len(bars)):
        h, low_ = bars[i].high, bars[i].low
        prev_close = bars[i - 1].close
        trs.append(max(h - low_, abs(h - prev_close), abs(low_ - prev_close)))
    atr_val = sum(trs[:period]) / period
    for tr in trs[period:]:
        atr_val = (atr_val * (period - 1) + tr) / period
    return atr_val


def realized_volatility(closes: list[float], annualization: int = 252) -> float | None:
    """Annualized realized volatility from daily log returns (population stdev)."""
    if len(closes) < 3:
        return None
    rets = [
        math.log(closes[i] / closes[i - 1])
        for i in range(1, len(closes))
        if closes[i - 1] > 0 and closes[i] > 0
    ]
    if len(rets) < 2:
        return None
    mean = sum(rets) / len(rets)
    var = sum((r - mean) ** 2 for r in rets) / len(rets)
    return math.sqrt(var) * math.sqrt(annualization)


# ── Swing structure (HH/HL/LH/LL, BOS/CHoCH) ─────────────────────────────────


@dataclass
class SwingPoint:
    index: int
    date: str
    price: float
    kind: str  # "high" | "low"


def swing_points(bars: list[Bar], left: int = 2, right: int = 2) -> list[SwingPoint]:
    """Fractal swing pivots: a swing high is a bar whose high is >= the ``left`` bars
    before and > the ``right`` bars after (strict on the right to avoid duplicate
    plateaus); mirror for swing lows. Deterministic and order-preserving."""
    points: list[SwingPoint] = []
    n = len(bars)
    for i in range(left, n - right):
        hi = bars[i].high
        lo = bars[i].low
        is_high = all(bars[j].high <= hi for j in range(i - left, i)) and all(
            bars[j].high < hi for j in range(i + 1, i + right + 1)
        )
        is_low = all(bars[j].low >= lo for j in range(i - left, i)) and all(
            bars[j].low > lo for j in range(i + 1, i + right + 1)
        )
        if is_high:
            points.append(SwingPoint(index=i, date=bars[i].date, price=hi, kind="high"))
        if is_low:
            points.append(SwingPoint(index=i, date=bars[i].date, price=lo, kind="low"))
    points.sort(key=lambda p: p.index)
    return points


@dataclass
class StructureRead:
    trend: str  # "Uptrend" | "Downtrend" | "Range / transition"
    sequence: str  # e.g. "HH-HL-HH" (last few swings)
    last_event: str  # "BOS (bullish)" | "CHoCH (bearish)" | "None (in range)" ...
    last_event_date: str | None
    recent_swings: list[SwingPoint] = field(default_factory=list)


def _classify_structure(points: list[SwingPoint]) -> StructureRead:
    highs = [p for p in points if p.kind == "high"]
    lows = [p for p in points if p.kind == "low"]
    labels: list[str] = []
    for i in range(1, len(highs)):
        labels.append("HH" if highs[i].price > highs[i - 1].price else "LH")
    for i in range(1, len(lows)):
        labels.append("LL" if lows[i].price < lows[i - 1].price else "HL")

    # Trend from the most recent high/low progression.
    hh = len(highs) >= 2 and highs[-1].price > highs[-2].price
    hl = len(lows) >= 2 and lows[-1].price > lows[-2].price
    lh = len(highs) >= 2 and highs[-1].price < highs[-2].price
    ll = len(lows) >= 2 and lows[-1].price < lows[-2].price
    if hh and hl:
        trend = "Uptrend"
    elif lh and ll:
        trend = "Downtrend"
    else:
        trend = "Range / transition"

    # BOS / CHoCH from the ordered swing-high / swing-low breaks.
    last_event = "None (insufficient structure)"
    last_event_date: str | None = None
    prev_trend: str | None = None
    for i in range(2, len(points)):
        window = points[: i + 1]
        w_highs = [p for p in window if p.kind == "high"]
        w_lows = [p for p in window if p.kind == "low"]
        up = (
            len(w_highs) >= 2
            and len(w_lows) >= 2
            and w_highs[-1].price > w_highs[-2].price
            and w_lows[-1].price > w_lows[-2].price
        )
        down = (
            len(w_highs) >= 2
            and len(w_lows) >= 2
            and w_highs[-1].price < w_highs[-2].price
            and w_lows[-1].price < w_lows[-2].price
        )
        cur = "Uptrend" if up else "Downtrend" if down else None
        if cur is None:
            continue
        pt = points[i]
        if prev_trend is None:
            prev_trend = cur
            continue
        if cur == prev_trend:
            last_event = f"BOS ({'bullish' if cur == 'Uptrend' else 'bearish'})"
            last_event_date = pt.date
        else:
            last_event = f"CHoCH ({'bullish' if cur == 'Uptrend' else 'bearish'})"
            last_event_date = pt.date
        prev_trend = cur

    seq = "-".join(labels[-4:]) if labels else "n/a"
    recent = points[-6:]
    return StructureRead(
        trend=trend,
        sequence=seq,
        last_event=last_event,
        last_event_date=last_event_date,
        recent_swings=recent,
    )


def support_resistance(
    bars: list[Bar], points: list[SwingPoint], max_levels: int = 3
) -> tuple[list[float], list[float]]:
    """Nearest support (below) & resistance (above) from recent swing lows / highs.

    Uses the most recent close as the reference; returns up to ``max_levels`` of each,
    sorted by proximity to price."""
    if not bars:
        return [], []
    price = bars[-1].close
    highs = sorted({round(p.price, 4) for p in points if p.kind == "high" and p.price > price})
    lows = sorted(
        {round(p.price, 4) for p in points if p.kind == "low" and p.price < price}, reverse=True
    )
    return lows[:max_levels], highs[:max_levels]


# ── Full technical read + trade setup ────────────────────────────────────────


@dataclass
class TradeSetup:
    bias: str  # "Long" | "Short" | "Neutral / wait"
    style: str  # "Swing", "Day/intraday", "Position/swing"
    trigger: float | None
    stop: float | None
    target: float | None
    risk_reward: float | None
    rationale: str


@dataclass
class TechnicalsRead:
    ticker: str
    timeframe: str  # "Daily" | "Weekly"
    as_of: str
    bars_used: int
    price: float
    # Indicators
    sma20: float | None
    sma50: float | None
    sma200: float | None
    ema12: float | None
    ema26: float | None
    ema20: float | None
    ema50: float | None
    ema200: float | None
    rsi14: float | None
    macd_line: float | None
    macd_signal: float | None
    macd_hist: float | None
    atr14: float | None
    atr_pct: float | None
    realized_vol: float | None
    # Structure
    trend: str
    structure_sequence: str
    last_structure_event: str
    last_structure_event_date: str | None
    supports: list[float]
    resistances: list[float]
    range_high: float
    range_low: float
    range_position_pct: float | None  # where price sits in the window range (0–100%)
    # Trade setups
    setups: list[TradeSetup] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def _range_position(price: float, lo: float, hi: float) -> float | None:
    if hi <= lo:
        return None
    return max(0.0, min(1.0, (price - lo) / (hi - lo))) * 100.0


def _ma_alignment_note(read: TechnicalsRead) -> str:
    if read.sma50 is None or read.sma200 is None:
        return "Insufficient history for the 50/200 moving-average regime."
    regime = "bullish (50 > 200 — golden-cross regime)" if read.sma50 > read.sma200 else (
        "bearish (50 < 200 — death-cross regime)"
    )
    loc = "above" if read.price >= (read.sma50 or read.price) else "below"
    return f"Price {loc} the 50-SMA; long-term regime {regime}."


def _build_setups(read: TechnicalsRead, bars: list[Bar]) -> list[TradeSetup]:
    setups: list[TradeSetup] = []
    price = read.price
    atr_val = read.atr14
    nearest_res = read.resistances[0] if read.resistances else None
    nearest_sup = read.supports[0] if read.supports else None
    bull = read.trend == "Uptrend" or (read.sma50 and read.sma200 and read.sma50 > read.sma200)
    bear = read.trend == "Downtrend" or (read.sma50 and read.sma200 and read.sma50 < read.sma200)

    swing_style = "Position/swing" if read.timeframe == "Weekly" else "Swing"

    # Primary trend-aligned setup.
    if bull and atr_val:
        trigger = round(nearest_res, 2) if nearest_res else round(price + 0.25 * atr_val, 2)
        stop = round((nearest_sup if nearest_sup else price - 1.5 * atr_val), 2)
        # Measured target: prior swing range projected, or 2R, whichever is defined.
        risk = trigger - stop
        target = round(trigger + max(2.0 * risk, 1.0 * atr_val * 3), 2) if risk > 0 else None
        rr = round((target - trigger) / risk, 2) if (target and risk > 0) else None
        setups.append(
            TradeSetup(
                bias="Long",
                style=swing_style,
                trigger=trigger,
                stop=stop,
                target=target,
                risk_reward=rr,
                rationale=(
                    f"Trend is up ({read.structure_sequence}); a break/hold above "
                    f"{trigger} targets a measured move with invalidation below the recent "
                    f"swing/ATR stop at {stop}."
                ),
            )
        )
    elif bear and atr_val:
        trigger = round(nearest_sup, 2) if nearest_sup else round(price - 0.25 * atr_val, 2)
        stop = round((nearest_res if nearest_res else price + 1.5 * atr_val), 2)
        risk = stop - trigger
        target = round(trigger - max(2.0 * risk, 1.0 * atr_val * 3), 2) if risk > 0 else None
        rr = round((trigger - target) / risk, 2) if (target and risk > 0) else None
        setups.append(
            TradeSetup(
                bias="Short",
                style=swing_style,
                trigger=trigger,
                stop=stop,
                target=target,
                risk_reward=rr,
                rationale=(
                    f"Trend is down ({read.structure_sequence}); a break below {trigger} "
                    f"targets a measured move with invalidation above the recent swing/ATR "
                    f"stop at {stop}."
                ),
            )
        )
    else:
        setups.append(
            TradeSetup(
                bias="Neutral / wait",
                style=swing_style,
                trigger=None,
                stop=None,
                target=None,
                risk_reward=None,
                rationale=(
                    "Structure is a range / transition — no trend-aligned edge. Wait for a "
                    "BOS/CHoCH to define direction; fade the range extremes only with a plan."
                ),
            )
        )

    # Daily-only intraday/mean-reversion overlay from RSI + ATR.
    if read.timeframe == "Daily" and read.rsi14 is not None and atr_val:
        if read.rsi14 <= 35 and nearest_sup:
            trigger = round(nearest_sup, 2)
            stop = round(nearest_sup - 1.0 * atr_val, 2)
            target = round(price + 1.5 * atr_val, 2)
            risk = trigger - stop
            rr = round((target - trigger) / risk, 2) if risk > 0 else None
            setups.append(
                TradeSetup(
                    bias="Long",
                    style="Day/intraday (mean-reversion)",
                    trigger=trigger,
                    stop=stop,
                    target=target,
                    risk_reward=rr,
                    rationale=(
                        f"RSI {read.rsi14:.0f} (oversold) into support {trigger}: a reclaim "
                        f"offers an intraday bounce, one ATR stop, +1.5 ATR target."
                    ),
                )
            )
        elif read.rsi14 >= 65 and nearest_res:
            trigger = round(nearest_res, 2)
            stop = round(nearest_res + 1.0 * atr_val, 2)
            target = round(price - 1.5 * atr_val, 2)
            risk = stop - trigger
            rr = round((trigger - target) / risk, 2) if risk > 0 else None
            setups.append(
                TradeSetup(
                    bias="Short",
                    style="Day/intraday (mean-reversion)",
                    trigger=trigger,
                    stop=stop,
                    target=target,
                    risk_reward=rr,
                    rationale=(
                        f"RSI {read.rsi14:.0f} (overbought) into resistance {trigger}: a "
                        f"rejection offers an intraday fade, one ATR stop, −1.5 ATR target."
                    ),
                )
            )
    return setups


@dataclass
class OptionsContext:
    """Deterministic, options-oriented framework derived from what we can compute —
    NO fabricated option-chain numbers. It surfaces realized/annualized volatility, an
    ATR-based expected move, a directional bias from structure, and clearly-labeled
    strategy archetypes given the trend+vol regime."""

    as_of: str
    price: float
    annualized_vol: float | None
    daily_atr_pct: float | None
    expected_move_1w: float | None  # +/- dollar move over ~5 trading days (ATR-based)
    expected_move_1m: float | None  # +/- dollar move over ~21 trading days (ATR-based)
    expected_move_1w_pct: float | None
    expected_move_1m_pct: float | None
    directional_bias: str
    vol_regime: str  # "Elevated" | "Moderate" | "Subdued"
    strategies: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def options_context(daily: TechnicalsRead, weekly: TechnicalsRead | None = None) -> OptionsContext:
    """Build the deterministic options framework from the daily (and optional weekly) read."""
    price = daily.price
    atr_val = daily.atr14
    vol = daily.realized_vol
    # ATR-based expected move: ATR × sqrt(horizon) is the desk shortcut for a ~1σ range.
    em_1w = (atr_val * math.sqrt(5)) if atr_val else None
    em_1m = (atr_val * math.sqrt(21)) if atr_val else None

    if vol is None:
        vol_regime = "Unknown"
    elif vol >= 0.45:
        vol_regime = "Elevated"
    elif vol >= 0.25:
        vol_regime = "Moderate"
    else:
        vol_regime = "Subdued"

    htf = weekly.trend if weekly else "n/a"
    if daily.trend == "Uptrend":
        bias = "Bullish"
    elif daily.trend == "Downtrend":
        bias = "Bearish"
    else:
        bias = "Neutral / range"

    strategies: list[str] = []
    if bias == "Bullish":
        strategies.append(
            "Directional up + elevated vol → bull call (debit) spread caps premium paid vs. a "
            "long call."
            if vol_regime == "Elevated"
            else "Directional up + subdued/moderate vol → long call or bull call spread; roll on "
            "trend continuation (BOS)."
        )
        strategies.append(
            "Income overlay on holdings → covered call above resistance / cash-secured put at "
            "support."
        )
    elif bias == "Bearish":
        strategies.append(
            "Directional down + elevated vol → bear put (debit) spread limits premium vs. a long "
            "put."
            if vol_regime == "Elevated"
            else "Directional down + subdued/moderate vol → long put or bear put spread below the "
            "broken structure."
        )
        strategies.append("Hedge overlay → protective put / collar against long exposure.")
    else:
        strategies.append(
            "Range + elevated vol → premium-selling archetypes (iron condor / short strangle) "
            "between S/R — defined-risk only."
            if vol_regime in ("Elevated", "Moderate")
            else "Range + subdued vol → wait for a volatility expansion or a structure break "
            "before committing premium."
        )

    notes = [
        "IV proxy: we do not consume a live option chain, so implied vol is proxied by "
        "annualized realized vol; treat the expected move as a realized-vol range, not an "
        "IV-implied one.",
        "Expected move = ATR × √(trading days) — a ~1σ range shortcut from realized volatility.",
        "Strategy archetypes are an educational FRAMEWORK matched to trend + vol regime — NOT a "
        "recommendation and NOT sized. Research, not investment advice.",
    ]
    return OptionsContext(
        as_of=daily.as_of,
        price=price,
        annualized_vol=vol,
        daily_atr_pct=daily.atr_pct,
        expected_move_1w=em_1w,
        expected_move_1m=em_1m,
        expected_move_1w_pct=(em_1w / price) if (em_1w and price) else None,
        expected_move_1m_pct=(em_1m / price) if (em_1m and price) else None,
        directional_bias=f"{bias} (daily) · higher-timeframe {htf}",
        vol_regime=vol_regime,
        strategies=strategies,
        notes=notes,
    )


def compute_technicals(
    rows: list[dict | Bar], ticker: str, timeframe: str = "Daily", window: int = 252
) -> TechnicalsRead:
    """Compute the full deterministic technical read on the supplied OHLC bars.

    ``window`` bounds the 52-week (or higher-timeframe) range lookback used for the
    range-high/low and support/resistance context. Indicators use the full series.
    """
    bars = to_bars(rows)
    if len(bars) < 2:
        raise ValueError(f"{ticker}: need at least 2 bars for a technical read (got {len(bars)}).")
    closes = [b.close for b in bars]
    price = closes[-1]

    points = swing_points(bars)
    structure = _classify_structure(points)
    supports, resistances = support_resistance(bars, points)

    win = bars[-window:] if len(bars) > window else bars
    range_high = max(b.high for b in win)
    range_low = min(b.low for b in win)

    atr14 = atr(bars)
    macd_vals = macd(closes)

    read = TechnicalsRead(
        ticker=ticker.upper(),
        timeframe=timeframe,
        as_of=bars[-1].date or datetime.utcnow().strftime("%Y-%m-%d"),
        bars_used=len(bars),
        price=price,
        sma20=sma(closes, 20),
        sma50=sma(closes, 50),
        sma200=sma(closes, 200),
        ema12=ema(closes, 12),
        ema26=ema(closes, 26),
        ema20=ema(closes, 20),
        ema50=ema(closes, 50),
        ema200=ema(closes, 200),
        rsi14=rsi(closes),
        macd_line=macd_vals[0] if macd_vals else None,
        macd_signal=macd_vals[1] if macd_vals else None,
        macd_hist=macd_vals[2] if macd_vals else None,
        atr14=atr14,
        atr_pct=(atr14 / price) if (atr14 and price) else None,
        realized_vol=realized_volatility(closes) if timeframe == "Daily" else realized_volatility(
            closes, annualization=52
        ),
        trend=structure.trend,
        structure_sequence=structure.sequence,
        last_structure_event=structure.last_event,
        last_structure_event_date=structure.last_event_date,
        supports=supports,
        resistances=resistances,
        range_high=range_high,
        range_low=range_low,
        range_position_pct=_range_position(price, range_low, range_high),
    )
    read.setups = _build_setups(read, bars)
    read.notes = [
        _ma_alignment_note(read),
        (
            f"Momentum: RSI {read.rsi14:.0f}" if read.rsi14 is not None else "RSI: n/a"
        )
        + (
            f", MACD {'bullish' if read.macd_hist and read.macd_hist > 0 else 'bearish'}"
            f" (hist {read.macd_hist:+.3f})"
            if read.macd_hist is not None
            else ", MACD: n/a"
        ),
        (
            f"Volatility: ATR {read.atr_pct * 100:.1f}% of price"
            if read.atr_pct is not None
            else "Volatility: ATR n/a"
        )
        + (
            f"; annualized realized vol {read.realized_vol * 100:.0f}%"
            if read.realized_vol is not None
            else ""
        ),
        "Deterministic market-structure read. Research, not investment advice.",
    ]
    return read
