# JHI-SIG: 69M2705M | Deal Pipeline | JHI Research & Analytics Firm, Inc. (proprietary)
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.pipeline_models import (
    STAGES,
    DealRecord,
    DealRecordCreate,
    DealRecordUpdate,
)
from app.pipeline_services import PipelineError, PipelineService

router = APIRouter(prefix="/pipeline", tags=["pipeline"])
_service = PipelineService()


@router.get("/stages")
def list_stages() -> list[str]:
    """Ordered pipeline stages (Screen → Analysis → QoE → Financing → Offer → Closed/Passed)."""
    return STAGES


@router.get("/deals", response_model=list[DealRecord])
def list_deals(db: Annotated[Session, Depends(get_db)]) -> list[DealRecord]:
    return _service.list(db)


@router.post("/deals", response_model=DealRecord)
def create_deal(payload: DealRecordCreate, db: Annotated[Session, Depends(get_db)]) -> DealRecord:
    try:
        return _service.create(db, payload)
    except PipelineError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/deals/{deal_id}", response_model=DealRecord)
def get_deal(deal_id: str, db: Annotated[Session, Depends(get_db)]) -> DealRecord:
    try:
        return _service.get(db, deal_id)
    except PipelineError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.patch("/deals/{deal_id}", response_model=DealRecord)
def update_deal(
    deal_id: str, payload: DealRecordUpdate, db: Annotated[Session, Depends(get_db)]
) -> DealRecord:
    try:
        return _service.update(db, deal_id, payload)
    except PipelineError as exc:
        code = 404 if "not found" in str(exc).lower() else 400
        raise HTTPException(status_code=code, detail=str(exc)) from exc


@router.delete("/deals/{deal_id}")
def delete_deal(deal_id: str, db: Annotated[Session, Depends(get_db)]) -> dict[str, bool]:
    try:
        _service.delete(db, deal_id)
    except PipelineError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"deleted": True}
