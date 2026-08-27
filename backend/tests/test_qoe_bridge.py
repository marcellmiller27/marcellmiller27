# JHI-SIG: 69M2705M | QoE bridge tests | JHI Research & Analytics Firm, Inc. (proprietary)
"""Unit tests for the QoE / EBITDA bridge engine (§11 of board minutes)."""

from __future__ import annotations

import math

import pytest

from app.qoe_bridge import (
    CATEGORIES,
    DEFAULT_REVENUE_TIER_MULTIPLIER,
    AdjustmentInput,
    BridgeInput,
    EvidenceGrade,
    Recurrence,
    RESERVED_OPINION_WORDS,
    Side,
    build_bridge,
    evaluate_adjustment,
    lint_reserved_vocabulary,
    materiality_threshold,
    owner_comp_adjustment,
    owner_comp_market,
    revenue_tier_multiplier,
    run_rate_stability_gate,
)


# --------------------------------------------------------------------------- #
# Category registry
# --------------------------------------------------------------------------- #
def test_20_categories_registered():
    """§11.2 — the 20-category adjustment library must be complete."""
    assert len(CATEGORIES) == 20
    # spot-check known ids from §11.2
    for cid in [
        "owner_comp_market",
        "related_party_rent",
        "related_party_services",
        "personal_expenses",
        "one_time_legal",
        "one_time_restructuring",
        "discontinued_operations",
        "non_recurring_bad_debt",
        "asset_sale_gain_loss",
        "insurance_recovery",
        "timing_deferred_revenue",
        "founder_benefits",
        "key_contracts_off_market",
        "pro_forma_synergies",
        "run_rate_revenue",
        "discontinued_product_line",
        "covid_anomalies",
        "litigation_open_reserves",
        "stock_based_compensation",
        "accounting_policy_change",
    ]:
        assert cid in CATEGORIES, f"missing category {cid}"


def test_every_category_has_authoritative_reference():
    for cat in CATEGORIES.values():
        assert cat.reference and cat.reference.strip(), f"{cat.id} missing reference"
        assert cat.name and cat.name.strip(), f"{cat.id} missing name"


# --------------------------------------------------------------------------- #
# Reserved-opinion vocabulary lint
# --------------------------------------------------------------------------- #
def test_lint_reserved_vocab_catches_audit_words():
    hits = lint_reserved_vocabulary("This is our audit opinion on the target.")
    assert "audit" in hits or "opinion" in hits


def test_lint_reserved_vocab_catches_fair_presentation_phrase():
    hits = lint_reserved_vocabulary(
        "Management presents the statements with fair presentation and full disclosure."
    )
    assert "fair presentation" in hits


def test_lint_reserved_vocab_clean_pass():
    assert lint_reserved_vocabulary(
        "This is decision-support analysis; not an assurance engagement."
    ) == []


def test_reserved_vocab_constant_shape():
    assert "audit" in RESERVED_OPINION_WORDS
    assert "opinion" in RESERVED_OPINION_WORDS
    assert "fair presentation" in RESERVED_OPINION_WORDS
    assert "attest" in RESERVED_OPINION_WORDS


# --------------------------------------------------------------------------- #
# Evidence-grade enforcement (§11.3-A)
# --------------------------------------------------------------------------- #
def test_grade_c_blocked_without_override():
    outcome = evaluate_adjustment(AdjustmentInput(
        category_id="personal_expenses",
        amount=25_000,
        evidence_grade=EvidenceGrade.C,
    ))
    assert outcome.blocked
    assert "evidence grade c" in outcome.block_reason.lower()
    assert outcome.seller_amount == 0
    assert outcome.buyer_amount == 0


def test_grade_c_allowed_with_override():
    outcome = evaluate_adjustment(AdjustmentInput(
        category_id="personal_expenses",
        amount=25_000,
        evidence_grade=EvidenceGrade.C,
        evidence_c_override=True,
    ))
    assert not outcome.blocked
    assert outcome.seller_amount > 0


def test_related_party_rent_blocks_c_evidence():
    outcome = evaluate_adjustment(AdjustmentInput(
        category_id="related_party_rent",
        amount=50_000,
        evidence_grade=EvidenceGrade.C,
    ))
    assert outcome.blocked


