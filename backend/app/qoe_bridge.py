# JHI-SIG: 69M2705M | EBITDA / QoE normalization bridge | JHI Research & Analytics Firm, Inc. (proprietary)
"""Aegira QoE bridge — deterministic EBITDA normalization engine.

Implements the 20-category adjustment library adopted in
`docs/board/BOARD_MINUTES_2026-08-26.md` §11:

  1. Owner / executive compensation to market      (BLS OEWS + revenue-tier)
  2. Related-party rent to fair-market rent        (ASC 850)
  3. Related-party service arrangements            (ASC 850)
  4. Personal / non-business expenses               (Reg S-K 10(e))
  5. One-time legal / settlement expenses           (ASC 450)
  6. One-time restructuring / severance             (ASC 420)
  7. Discontinued / divested operations             (ASC 205-20 / IFRS 5)
  8. Non-recurring bad-debt write-offs              (ASC 326)
  9. One-time gain / loss on asset sale             (ASC 610-20)
 10. Insurance / catastrophe recovery
 11. Deferred-revenue / cash-vs-accrual timing     (ASC 606)
 12. Founder-only healthcare / benefits             (replacement-cost)
 13. Above / below-market key contracts             (ASC 805 analog)
 14. Pro-forma synergies  (BUYER-SIDE FLAG ONLY — never in seller bridge)
 15. Run-rate revenue adjustments                   (Liberto stability gate)
 16. Discontinued product-line contribution margin  (ASC 205-20 analog)
 17. COVID / pandemic-era anomalies
 18. Litigation-in-progress reserves  (ASC 450 — NEVER removed while open)
 19. Non-cash stock-based compensation  (ASC 718 — DEFAULT: no add-back)
 20. Change in accounting policy                    (ASC 250)

Doctrine (§11.1, verbatim from Founder research):
  - Each add-back / deduction is a separately reconciled, evidence-based
    adjustment. If it persists / recurs it stays in normalized EBITDA
    regardless of what management calls it.
  - Owner-comp adjusts to market via a documented replacement-cost test.
  - Run-rate annualization is a forecast assumption, not evidence — gated
    by a stability test (COV + seasonality + operational anchor).
  - Buyer / seller views are BOTH shown; disagreements are visible.
  - Evidence Quality Grade (A external / B original internal / C
    management representation) is required on every adjustment; C blocked
    without explicit override.
  - Aegira output is decision-support / research — NOT an audit or a
    formal QoE opinion.  JHI-SIG: 69M2705M
"""

from __future__ import annotations

import logging
import math
import statistics
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)

_SIG = "JHI-SIG: 69M2705M"

# --------------------------------------------------------------------------- #
# Reserved-opinion vocabulary lint (from §10.8) — enforced on every driver
# note and description string produced by this engine.
# --------------------------------------------------------------------------- #
RESERVED_OPINION_WORDS: frozenset[str] = frozenset(
    {
        "audited",
        "audit",
        "opinion",
        "unqualified",
        "qualified",
        "adverse",
        "disclaimer",
        "fair presentation",
        "certified",
        "attest",
        "attested",
    }
)


def lint_reserved_vocabulary(text: str) -> list[str]:
    """Return any reserved-opinion words appearing as whole-word tokens.

    Case-insensitive. Multi-word phrases (e.g. "fair presentation") are
    matched as substrings. Returns an empty list when the text is clean.
    """
    lowered = f" {text.lower()} "
    hits: list[str] = []
    for word in RESERVED_OPINION_WORDS:
        if " " in word:
            if word in lowered:
                hits.append(word)
        else:
            token = f" {word} "
            punct_hits = any(
                f" {word}{p} " in lowered or f"{p}{word} " in lowered
                for p in (".", ",", ";", ":", "!", "?", ")", "(")
            )
            if token in lowered or punct_hits:
                hits.append(word)
    return sorted(set(hits))


