# JHI-SIG: 69M2705M | Newsletter chart/visual layer (server-rendered) | JHI Research & Analytics Firm, Inc. (proprietary)
"""Deterministic, print-friendly institutional charts for the dynamic newsletter.

Renders clean navy/gold Aegira-palette charts to PNG with matplotlib's headless Agg
backend and returns them as base64 ``data:`` URIs so the frontend can show them as
plain ``<img>`` elements and the headless-Chromium PDF captures them automatically
(it prints the real page). No interactive/JS charting, no external services.

Governance: charts are built ONLY from DERIVED figures the engine already computes
(quote levels, disclosed reference anchors, derived opportunity scores / factor
contributions). No raw licensed SF1 rows are ever plotted or embedded. Nothing here
fabricates history — a macro series is drawn only when real history is supplied;
otherwise a current-vs-reference bar is rendered from released levels.
"""

from __future__ import annotations

import base64
import io

import matplotlib

matplotlib.use("Agg")  # headless: no display, deterministic raster output

import matplotlib.pyplot as plt  # noqa: E402  (must follow the Agg backend selection)
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

# ── Aegira palette (navy / gold), tuned for print on white ────────────────────
NAVY = "#0C1F33"
NAVY_SOFT = "#3A5A7A"
GOLD = "#9A6B12"
GOLD_SOFT = "#C7A867"
INK = "#0C1F33"
MUTED = "#5A6B7D"
GRID = "#D5DEE8"
PAPER = "#FFFFFF"

# Factor-family colors for the opportunity decomposition (stable order).
FACTOR_ORDER = ("Value", "Quality", "Growth", "Momentum")
FACTOR_COLORS = {
    "Value": GOLD,
    "Quality": NAVY,
    "Growth": NAVY_SOFT,
    "Momentum": GOLD_SOFT,
}

_FONT = "DejaVu Serif"  # bundled with matplotlib → deterministic across machines


def _base_style(fig: Figure) -> None:
    fig.patch.set_facecolor(PAPER)
    for ax in fig.axes:
        ax.set_facecolor(PAPER)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        for spine in ("left", "bottom"):
            ax.spines[spine].set_color(GRID)
        ax.tick_params(colors=MUTED, labelsize=9)
        ax.title.set_color(INK)


def _to_data_uri(fig: Figure) -> str:
    """Serialize a figure to a deterministic base64 PNG ``data:`` URI, then close it."""
    buf = io.BytesIO()
    # metadata={} strips the timestamp PNG chunk so identical inputs → identical bytes.
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=PAPER, metadata={"Software": "Aegira"})
    plt.close(fig)
    encoded = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def reference_bar(
    title: str,
    labels: list[str],
    current: list[float],
    reference: list[float],
    unit: str = "%",
) -> str:
    """Current-vs-reference grouped bars (used when no real history is available).

    Honest by construction: plots released levels against disclosed anchors — it
    never fabricates a time series.
    """
    fig = Figure(figsize=(6.6, 3.4))
    ax = fig.add_subplot(111)
    n = len(labels)
    x = list(range(n))
    width = 0.38
    ax.bar([i - width / 2 for i in x], current, width, label="Current",
           color=NAVY, edgecolor=NAVY, zorder=3)
    ax.bar([i + width / 2 for i in x], reference, width, label="Reference",
           color=GOLD_SOFT, edgecolor=GOLD, zorder=3)
    for i, v in enumerate(current):
        ax.text(i - width / 2, v, f"{v:.2f}{unit}", ha="center", va="bottom",
                fontsize=8, color=NAVY, fontfamily=_FONT)
    for i, v in enumerate(reference):
        ax.text(i + width / 2, v, f"{v:.2f}{unit}", ha="center", va="bottom",
                fontsize=8, color=GOLD, fontfamily=_FONT)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9, color=INK, fontfamily=_FONT)
    ax.set_title(title, fontsize=12, fontfamily=_FONT, pad=10, loc="left")
    ax.grid(axis="y", color=GRID, linewidth=0.6, zorder=0)
    ax.legend(frameon=False, fontsize=8, loc="upper right", labelcolor=MUTED)
    ax.margins(y=0.18)
    _base_style(fig)
    return _to_data_uri(fig)


