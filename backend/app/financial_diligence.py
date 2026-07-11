# JHI-SIG: 69M2705M | Financial Diligence Suite | John Henry Investments (proprietary)
"""Financial Diligence Suite engine — software-accelerated Quality-of-Earnings support.

Pure, deterministic computation (unit-testable). Runs the core buy-side QoE
procedures on user-supplied figures, produces a Financial Integrity Score, a
recommended assurance tier, add-on pricing, and a partner-CPA engagement quote.

NOT an audit, review, or CPA opinion. Formal assurance opinions are issued only by
a licensed partner CPA firm that engages the target entity.
"""

from __future__ import annotations

import uuid

from app.financial_diligence_models import (
    DiligenceInput,
    DiligenceReport,
    DiligenceTier,
    EngagementQuote,
    EngagementRequest,
    PricingBand,
    ProofOfCash,
    RevenueQuality,
    WorkingCapital,
)

# --- Product tiers -----------------------------------------------------------
TIERS: list[DiligenceTier] = [
    DiligenceTier(
        tier="A",
        name="Financial Integrity Screening",
        attest=False,
        delivered_by="JHI platform (automated)",
        description=(
            "Automated analytics on every active subscription: proof-of-cash flags, "
            "EBITDA normalization, working-capital and revenue-quality checks, and a "
            "Financial Integrity Score. Decision-support only — no assurance."
        ),
    ),
    DiligenceTier(
        tier="B",
        name="Quality of Earnings (buy-side FDD)",
        attest=False,
        delivered_by="Partner CPA (advisory, signed)",
        description=(
            "Software-accelerated QoE workpapers reviewed and signed by a licensed "
            "partner CPA as a non-attest advisory report. The flagship add-on for "
            "post-LOI diligence — faster and lower-cost than a manual engagement."
        ),
    ),
    DiligenceTier(
        tier="C",
        name="Formal attest (AUP / review / audit)",
        attest=True,
        delivered_by="Partner CPA firm (engages the target)",
        description=(
            "When a lender or the deal requires assurance, routed to a partner CPA "
            "firm that engages the target entity and issues under professional "
            "standards. The four opinions (Unqualified / Qualified / Adverse / "
            "Disclaimer) exist only here."
        ),
    ),
]

# --- Pricing bands (illustrative benchmarks, keyed by EBITDA/SDE) -------------
# (ebitda_ceiling, band, manual_low, manual_high, platform_low, platform_high, jhi_fee_low, jhi_fee_high)
_PRICING: list[tuple[float, str, float, float, float, float, float, float]] = [
    (1_000_000, "SBA / search-fund (SDE < $1M)", 15_000, 30_000, 3_900, 6_500, 1_500, 2_500),
    (3_000_000, "$1M–$3M EBITDA", 25_000, 50_000, 8_000, 16_000, 3_000, 5_000),
    (10_000_000, "$3M–$10M EBITDA", 40_000, 80_000, 18_000, 35_000, 6_000, 10_000),
    (float("inf"), "$10M–$20M EBITDA", 75_000, 150_000, 40_000, 70_000, 12_000, 20_000),
]

_DISCLAIMER = (
    "Software-generated financial due-diligence analysis / Quality-of-Earnings support — "
    "decision-support only. This is NOT an audit, review, compilation, or CPA opinion, and "
    "no assurance is expressed. Formal opinions (Unqualified / Qualified / Adverse / "
    "Disclaimer) are issued solely by a licensed partner CPA firm that engages the target "
    "entity. Verify all figures against source documents before making an offer."
)


def _clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))


def pricing_band(ebitda: float) -> PricingBand:
    for ceiling, band, m_lo, m_hi, p_lo, p_hi, f_lo, f_hi in _PRICING:
        if ebitda < ceiling:
            return PricingBand(
                band=band, manual_low=m_lo, manual_high=m_hi,
                platform_low=p_lo, platform_high=p_hi,
                jhi_software_fee_low=f_lo, jhi_software_fee_high=f_hi,
            )
    ceiling, band, m_lo, m_hi, p_lo, p_hi, f_lo, f_hi = _PRICING[-1]
    return PricingBand(
        band=band, manual_low=m_lo, manual_high=m_hi,
        platform_low=p_lo, platform_high=p_hi,
        jhi_software_fee_low=f_lo, jhi_software_fee_high=f_hi,
    )


