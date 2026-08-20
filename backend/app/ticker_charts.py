# JHI-SIG: 69M2705M | Per-ticker technical chart layer (server-rendered PNG) | JHI Research & Analytics Firm, Inc. (proprietary)
"""Deterministic, print-friendly VISUAL technical charts for the institutional
per-ticker Excel workbook.

This is the *visual* companion to the numeric technicals engine
(:mod:`app.equity_technicals`). Given the OHLC bars the workbook already fetched
(no new vendor, no new key) and the computed :class:`~app.equity_technicals.TechnicalsRead`,
it renders a multi-panel, Aegira-palette PNG with matplotlib's headless Agg backend:

  * Price panel   — candlesticks + SMA 20/50/200 + EMA 12/26 overlays, support /
                    resistance lines, the 52-week (window) high/low, and annotated
                    swing structure (HH/HL/LH/LL) plus the last BOS/CHoCH event.
  * Volume panel  — per-bar volume, up/down coloured.
  * RSI panel     — RSI(14) with the 30 / 70 bands.
  * MACD panel    — MACD(12,26,9) line + signal + histogram.

Governance / Data Foundation doctrine: nothing here fabricates data. Every line is
drawn from the supplied bars or the derived figures the engine already computed. If
OHLC is unavailable (empty / too-short series) the renderer returns ``None`` so the
caller keeps the existing numeric table untouched — never a fabricated picture.

The output is raw PNG *bytes* (not a data URI) so ``openpyxl`` can embed it via
``openpyxl.drawing.image.Image`` — the reliability anchor that renders identically in
both Microsoft Excel and Apple Numbers.
"""

from __future__ import annotations

import io

import matplotlib

matplotlib.use("Agg")  # headless: no display, deterministic raster output

import matplotlib.pyplot as plt  # noqa: E402  (must follow the Agg backend selection)
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.gridspec import GridSpec  # noqa: E402

from app import equity_technicals  # noqa: E402
from app.equity_technicals import Bar, TechnicalsRead  # noqa: E402
from app.price_format import format_price  # noqa: E402

# ── Aegira palette (navy / gold), tuned for print on white ────────────────────
NAVY = "#0C1F33"
NAVY_SOFT = "#3A5A7A"
GOLD = "#9A6B12"
GOLD_SOFT = "#C7A867"
INK = "#0C1F33"
MUTED = "#5A6B7D"
GRID = "#D5DEE8"
PAPER = "#FFFFFF"
UP = "#0C1F33"  # up candle / positive: navy
DOWN = "#9A6B12"  # down candle / negative: gold

_FONT = "DejaVu Serif"  # bundled with matplotlib → deterministic across machines

# How many trailing bars to draw so candlesticks stay legible (indicators still use
# the full history — only the *plot window* is trimmed).
_DAILY_WINDOW = 200
_WEEKLY_WINDOW = 120


# ── Rolling indicator series (deterministic, aligned to bar index) ────────────
def _sma_series(values: list[float], period: int) -> list[float | None]:
    out: list[float | None] = [None] * len(values)
    if period <= 0 or len(values) < period:
        return out
    running = sum(values[:period])
    out[period - 1] = running / period
    for i in range(period, len(values)):
        running += values[i] - values[i - period]
        out[i] = running / period
    return out


def _ema_series_aligned(values: list[float], period: int) -> list[float | None]:
    """EMA aligned to the full series (None during the seed warm-up), reusing the
    engine's standard SMA-seeded EMA so the plotted overlay matches the numbers."""
    out: list[float | None] = [None] * len(values)
    series = equity_technicals.ema_series(values, period)
    for i, v in enumerate(series):
        out[period - 1 + i] = v
    return out


def _rsi_series(values: list[float], period: int = 14) -> list[float | None]:
    out: list[float | None] = [None] * len(values)
    if len(values) < period + 1:
        return out
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
    out[period] = 100.0 if avg_loss == 0 else 100.0 - (100.0 / (1.0 + avg_gain / avg_loss))
    for i in range(period + 1, len(values)):
        change = values[i] - values[i - 1]
        gain = change if change > 0 else 0.0
        loss = -change if change < 0 else 0.0
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
        out[i] = 100.0 if avg_loss == 0 else 100.0 - (100.0 / (1.0 + avg_gain / avg_loss))
    return out