def test_related_party_rent_accepts_a_grade_benchmark():
    outcome = evaluate_adjustment(AdjustmentInput(
        category_id="related_party_rent",
        amount=50_000,
        evidence_grade=EvidenceGrade.A,
        evidence_source="CoStar comparable #12345 · 2026-01",
    ))
    assert not outcome.blocked
    assert outcome.seller_amount == 50_000


# --------------------------------------------------------------------------- #
# Owner-comp calculator
# --------------------------------------------------------------------------- #
def test_revenue_tier_multiplier_bands():
    assert revenue_tier_multiplier(500_000) == 1.00
    assert revenue_tier_multiplier(1_999_999) == 1.00
    assert revenue_tier_multiplier(2_000_000) == 1.15
    assert revenue_tier_multiplier(9_999_999) == 1.15
    assert revenue_tier_multiplier(10_000_000) == 1.30
    assert revenue_tier_multiplier(49_999_999) == 1.30
    assert revenue_tier_multiplier(50_000_000) == 1.50
    assert revenue_tier_multiplier(500_000_000) == 1.50


def test_owner_comp_market_math():
    # BLS median $150k, $5M revenue → $150k × 1.15 = $172.5k
    assert owner_comp_market(150_000, 5_000_000) == pytest.approx(172_500)


def test_owner_comp_overpay_add_back():
    adj = owner_comp_adjustment(
        reported_comp=400_000, bls_median=150_000, revenue=5_000_000
    )
    # 400k − (150k × 1.15) = 227.5k add-back
    assert adj == pytest.approx(227_500)


def test_owner_comp_underpay_deduction():
    adj = owner_comp_adjustment(
        reported_comp=100_000, bls_median=150_000, revenue=5_000_000
    )
    assert adj < 0
    assert adj == pytest.approx(-72_500)


def test_revenue_tier_ladder_shape():
    for ceiling, mult in DEFAULT_REVENUE_TIER_MULTIPLIER:
        assert mult > 0
    # last band must be inf
    assert DEFAULT_REVENUE_TIER_MULTIPLIER[-1][0] == float("inf")


# --------------------------------------------------------------------------- #
# Run-rate stability gate (Liberto rule — §11.3-B)
# --------------------------------------------------------------------------- #
def _flat_monthly(base: float, months: int = 30) -> list[float]:
    return [base for _ in range(months)]


def _seasonal_monthly(base: float, months: int = 36) -> list[float]:
    return [base * (1.0 + (0.6 if (i % 12) in (10, 11) else -0.2)) for i in range(months)]


def _volatile_monthly(base: float, months: int = 30) -> list[float]:
    return [base * (2.0 if i % 3 == 0 else 0.4) for i in range(months)]


def test_run_rate_gate_passes_on_stable_series_with_anchor():
    gate = run_rate_stability_gate(
        _flat_monthly(100_000), operational_anchor="Acme MSA contract signed 2026-Q1"
    )
    assert gate.passed
    assert gate.months >= 24
    assert gate.cov is not None and gate.cov < 0.30


def test_run_rate_gate_blocks_on_missing_anchor():
    gate = run_rate_stability_gate(_flat_monthly(100_000), operational_anchor="")
    assert not gate.passed
    assert "anchor" in gate.reason.lower()


def test_run_rate_gate_blocks_on_short_history():
    gate = run_rate_stability_gate(
        _flat_monthly(100_000, months=12), operational_anchor="anchor"
    )
    assert not gate.passed
    assert "insufficient" in gate.reason.lower() or "12" in gate.reason


def test_run_rate_gate_blocks_on_seasonality():
    gate = run_rate_stability_gate(
        _seasonal_monthly(100_000), operational_anchor="anchor"
    )
    assert not gate.passed
    # either the volatility gate OR the seasonality gate rejects seasonal data —
    # in either case, run-rate MUST be blocked (Liberto rule).
    assert not gate.passed


def test_run_rate_gate_blocks_on_high_volatility():
    gate = run_rate_stability_gate(
        _volatile_monthly(100_000), operational_anchor="anchor"
    )
    assert not gate.passed