def analyze(deal: DiligenceInput) -> DiligenceReport:
    revenue = deal.revenue
    reported = deal.reported_ebitda

    # --- EBITDA normalization: discount unsupported add-backs 50%, remove one-time items ---
    adjustment = 0.5 * deal.questionable_addbacks + deal.one_time_items
    adjusted_ebitda = max(0.0, reported - adjustment)

    red_flags: list[str] = []

    # --- Proof of cash ---
    if deal.bank_deposits is not None and deal.bank_deposits > 0:
        variance = (deal.bank_deposits - revenue) / revenue if revenue else 0.0
        if variance <= -0.05:
            flag = "Bank deposits trail reported revenue >5% — possible revenue overstatement."
            red_flags.append(flag)
        elif variance >= 0.10:
            flag = "Deposits exceed revenue >10% — confirm other income / financing inflows."
            red_flags.append(flag)
        else:
            flag = "Deposits reconcile to revenue within materiality."
        proof = ProofOfCash(
            checked=True, reported_revenue=round(revenue), bank_deposits=round(deal.bank_deposits),
            variance_pct=round(variance * 100, 1), flag=flag,
        )
    else:
        proof = ProofOfCash(
            checked=False, reported_revenue=round(revenue), bank_deposits=None,
            variance_pct=None, flag="No bank deposits supplied — proof-of-cash not performed.",
        )
        red_flags.append("Proof-of-cash not performed — request bank statements to tie out revenue.")

    # --- Net working capital ---
    nwc = deal.accounts_receivable + deal.inventory - deal.accounts_payable
    nwc_pct = (nwc / revenue) if revenue else 0.0
    wc = WorkingCapital(
        accounts_receivable=round(deal.accounts_receivable), inventory=round(deal.inventory),
        accounts_payable=round(deal.accounts_payable), net_working_capital=round(nwc),
        nwc_pct_of_revenue=round(nwc_pct * 100, 1),
        note=(
            f"NWC is {nwc_pct*100:.1f}% of revenue — the buyer must fund this peg at close. "
            "Negotiate a working-capital target in the LOI."
        ),
    )

    # --- Quality of revenue ---
    rq_score = 50.0 + deal.recurring_revenue_pct * 0.35
    rq_score -= _clamp((deal.customer_concentration_pct - 20) * 1.2, 0, 40)
    rq = RevenueQuality(
        recurring_revenue_pct=deal.recurring_revenue_pct,
        customer_concentration_pct=deal.customer_concentration_pct,
        score=int(_clamp(rq_score)),
        note=(
            f"{deal.recurring_revenue_pct:.0f}% recurring; top customer {deal.customer_concentration_pct:.0f}%."
        ),
    )
    if deal.customer_concentration_pct >= 35:
        red_flags.append(
            f"Customer concentration {deal.customer_concentration_pct:.0f}% — a churn of the top account is an existential risk."
        )

    # --- Add-back aggressiveness ---
    addback_ratio = (deal.addbacks_claimed / reported) if reported > 0 else 0.0
    if addback_ratio > 0.25:
        red_flags.append(
            f"Add-backs are {addback_ratio*100:.0f}% of EBITDA — require documentary support for each."
        )
    if deal.one_time_items > 0:
        red_flags.append("One-time items removed from EBITDA — confirm they are truly non-recurring.")
    if deal.debt_like_items > 0:
        red_flags.append(
            f"Debt-like items of ${deal.debt_like_items:,.0f} reduce equity value — treat as debt at close."
        )

    # --- Financial Integrity Score (0-100) ---
    score = 100.0
    if proof.checked and proof.variance_pct is not None:
        score -= _clamp((abs(proof.variance_pct) - 5) * 1.5, 0, 25)
    else:
        score -= 12  # cannot tie out cash
    score -= _clamp((addback_ratio - 0.15) * 120, 0, 25)
    score -= _clamp((deal.one_time_items / reported * 100) if reported > 0 else 0, 0, 15)
    score -= _clamp((deal.customer_concentration_pct - 20) * 0.8, 0, 20)
    score += _clamp(deal.recurring_revenue_pct * 0.15, 0, 12)
    integrity = int(_clamp(score))

    procedures = [
        "EBITDA normalization & add-back scrutiny",
        "Proof-of-cash (deposits vs. reported revenue)",
        "Net-working-capital peg",
        "Quality-of-revenue (recurring & concentration)",
        "Debt-like items review",
    ]

    # --- Recommended path ---
    if integrity >= 75 and (deal.asking_price is None or deal.asking_price < 2_000_000):
        recommended_tier = "B"
        recommended_action = (
            "Screen looks clean. Commission a Tier B partner-CPA QoE before LOI to confirm."
        )
    elif integrity >= 60:
        recommended_tier = "B"
        recommended_action = (
            "Proceed to a Tier B partner-CPA Quality-of-Earnings review; resolve the flags below in diligence."
        )
    else:
        recommended_tier = "C"
        recommended_action = (
            "Material red flags. Commission Tier B QoE and, if a lender requires assurance, a "
            "Tier C attest engagement (AUP/review) via a partner CPA firm."
        )
    if not deal.post_loi:
        recommended_action += " (Tier A screening is included with your subscription pre-LOI.)"

    return DiligenceReport(
        business_name=deal.business_name, period_label=deal.period_label,
        financial_integrity_score=integrity,
        adjusted_ebitda=round(adjusted_ebitda), reported_ebitda=round(reported),
        ebitda_adjustment=round(adjustment),
        proof_of_cash=proof, working_capital=wc, revenue_quality=rq,
        debt_like_items=round(deal.debt_like_items),
        procedures_performed=procedures, red_flags=red_flags,
        recommended_tier=recommended_tier, recommended_action=recommended_action,
        add_on_pricing=pricing_band(adjusted_ebitda if adjusted_ebitda > 0 else reported),
        disclaimer=_DISCLAIMER,
    )