def _macd_series(
    values: list[float], fast: int = 12, slow: int = 26, signal: int = 9
) -> tuple[list[float | None], list[float | None], list[float | None]]:
    n = len(values)
    macd_line: list[float | None] = [None] * n
    signal_line: list[float | None] = [None] * n
    hist: list[float | None] = [None] * n
    fast_s = _ema_series_aligned(values, fast)
    slow_s = _ema_series_aligned(values, slow)
    valid_vals: list[float] = []
    valid_idx: list[int] = []
    for i in range(n):
        if fast_s[i] is not None and slow_s[i] is not None:
            m = fast_s[i] - slow_s[i]  # type: ignore[operator]
            macd_line[i] = m
            valid_vals.append(m)
            valid_idx.append(i)
    sig_series = equity_technicals.ema_series(valid_vals, signal)
    for k, v in enumerate(sig_series):
        i = valid_idx[signal - 1 + k]
        signal_line[i] = v
        hist[i] = macd_line[i] - v  # type: ignore[operator]
    return macd_line, signal_line, hist


# ── Swing-structure labels (HH/HL/LH/LL) for annotation ──────────────────────
def _labelled_swings(bars: list[Bar]) -> list[tuple[int, float, str, str]]:
    """Return (bar_index, price, kind, label) for each swing pivot, where label is
    HH/LH for highs and HL/LL for lows (relative to the prior same-kind pivot)."""
    points = equity_technicals.swing_points(bars)
    highs = [p for p in points if p.kind == "high"]
    lows = [p for p in points if p.kind == "low"]
    out: list[tuple[int, float, str, str]] = []
    for i, p in enumerate(highs):
        label = "HH" if i > 0 and p.price > highs[i - 1].price else ("LH" if i > 0 else "H")
        out.append((p.index, p.price, "high", label))
    for i, p in enumerate(lows):
        label = "LL" if i > 0 and p.price < lows[i - 1].price else ("HL" if i > 0 else "L")
        out.append((p.index, p.price, "low", label))
    out.sort(key=lambda t: t[0])
    return out


def _style_axis(ax) -> None:
    ax.set_facecolor(PAPER)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.title.set_color(INK)


def _to_png(fig: Figure) -> bytes:
    """Serialize a figure to deterministic PNG bytes, then close it."""
    buf = io.BytesIO()
    # metadata strips the timestamp PNG chunk so identical inputs → identical bytes.
    fig.savefig(buf, format="png", dpi=120, facecolor=PAPER, metadata={"Software": "Aegira"})
    plt.close(fig)
    return buf.getvalue()


def _window(bars: list[Bar], timeframe_label: str) -> int:
    n = _WEEKLY_WINDOW if timeframe_label.lower().startswith("week") else _DAILY_WINDOW
    return min(len(bars), n)


def _draw_candles(ax, bars: list[Bar], offset: int) -> None:
    for i in range(offset, len(bars)):
        b = bars[i]
        x = i - offset
        color = UP if b.close >= b.open else DOWN
        ax.vlines(x, b.low, b.high, color=color, linewidth=0.7, zorder=3)
        lo = min(b.open, b.close)
        hi = max(b.open, b.close)
        ax.add_line(
            plt.Line2D(
                [x, x], [lo, hi], color=color, linewidth=2.4, solid_capstyle="butt", zorder=4
            )
        )


def _plot_overlay(ax, series: list[float | None], offset: int, color: str, label: str,
                  lw: float = 1.2) -> None:
    xs = [i - offset for i in range(offset, len(series)) if series[i] is not None]
    ys = [series[i] for i in range(offset, len(series)) if series[i] is not None]
    if xs:
        ax.plot(xs, ys, color=color, linewidth=lw, label=label, zorder=5)