# --------------------------------------------------------------------------- #
# Evidence Quality Grade (§10.8 + §11.3-A)
# --------------------------------------------------------------------------- #
class EvidenceGrade(str, Enum):
    A = "A"  # external / independent (attorney letter, gov't source, third-party benchmark)
    B = "B"  # original internal document (contract, invoice, plan, board resolution)
    C = "C"  # management-prepared / representation only

    @classmethod
    def normalize(cls, value: str | "EvidenceGrade") -> "EvidenceGrade":
        if isinstance(value, cls):
            return value
        text = str(value).strip().upper()
        if text in ("A", "B", "C"):
            return cls(text)
        raise ValueError(f"Unknown evidence grade: {value!r}")


class Recurrence(str, Enum):
    """Whether the adjustment reflects a recurring or one-time item.

    Doctrine (§11.1C): if an item persists or recurs, it stays in normalized
    EBITDA — the recurrence label decides whether the adjustment is defensible
    at all, not just how it's presented.
    """

    ONE_TIME = "one-time"
    RECURRING = "recurring"
    FLAG_ONLY = "flag-only"       # e.g. buyer synergies, open-litigation reserves — never applied


class Side(str, Enum):
    """Which side of the bridge the adjustment is presented on."""

    SELLER = "seller"       # applied only in the seller-view Adjusted EBITDA
    BUYER = "buyer"         # applied only in the buyer-view Adjusted EBITDA
    BOTH = "both"           # applied on both sides (most owner-comp / related-party adjustments)


class AdjustmentBlocked(Exception):
    """Raised (or captured as a note) when a guardrail refuses an adjustment.

    Emitted when Evidence Grade C is used without an explicit override, when
    a run-rate adjustment fails the stability gate, or when a related-party
    rent adjustment lacks a third-party benchmark.
    """


# --------------------------------------------------------------------------- #
# Adjustment inputs / outputs
# --------------------------------------------------------------------------- #
@dataclass
class AdjustmentInput:
    """One proposed EBITDA adjustment.

    ``category_id`` matches the ``id`` of a registered :class:`AdjustmentCategory`.
    ``amount`` is the *reported* amount as it appears in the P&L (positive), and
    ``sign`` tells the engine whether the adjustment INCREASES (+1) or DECREASES
    (-1) EBITDA on its applied side(s).
    """

    category_id: str
    amount: float
    sign: int = 1                                        # +1 add-back (EBITDA up); -1 deduction (EBITDA down)
    side: Side = Side.BOTH
    evidence_grade: EvidenceGrade = EvidenceGrade.B
    evidence_c_override: bool = False                    # required for grade C to ship
    evidence_source: str = ""                            # human citation ("BLS OEWS 11-1021 · Chicago · 2025")
    recurrence: Recurrence | None = None                 # None → engine uses category default
    note: str = ""                                       # optional analyst context
    # Category-specific extras keyed by field name.
    extras: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.sign = 1 if self.sign >= 0 else -1
        if self.amount < 0:
            self.amount = abs(self.amount)


@dataclass
class AdjustmentOutcome:
    """One category's evaluated adjustment (what actually enters the bridge)."""

    category_id: str
    category_name: str
    seller_amount: float                                 # applied to seller-view Adjusted EBITDA
    buyer_amount: float                                  # applied to buyer-view Adjusted EBITDA
    evidence_grade: EvidenceGrade
    recurrence: Recurrence
    reference: str                                       # authoritative reference (ASC / BLS / doctrine)
    driver_note: str                                     # deterministic explanation
    blocked: bool = False
    block_reason: str = ""
    warnings: list[str] = field(default_factory=list)


@dataclass
class EBITDABridge:
    """Complete EBITDA bridge output for one engagement / period."""

    business_name: str
    period_label: str
    reported_ebitda: float
    adjusted_ebitda_seller: float
    adjusted_ebitda_buyer: float
    adjustments: list[AdjustmentOutcome] = field(default_factory=list)
    blocked_adjustments: list[AdjustmentOutcome] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    ltm_ebitda: float | None = None
    run_rate_ebitda: float | None = None                 # None when stability gate fails
    three_year_avg_ebitda: float | None = None
    run_rate_gate: dict[str, Any] | None = None          # gate results for transparency
    materiality_threshold: float = 0.0                   # materiality applied ($)
    material_flags: list[str] = field(default_factory=list)
    sig: str = _SIG
    disclaimer: str = (
        "Decision-support / research — NOT an audit, review, compilation, or CPA "
        "opinion. Formal opinions come only from a licensed partner CPA firm that "
        "engages the target."
    )