def time_series(
    title: str,
    dates: list[str],
    series: dict[str, list[float]],
    reference: tuple[str, float] | None = None,
    unit: str = "%",
) -> str:
    """A macro time-series line chart. Only call this with REAL history (never faked).

    ``reference`` draws a labeled horizontal anchor (e.g. the 2% CPI target).
    """
    fig = Figure(figsize=(6.6, 3.4))
    ax = fig.add_subplot(111)
    colors = [NAVY, GOLD, NAVY_SOFT, GOLD_SOFT]
    x = list(range(len(dates)))
    for i, (name, ys) in enumerate(series.items()):
        ax.plot(x, ys, color=colors[i % len(colors)], linewidth=1.8,
                marker="o", markersize=2.5, label=name, zorder=3)
    if reference is not None:
        ref_label, ref_val = reference
        ax.axhline(ref_val, color=GOLD, linestyle="--", linewidth=1.2, zorder=2)
        ax.text(x[-1], ref_val, f" {ref_label}", va="center", ha="left",
                fontsize=8, color=GOLD, fontfamily=_FONT)
    step = max(1, len(dates) // 6)
    ax.set_xticks(x[::step])
    ax.set_xticklabels([dates[i] for i in x[::step]], fontsize=8, color=MUTED,
                       rotation=0, fontfamily=_FONT)
    ax.set_ylabel(unit, fontsize=9, color=MUTED, fontfamily=_FONT)
    ax.set_title(title, fontsize=12, fontfamily=_FONT, pad=10, loc="left")
    ax.grid(axis="y", color=GRID, linewidth=0.6, zorder=0)
    if len(series) > 1:
        ax.legend(frameon=False, fontsize=8, loc="best", labelcolor=MUTED)
    _base_style(fig)
    return _to_data_uri(fig)


def ranked_scores(title: str, names: list[str], scores: list[float]) -> str:
    """Horizontal ranked bar of the top opportunities' derived scores (0-100)."""
    fig = Figure(figsize=(6.6, 0.5 * len(names) + 1.4))
    ax = fig.add_subplot(111)
    order = list(range(len(names)))[::-1]  # highest score at the top
    y = list(range(len(names)))
    vals = [scores[i] for i in order]
    labs = [names[i] for i in order]
    ax.barh(y, vals, color=NAVY, edgecolor=NAVY, height=0.62, zorder=3)
    for i, v in enumerate(vals):
        ax.text(v + 1.2, i, f"{v:.0f}", va="center", ha="left",
                fontsize=9, color=GOLD, fontfamily=_FONT)
    ax.set_yticks(y)
    ax.set_yticklabels(labs, fontsize=10, color=INK, fontfamily=_FONT)
    ax.set_xlim(0, 105)
    ax.set_xlabel("Opportunity Score (0–100, cross-sectional)", fontsize=9,
                  color=MUTED, fontfamily=_FONT)
    ax.set_title(title, fontsize=12, fontfamily=_FONT, pad=10, loc="left")
    ax.grid(axis="x", color=GRID, linewidth=0.6, zorder=0)
    _base_style(fig)
    return _to_data_uri(fig)


def factor_decomposition(
    title: str,
    names: list[str],
    contributions: list[dict[str, float]],
) -> str:
    """Diverging stacked bars of each name's Value/Quality/Growth/Momentum contribution.

    Contributions are the (signed) weighted factor z-score contributions the engine
    computes — positive extends right, negative left — so a reader sees WHICH factors
    drive each pick, not just the headline score.
    """
    fig = Figure(figsize=(6.8, 0.62 * len(names) + 1.7))
    ax = fig.add_subplot(111)
    y = list(range(len(names)))[::-1]  # first name at the top
    pos_off = [0.0] * len(names)
    neg_off = [0.0] * len(names)
    for factor in FACTOR_ORDER:
        widths = [c.get(factor, 0.0) for c in contributions]
        lefts: list[float] = []
        for i, w in enumerate(widths):
            if w >= 0:
                lefts.append(pos_off[i])
                pos_off[i] += w
            else:
                neg_off[i] += w
                lefts.append(neg_off[i])
        ax.barh(y, widths, left=lefts, height=0.6, label=factor,
                color=FACTOR_COLORS[factor], edgecolor=PAPER, linewidth=0.5, zorder=3)
    ax.axvline(0, color=MUTED, linewidth=0.9, zorder=4)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=10, color=INK, fontfamily=_FONT)
    ax.set_xlabel("Factor contribution to composite (weighted z-score)", fontsize=9,
                  color=MUTED, fontfamily=_FONT)
    ax.set_title(title, fontsize=12, fontfamily=_FONT, pad=10, loc="left")
    ax.grid(axis="x", color=GRID, linewidth=0.6, zorder=0)
    ax.legend(frameon=False, fontsize=8, ncol=4, loc="upper center",
              bbox_to_anchor=(0.5, -0.18 / (0.62 * len(names) + 1.7) * 6 - 0.02),
              labelcolor=MUTED)
    _base_style(fig)
    return _to_data_uri(fig)


