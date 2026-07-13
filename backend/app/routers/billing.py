from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.billing_webhook import verify_and_parse
from app.database import get_db
from app.dependencies import get_current_principal, require_admin
from app.foundation_models import (
    AuditLogRead,
    BillingPlan,
    CheckoutSessionRequest,
    CheckoutSessionResponse,
    MeResponse,
    Principal,
    SubscriptionRead,
)
from app.foundation_services import FoundationService

router = APIRouter(prefix="/billing", tags=["billing"])


@router.get("/plans", response_model=list[BillingPlan])
def list_plans(db: Annotated[Session, Depends(get_db)]) -> list[BillingPlan]:
    return FoundationService(db).billing_plans()


@router.get("/subscription", response_model=MeResponse)
def current_subscription(
    principal: Annotated[Principal, Depends(get_current_principal)],
    db: Annotated[Session, Depends(get_db)],
) -> MeResponse:
    return FoundationService(db).me(principal)


@router.post("/checkout-session", response_model=CheckoutSessionResponse)
def create_checkout_session(
    payload: CheckoutSessionRequest,
    principal: Annotated[Principal, Depends(get_current_principal)],
    db: Annotated[Session, Depends(get_db)],
) -> CheckoutSessionResponse:
    return FoundationService(db).create_checkout_session(principal, payload)


@router.post("/webhook", response_model=SubscriptionRead)
async def billing_webhook(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> SubscriptionRead:
    raw_body = await request.body()
    signature = request.headers.get("stripe-signature")
    try:
        event = verify_and_parse(raw_body, signature)
        return FoundationService(db).apply_billing_webhook(event)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/audit-logs", response_model=list[AuditLogRead])
def list_billing_audit_logs(
    principal: Annotated[Principal, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)],
) -> list[AuditLogRead]:
    return FoundationService(db).list_audit_logs(principal)
