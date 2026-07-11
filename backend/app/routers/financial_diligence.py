# JHI-SIG: 69M2705M | Financial Diligence Suite | John Henry Investments (proprietary)
import re

from fastapi import APIRouter, Response

from app.excel_export import diligence_workbook
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
from app.pdf_export import diligence_pdf

router = APIRouter(prefix="/financial-diligence", tags=["financial-diligence"])

_XLSX_MEDIA = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


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


@router.post("/export.xlsx")
def export_diligence(payload: DiligenceInput) -> Response:
    """Interactive Excel workbook: editable QoE inputs → live proof-of-cash / NWC formulas."""
    report = analyze(payload)
    data = diligence_workbook(payload, report)
    safe = re.sub(r"[^A-Za-z0-9]+", "_", payload.business_name).strip("_") or "target"
    return Response(
        content=data,
        media_type=_XLSX_MEDIA,
        headers={"Content-Disposition": f'attachment; filename="JHI_QoE_{safe}.xlsx"'},
    )


@router.post("/export.pdf")
def export_diligence_pdf(payload: DiligenceInput) -> Response:
    """Branded one-page PDF QoE memo (client-ready leave-behind)."""
    report = analyze(payload)
    data = diligence_pdf(payload, report)
    safe = re.sub(r"[^A-Za-z0-9]+", "_", payload.business_name).strip("_") or "target"
    return Response(
        content=data,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="JHI_QoE_{safe}.pdf"'},
    )
