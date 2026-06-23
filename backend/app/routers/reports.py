from datetime import date

from fastapi import APIRouter, HTTPException, Query

from app.models import AuditReport, FinancialReport
from app.services import ReportingService
from app.store import store

router = APIRouter(prefix="/reports", tags=["reports"])
reporting_service = ReportingService(store)


@router.get("/audit", response_model=AuditReport)
def get_audit_report(
    period_start: date = Query(...),
    period_end: date = Query(...),
) -> AuditReport:
    if period_end < period_start:
        raise HTTPException(status_code=400, detail="period_end must be after period_start")
    return reporting_service.audit_report(period_start, period_end)


@router.get("/financial", response_model=FinancialReport)
def get_financial_report(
    period_start: date = Query(...),
    period_end: date = Query(...),
) -> FinancialReport:
    if period_end < period_start:
        raise HTTPException(status_code=400, detail="period_end must be after period_start")
    return reporting_service.financial_report(period_start, period_end)
