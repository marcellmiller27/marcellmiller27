from datetime import date

from fastapi import APIRouter, HTTPException, Query, status

from app.models import Account, JournalEntry, JournalEntryCreate, TrialBalance
from app.services import AccountingService
from app.store import store

router = APIRouter(prefix="/accounting", tags=["accounting"])
accounting_service = AccountingService(store)


@router.get("/chart-of-accounts", response_model=list[Account])
def list_chart_of_accounts() -> list[Account]:
    return list(store.accounts.values())


@router.get("/journal-entries", response_model=list[JournalEntry])
def list_journal_entries(
    period_start: date | None = Query(default=None),
    period_end: date | None = Query(default=None),
) -> list[JournalEntry]:
    return store.list_journal_entries(period_start, period_end)


@router.post(
    "/journal-entries",
    response_model=JournalEntry,
    status_code=status.HTTP_201_CREATED,
)
def create_journal_entry(payload: JournalEntryCreate) -> JournalEntry:
    try:
        return store.create_journal_entry(payload)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/trial-balance", response_model=TrialBalance)
def get_trial_balance(
    period_start: date = Query(...),
    period_end: date = Query(...),
) -> TrialBalance:
    if period_end < period_start:
        raise HTTPException(status_code=400, detail="period_end must be after period_start")
    return accounting_service.trial_balance(period_start, period_end)
