# JHI-SIG: 69M2705M | Acquisition / Deal X-Ray | John Henry Investments (proprietary)
"""Deal X-Ray engine — analyzes a CIM's key figures for search-fund/SMB buyers.

Pure, deterministic computation (unit-testable). Produces a 7-segment scorecard, an
honest ethic/credibility rating, a per-deal DCF + multiple valuation, DSCR/SBA fit,
financing/offer alternatives, and a Buy/Watch/Pass recommendation.

Decision-support only — NOT investment advice, appraisal, or a brokerage service.
"""

from __future__ import annotations

from app.deal_xray_models import (
    DealInput,
    DealXRayReport,
    FinancingOption,
    SegmentScore,
    ValuationView,
)

# industry -> (mult_low, mult_base, mult_high, recession_resilience[0-1], capex_intensity)
_INDUSTRY: dict[str, tuple[float, float, float, float, float]] = {
    "hvac": (2.5, 3.2, 4.0, 0.80, 0.03),
    "plumbing": (2.5, 3.2, 4.0, 0.80, 0.03),
    "electrical": (2.5, 3.2, 4.0, 0.78, 0.03),
    "landscaping": (2.0, 2.8, 3.5, 0.60, 0.05),
    "restaurant": (1.5, 2.2, 3.0, 0.40, 0.04),
    "ecommerce": (2.5, 3.5, 4.5, 0.50, 0.02),
    "manufacturing": (3.0, 4.0, 5.5, 0.60, 0.06),
    "healthcare_services": (3.5, 4.5, 6.0, 0.85, 0.04),
    "professional_services": (2.5, 3.5, 4.5, 0.70, 0.02),
    "logistics": (2.5, 3.3, 4.2, 0.65, 0.05),
    "saas": (4.0, 6.0, 9.0, 0.70, 0.03),
    # Construction is cyclical (lower recession-resilience). Construction *management*
    # firms outsource the build → asset-light, so a low capex intensity.
    "construction": (2.0, 2.8, 3.5, 0.45, 0.04),
    "construction_management": (2.5, 3.2, 4.0, 0.50, 0.015),
    "general": (2.5, 3.2, 4.0, 0.60, 0.04),
}

_OWNER_RISK = {  # higher = more owner-dependent (worse for a search-fund buyer)
    "absentee": 0.05,
    "semi_absentee": 0.25,
    "owner_operated": 0.55,
    "owner_critical": 0.90,
}


def _clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))


def _amortized_annual_payment(principal: float, apr_pct: float, years: int) -> float:
    if principal <= 0:
        return 0.0
    r = apr_pct / 100.0
    n = years
    if r == 0:
        return principal / n
    return principal * r / (1.0 - (1.0 + r) ** (-n))


def _industry(key: str) -> tuple[float, float, float, float, float]:
    return _INDUSTRY.get(key.strip().lower().replace(" ", "_"), _INDUSTRY["general"])


