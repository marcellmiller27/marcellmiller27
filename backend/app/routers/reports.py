# JHI-SIG: 69M2705M | Accounting & Reporting | John Henry Investments (proprietary)
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AuditReport, FinancialReport
from app.reporting_services import ReportingService

router = APIRouter(prefix="/reports", tags=["reports"])
reporting_service = ReportingService()


@router.get("/audit", response_model=AuditReport)
def get_audit_report(
    db: Annotated[Session, Depends(get_db)],
    period_start: date = Query(...),
    period_end: date = Query(...),
) -> AuditReport:
    if period_end < period_start:
        raise HTTPException(status_code=400, detail="period_end must be after period_start")
    return reporting_service.audit_report(db, period_start, period_end)


@router.get("/financial", response_model=FinancialReport)
def get_financial_report(
    db: Annotated[Session, Depends(get_db)],
    period_start: date = Query(...),
    period_end: date = Query(...),
) -> FinancialReport:
    if period_end < period_start:
        raise HTTPException(status_code=400, detail="period_end must be after period_start")
    return reporting_service.financial_report(db, period_start, period_end)