# --------------------------------------------------------------------------- #
# BLS OEWS / owner-comp calculator
# --------------------------------------------------------------------------- #
# Revenue-tier multiplier ladder — §11.3-C, editable per engagement.
# No published band exists (Investopedia gap confirmed by Founder research);
# this is a stated Aegira convention grounded in practitioner norms.
DEFAULT_REVENUE_TIER_MULTIPLIER: tuple[tuple[float, float], ...] = (
    (2_000_000, 1.00),        # < $2M revenue → owner-comp = BLS median × 1.00
    (10_000_000, 1.15),       # $2M–$10M     → × 1.15
    (50_000_000, 1.30),       # $10M–$50M    → × 1.30
    (float("inf"), 1.50),     # > $50M       → × 1.50
)


def revenue_tier_multiplier(
    revenue: float,
    ladder: tuple[tuple[float, float], ...] = DEFAULT_REVENUE_TIER_MULTIPLIER,
) -> float:
    """Return the multiplier applied to the BLS OEWS median for a given revenue.

    Ladder must be ordered by ascending ceiling. The first ceiling ≥ revenue
    wins; the last entry should carry `float("inf")` as its ceiling.
    """
    revenue = max(0.0, float(revenue))
    for ceiling, mult in ladder:
        if revenue < ceiling:
            return float(mult)
    return float(ladder[-1][1])


def owner_comp_market(
    bls_median: float,
    revenue: float,
    ladder: tuple[tuple[float, float], ...] = DEFAULT_REVENUE_TIER_MULTIPLIER,
) -> float:
    """Compute the market owner-compensation from a BLS OEWS median and revenue.

    ``market_comp = bls_median × revenue-tier multiplier``
    """
    return float(bls_median) * revenue_tier_multiplier(revenue, ladder)


def owner_comp_adjustment(
    reported_comp: float,
    bls_median: float,
    revenue: float,
    ladder: tuple[tuple[float, float], ...] = DEFAULT_REVENUE_TIER_MULTIPLIER,
) -> float:
    """Return the EBITDA add-back for owner compensation (seller-view positive
    when the reported comp EXCEEDS market, seller-view negative when it is
    below market — a buyer-side deflation).

    Sign convention: **returned value is added to EBITDA.**
        reported_comp > market  →  positive (owner overpay: buyer will reduce
                                    compensation → add-back)
        reported_comp < market  →  negative (owner underpay: buyer must add
                                    market comp → deduction)
    """
    market = owner_comp_market(bls_median, revenue, ladder)
    return float(reported_comp) - market


# --------------------------------------------------------------------------- #
# Run-rate stability gate (Liberto rule — §11.3-B)
# --------------------------------------------------------------------------- #
DEFAULT_RUN_RATE_COV_LIMIT: float = 0.30
DEFAULT_RUN_RATE_MIN_MONTHS: int = 24


@dataclass
class RunRateGateResult:
    passed: bool
    reason: str
    cov: float | None
    months: int
    operational_anchor: str
    seasonality_flag: bool


def _coefficient_of_variation(series: list[float]) -> float | None:
    clean = [float(v) for v in series if v is not None and math.isfinite(float(v))]
    if len(clean) < 2:
        return None
    mean = statistics.mean(clean)
    if mean == 0:
        return None
    stdev = statistics.pstdev(clean)
    return abs(stdev / mean)