def analyze(deal: DealInput) -> DealXRayReport:
    mult_low, mult_base, mult_high, resilience, capex_intensity = _industry(deal.industry)
    revenue = deal.revenue
    reported = deal.reported_ebitda

    # --- Capex resolution: explicit > depreciation proxy (maintenance capex) > industry estimate.
    # Fixes asset-light service firms (e.g. construction management) that would otherwise be
    # crushed by a blanket industry capex-intensity assumption. ---
    if deal.annual_capex is not None:
        capex = deal.annual_capex
        capex_source = "provided"
    elif deal.annual_depreciation is not None:
        capex = deal.annual_depreciation
        capex_source = "depreciation proxy"
    else:
        capex = revenue * capex_intensity
        capex_source = "industry estimate"

    ebitda_margin = (reported / revenue) if revenue else 0.0
    addback_ratio = (deal.addbacks / reported) if reported > 0 else 0.0

    # --- Honest normalization: discount aggressive add-backs (>25% of EBITDA) by half ---
    excess_addbacks = max(0.0, deal.addbacks - 0.25 * reported)
    normalized_ebitda = max(0.0, reported - 0.5 * excess_addbacks)
    quality_haircut = (normalized_ebitda / reported) if reported > 0 else 1.0

    # --- Valuation basis: blend the two most-recent years so we never price on a peak year;
    # gauge earnings volatility across all supplied years (a durability signal). ---
    history = [e for e in (deal.earnings_history or []) if e and e > 0]
    if len(history) >= 2:
        blend_raw = sum(history[:2]) / 2.0
        valuation_ebitda = max(0.0, blend_raw * quality_haircut)
        basis_note = (
            "2-yr average of "
            + " & ".join(f"${e:,.0f}" for e in history[:2])
            + f" = ${blend_raw:,.0f}"
            + (f", add-back adjusted to ${valuation_ebitda:,.0f}." if quality_haircut < 1 else ".")
        )
    else:
        valuation_ebitda = normalized_ebitda
        basis_note = (
            f"Single-year normalized EBITDA/SDE ${valuation_ebitda:,.0f} "
            "(supply multi-year history to blend a durable basis)."
        )

    earnings_volatility = 0.0
    if len(history) >= 2:
        mean_e = sum(history) / len(history)
        if mean_e > 0:
            variance = sum((e - mean_e) ** 2 for e in history) / len(history)
            earnings_volatility = (variance**0.5) / mean_e

    # Cash flow available for debt service / DCF uses the durable (blended) basis.
    fcf = valuation_ebitda - capex
    fcf_conversion = (fcf / valuation_ebitda) if valuation_ebitda > 0 else 0.0

    segments: list[SegmentScore] = []
    questions: list[str] = []

    # 1) Financial quality (0.28)
    fin = 50.0
    fin += _clamp((ebitda_margin - 0.10) * 250, -30, 30)  # 10% margin neutral
    fin += _clamp((fcf_conversion - 0.6) * 60, -20, 20)
    fin -= _clamp((addback_ratio - 0.25) * 120, 0, 30)  # penalize aggressive add-backs
    fin_findings = [
        f"EBITDA margin {ebitda_margin*100:.1f}%; FCF conversion {fcf_conversion*100:.0f}%.",
        f"Add-backs are {addback_ratio*100:.0f}% of EBITDA"
        + (" — aggressive; verify with a QoE." if addback_ratio > 0.25 else "."),
    ]
    if addback_ratio > 0.25:
        questions.append("Provide documentation for each add-back (quality-of-earnings review).")
    segments.append(SegmentScore(segment="Financial quality", score=int(_clamp(fin)), weight=0.28, findings=fin_findings))

    # 2) Growth (0.15)
    if deal.revenue_prior and deal.revenue_prior > 0:
        yoy = (revenue - deal.revenue_prior) / deal.revenue_prior
        grow = _clamp(50 + yoy * 300, 0, 100)
        grow_findings = [f"Revenue YoY growth {yoy*100:.1f}%."]
        if yoy < 0:
            questions.append("Explain the revenue decline and the turnaround plan.")
        if earnings_volatility >= 0.20:
            grow -= _clamp((earnings_volatility - 0.20) * 100, 0, 25)
            grow_findings.append(
                f"Earnings volatility {earnings_volatility*100:.0f}% (CoV across supplied years) — "
                "growth is uneven; discount a single peak year."
            )
            questions.append("Reconcile the year-over-year earnings swings — what drove each move?")
    else:
        yoy = None
        grow = 50.0
        grow_findings = ["No prior-year revenue provided — growth not verifiable."]
        questions.append("Provide at least 3 years of financials to assess growth durability.")
    segments.append(SegmentScore(segment="Growth trajectory", score=int(grow), weight=0.15, findings=grow_findings))

    # 3) People & execution (0.15)
    rev_per_emp = (revenue / deal.employees) if deal.employees else revenue
    owner_risk = _OWNER_RISK.get(deal.owner_involvement, 0.55)
    ppl = 50.0 + _clamp((rev_per_emp / 200_000 - 1) * 25, -25, 25) - owner_risk * 40
    ppl_findings = [
        f"Revenue/employee ${rev_per_emp:,.0f} across {deal.employees} staff.",
        f"Owner involvement: {deal.owner_involvement.replace('_', ' ')}"
        + (" — high key-person risk." if owner_risk >= 0.55 else "."),
    ]
    if owner_risk >= 0.55:
        questions.append("Detail the owner's role and a realistic transition/handover plan.")
    segments.append(SegmentScore(segment="People & execution", score=int(_clamp(ppl)), weight=0.15, findings=ppl_findings))

    # 4) Assets (0.10)
    ast = 60.0
    ast_findings: list[str] = []
    if deal.equipment_age_years is not None:
        ast -= _clamp((deal.equipment_age_years - 7) * 4, 0, 25)
        ast_findings.append(f"Equipment ~{deal.equipment_age_years:.0f} yrs old.")
        if deal.equipment_age_years > 10:
            questions.append("Provide an equipment replacement/capex schedule.")
    ast -= _clamp((capex / revenue - 0.05) * 200, 0, 20) if revenue else 0
    if deal.annual_lease and revenue:
        lease_burden = deal.annual_lease / revenue
        ast -= _clamp((lease_burden - 0.08) * 150, 0, 20)
        ast_findings.append(f"Lease burden {lease_burden*100:.1f}% of revenue.")
        questions.append("Review lease term, renewal options, and rent escalation.")
    if deal.real_estate_included:
        ast_findings.append("Real estate included — value separately from the business EV.")
    if capex_source == "depreciation proxy":
        ast_findings.append(f"Maintenance capex proxied from depreciation (${capex:,.0f}/yr).")
    elif capex_source == "industry estimate":
        ast_findings.append(f"Capex estimated at industry norm (${capex:,.0f}/yr) — confirm actual spend.")
    if not ast_findings:
        ast_findings.append("Limited asset detail provided.")
    segments.append(SegmentScore(segment="Assets", score=int(_clamp(ast)), weight=0.10, findings=ast_findings))

    # 5) Market / durability (0.15)
    mkt = resilience * 100
    mkt -= _clamp((deal.customer_concentration_pct - 20) * 1.5, 0, 35)
    mkt += _clamp(deal.recurring_revenue_pct * 0.25, 0, 20)
    mkt_findings = [
        f"Industry recession-resilience {resilience*100:.0f}/100.",
        f"Top-customer concentration {deal.customer_concentration_pct:.0f}%; recurring revenue {deal.recurring_revenue_pct:.0f}%.",
    ]
    if deal.customer_concentration_pct > 20:
        questions.append("Break down revenue by top 5 customers and contract terms.")
    segments.append(SegmentScore(segment="Market & durability", score=int(_clamp(mkt)), weight=0.15, findings=mkt_findings))

    # 6) Risk (0.17) — inverse of concentration + add-back aggressiveness + owner + capex
    risk_pen = (
        _clamp((deal.customer_concentration_pct - 15) * 1.2, 0, 35)
        + _clamp((addback_ratio - 0.2) * 100, 0, 25)
        + owner_risk * 25
        + _clamp((capex / revenue - 0.05) * 150, 0, 15) if revenue else 0
    )
    rsk = _clamp(100 - risk_pen)
    segments.append(SegmentScore(segment="Risk profile", score=int(rsk), weight=0.17,
                                 findings=[f"Composite risk penalty {risk_pen:.0f}/100 (lower is better)."]))

    # --- Honest ethic / credibility rating ---
    ethic = 100.0
    ethic_flags: list[str] = []
    if addback_ratio > 0.25:
        ethic -= _clamp((addback_ratio - 0.25) * 120, 0, 35)
        ethic_flags.append("aggressive add-backs")
    if ebitda_margin > 0.35 and deal.industry.lower() not in ("saas", "professional_services"):
        ethic -= 15
        ethic_flags.append("margins look high for the industry (verify)")
    if deal.revenue_prior is None:
        ethic -= 10
        ethic_flags.append("incomplete history")
    if deal.owner_involvement == "owner_critical" and ebitda_margin > 0.25:
        ethic -= 10
        ethic_flags.append("owner-dependent yet high margin")
    # Heavy customer concentration is a durability/credibility risk, not just a score input.
    if deal.customer_concentration_pct >= 40:
        ethic -= _clamp((deal.customer_concentration_pct - 40) * 1.0, 0, 25)
        ethic_flags.append(f"customer concentration {deal.customer_concentration_pct:.0f}%")
    # Volatile earnings undercut the reliability of the presented figures.
    if earnings_volatility >= 0.20:
        ethic -= _clamp((earnings_volatility - 0.20) * 80, 0, 20)
        ethic_flags.append(f"volatile earnings history ({earnings_volatility*100:.0f}% CoV)")
    # An owner-driven recent recovery that the buyer must inherit is unproven durability.
    if earnings_volatility >= 0.25 and _OWNER_RISK.get(deal.owner_involvement, 0.55) >= 0.55:
        ethic -= 5
        ethic_flags.append("recent owner-driven turnaround — durability unproven")
    ethic = int(_clamp(ethic))
    ethic_note = (
        "CIM presentation looks credible and internally consistent."
        if ethic >= 75
        else "Credibility & risk concerns — " + ", ".join(ethic_flags) + ". Insist on a QoE before an offer."
    )

    # --- Valuation: multiple (on the durable/blended basis) + a curbed DCF cross-check ---
    v_low = round(valuation_ebitda * mult_low)
    v_base = round(valuation_ebitda * mult_base)
    v_high = round(valuation_ebitda * mult_high)

    # Growth used in the DCF is deliberately conservative: cap optimistic prints, halve for
    # heavy concentration, and hold back when revenue isn't recurring.
    if yoy is not None:
        g = max(-0.05, min(0.08, yoy))
    else:
        g = 0.02
    if deal.customer_concentration_pct >= 40:
        g *= 0.5
    if deal.recurring_revenue_pct < 20:
        g = min(g, 0.04)

    # Risk-adjusted discount rate: small/illiquid base + concentration + key-person + non-recurring.
    wacc = 0.18
    wacc += _clamp((deal.customer_concentration_pct - 30) * 0.0015, 0, 0.06)
    wacc += _OWNER_RISK.get(deal.owner_involvement, 0.55) * 0.05
    if deal.recurring_revenue_pct < 20:
        wacc += 0.02
    wacc = min(0.32, wacc)

    g_term = 0.02
    dcf_ev = 0.0
    fcf_t = fcf
    for t in range(1, 6):
        # Fade growth linearly toward the terminal rate so one strong year can't compound away.
        g_t = g + (g_term - g) * (t - 1) / 4
        fcf_t = fcf_t * (1 + g_t)
        dcf_ev += fcf_t / ((1 + wacc) ** t)
    terminal = (fcf_t * (1 + g_term)) / (wacc - g_term)
    dcf_ev += terminal / ((1 + wacc) ** 5)
    dcf_ev = round(max(0.0, dcf_ev))
    # Sanity cap: the DCF is a cross-check, not a fantasy — bound it to the multiple range.
    dcf_ev = max(round(v_low * 0.75), min(dcf_ev, v_high))

    # Fair value leans on market multiples (75%) with the DCF as a light cross-check (25%).
    fair = 0.75 * v_base + 0.25 * dcf_ev if dcf_ev > 0 else v_base
    if deal.asking_price < fair * 0.9:
        verdict = "undervalued"
    elif deal.asking_price > fair * 1.15:
        verdict = "overvalued"
    else:
        verdict = "fairly priced"

    valuation = ValuationView(
        normalized_ebitda=round(valuation_ebitda),
        basis_note=basis_note,
        industry_multiple_low=mult_low, industry_multiple_base=mult_base, industry_multiple_high=mult_high,
        multiple_value_low=v_low, multiple_value_base=v_base, multiple_value_high=v_high,
        dcf_enterprise_value=dcf_ev,
        dcf_assumptions={"growth": round(g, 3), "discount_rate_wacc": round(wacc, 3),
                         "terminal_growth": g_term, "years": 5, "capex": round(capex)},
        asking_price=deal.asking_price, verdict=verdict,
    )

    # --- Financing / offer alternatives ---
    cfads = fcf  # cash flow available for debt service (normalized EBITDA - capex)
    financing = _financing_options(deal, cfads)
    best_dscr = max((f.dscr for f in financing if f.dscr is not None), default=None)

    # --- Deal Score (weighted) + adjustments ---
    weighted = sum(s.score * s.weight for s in segments)
    if verdict == "undervalued":
        weighted += 5
    elif verdict == "overvalued":
        weighted -= 8
    if ethic < 60:
        weighted -= 8
    score = int(_clamp(weighted))

    # --- Recommendation ---
    financeable = best_dscr is not None and best_dscr >= 1.0
    if not financeable:
        recommendation = "Pass"
    elif score >= 70 and ethic >= 60 and best_dscr >= 1.25:
        recommendation = "Buy"
    elif score >= 50:
        recommendation = "Watch"
    else:
        recommendation = "Pass"
    if ethic < 50 and recommendation == "Buy":
        recommendation = "Watch"  # credibility gate

    key_metrics = {
        "Valuation EBITDA (basis)": f"${round(valuation_ebitda):,}",
        "EBITDA margin": f"{ebitda_margin*100:.1f}%",
        "Add-back ratio": f"{addback_ratio*100:.0f}%",
        "Revenue/employee": f"${rev_per_emp:,.0f}",
        "Asking multiple (on basis)": f"{deal.asking_price/valuation_ebitda:.1f}x" if valuation_ebitda > 0 else "n/a",
        "Best-case DSCR": f"{best_dscr:.2f}" if best_dscr is not None else "n/a",
    }
    if len(history) >= 2:
        key_metrics["Earnings volatility"] = f"{earnings_volatility*100:.0f}%"

    if not questions:
        questions.append("Request trailing-twelve-month financials and bank statements to reconcile.")

    return DealXRayReport(
        business_name=deal.business_name, industry=deal.industry,
        deal_score=score, recommendation=recommendation,
        ethic_rating=ethic, ethic_note=ethic_note,
        segments=segments, valuation=valuation, financing_options=financing,
        key_metrics=key_metrics, diligence_questions=questions,
        disclaimer=(
            "Decision-support analysis from user-supplied figures — NOT investment advice, a "
            "valuation/appraisal, or brokerage. Verify all figures with a quality-of-earnings "
            "review and licensed professionals before making an offer."
        ),
    )


