# JHI-SIG: 69M2705M | Financial Diligence Suite | John Henry Investments (proprietary)
from fastapi import APIRouter

from app.financial_diligence import (
    TIERS,
    analyze,
    pricing_band,
    quote_engagement,
)
from app.financial_diligence_models import (
    DiligenceInput,
    DiligenceReport,
    DiligenceTier,
    EngagementQuote,
    EngagementRequest,
    PricingBand,
)

router = APIRouter(prefix="/financial-diligence", tags=["financial-diligence"])


@router.post("/analyze", response_model=DiligenceReport)
def analyze_diligence(payload: DiligenceInput) -> DiligenceReport:
    """Run software-accelerated QoE procedures → integrity score, tier, pricing."""
    return analyze(payload)


@router.get("/tiers", response_model=list[DiligenceTier])
def list_tiers() -> list[DiligenceTier]:
    """The three-tier Financial Diligence Suite (screening → QoE → attest)."""
    return TIERS


@router.get("/pricing", response_model=list[PricingBand])
def list_pricing() -> list[PricingBand]:
    """Add-on price bands vs. the manual market, keyed by target EBITDA/SDE."""
    return [pricing_band(x) for x in (999_999, 2_999_999, 9_999_999, 15_000_000)]


@router.post("/engagement", response_model=EngagementQuote)
def request_engagement(payload: EngagementRequest) -> EngagementQuote:
    """Request a partner-CPA engagement (QoE/AUP/review/audit) → quote + routing."""
    return quote_engagement(payload)