def horizontal_bars(
    title: str,
    labels: list[str],
    values: list[float],
    value_suffix: str = "",
    xlabel: str = "",
    scale: float = 1.0,
) -> str:
    """A generic horizontal bar for derived dollar/count aggregates (e.g. SBA volume).

    ``scale`` divides the raw values for display (e.g. 1e6 to show $millions); the bar
    lengths and the printed labels both use the scaled value so the axis is readable.
    """
    scaled = [v / scale for v in values]
    fig = Figure(figsize=(6.8, 0.5 * len(labels) + 1.4))
    ax = fig.add_subplot(111)
    y = list(range(len(labels)))[::-1]  # first (largest) at the top
    ax.barh(y, scaled, color=NAVY, edgecolor=NAVY, height=0.62, zorder=3)
    span = max(scaled) if scaled else 1.0
    for i, v in zip(y, scaled):
        ax.text(v + span * 0.01, i, f"{v:,.1f}{value_suffix}", va="center", ha="left",
                fontsize=9, color=GOLD, fontfamily=_FONT)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9, color=INK, fontfamily=_FONT)
    ax.set_xlim(0, span * 1.18)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=9, color=MUTED, fontfamily=_FONT)
    ax.set_title(title, fontsize=12, fontfamily=_FONT, pad=10, loc="left")
    ax.grid(axis="x", color=GRID, linewidth=0.6, zorder=0)
    _base_style(fig)
    return _to_data_uri(fig)


def labeled_levels(title: str, labels: list[str], values: list[float],
                   unit: str = "%", note: str | None = None) -> str:
    """A single-series labeled bar for a thematic deep-dive (e.g. rate stack)."""
    fig = Figure(figsize=(6.6, 3.2))
    ax = fig.add_subplot(111)
    x = list(range(len(labels)))
    colors = [NAVY if v >= 0 else GOLD for v in values]
    ax.bar(x, values, width=0.55, color=colors, edgecolor=colors, zorder=3)
    for i, v in enumerate(values):
        ax.text(i, v, f"{v:.2f}{unit}", ha="center",
                va="bottom" if v >= 0 else "top", fontsize=9, color=INK,
                fontfamily=_FONT)
    ax.axhline(0, color=MUTED, linewidth=0.9, zorder=4)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9, color=INK, fontfamily=_FONT)
    ax.set_title(title, fontsize=12, fontfamily=_FONT, pad=10, loc="left")
    ax.grid(axis="y", color=GRID, linewidth=0.6, zorder=0)
    ax.margins(y=0.2)
    if note:
        ax.text(0.0, -0.22, note, transform=ax.transAxes, fontsize=8,
                color=MUTED, fontfamily=_FONT)
    _base_style(fig)
    return _to_data_uri(fig)


# ── The newsletter "visual layer" (macro regime + cross-asset posture) ────────
# Two deterministic, print-friendly exhibits that lead the edition (above the body):
#   • regime_quadrant_chart — Aegira's own 2x2 macro-regime map (growth × inflation)
#   • signal_heatmap_chart  — a shaded cross-asset posture grid (monochrome intensity)
# Both are built ONLY from released levels / derived figures the engine already computes.

# Generic (non-proprietary) quadrant labels; positions are (x-sign, y-sign) corners.
_QUADRANT_LABELS = {
    (1, 1): "Reflation",
    (1, -1): "Goldilocks",
    (-1, 1): "Stagflation",
    (-1, -1): "Deflation /\nSlowdown",
}
# Very light monochrome tints so the four cells read without competing with the marker.
_QUADRANT_TINTS = {
    (1, 1): "#EEF2F7",
    (1, -1): "#F6F8FB",
    (-1, 1): "#E7ECF3",
    (-1, -1): "#F1F4F8",
}


