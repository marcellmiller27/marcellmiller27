# JHI-SIG: 69M2705M | Acquisition / Deal X-Ray | John Henry Investments (proprietary)
"""Pydantic models for the Deal X-Ray CIM analyzer (search-fund / SMB acquisition).

Structured-input v1: the user supplies key figures from a CIM; a future v2 will
auto-extract these from an uploaded PDF. Output is a 7-segment scorecard, an honest
ethic/credibility rating, a per-deal DCF + multiple valuation, DSCR/SBA fit,
financing/offer alternatives, and a Buy/Watch/Pass recommendation.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class DealInput(BaseModel):
    # --- Identity ---
    business_name: str = Field(min_length=1)
    industry: str = "general"
    year_founded: int | None = Field(default=None, ge=1800, le=2100)

    # --- Financials (most recent full year) ---
    revenue: float = Field(gt=0)
    revenue_prior: float | None = Field(default=None, ge=0)
    reported_ebitda: float = Field(description="Seller-presented EBITDA/SDE for the year.")
    addbacks: float = Field(default=0.0, ge=0, description="Total add-backs included in EBITDA/SDE.")
    annual_capex: float | None = Field(default=None, ge=0)

    # --- People / operations ---
    employees: int = Field(default=1, ge=0)
    owner_involvement: str = Field(
        default="owner_operated",
        description="absentee | semi_absentee | owner_operated | owner_critical",
    )

    # --- Assets ---
    real_estate_included: bool = False
    real_estate_value: float | None = Field(default=None, ge=0)
    annual_lease: float | None = Field(default=None, ge=0)
    equipment_value: float | None = Field(default=None, ge=0)
    equipment_age_years: float | None = Field(default=None, ge=0)

    # --- Market / quality ---
    customer_concentration_pct: float = Field(
        default=0.0, ge=0, le=100, description="Top customer's % of revenue."
    )
    recurring_revenue_pct: float = Field(default=0.0, ge=0, le=100)

    # --- Deal / financing assumptions ---
    asking_price: float = Field(gt=0)
    down_payment_pct: float = Field(default=10.0, ge=0, le=100)
    seller_note_pct: float = Field(default=0.0, ge=0, le=100)
    loan_rate_pct: float = Field(default=11.5, gt=0, le=40, description="SBA/acquisition loan APR.")
    loan_term_years: int = Field(default=10, ge=1, le=30)


class SegmentScore(BaseModel):
    segment: str
    score: int = Field(ge=0, le=100)
    weight: float
    findings: list[str] = Field(default_factory=list)


class ValuationView(BaseModel):
    normalized_ebitda: float
    industry_multiple_low: float
    industry_multiple_base: float
    industry_multiple_high: float
    multiple_value_low: float
    multiple_value_base: float
    multiple_value_high: float
    dcf_enterprise_value: float
    dcf_assumptions: dict[str, float]
    asking_price: float
    verdict: str  # "undervalued" | "fairly priced" | "overvalued"


class FinancingOption(BaseModel):
    label: str
    equity_required: float
    loan_amount: float
    seller_note: float
    annual_debt_service: float
    dscr: float | None
    sba_fit: bool
    note: str


class DealXRayReport(BaseModel):
    business_name: str
    industry: str
    opportunity_score: int = Field(ge=0, le=100)
    recommendation: str  # "Buy" | "Watch" | "Pass"
    ethic_rating: int = Field(ge=0, le=100)
    ethic_note: str
    segments: list[SegmentScore]
    valuation: ValuationView
    financing_options: list[FinancingOption]
    key_metrics: dict[str, str]
    diligence_questions: list[str]
    disclaimer: str
