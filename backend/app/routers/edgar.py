import re
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_premium
from app.edgar_models import EdgarFinancials
from app.edgar_services import EdgarService, ProviderError
from app.edgar_workbook import company_workbook
from app.foundation_models import Principal, SubscriptionPlan
from app.foundation_services import FoundationService

router = APIRouter(prefix="/fundamentals/edgar", tags=["edgar-fundamentals"])

_XLSX_MEDIA = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


@router.get("/{ticker}", response_model=EdgarFinancials)
def edgar_financials(ticker: str) -> EdgarFinancials:
    """Normalized headline annual financials for a US filer from SEC EDGAR (no key)."""
    try:
        return EdgarService().financials(ticker)
    except ProviderError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{ticker}/export.xlsx")
def export_edgar_workbook(
    ticker: str,
    principal: Annotated[Principal, Depends(require_premium)],
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    """Premium (T1/T2) client-ready Excel workbook of a company's SEC financials.

    Gated to Professional/Enterprise; Enterprise (T1) receives a branded workbook.
    """
    try:
        fin = EdgarService().financials(ticker)
    except ProviderError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    plan = FoundationService(db).me(principal).subscription.plan
    data = company_workbook(fin, branded=(plan == SubscriptionPlan.ENTERPRISE))
    safe = re.sub(r"[^A-Za-z0-9]+", "_", ticker).strip("_").upper() or "COMPANY"
    return Response(
        content=data,
        media_type=_XLSX_MEDIA,
        headers={"Content-Disposition": f'attachment; filename="JHI_{safe}_Financials.xlsx"'},
    )
