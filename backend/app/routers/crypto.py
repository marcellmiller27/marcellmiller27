from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crypto_models import (
    CryptoHoldingCreate,
    CryptoHoldingRead,
    CryptoHoldingsSummary,
    NetworksResponse,
)
from app.crypto_services import CryptoSecretRejected, CryptoService
from app.database import get_db
from app.dependencies import get_current_principal
from app.foundation_models import Principal

router = APIRouter(prefix="/crypto", tags=["crypto"])


@router.get("/networks", response_model=NetworksResponse)
def supported_networks(db: Annotated[Session, Depends(get_db)]) -> NetworksResponse:
    return CryptoService(db).networks()


@router.post("/holdings", response_model=CryptoHoldingRead, status_code=status.HTTP_201_CREATED)
def add_holding(
    payload: CryptoHoldingCreate,
    principal: Annotated[Principal, Depends(get_current_principal)],
    db: Annotated[Session, Depends(get_db)],
) -> CryptoHoldingRead:
    try:
        return CryptoService(db).add_holding(principal, payload)
    except CryptoSecretRejected as exc:
        # 422: the request is well-formed but semantically refused for safety.
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/holdings", response_model=list[CryptoHoldingRead])
def list_holdings(
    principal: Annotated[Principal, Depends(get_current_principal)],
    db: Annotated[Session, Depends(get_db)],
) -> list[CryptoHoldingRead]:
    return CryptoService(db).list_holdings(principal)


@router.get("/holdings/summary", response_model=CryptoHoldingsSummary)
def holdings_summary(
    principal: Annotated[Principal, Depends(get_current_principal)],
    db: Annotated[Session, Depends(get_db)],
) -> CryptoHoldingsSummary:
    return CryptoService(db).summary(principal)


@router.delete("/holdings/{holding_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_holding(
    holding_id: str,
    principal: Annotated[Principal, Depends(get_current_principal)],
    db: Annotated[Session, Depends(get_db)],
) -> None:
    try:
        CryptoService(db).delete_holding(principal, holding_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