def regime_quadrant_chart(
    growth: float,
    inflation: float,
    regime_label: str,
    trail: list[tuple[float, float]] | None = None,
    as_of: str | None = None,
    growth_caption: str = "",
    inflation_caption: str = "",
) -> str:
    """Aegira's 2x2 macro-regime quadrant (Growth × Inflation) as a PNG data-URI.

    ``growth`` / ``inflation`` are signed scores (positive = accelerating). The four
    quadrants carry GENERIC macro labels (Reflation / Goldilocks / Stagflation /
    Deflation-Slowdown). ``trail`` (oldest→newest, current last) draws a short path of
    recent readings; with a single point only the current marker is shown. The exhibit is
    explicitly labeled as Aegira's own computation and as-of dated. Fact-locked: the caller
    passes only scores derived from released levels.
    """
    lim = 1.15
    fig = Figure(figsize=(6.6, 5.0))
    ax = fig.add_subplot(111)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")

    # Quadrant tints + corner labels.
    for (sx, sy), tint in _QUADRANT_TINTS.items():
        x0 = 0 if sx > 0 else -lim
        y0 = 0 if sy > 0 else -lim
        ax.add_patch(Rectangle((x0, y0), lim, lim, facecolor=tint, edgecolor="none", zorder=0))
    for (sx, sy), label in _QUADRANT_LABELS.items():
        ax.text(sx * lim * 0.94, sy * lim * 0.90, label,
                ha="right" if sx > 0 else "left",
                va="top" if sy > 0 else "bottom",
                fontsize=11, color=NAVY_SOFT, fontfamily=_FONT, fontweight="bold",
                linespacing=0.95, zorder=1)

    # Center cross-hairs (the accelerating/decelerating divides).
    ax.axhline(0, color=MUTED, linewidth=1.0, zorder=2)
    ax.axvline(0, color=MUTED, linewidth=1.0, zorder=2)

    # The trail of recent readings (real history only; may be just the current point).
    pts = list(trail or [(growth, inflation)])
    if (growth, inflation) not in pts:
        pts.append((growth, inflation))
    if len(pts) > 1:
        xs = [_clamp_pt(p[0], lim) for p in pts]
        ys = [_clamp_pt(p[1], lim) for p in pts]
        ax.plot(xs, ys, color=NAVY_SOFT, linewidth=1.4, linestyle="--", zorder=3,
                alpha=0.8)
        ax.scatter(xs[:-1], ys[:-1], s=26, color=NAVY_SOFT, edgecolor=PAPER,
                   linewidth=0.6, zorder=4, alpha=0.7)

    # The current position marker.
    cx, cy = _clamp_pt(growth, lim), _clamp_pt(inflation, lim)
    ax.scatter([cx], [cy], s=180, color=GOLD, edgecolor=NAVY, linewidth=1.4, zorder=6)
    ax.annotate(f" {regime_label}", (cx, cy), fontsize=11, color=NAVY,
                fontfamily=_FONT, fontweight="bold", va="center",
                ha="left" if cx < lim * 0.4 else "right", zorder=7,
                xytext=(8 if cx < lim * 0.4 else -8, 0), textcoords="offset points")

    # Axis labels (the two regime dimensions), as requested.
    ax.set_xlabel("Growth  ·  decelerating  ◀——▶  accelerating",
                  fontsize=9.5, color=INK, fontfamily=_FONT)
    ax.set_ylabel("Inflation  ·  cooling  ◀——▶  accelerating",
                  fontsize=9.5, color=INK, fontfamily=_FONT)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(GRID)

    title = "Macro Regime — Aegira's own computation"
    ax.set_title(title, fontsize=12.5, fontfamily=_FONT, pad=12, loc="left", color=INK)

    # As-of + input disclosure beneath the plot (never fabricated).
    sub_bits = [b for b in (growth_caption, inflation_caption) if b]
    if as_of:
        sub_bits.append(f"As of {as_of}")
    if sub_bits:
        fig.text(0.02, 0.005, "  ·  ".join(sub_bits), fontsize=7.5, color=MUTED,
                 fontfamily=_FONT, ha="left")

    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(PAPER)
    return _to_data_uri(fig)