_TIER_NAMES = {
    "qoe": "Quality of Earnings (buy-side FDD)",
    "aup": "Agreed-Upon Procedures (attest)",
    "review": "Financial statement review (attest)",
    "audit": "Financial statement audit (attest)",
}


def quote_engagement(req: EngagementRequest) -> EngagementQuote:
    band = pricing_band(req.target_ebitda)
    tier = req.tier.strip().lower()
    tier_name = _TIER_NAMES.get(tier, "Quality of Earnings (buy-side FDD)")

    if tier == "qoe":
        low, high = band.platform_low, band.platform_high
        turnaround = "~2 weeks"
    elif tier == "aup":
        low, high = band.platform_high, band.platform_high * 1.6
        turnaround = "~3 weeks"
    elif tier == "review":
        low, high = band.manual_low * 0.6, band.manual_low
        turnaround = "~4 weeks"
    else:  # audit
        low, high = band.manual_low, band.manual_high
        turnaround = "~6–10 weeks"

    return EngagementQuote(
        reference="FDS-" + uuid.uuid4().hex[:10].upper(),
        business_name=req.business_name, tier=tier, tier_name=tier_name,
        estimated_price_low=round(low), estimated_price_high=round(high),
        jhi_software_fee_low=band.jhi_software_fee_low, jhi_software_fee_high=band.jhi_software_fee_high,
        partner_match_status="pending_match",
        turnaround_estimate=turnaround,
        next_steps=[
            "JHI matches a licensed partner CPA in "
            + (req.state or "the target's state") + ".",
            "Partner issues an engagement letter directly to you (fees + scope confirmed).",
            "Connect the target's accounting data or upload financials + bank statements.",
            "Software prepares workpapers; the partner CPA reviews, finalizes, and signs.",
        ],
        disclaimer=_DISCLAIMER,
    )