def _seasonality_flag(monthly: list[float]) -> bool:
    """Cheap seasonality heuristic: within the trailing ≥12-month window, group by
    calendar-month position and check whether the ratio of the max-month mean to
    the min-month mean exceeds 1.5×. Deliberately conservative — this is a gate,
    not a decomposition. Returns True when seasonality is present.
    """
    if len(monthly) < 12:
        return False
    tail = monthly[-24:] if len(monthly) >= 24 else monthly[-12:]
    buckets: dict[int, list[float]] = {}
    for i, val in enumerate(tail):
        if val is None or not math.isfinite(val):
            continue
        buckets.setdefault(i % 12, []).append(float(val))
    means = [statistics.mean(v) for v in buckets.values() if v]
    if len(means) < 6:
        return False
    lo = min(means)
    hi = max(means)
    if lo <= 0:
        return True
    return (hi / lo) > 1.5


def run_rate_stability_gate(
    monthly_revenue: list[float],
    operational_anchor: str,
    cov_limit: float = DEFAULT_RUN_RATE_COV_LIMIT,
    min_months: int = DEFAULT_RUN_RATE_MIN_MONTHS,
) -> RunRateGateResult:
    """Enforce the Liberto rule deterministically before any run-rate
    annualization is permitted.

    Requires:
      - ``len(monthly_revenue) >= min_months``
      - coefficient of variation < ``cov_limit`` (default 0.30)
      - seasonality bucket-ratio < 1.5×
      - an ``operational_anchor`` string (contract / capacity / pricing)
    """
    months = sum(
        1 for v in monthly_revenue if v is not None and math.isfinite(float(v))
    )
    if months < min_months:
        return RunRateGateResult(
            passed=False,
            reason=f"Insufficient monthly detail — {months} of {min_months} required.",
            cov=None, months=months, operational_anchor=operational_anchor,
            seasonality_flag=False,
        )
    cov = _coefficient_of_variation(monthly_revenue)
    if cov is None:
        return RunRateGateResult(
            passed=False,
            reason="Coefficient of variation unavailable (constant or missing series).",
            cov=None, months=months, operational_anchor=operational_anchor,
            seasonality_flag=False,
        )
    if cov >= cov_limit:
        return RunRateGateResult(
            passed=False,
            reason=(
                f"Volatility gate — COV {cov:.2f} ≥ limit {cov_limit:.2f}. "
                "Liberto rule blocks annualization for volatile series."
            ),
            cov=cov, months=months, operational_anchor=operational_anchor,
            seasonality_flag=False,
        )
    if _seasonality_flag(monthly_revenue):
        return RunRateGateResult(
            passed=False,
            reason=(
                "Seasonality detected — bucket max/min ratio > 1.5×. "
                "Use seasonality-adjusted normalization instead of run-rate."
            ),
            cov=cov, months=months, operational_anchor=operational_anchor,
            seasonality_flag=True,
        )
    if not operational_anchor or not operational_anchor.strip():
        return RunRateGateResult(
            passed=False,
            reason=(
                "Operational anchor missing — cite the contract / capacity / "
                "pricing change that supports the step-change."
            ),
            cov=cov, months=months, operational_anchor="",
            seasonality_flag=False,
        )
    return RunRateGateResult(
        passed=True,
        reason="Stability gate passed.",
        cov=cov, months=months, operational_anchor=operational_anchor,
        seasonality_flag=False,
    )


# --------------------------------------------------------------------------- #
# Category registry
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class AdjustmentCategory:
    id: str
    name: str
    reference: str
    default_recurrence: Recurrence
    default_side: Side