def test_run_rate_adjustment_blocked_end_to_end():
    """A run-rate adjustment must be BLOCKED by the bridge builder when the
    stability gate fails."""
    adjustment = AdjustmentInput(
        category_id="run_rate_revenue",
        amount=300_000,
        sign=+1,
        evidence_grade=EvidenceGrade.B,
        extras={
            "monthly_revenue": _volatile_monthly(100_000),
            "operational_anchor": "new contract",
        },
    )
    bridge = build_bridge(BridgeInput(
        business_name="TestCo",
        reported_ebitda=1_000_000,
        adjustments=[adjustment],
    ))
    assert bridge.adjusted_ebitda_seller == 1_000_000  # unchanged
    assert bridge.run_rate_ebitda is None
    assert bridge.run_rate_gate is not None
    assert bridge.run_rate_gate["passed"] is False
    assert any(oc.category_id == "run_rate_revenue" for oc in bridge.blocked_adjustments)


def test_run_rate_adjustment_passes_with_stable_anchor():
    adjustment = AdjustmentInput(
        category_id="run_rate_revenue",
        amount=200_000,
        sign=+1,
        evidence_grade=EvidenceGrade.A,
        extras={
            "monthly_revenue": _flat_monthly(120_000),
            "operational_anchor": "Enterprise MSA signed 2026-Q1",
        },
    )
    bridge = build_bridge(BridgeInput(
        business_name="TestCo",
        reported_ebitda=1_000_000,
        adjustments=[adjustment],
    ))
    assert bridge.adjusted_ebitda_seller == 1_200_000
    assert bridge.run_rate_ebitda == 1_200_000


# --------------------------------------------------------------------------- #
# Stock-based compensation — DEFAULT: no add-back
# --------------------------------------------------------------------------- #
def test_sbc_default_is_no_addback():
    outcome = evaluate_adjustment(AdjustmentInput(
        category_id="stock_based_compensation",
        amount=500_000,
        evidence_grade=EvidenceGrade.A,
    ))
    assert not outcome.blocked
    assert outcome.seller_amount == 0
    assert outcome.buyer_amount == 0


def test_sbc_addback_applies_only_with_both_flags():
    outcome = evaluate_adjustment(AdjustmentInput(
        category_id="stock_based_compensation",
        amount=500_000,
        evidence_grade=EvidenceGrade.A,
        extras={"plan_closed_post_close": True, "not_replaced_with_cash": True},
    ))
    assert outcome.seller_amount == 500_000


def test_sbc_addback_suppressed_when_only_one_flag():
    outcome = evaluate_adjustment(AdjustmentInput(
        category_id="stock_based_compensation",
        amount=500_000,
        evidence_grade=EvidenceGrade.A,
        extras={"plan_closed_post_close": True},  # missing not_replaced_with_cash
    ))
    assert outcome.seller_amount == 0


# --------------------------------------------------------------------------- #
# Flag-only categories — pro-forma synergies + open litigation reserves
# --------------------------------------------------------------------------- #
def test_pro_forma_synergies_never_in_seller_view():
    outcome = evaluate_adjustment(AdjustmentInput(
        category_id="pro_forma_synergies",
        amount=1_000_000,
        evidence_grade=EvidenceGrade.B,
    ))
    assert outcome.seller_amount == 0
    assert outcome.buyer_amount == 1_000_000
    assert outcome.recurrence == Recurrence.FLAG_ONLY


def test_open_litigation_reserves_stay_in_ebitda():
    outcome = evaluate_adjustment(AdjustmentInput(
        category_id="litigation_open_reserves",
        amount=250_000,
        evidence_grade=EvidenceGrade.A,
    ))
    assert outcome.seller_amount == 0
    assert outcome.buyer_amount == 0


# --------------------------------------------------------------------------- #
# Buyer vs seller side divergence
# --------------------------------------------------------------------------- #
def test_seller_and_buyer_views_diverge_when_side_seller_only():
    adjustments = [
        AdjustmentInput(
            category_id="personal_expenses",
            amount=30_000,
            side=Side.SELLER,
            evidence_grade=EvidenceGrade.B,
            evidence_source="Expense-report sample n=142",
        ),
    ]
    bridge = build_bridge(BridgeInput(
        business_name="TestCo",
        reported_ebitda=1_000_000,
        adjustments=adjustments,
    ))
    assert bridge.adjusted_ebitda_seller == 1_030_000
    assert bridge.adjusted_ebitda_buyer == 1_000_000