def price_technical_chart(
    bars: list[Bar] | list[dict],
    timeframe_label: str,
    technicals: TechnicalsRead | None = None,
    *,
    thumbnail: bool = False,
) -> bytes | None:
    """Render the multi-panel technical chart for one timeframe to PNG bytes.

    Returns ``None`` (graceful degradation) when there are too few bars to draw a
    meaningful chart — the caller then leaves the existing numeric table in place.

    ``thumbnail=True`` renders a compact single-panel price snapshot (used on the
    Cover & Summary sheet).
    """
    bars = equity_technicals.to_bars(bars)
    if len(bars) < 5:
        return None

    closes = [b.close for b in bars]
    offset = len(bars) - _window(bars, timeframe_label)
    n_plot = len(bars) - offset

    sma20 = _sma_series(closes, 20)
    sma50 = _sma_series(closes, 50)
    sma200 = _sma_series(closes, 200)
    ema12 = _ema_series_aligned(closes, 12)
    ema26 = _ema_series_aligned(closes, 26)

    as_of = bars[-1].date or ""
    dates = [b.date for b in bars]

    def _date_ticks(ax) -> None:
        step = max(1, n_plot // 6)
        ticks = list(range(0, n_plot, step))
        ax.set_xticks(ticks)
        ax.set_xticklabels([dates[offset + t][2:] for t in ticks], fontsize=7, color=MUTED,
                           fontfamily=_FONT)
        ax.set_xlim(-1, n_plot)

    # ── Thumbnail: single compact price panel with the trend MAs ──────────────
    if thumbnail:
        fig = Figure(figsize=(4.6, 2.6))
        ax = fig.add_subplot(111)
        _draw_candles(ax, bars, offset)
        _plot_overlay(ax, sma20, offset, GOLD, "SMA20", lw=1.0)
        _plot_overlay(ax, sma50, offset, NAVY_SOFT, "SMA50", lw=1.0)
        _plot_overlay(ax, sma200, offset, GOLD_SOFT, "SMA200", lw=1.0)
        ax.set_title(
            f"{technicals.ticker if technicals else ''} {timeframe_label} — as of {as_of}".strip(),
            fontsize=10, fontfamily=_FONT, loc="left", pad=6,
        )
        ax.grid(axis="y", color=GRID, linewidth=0.5, zorder=0)
        ax.legend(frameon=False, fontsize=6, loc="upper left", labelcolor=MUTED, ncol=3)
        _date_ticks(ax)
        _style_axis(ax)
        fig.patch.set_facecolor(PAPER)
        fig.tight_layout()
        return _to_png(fig)

    # ── Full multi-panel chart ────────────────────────────────────────────────
    fig = Figure(figsize=(9.2, 9.6))
    gs = GridSpec(4, 1, height_ratios=[3.0, 0.9, 1.1, 1.1], hspace=0.28, figure=fig)
    ax_price = fig.add_subplot(gs[0])
    ax_vol = fig.add_subplot(gs[1], sharex=ax_price)
    ax_rsi = fig.add_subplot(gs[2], sharex=ax_price)
    ax_macd = fig.add_subplot(gs[3], sharex=ax_price)

    # Price panel -------------------------------------------------------------
    _draw_candles(ax_price, bars, offset)
    _plot_overlay(ax_price, sma20, offset, GOLD, "SMA 20")
    _plot_overlay(ax_price, sma50, offset, NAVY_SOFT, "SMA 50")
    _plot_overlay(ax_price, sma200, offset, GOLD_SOFT, "SMA 200")
    _plot_overlay(ax_price, ema12, offset, NAVY, "EMA 12", lw=0.9)
    _plot_overlay(ax_price, ema26, offset, MUTED, "EMA 26", lw=0.9)

    if technicals is not None:
        for lvl in technicals.resistances:
            ax_price.axhline(lvl, color=DOWN, linestyle="--", linewidth=0.7, zorder=2)
            ax_price.text(n_plot - 1, lvl, f" R {format_price(lvl, asset_class='equity')}",
                          va="center", ha="left",
                          fontsize=6.5, color=DOWN, fontfamily=_FONT)
        for lvl in technicals.supports:
            ax_price.axhline(lvl, color=NAVY_SOFT, linestyle="--", linewidth=0.7, zorder=2)
            ax_price.text(n_plot - 1, lvl, f" S {format_price(lvl, asset_class='equity')}",
                          va="center", ha="left",
                          fontsize=6.5, color=NAVY_SOFT, fontfamily=_FONT)
        # 52-week / window high & low
        ax_price.axhline(technicals.range_high, color=GOLD, linewidth=0.8, alpha=0.6, zorder=1)
        ax_price.axhline(technicals.range_low, color=GOLD, linewidth=0.8, alpha=0.6, zorder=1)
        ax_price.text(0, technicals.range_high, " 52-wk high", va="bottom", ha="left",
                      fontsize=6.5, color=GOLD, fontfamily=_FONT)
        ax_price.text(0, technicals.range_low, " 52-wk low", va="top", ha="left",
                      fontsize=6.5, color=GOLD, fontfamily=_FONT)

    # Swing-structure labels (only those inside the plotted window, last few).
    swings = [s for s in _labelled_swings(bars) if s[0] >= offset]
    for idx, price, kind, label in swings[-8:]:
        x = idx - offset
        va = "bottom" if kind == "high" else "top"
        dy = 1.0 if kind == "high" else -1.0
        ax_price.annotate(
            label, xy=(x, price), xytext=(x, price + dy),
            fontsize=6.5, color=INK, fontfamily=_FONT, ha="center", va=va,
            textcoords="data", zorder=6,
        )
        ax_price.plot([x], [price], marker="o", markersize=2.2, color=INK, zorder=6)

    # Last BOS / CHoCH event marker.
    if technicals is not None and technicals.last_structure_event_date:
        ev_date = technicals.last_structure_event_date
        if ev_date in dates:
            ev_idx = dates.index(ev_date)
            if ev_idx >= offset:
                x = ev_idx - offset
                ax_price.axvline(x, color=GOLD, linestyle=":", linewidth=1.0, zorder=2)
                ax_price.text(x, ax_price.get_ylim()[1], f" {technicals.last_structure_event}",
                              rotation=90, va="top", ha="left", fontsize=6.5, color=GOLD,
                              fontfamily=_FONT)

    title_ticker = technicals.ticker if technicals else ""
    ax_price.set_title(
        f"{title_ticker} — Technicals ({timeframe_label}) — as of {as_of}".strip(" —"),
        fontsize=12, fontfamily=_FONT, loc="left", pad=10,
    )
    ax_price.grid(axis="y", color=GRID, linewidth=0.5, zorder=0)
    ax_price.legend(frameon=False, fontsize=7, loc="upper left", labelcolor=MUTED, ncol=5)
    ax_price.set_ylabel("Price", fontsize=8, color=MUTED, fontfamily=_FONT)

    # Volume panel ------------------------------------------------------------
    for i in range(offset, len(bars)):
        b = bars[i]
        color = UP if b.close >= b.open else DOWN
        ax_vol.bar(i - offset, b.volume, width=0.8, color=color, alpha=0.55, zorder=3)
    ax_vol.set_ylabel("Volume", fontsize=8, color=MUTED, fontfamily=_FONT)
    ax_vol.grid(axis="y", color=GRID, linewidth=0.5, zorder=0)

    # RSI panel ---------------------------------------------------------------
    rsi = _rsi_series(closes, 14)
    _plot_overlay(ax_rsi, rsi, offset, NAVY, "RSI(14)")
    ax_rsi.axhline(70, color=DOWN, linestyle="--", linewidth=0.7, zorder=2)
    ax_rsi.axhline(30, color=NAVY_SOFT, linestyle="--", linewidth=0.7, zorder=2)
    ax_rsi.axhspan(30, 70, color=GRID, alpha=0.25, zorder=0)
    ax_rsi.set_ylim(0, 100)
    ax_rsi.set_yticks([30, 50, 70])
    ax_rsi.set_ylabel("RSI", fontsize=8, color=MUTED, fontfamily=_FONT)

    # MACD panel --------------------------------------------------------------
    macd_line, signal_line, hist = _macd_series(closes)
    _plot_overlay(ax_macd, macd_line, offset, NAVY, "MACD")
    _plot_overlay(ax_macd, signal_line, offset, GOLD, "Signal")
    for i in range(offset, len(bars)):
        h = hist[i]
        if h is not None:
            ax_macd.bar(i - offset, h, width=0.8, color=(UP if h >= 0 else DOWN), alpha=0.5,
                        zorder=2)
    ax_macd.axhline(0, color=MUTED, linewidth=0.7, zorder=1)
    ax_macd.set_ylabel("MACD", fontsize=8, color=MUTED, fontfamily=_FONT)
    ax_macd.legend(frameon=False, fontsize=7, loc="upper left", labelcolor=MUTED, ncol=2)

    for ax in (ax_price, ax_vol, ax_rsi, ax_macd):
        _style_axis(ax)
    for ax in (ax_price, ax_vol, ax_rsi):
        ax.tick_params(labelbottom=False)
    _date_ticks(ax_macd)

    fig.patch.set_facecolor(PAPER)
    return _to_png(fig)