CATEGORIES: dict[str, AdjustmentCategory] = {
    c.id: c for c in [
        AdjustmentCategory("owner_comp_market", "Owner / executive compensation to market",
                           "Replacement-cost doctrine (§11.1D) + BLS OEWS",
                           Recurrence.RECURRING, Side.BOTH),
        AdjustmentCategory("related_party_rent", "Related-party rent to fair-market rent",
                           "ASC 850 Related Party Disclosures + CoStar / LoopNet",
                           Recurrence.RECURRING, Side.BOTH),
        AdjustmentCategory("related_party_services", "Related-party service arrangements",
                           "ASC 850 Related Party Disclosures",
                           Recurrence.RECURRING, Side.BOTH),
        AdjustmentCategory("personal_expenses", "Personal / non-business expenses",
                           "Reg S-K Item 10(e); practitioner convention",
                           Recurrence.RECURRING, Side.SELLER),
        AdjustmentCategory("one_time_legal", "One-time legal / settlement expenses",
                           "ASC 450 Contingencies (closed matters only)",
                           Recurrence.ONE_TIME, Side.SELLER),
        AdjustmentCategory("one_time_restructuring", "One-time restructuring / severance",
                           "ASC 420 Exit or Disposal Cost Obligations",
                           Recurrence.ONE_TIME, Side.SELLER),
        AdjustmentCategory("discontinued_operations", "Discontinued / divested operations",
                           "ASC 205-20 Discontinued Operations / IFRS 5",
                           Recurrence.ONE_TIME, Side.BOTH),
        AdjustmentCategory("non_recurring_bad_debt", "Non-recurring bad-debt write-offs",
                           "ASC 326 Financial Instruments — Credit Losses",
                           Recurrence.ONE_TIME, Side.SELLER),
        AdjustmentCategory("asset_sale_gain_loss", "One-time gain / loss on asset sale",
                           "ASC 610-20 Gains and Losses from Derecognition",
                           Recurrence.ONE_TIME, Side.BOTH),
        AdjustmentCategory("insurance_recovery", "Insurance / catastrophe recovery",
                           "Evidence + recurrence test (§11.1C)",
                           Recurrence.ONE_TIME, Side.BOTH),
        AdjustmentCategory("timing_deferred_revenue", "Deferred-revenue / cash-vs-accrual timing",
                           "ASC 606 Revenue from Contracts",
                           Recurrence.RECURRING, Side.BOTH),
        AdjustmentCategory("founder_benefits", "Founder-only healthcare / benefits",
                           "Replacement-cost doctrine (§11.1D)",
                           Recurrence.RECURRING, Side.BOTH),
        AdjustmentCategory("key_contracts_off_market", "Above / below-market key contracts",
                           "ASC 805 purchase-accounting analog",
                           Recurrence.RECURRING, Side.BOTH),
        AdjustmentCategory("pro_forma_synergies", "Pro-forma synergies (BUYER-SIDE FLAG ONLY)",
                           "Practitioner convention — never in seller bridge",
                           Recurrence.FLAG_ONLY, Side.BUYER),
        AdjustmentCategory("run_rate_revenue", "Run-rate revenue adjustments",
                           "Liberto stability gate (§11.1E + §11.3-B)",
                           Recurrence.ONE_TIME, Side.SELLER),
        AdjustmentCategory("discontinued_product_line",
                           "Discontinued product-line contribution margin",
                           "ASC 205-20 analog (below-component exit)",
                           Recurrence.ONE_TIME, Side.BOTH),
        AdjustmentCategory("covid_anomalies", "COVID / pandemic-era anomalies",
                           "Evidence + recurrence test (§11.1C)",
                           Recurrence.ONE_TIME, Side.BOTH),
        AdjustmentCategory("litigation_open_reserves", "Litigation-in-progress reserves",
                           "ASC 450 Contingencies — NEVER removed while open",
                           Recurrence.FLAG_ONLY, Side.SELLER),
        AdjustmentCategory("stock_based_compensation", "Non-cash stock-based compensation",
                           "ASC 718 — default: NO add-back",
                           Recurrence.RECURRING, Side.SELLER),
        AdjustmentCategory("accounting_policy_change", "Change in accounting policy",
                           "ASC 250 Accounting Changes and Error Corrections",
                           Recurrence.ONE_TIME, Side.BOTH),
    ]
}


# --------------------------------------------------------------------------- #
# Category-specific rules that require extras / guardrails
# --------------------------------------------------------------------------- #
def _related_party_rent_evidence_ok(adj: AdjustmentInput) -> tuple[bool, str]:
    """§11.3-D: related-party rent requires at least one third-party benchmark
    at grade A/B. C-grade owner assertion is blocked without override."""
    if adj.evidence_grade == EvidenceGrade.C and not adj.evidence_c_override:
        return False, (
            "Related-party rent requires a third-party benchmark "
            "(broker letter, CoStar / LoopNet comp) at evidence grade A or B. "
            "C-grade owner assertion blocked."
        )
    return True, ""