def test_seller_and_buyer_views_equal_when_side_both():
    adjustments = [
        AdjustmentInput(
            category_id="owner_comp_market",
            amount=100_000,
            side=Side.BOTH,
            evidence_grade=EvidenceGrade.A,
            evidence_source="BLS OEWS 11-1021 · Chicago · 2025",
        ),
    ]
    bridge = build_bridge(BridgeInput(
        business_name="TestCo",
        reported_ebitda=1_000_000,
        adjustments=adjustments,
    ))
    assert bridge.adjusted_ebitda_seller == 1_100_000
    assert bridge.adjusted_ebitda_buyer == 1_100_000


# --------------------------------------------------------------------------- #
# Materiality
# --------------------------------------------------------------------------- #
def test_materiality_uses_greater_of_pct_or_floor():
    # 5% of $2M EBITDA = $100k > $50k floor → $100k
    assert materiality_threshold(2_000_000) == 100_000
    # 5% of $200k EBITDA = $10k < $50k floor → $50k
    assert materiality_threshold(200_000) == 50_000


def test_material_flags_populated():
    adjustments = [
        AdjustmentInput(
            category_id="one_time_legal",
            amount=200_000,
            side=Side.SELLER,
            evidence_grade=EvidenceGrade.A,
            evidence_source="Matter #45231 closed 2026-Q1",
        ),
        AdjustmentInput(
            category_id="personal_expenses",
            amount=8_000,          # well below materiality
            side=Side.SELLER,
            evidence_grade=EvidenceGrade.B,
        ),
    ]
    bridge = build_bridge(BridgeInput(
        business_name="TestCo",
        reported_ebitda=1_000_000,
        adjustments=adjustments,
    ))
    # Materiality = max(5% × 1M, 50k) = 50k. 200k qualifies; 8k doesn't.
    assert len(bridge.material_flags) == 1
    assert "One-time legal" in bridge.material_flags[0]


# --------------------------------------------------------------------------- #
# Full-bridge disclaimer + signature
# --------------------------------------------------------------------------- #
def test_bridge_carries_disclaimer_and_signature():
    bridge = build_bridge(BridgeInput(
        business_name="TestCo",
        reported_ebitda=500_000,
        adjustments=[],
    ))
    assert "audit" not in bridge.disclaimer.lower() or "not an audit" in bridge.disclaimer.lower()
    assert "not an audit" in bridge.disclaimer.lower()
    assert bridge.sig == "JHI-SIG: 69M2705M"


def test_bridge_driver_notes_lint_clean():
    """No driver note may leak reserved-opinion vocabulary out to the deliverable."""
    adjustments = [
        AdjustmentInput(
            category_id="owner_comp_market",
            amount=50_000,
            evidence_grade=EvidenceGrade.A,
            evidence_source="BLS OEWS 11-1021 · Chicago · 2025",
            note="Owner drew $200k above the benchmarked comp band.",
        ),
    ]
    bridge = build_bridge(BridgeInput(
        business_name="TestCo",
        reported_ebitda=1_000_000,
        adjustments=adjustments,
    ))
    for oc in bridge.adjustments:
        assert lint_reserved_vocabulary(oc.driver_note) == [], (
            f"driver note leaked reserved vocab: {oc.driver_note!r}"
        )


def test_unknown_category_raises():
    with pytest.raises(ValueError):
        evaluate_adjustment(AdjustmentInput(
            category_id="not_a_real_category",
            amount=10_000,
        ))


# --------------------------------------------------------------------------- #
# NaN / inf inputs handled gracefully
# --------------------------------------------------------------------------- #
def test_bridge_handles_zero_reported():
    bridge = build_bridge(BridgeInput(
        business_name="TestCo",
        reported_ebitda=0.0,
        adjustments=[],
    ))
    assert bridge.adjusted_ebitda_seller == 0
    assert bridge.adjusted_ebitda_buyer == 0
    assert bridge.materiality_threshold >= 50_000  # floor kicks in


def test_run_rate_gate_handles_nan_gracefully():
    gate = run_rate_stability_gate(
        [math.nan] * 30, operational_anchor="anchor"
    )
    assert not gate.passed
