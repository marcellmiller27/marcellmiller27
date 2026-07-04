# JHI-SIG: 69M2705M | Acquisition / Deal X-Ray | John Henry Investments (proprietary)
from fastapi import APIRouter

from app.deal_xray import analyze
from app.deal_xray_models import DealInput, DealXRayReport

router = APIRouter(prefix="/deal-xray", tags=["deal-xray"])


@router.post("/analyze", response_model=DealXRayReport)
def analyze_deal(payload: DealInput) -> DealXRayReport:
    """Analyze a CIM's key figures → 7-segment scorecard, ethic rating, DCF, financing."""
    return analyze(payload)