def _apply_stock_based_comp(adj: AdjustmentInput) -> tuple[float, list[str]]:
    """§11.2 #19: DEFAULT is no add-back for SBC. Only when both:
      - plan is closed post-close (extras['plan_closed_post_close'] = True)
      - not being replaced with equivalent cash comp
        (extras['not_replaced_with_cash'] = True)
    is the SBC amount added back.
    """
    plan_closed = bool(adj.extras.get("plan_closed_post_close", False))
    not_replaced = bool(adj.extras.get("not_replaced_with_cash", False))
    if plan_closed and not_replaced:
        return adj.amount * adj.sign, [
            "SBC add-back applied: plan closed post-close AND not replaced with cash comp."
        ]
    return 0.0, [
        "SBC add-back suppressed (default) — SBC is a real cost of retaining talent. "
        "Set extras['plan_closed_post_close']=True AND extras['not_replaced_with_cash']=True to add back."
    ]


def _apply_run_rate(adj: AdjustmentInput) -> tuple[float, RunRateGateResult, list[str]]:
    """§11.2 #15 + §11.3-B: enforce the stability gate before applying."""
    monthly = adj.extras.get("monthly_revenue") or []
    anchor = adj.extras.get("operational_anchor", "")
    gate = run_rate_stability_gate(list(monthly), anchor)
    if not gate.passed:
        return 0.0, gate, [f"Run-rate adjustment BLOCKED: {gate.reason}"]
    return adj.amount * adj.sign, gate, ["Run-rate adjustment applied (stability gate passed)."]


def _apply_flag_only(adj: AdjustmentInput, category: AdjustmentCategory) -> tuple[float, list[str]]:
    """§11.2 #14 / #18: pro-forma synergies + open-litigation reserves. Value flows
    to the buyer-view side (for synergies) and is otherwise flagged only."""
    if category.id == "pro_forma_synergies":
        return 0.0, [
            "Pro-forma synergies FLAGGED (buyer view only) — not applied in seller "
            "bridge; carried as buyer's own realization risk."
        ]
    if category.id == "litigation_open_reserves":
        return 0.0, [
            "Open-litigation reserves NEVER removed (ASC 450). Adjustment recorded "
            "as a flag; reserve stays in EBITDA."
        ]
    return 0.0, []


# --------------------------------------------------------------------------- #
# Materiality (§10.9 + §11.4-C)
# --------------------------------------------------------------------------- #
DEFAULT_MATERIALITY_PCT: float = 0.05          # 5% of reported EBITDA
DEFAULT_MATERIALITY_FLOOR: float = 50_000.0    # or $50k floor, whichever greater


def materiality_threshold(
    reported_ebitda: float,
    pct: float = DEFAULT_MATERIALITY_PCT,
    floor: float = DEFAULT_MATERIALITY_FLOOR,
) -> float:
    return max(abs(float(reported_ebitda)) * pct, float(floor))


# --------------------------------------------------------------------------- #
# Bridge builder
# --------------------------------------------------------------------------- #
@dataclass
class BridgeInput:
    business_name: str
    period_label: str = "Most recent FY"
    reported_ebitda: float = 0.0
    ltm_ebitda: float | None = None
    three_year_avg_ebitda: float | None = None
    materiality_pct: float = DEFAULT_MATERIALITY_PCT
    materiality_floor: float = DEFAULT_MATERIALITY_FLOOR
    adjustments: list[AdjustmentInput] = field(default_factory=list)


def _driver_note(adj: AdjustmentInput, cat: AdjustmentCategory, applied: float) -> str:
    """Deterministic, house-style driver note for one adjustment. Reserved-opinion
    vocabulary lint is enforced by the caller."""
    direction = "add-back" if applied >= 0 else "deduction"
    amt = f"${abs(applied):,.0f}"
    parts = [f"{cat.name}: {direction} of {amt}."]
    if adj.evidence_source:
        parts.append(f"Source: {adj.evidence_source}.")
    if adj.note:
        parts.append(adj.note)
    parts.append(f"Reference: {cat.reference}.")
    text = " ".join(parts)
    return text