def _financing_options(deal: DealInput, cfads: float) -> list[FinancingOption]:
    price = deal.asking_price
    opts: list[FinancingOption] = []

    def build(label: str, down_pct: float, note_pct: float, note: str) -> FinancingOption:
        equity = price * down_pct / 100
        seller_note = price * note_pct / 100
        loan = max(0.0, price - equity - seller_note)
        ds = (
            _amortized_annual_payment(loan, deal.loan_rate_pct, deal.loan_term_years)
            + _amortized_annual_payment(seller_note, deal.loan_rate_pct, deal.loan_term_years)
        )
        dscr = (cfads / ds) if ds > 0 else None
        return FinancingOption(
            label=label, equity_required=round(equity), loan_amount=round(loan),
            seller_note=round(seller_note), annual_debt_service=round(ds),
            dscr=round(dscr, 2) if dscr is not None else None,
            sba_fit=(dscr is not None and dscr >= 1.25 and down_pct >= 10), note=note,
        )

    opts.append(build("As entered", deal.down_payment_pct, deal.seller_note_pct,
                      "Your stated structure."))
    opts.append(build("SBA 7(a) 90/10 + 10% seller note", 10.0, 10.0,
                      "Classic search-fund structure: 10% equity, 10% seller note, SBA balance."))
    opts.append(build("Conservative (20% down)", 20.0, 10.0,
                      "Higher equity to strengthen DSCR and lender appetite."))
    return opts