def _clamp_pt(v: float, lim: float) -> float:
    """Keep a plotted point inside the visible grid (scores are already ~[-1, 1])."""
    return max(-lim * 0.98, min(lim * 0.98, v))


def _sev_style(severity: float) -> tuple[tuple[float, float, float], str]:
    """Monochrome intensity fill + a readable text color for one heat-map cell.

    ``severity`` is a magnitude in [0, 1]: 0 ⇒ pale paper, 1 ⇒ deep navy (the platform's
    "Rule B" monochrome/severity approach). Text flips to white once the fill is dark."""
    s = max(0.0, min(1.0, severity))
    # Interpolate PAPER (white) → NAVY (0C1F33) in RGB.
    nav = (0x0C / 255, 0x1F / 255, 0x33 / 255)
    fill = tuple(1.0 + (nav[i] - 1.0) * s for i in range(3))
    text = "#FFFFFF" if s >= 0.55 else INK
    return fill, text  # type: ignore[return-value]


def signal_heatmap_chart(
    rows: list[dict],
    columns: tuple[str, ...] = ("Level", "Momentum", "Posture"),
    as_of: str | None = None,
    title: str = "Cross-Asset Signal Heat Map",
) -> str:
    """A shaded cross-asset posture grid as a PNG data-URI.

    Each ``rows`` entry is ``{"label": str, "cells": [{"text": str, "severity": float}, ...]}``
    with one cell per column; ``severity`` (magnitude 0..1) drives the monochrome intensity
    shading. Deterministic and print-friendly; every value traces to a released level or a
    derived figure disclosed in-copy (fact-locked). Renders whatever rows are supplied, so a
    briefly-missing series simply drops its row (graceful degradation)."""
    n_rows = max(1, len(rows))
    n_cols = len(columns)
    fig = Figure(figsize=(8.0, 0.52 * n_rows + 1.6))
    ax = fig.add_subplot(111)

    label_w = 2.6  # x-space reserved for the row labels (in cell units)
    cell_w = 1.7
    cell_h = 1.0
    total_w = label_w + n_cols * cell_w
    total_h = n_rows * cell_h

    ax.set_xlim(0, total_w)
    ax.set_ylim(0, total_h + 1.0)  # +1 row of headroom for the column headers
    ax.axis("off")

    # Column headers.
    for c, col in enumerate(columns):
        cx = label_w + c * cell_w + cell_w / 2
        ax.text(cx, total_h + 0.35, col, ha="center", va="center", fontsize=9,
                color=INK, fontfamily=_FONT, fontweight="bold")

    # Rows (top-to-bottom): first row at the top.
    for r, row in enumerate(rows):
        y = total_h - (r + 1) * cell_h
        ax.text(label_w - 0.15, y + cell_h / 2, str(row.get("label", "")),
                ha="right", va="center", fontsize=9.5, color=INK, fontfamily=_FONT,
                fontweight="bold")
        cells = row.get("cells", [])
        for c in range(n_cols):
            cell = cells[c] if c < len(cells) else {"text": "—", "severity": 0.0}
            fill, text_color = _sev_style(float(cell.get("severity", 0.0)))
            x = label_w + c * cell_w
            ax.add_patch(Rectangle((x, y), cell_w, cell_h, facecolor=fill,
                                   edgecolor=PAPER, linewidth=1.5, zorder=2))
            ax.text(x + cell_w / 2, y + cell_h / 2, str(cell.get("text", "")),
                    ha="center", va="center", fontsize=8.5, color=text_color,
                    fontfamily=_FONT, zorder=3)

    ax.set_title(title, fontsize=12.5, fontfamily=_FONT, pad=10, loc="left", color=INK)
    if as_of:
        fig.text(0.02, 0.005, f"As of {as_of}  ·  Aegira monochrome severity — darker = stronger signal",
                 fontsize=7.5, color=MUTED, fontfamily=_FONT, ha="left")
    else:
        fig.text(0.02, 0.005, "Aegira monochrome severity — darker = stronger signal",
                 fontsize=7.5, color=MUTED, fontfamily=_FONT, ha="left")

    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(PAPER)
    return _to_data_uri(fig)
