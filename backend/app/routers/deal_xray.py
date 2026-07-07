# JHI-SIG: 69M2705M | Acquisition / Deal X-Ray | John Henry Investments (proprietary)
import re

from fastapi import APIRouter, Response

from app.deal_xray import analyze
from app.deal_xray_models import DealInput, DealXRayReport
from app.excel_export import deal_xray_workbook

router = APIRouter(prefix="/deal-xray", tags=["deal-xray"])

_XLSX_MEDIA = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


@router.post("/analyze", response_model=DealXRayReport)
def analyze_deal(payload: DealInput) -> DealXRayReport:
    """Analyze a CIM's key figures → 7-segment scorecard, ethic rating, DCF, financing."""
    return analyze(payload)


@router.post("/export.xlsx")
def export_deal_xray(payload: DealInput) -> Response:
    """Interactive Excel workbook: editable inputs → live DSCR/valuation formulas + BQA."""
    report = analyze(payload)
    data = deal_xray_workbook(payload, report)
    safe = re.sub(r"[^A-Za-z0-9]+", "_", payload.business_name).strip("_") or "deal"
    return Response(
        content=data,
        media_type=_XLSX_MEDIA,
        headers={"Content-Disposition": f'attachment; filename="JHI_BQA_{safe}.xlsx"'},
    )
