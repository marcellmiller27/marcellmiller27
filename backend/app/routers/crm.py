from fastapi import APIRouter, HTTPException, status

from app.models import (
    CRMActivity,
    CRMActivityCreate,
    CRMContact,
    CRMContactCreate,
    CRMDeal,
    CRMDealCreate,
    CRMSummary,
)
from app.services import CRMService
from app.store import store

router = APIRouter(prefix="/crm", tags=["crm"])
crm_service = CRMService(store)


@router.get("/contacts", response_model=list[CRMContact])
def list_contacts() -> list[CRMContact]:
    return list(store.contacts.values())


@router.post("/contacts", response_model=CRMContact, status_code=status.HTTP_201_CREATED)
def create_contact(payload: CRMContactCreate) -> CRMContact:
    return store.create_contact(payload)


@router.get("/deals", response_model=list[CRMDeal])
def list_deals() -> list[CRMDeal]:
    return list(store.deals.values())


@router.post("/deals", response_model=CRMDeal, status_code=status.HTTP_201_CREATED)
def create_deal(payload: CRMDealCreate) -> CRMDeal:
    try:
        return store.create_deal(payload)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/activities", response_model=list[CRMActivity])
def list_activities() -> list[CRMActivity]:
    return list(store.activities.values())


@router.post("/activities", response_model=CRMActivity, status_code=status.HTTP_201_CREATED)
def create_activity(payload: CRMActivityCreate) -> CRMActivity:
    try:
        return store.create_activity(payload)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/summary", response_model=CRMSummary)
def get_crm_summary() -> CRMSummary:
    return crm_service.summary()