def evaluate_adjustment(
    adj: AdjustmentInput,
) -> AdjustmentOutcome:
    """Evaluate a single adjustment against category rules + guardrails."""
    cat = CATEGORIES.get(adj.category_id)
    if cat is None:
        raise ValueError(f"Unknown adjustment category: {adj.category_id!r}")

    recurrence = adj.recurrence or cat.default_recurrence
    warnings: list[str] = []
    blocked = False
    block_reason = ""

    # Evidence grade C requires explicit override (§11.3-A)
    if adj.evidence_grade == EvidenceGrade.C and not adj.evidence_c_override:
        blocked = True
        block_reason = (
            "Evidence grade C not permitted without evidence_c_override=True and a "
            "written rationale in the working-paper artifact."
        )

    # Related-party rent additional guardrail (§11.3-D)
    if not blocked and cat.id == "related_party_rent":
        ok, reason = _related_party_rent_evidence_ok(adj)
        if not ok:
            blocked = True
            block_reason = reason

    if blocked:
        return AdjustmentOutcome(
            category_id=cat.id,
            category_name=cat.name,
            seller_amount=0.0,
            buyer_amount=0.0,
            evidence_grade=adj.evidence_grade,
            recurrence=recurrence,
            reference=cat.reference,
            driver_note=f"BLOCKED: {block_reason}",
            blocked=True,
            block_reason=block_reason,
            warnings=warnings,
        )

    # Compute the applied amount per category-specific rule
    applied: float
    if cat.id == "stock_based_compensation":
        applied, extra_warnings = _apply_stock_based_comp(adj)
        warnings.extend(extra_warnings)
    elif cat.id == "run_rate_revenue":
        applied, gate, extra_warnings = _apply_run_rate(adj)
        warnings.extend(extra_warnings)
        if not gate.passed:
            return AdjustmentOutcome(
                category_id=cat.id,
                category_name=cat.name,
                seller_amount=0.0,
                buyer_amount=0.0,
                evidence_grade=adj.evidence_grade,
                recurrence=Recurrence.FLAG_ONLY,
                reference=cat.reference,
                driver_note=f"BLOCKED: {gate.reason}",
                blocked=True,
                block_reason=gate.reason,
                warnings=warnings,
            )
    elif recurrence == Recurrence.FLAG_ONLY:
        applied, extra_warnings = _apply_flag_only(adj, cat)
        warnings.extend(extra_warnings)
    elif cat.id == "litigation_open_reserves":
        applied = 0.0
        warnings.append(
            "Open litigation — reserve stays in EBITDA (ASC 450). Only closeout "
            "movements after settlement qualify for adjustment."
        )
    else:
        applied = adj.amount * adj.sign

    # Side application
    side = adj.side if adj.side is not None else cat.default_side
    if cat.id == "pro_forma_synergies":
        seller_amt = 0.0
        buyer_amt = adj.amount * adj.sign
    elif side == Side.SELLER:
        seller_amt = applied
        buyer_amt = 0.0
    elif side == Side.BUYER:
        seller_amt = 0.0
        buyer_amt = applied
    else:  # BOTH
        seller_amt = applied
        buyer_amt = applied

    driver = _driver_note(adj, cat, applied)
    hits = lint_reserved_vocabulary(driver)
    if hits:
        warnings.append(
            f"Driver note contained reserved-opinion words {hits}; scrubbed."
        )
        driver = " " + driver + " "
        for w in hits:
            driver = driver.replace(f" {w} ", " [reserved] ")
            driver = driver.replace(f" {w}.", " [reserved].")
        driver = driver.strip()

    return AdjustmentOutcome(
        category_id=cat.id,
        category_name=cat.name,
        seller_amount=seller_amt,
        buyer_amount=buyer_amt,
        evidence_grade=adj.evidence_grade,
        recurrence=recurrence,
        reference=cat.reference,
        driver_note=driver,
        blocked=False,
        block_reason="",
        warnings=warnings,
    )


