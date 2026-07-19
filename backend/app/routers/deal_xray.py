# JHI-SIG: 69M2705M | Acquisition / Deal X-Ray | JHI Research & Analytics Firm, Inc. (proprietary)
import re

from fastapi import APIRouter, Response

from app.deal_xray import analyze, build_comp_benchmark
from app.deal_xray_models import CompanyComp, CompBenchmark, DealInput, DealXRayReport
from app.edgar_services import EdgarService
from app.edgar_services import ProviderError as EdgarProviderError
from app.excel_export import deal_xray_workbook
from app.pdf_export import deal_xray_pdf

router = APIRouter(prefix="/deal-xray", tags=["deal-xray"])

_XLSX_MEDIA = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
_MAX_COMPS = 5


def _comp_benchmark(payload: DealInput) -> CompBenchmark | None:
    """Resolve optional public-comp tickers to a SEC EDGAR margin benchmark (I/O)."""
    if not payload.comp_tickers:
        return None
    service = EdgarService()
    comps: list[CompanyComp] = []
    unavailable: list[str] = []
    for ticker in payload.comp_tickers[:_MAX_COMPS]:
        try:
            fin = service.financials(ticker)
        except EdgarProviderError:
            unavailable.append(ticker.strip().upper())
            continue
        comps.append(
            CompanyComp(
                ticker=fin.ticker,
                entity_name=fin.entity_name,
                fiscal_year=fin.fiscal_year,
                revenue=fin.revenue,
                gross_margin=fin.gross_margin,
                operating_margin=fin.operating_margin,
                net_margin=fin.net_margin,
            )
        )
    deal_margin = (payload.reported_ebitda / payload.revenue) if payload.revenue else None
    return build_comp_benchmark(deal_margin, comps, unavailable)


def _report(payload: DealInput) -> DealXRayReport:
    return analyze(payload, comp_benchmark=_comp_benchmark(payload))


@router.post("/analyze", response_model=DealXRayReport)
def analyze_deal(payload: DealInput) -> DealXRayReport:
    """Analyze a CIM's key figures → 7-segment scorecard, ethic rating, DCF, financing.

    Optionally supply ``comp_tickers`` to benchmark margins against public peers (SEC EDGAR).
    """
    return _report(payload)


@router.post("/export.xlsx")
def export_deal_xray(payload: DealInput) -> Response:
    """Interactive Excel workbook: editable inputs → live DSCR/valuation formulas + BQA."""
    report = _report(payload)
    data = deal_xray_workbook(payload, report)
    safe = re.sub(r"[^A-Za-z0-9]+", "_", payload.business_name).strip("_") or "deal"
    return Response(
        content=data,
        media_type=_XLSX_MEDIA,
        headers={"Content-Disposition": f'attachment; filename="JHI_BQA_{safe}.xlsx"'},
    )


@router.post("/export.pdf")
def export_deal_xray_pdf(payload: DealInput) -> Response:
    """Branded one-page PDF deal memo (client-ready leave-behind)."""
    report = _report(payload)
    data = deal_xray_pdf(payload, report)
    safe = re.sub(r"[^A-Za-z0-9]+", "_", payload.business_name).strip("_") or "deal"
    return Response(
        content=data,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="JHI_BQA_{safe}.pdf"'},
    )
