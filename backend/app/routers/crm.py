from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crm_services import CRMService
from app.database import get_db
from app.models import (
    CRMActivity,
    CRMActivityCreate,
    CRMContact,
    CRMContactCreate,
    CRMDeal,
    CRMDealCreate,
    CRMSummary,
)

router = APIRouter(prefix="/crm", tags=["crm"])
crm_service = CRMService()


@router.get("/contacts", response_model=list[CRMContact])
def list_contacts(db: Annotated[Session, Depends(get_db)]) -> list[CRMContact]:
    return crm_service.list_contacts(db)


@router.post("/contacts", response_model=CRMContact, status_code=status.HTTP_201_CREATED)
def create_contact(
    payload: CRMContactCreate, db: Annotated[Session, Depends(get_db)]
) -> CRMContact:
    return crm_service.create_contact(db, payload)


@router.get("/deals", response_model=list[CRMDeal])
def list_deals(db: Annotated[Session, Depends(get_db)]) -> list[CRMDeal]:
    return crm_service.list_deals(db)


@router.post("/deals", response_model=CRMDeal, status_code=status.HTTP_201_CREATED)
def create_deal(payload: CRMDealCreate, db: Annotated[Session, Depends(get_db)]) -> CRMDeal:
    try:
        return crm_service.create_deal(db, payload)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/activities", response_model=list[CRMActivity])
def list_activities(db: Annotated[Session, Depends(get_db)]) -> list[CRMActivity]:
    return crm_service.list_activities(db)


@router.post("/activities", response_model=CRMActivity, status_code=status.HTTP_201_CREATED)
def create_activity(
    payload: CRMActivityCreate, db: Annotated[Session, Depends(get_db)]
) -> CRMActivity:
    try:
        return crm_service.create_activity(db, payload)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/summary", response_model=CRMSummary)
def get_crm_summary(db: Annotated[Session, Depends(get_db)]) -> CRMSummary:
    return crm_service.summary(db)
