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