def build_bridge(inp: BridgeInput) -> EBITDABridge:
    """Assemble the full EBITDA bridge from category-evaluated adjustments."""
    reported = float(inp.reported_ebitda)
    seller_total = reported
    buyer_total = reported
    outcomes: list[AdjustmentOutcome] = []
    blocked: list[AdjustmentOutcome] = []
    warnings: list[str] = []
    run_rate_gate_result: dict[str, Any] | None = None

    for adj in inp.adjustments:
        outcome = evaluate_adjustment(adj)
        if adj.category_id == "run_rate_revenue":
            # capture the gate result for transparency even if it blocked
            gate = adj.extras.get("_gate_snapshot")
            if gate is None:
                # re-run gate (cheap) to snapshot for the output
                gate = run_rate_stability_gate(
                    list(adj.extras.get("monthly_revenue") or []),
                    adj.extras.get("operational_anchor", ""),
                )
            run_rate_gate_result = {
                "passed": gate.passed,
                "reason": gate.reason,
                "cov": gate.cov,
                "months": gate.months,
                "operational_anchor": gate.operational_anchor,
                "seasonality_flag": gate.seasonality_flag,
            }
        if outcome.blocked:
            blocked.append(outcome)
            warnings.extend(outcome.warnings)
            continue
        seller_total += outcome.seller_amount
        buyer_total += outcome.buyer_amount
        outcomes.append(outcome)
        warnings.extend(outcome.warnings)

    mat = materiality_threshold(reported, inp.materiality_pct, inp.materiality_floor)
    material_flags: list[str] = []
    for oc in outcomes:
        if abs(oc.seller_amount) >= mat or abs(oc.buyer_amount) >= mat:
            amt = max(abs(oc.seller_amount), abs(oc.buyer_amount))
            material_flags.append(
                f"{oc.category_name} — ${amt:,.0f} (≥ materiality ${mat:,.0f})"
            )

    # Run-rate presentation: only surface run_rate_ebitda if the gate passed
    run_rate_ebitda: float | None = None
    if run_rate_gate_result and run_rate_gate_result["passed"]:
        rr_delta = sum(
            oc.seller_amount for oc in outcomes if oc.category_id == "run_rate_revenue"
        )
        run_rate_ebitda = reported + rr_delta

    return EBITDABridge(
        business_name=inp.business_name,
        period_label=inp.period_label,
        reported_ebitda=reported,
        adjusted_ebitda_seller=seller_total,
        adjusted_ebitda_buyer=buyer_total,
        adjustments=outcomes,
        blocked_adjustments=blocked,
        warnings=warnings,
        ltm_ebitda=inp.ltm_ebitda,
        run_rate_ebitda=run_rate_ebitda,
        three_year_avg_ebitda=inp.three_year_avg_ebitda,
        run_rate_gate=run_rate_gate_result,
        materiality_threshold=mat,
        material_flags=material_flags,
    )


# --------------------------------------------------------------------------- #
# Public constants exported for other modules (workbook renderer, tests, …)
# --------------------------------------------------------------------------- #
__all__ = [
    "AdjustmentCategory",
    "AdjustmentInput",
    "AdjustmentOutcome",
    "BridgeInput",
    "CATEGORIES",
    "DEFAULT_MATERIALITY_FLOOR",
    "DEFAULT_MATERIALITY_PCT",
    "DEFAULT_REVENUE_TIER_MULTIPLIER",
    "DEFAULT_RUN_RATE_COV_LIMIT",
    "DEFAULT_RUN_RATE_MIN_MONTHS",
    "EBITDABridge",
    "EvidenceGrade",
    "Recurrence",
    "RESERVED_OPINION_WORDS",
    "RunRateGateResult",
    "Side",
    "build_bridge",
    "evaluate_adjustment",
    "lint_reserved_vocabulary",
    "materiality_threshold",
    "owner_comp_adjustment",
    "owner_comp_market",
    "revenue_tier_multiplier",
    "run_rate_stability_gate",
]
