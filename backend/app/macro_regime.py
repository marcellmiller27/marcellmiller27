# JHI-SIG: 69M2705M | Macro regime classifier (deterministic) | JHI Research & Analytics Firm, Inc. (proprietary)
"""Aegira's own deterministic macro-regime classifier — the engine behind the
newsletter "visual layer" Regime Quadrant.

Two orthogonal axes, each computed from data the platform ALREADY pulls (FRED / BLS /
BEA / market feeds):

  • Growth  — accelerating (>0) vs. decelerating (<0): derived from the labor market
    (unemployment vs. the ~4% full-employment reference, inverted) and household demand
    (consumer sentiment vs. a ~70 reference), with an optional cyclical read from
    industrial production. Rising joblessness / weakening sentiment ⇒ decelerating.

  • Inflation — accelerating/hot (>0) vs. decelerating/cooling (<0): derived from headline
    CPI relative to a ~2.5% reference (the 2% target plus a small tolerance band). Above
    the band reads "hot"; at/below reads "cooling".

The (growth, inflation) sign pair maps to one of four GENERIC macro regimes — deliberately
NOT any vendor's proprietary framework naming:

  ┌──────────────────────────┬──────────────────────────┐
  │ Goldilocks               │ Reflation                │   (inflation up →)
  │ growth↑ / inflation↓     │ growth↑ / inflation↑     │
  ├──────────────────────────┼──────────────────────────┤
  │ Deflation / Slowdown     │ Stagflation              │
  │ growth↓ / inflation↓     │ growth↓ / inflation↑     │
  └──────────────────────────┴──────────────────────────┘
        (← growth down)              (growth up →)

Governance / fact-lock: every number consumed here is a released level already disclosed
in the edition body; NOTHING is fabricated. When an input series is briefly unavailable the
axis degrades gracefully (fewer inputs, or — if nothing usable remains — no read at all,
in which case the caller omits the marker rather than inventing a position).

The core ``classify_regime`` is a pure function of two floats, so it is exhaustively
unit-testable on synthetic inputs across all four quadrants and the boundary cases.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.market_models import Quote

QuoteMap = dict[str, Quote]

# ── Reference anchors (shared vocabulary with newsletter_content; disclosed in-copy) ──
_FULL_EMPLOYMENT = 4.0   # ~ natural rate of unemployment reference
_SENTIMENT_REF = 70.0    # subdued/So-so consumer-sentiment reference (index)
_IP_REF = 100.0          # industrial-production index reference (rebased ~100)
_INFLATION_NEUTRAL = 2.5  # 2.0% target + 0.5pt tolerance: above ⇒ "hot", below ⇒ "cooling"

# Axis weights (sum to 1.0 within each axis) — labor leads the growth read.
_W_UNEMP = 0.6
_W_SENTIMENT = 0.3
_W_IP = 0.1

# Plot scaling: each sub-score is clamped to [-1, 1] so the marker lives on a stable grid.
_CLAMP = 1.0


def _clamp(x: float, lo: float = -_CLAMP, hi: float = _CLAMP) -> float:
    return max(lo, min(hi, x))


def _price(m: QuoteMap, symbol: str) -> float | None:
    """A usable released level for ``symbol`` (None when missing/unavailable)."""
    q = m.get(symbol)
    if q is None or q.price is None or q.status == "unavailable":
        return None
    return float(q.price)


# ── The four generic regimes ─────────────────────────────────────────────────
@dataclass(frozen=True)
class Regime:
    """A classified macro regime with human-readable, generic (non-proprietary) labels."""

    quadrant: str        # stable key: reflation | goldilocks | stagflation | deflation
    label: str           # display label
    growth_state: str    # "accelerating" | "decelerating"
    inflation_state: str  # "accelerating" | "decelerating"
    caption: str         # e.g. "Growth accelerating · Inflation cooling"
    blurb: str           # one-line institutional read of the regime


# key -> (label, one-line blurb). Generic macro vocabulary only.
_REGIME_META: dict[str, tuple[str, str]] = {
    "reflation": (
        "Reflation",
        "Growth and inflation are both firming — a pro-cyclical backdrop that favors "
        "real assets and hard-asset hedges over long-duration bonds.",
    ),
    "goldilocks": (
        "Goldilocks",
        "Growth is holding while inflation cools — the most benign mix for risk assets "
        "and duration alike, though rarely a stable equilibrium.",
    ),
    "stagflation": (
        "Stagflation",
        "Growth is fading while inflation stays hot — the hardest regime for policy, "
        "rewarding quality, cash flow, and inflation protection.",
    ),
    "deflation": (
        "Deflation / Slowdown",
        "Growth and inflation are both easing — a disinflationary slowdown that favors "
        "high-quality duration and defensives over cyclical risk.",
    ),
}


def classify_regime(growth: float, inflation: float) -> Regime:
    """Map a (growth, inflation) score pair to one of the four generic regimes.

    Sign convention: ``growth >= 0`` ⇒ accelerating, ``inflation >= 0`` ⇒ accelerating
    (hot). The boundary (exactly 0) is treated as the accelerating side so a reading is
    always well-defined. Pure function — no I/O — so it is exhaustively unit-testable.
    """
    g_up = growth >= 0
    i_up = inflation >= 0
    if g_up and i_up:
        key = "reflation"
    elif g_up and not i_up:
        key = "goldilocks"
    elif not g_up and i_up:
        key = "stagflation"
    else:
        key = "deflation"
    label, blurb = _REGIME_META[key]
    growth_state = "accelerating" if g_up else "decelerating"
    inflation_state = "accelerating" if i_up else "decelerating"
    caption = (
        f"Growth {'accelerating' if g_up else 'decelerating'} · "
        f"Inflation {'hot' if i_up else 'cooling'}"
    )
    return Regime(
        quadrant=key, label=label, growth_state=growth_state,
        inflation_state=inflation_state, caption=caption, blurb=blurb,
    )


# ── Axis derivation (deterministic, from released levels) ─────────────────────
@dataclass
class AxisReading:
    """One regime axis (growth or inflation) derived from released levels.

    ``score`` is signed (positive = accelerating); ``None`` when no input series was
    available. ``components`` discloses exactly which released figures fed the read.
    """

    score: float | None
    available: bool
    components: list[str] = field(default_factory=list)


def derive_growth(m: QuoteMap) -> AxisReading:
    """Growth axis: labor + demand (+ optional cyclical output), each vs. a reference.

    Positive ⇒ accelerating. Degrades gracefully: any missing input is dropped and the
    remaining weights are renormalized; if nothing is available, returns an empty read.
    """
    terms: list[tuple[float, float]] = []  # (weight, clamped sub-score)
    components: list[str] = []

    unemp = _price(m, "UNEMPLOYMENT")
    if unemp is not None:
        # Below full employment ⇒ tight labor ⇒ growth accelerating (positive).
        sub = _clamp((_FULL_EMPLOYMENT - unemp) / 1.5)
        terms.append((_W_UNEMP, sub))
        components.append(f"Unemployment {unemp:.2f}% vs ~{_FULL_EMPLOYMENT:.1f}% reference")

    sentiment = _price(m, "CONSUMER_SENTIMENT")
    if sentiment is not None:
        sub = _clamp((sentiment - _SENTIMENT_REF) / 25.0)
        terms.append((_W_SENTIMENT, sub))
        components.append(f"Consumer sentiment {sentiment:.1f} vs ~{_SENTIMENT_REF:.0f} reference")

    ip = _price(m, "INDUSTRIAL_PRODUCTION")
    if ip is not None:
        sub = _clamp((ip - _IP_REF) / 8.0)
        terms.append((_W_IP, sub))
        components.append(f"Industrial production {ip:.1f} vs ~{_IP_REF:.0f} index reference")

    if not terms:
        return AxisReading(score=None, available=False, components=[])
    weight_sum = sum(w for w, _ in terms)
    score = sum(w * s for w, s in terms) / weight_sum
    return AxisReading(score=round(score, 4), available=True, components=components)


def derive_inflation(m: QuoteMap) -> AxisReading:
    """Inflation axis: headline CPI vs. a ~2.5% reference (2% target + tolerance).

    Positive ⇒ hot/accelerating. Returns an empty read when CPI is unavailable.
    """
    cpi = _price(m, "INFLATION")
    if cpi is None:
        return AxisReading(score=None, available=False, components=[])
    score = _clamp((cpi - _INFLATION_NEUTRAL) / 1.5)
    return AxisReading(
        score=round(score, 4), available=True,
        components=[f"CPI {cpi:.2f}% vs ~{_INFLATION_NEUTRAL:.1f}% reference (2% target + tolerance)"],
    )


# ── The full assessment (what the newsletter consumes) ────────────────────────
@dataclass
class RegimeAssessment:
    """The regime read for one edition: classified regime, both axes, an optional
    trail of recent (growth, inflation) points, and the as-of disclosure."""

    regime: Regime | None
    growth: AxisReading
    inflation: AxisReading
    trail: list[tuple[float, float]]  # recent points, current LAST; [] or [current] when no history
    as_of: str | None
    available: bool                   # True only when both axes placed the current marker


def _as_of(m: QuoteMap) -> str | None:
    """A best-effort as-of date from the macro inputs (the period the read belongs to).

    Prefers the value's disclosed as-of label but returns only its DATE portion (e.g.
    "Jun 2026"), so callers can render "As of Jun 2026" without the doubled "as of"."""
    for symbol in ("INFLATION", "UNEMPLOYMENT", "CONSUMER_SENTIMENT"):
        q = m.get(symbol)
        if q is None:
            continue
        if q.as_of_label:
            # Labels look like "Monthly · as of Jun 2026"; keep the trailing date.
            label = q.as_of_label
            marker = "as of "
            idx = label.lower().rfind(marker)
            return label[idx + len(marker):].strip() if idx != -1 else label
        if q.observation_date:
            return q.observation_date
    return None


def assess_regime(m: QuoteMap, history: list[QuoteMap] | None = None) -> RegimeAssessment:
    """Classify the current macro regime and (optionally) build a short trail.

    ``history`` — oldest→newest prior snapshots — is optional. When supplied, each snapshot
    that yields BOTH axes contributes a real prior point to the trail; the current reading is
    always appended last. With no history the trail holds just the current point (graceful
    degradation — never a fabricated series). When the current reading is missing an axis the
    assessment is ``available=False`` and the caller omits the marker.
    """
    growth = derive_growth(m)
    inflation = derive_inflation(m)
    as_of = _as_of(m)

    trail: list[tuple[float, float]] = []
    for snap in history or []:
        g, i = derive_growth(snap), derive_inflation(snap)
        if g.available and i.available and g.score is not None and i.score is not None:
            trail.append((g.score, i.score))

    if not (growth.available and inflation.available
            and growth.score is not None and inflation.score is not None):
        return RegimeAssessment(regime=None, growth=growth, inflation=inflation,
                                trail=trail, as_of=as_of, available=False)

    current = (growth.score, inflation.score)
    trail.append(current)
    regime = classify_regime(growth.score, inflation.score)
    return RegimeAssessment(regime=regime, growth=growth, inflation=inflation,
                            trail=trail, as_of=as_of, available=True)
