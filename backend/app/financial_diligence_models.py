# JHI-SIG: 69M2705M | Financial Diligence Suite | John Henry Investments (proprietary)
"""Pydantic models for the Financial Diligence Suite (Quality-of-Earnings support).

Software-accelerated buy-side financial due-diligence: proof-of-cash, EBITDA
normalization, net-working-capital peg, quality-of-revenue, and debt-like items,
plus a Financial Integrity Score, a recommended assurance tier, add-on pricing,
and a partner-CPA engagement quote.

IMPORTANT: this is decision-support / QoE support — NOT an audit, review, or CPA
opinion. Formal assurance opinions (Unqualified / Qualified / Adverse / Disclaimer)
are issued only by a licensed partner CPA firm that engages the target entity.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class DiligenceInput(BaseModel):
    # --- Identity ---
    business_name: str = Field(min_length=1)
    industry: str = "general"
    period_label: str = Field(default="Most recent FY", description="e.g. 'FY2025'.")

    # --- Earnings ---
    revenue: float = Field(gt=0)
    reported_ebitda: float = Field(description="Seller-presented EBITDA/SDE.")
    addbacks_claimed: float = Field(default=0.0, ge=0, description="Total add-backs the seller included.")
    questionable_addbacks: float = Field(
        default=0.0, ge=0, description="Add-backs that lack clear support (discounted 50%)."
    )
    one_time_items: float = Field(
        default=0.0, ge=0, description="Non-recurring items inflating EBITDA (removed in full)."
    )

    # --- Proof of cash ---
    bank_deposits: float | None = Field(
        default=None, ge=0, description="Total bank deposits for the period (ties to revenue)."
    )

    # --- Net working capital components ---
    accounts_receivable: float = Field(default=0.0, ge=0)
    inventory: float = Field(default=0.0, ge=0)
    accounts_payable: float = Field(default=0.0, ge=0)

    # --- Quality of revenue ---
    recurring_revenue_pct: float = Field(default=0.0, ge=0, le=100)
    customer_concentration_pct: float = Field(default=0.0, ge=0, le=100)

    # --- Balance-sheet risk ---
    debt_like_items: float = Field(
        default=0.0, ge=0, description="Deferred revenue, capital leases, unpaid taxes, etc."
    )

    # --- Deal context (optional) ---
    asking_price: float | None = Field(default=None, gt=0)
    post_loi: bool = Field(default=False, description="Is the buyer past a signed LOI?")


class ProofOfCash(BaseModel):
    checked: bool
    reported_revenue: float
    bank_deposits: float | None
    variance_pct: float | None
    flag: str


class WorkingCapital(BaseModel):
    accounts_receivable: float
    inventory: float
    accounts_payable: float
    net_working_capital: float
    nwc_pct_of_revenue: float
    note: str


class RevenueQuality(BaseModel):
    recurring_revenue_pct: float
    customer_concentration_pct: float
    score: int = Field(ge=0, le=100)
    note: str


class PricingBand(BaseModel):
    band: str
    manual_low: float
    manual_high: float
    platform_low: float
    platform_high: float
    jhi_software_fee_low: float
    jhi_software_fee_high: float


class DiligenceTier(BaseModel):
    tier: str
    name: str
    attest: bool
    delivered_by: str
    description: str


class DiligenceReport(BaseModel):
    business_name: str
    period_label: str
    financial_integrity_score: int = Field(ge=0, le=100)
    adjusted_ebitda: float
    reported_ebitda: float
    ebitda_adjustment: float
    proof_of_cash: ProofOfCash
    working_capital: WorkingCapital
    revenue_quality: RevenueQuality
    debt_like_items: float
    procedures_performed: list[str]
    red_flags: list[str]
    recommended_tier: str
    recommended_action: str
    add_on_pricing: PricingBand
    disclaimer: str


class EngagementRequest(BaseModel):
    business_name: str = Field(min_length=1)
    tier: str = Field(description="qoe | aup | review | audit")
    target_ebitda: float = Field(gt=0)
    state: str = Field(default="", description="State where the target operates (for CPA licensing).")
    contact_email: str = Field(min_length=3)
    notes: str = ""


class EngagementQuote(BaseModel):
    reference: str
    business_name: str
    tier: str
    tier_name: str
    estimated_price_low: float
    estimated_price_high: float
    jhi_software_fee_low: float
    jhi_software_fee_high: float
    partner_match_status: str
    turnaround_estimate: str
    next_steps: list[str]
    disclaimer: str
