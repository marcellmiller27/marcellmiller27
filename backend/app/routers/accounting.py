from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.accounting_services import AccountingService
from app.database import get_db
from app.foundation_models import Principal
from app.models import Account, JournalEntry, JournalEntryCreate, TrialBalance
from app.rbac import require_staff

# Accounting is a back-office / firm-operations module — staff only.
router = APIRouter(prefix="/accounting", tags=["accounting"])
accounting_service = AccountingService()


@router.get("/chart-of-accounts", response_model=list[Account])
def list_chart_of_accounts(
    db: Annotated[Session, Depends(get_db)],
    _staff: Annotated[Principal, Depends(require_staff)],
) -> list[Account]:
    return accounting_service.list_accounts(db)


@router.get("/journal-entries", response_model=list[JournalEntry])
def list_journal_entries(
    db: Annotated[Session, Depends(get_db)],
    _staff: Annotated[Principal, Depends(require_staff)],
    period_start: date | None = Query(default=None),
    period_end: date | None = Query(default=None),
) -> list[JournalEntry]:
    return accounting_service.list_journal_entries(db, period_start, period_end)


@router.post(
    "/journal-entries",
    response_model=JournalEntry,
    status_code=status.HTTP_201_CREATED,
)
def create_journal_entry(
    payload: JournalEntryCreate,
    db: Annotated[Session, Depends(get_db)],
    _staff: Annotated[Principal, Depends(require_staff)],
) -> JournalEntry:
    try:
        return accounting_service.create_journal_entry(db, payload)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/trial-balance", response_model=TrialBalance)
def get_trial_balance(
    db: Annotated[Session, Depends(get_db)],
    _staff: Annotated[Principal, Depends(require_staff)],
    period_start: date = Query(...),
    period_end: date = Query(...),
) -> TrialBalance:
    if period_end < period_start:
        raise HTTPException(status_code=400, detail="period_end must be after period_start")
    return accounting_service.trial_balance(db, period_start, period_end)
