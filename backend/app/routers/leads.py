import re
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.db_models import LeadDB
from app.dependencies import get_current_principal
from app.foundation_models import Principal
from app.lead_models import LeadCaptureResponse, LeadCount, LeadCreate, LeadRead

router = APIRouter(prefix="/leads", tags=["leads"])

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@router.post("", response_model=LeadCaptureResponse, status_code=status.HTTP_201_CREATED)
def capture_lead(
    payload: LeadCreate,
    db: Annotated[Session, Depends(get_db)],
) -> LeadCaptureResponse:
    email = payload.email.strip().lower()
    if not _EMAIL_RE.match(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Enter a valid email.")

    existing = db.scalar(select(LeadDB).where(LeadDB.email == email))
    total_before = db.scalar(select(func.count()).select_from(LeadDB)) or 0
    if existing is not None:
        return LeadCaptureResponse(
            status="already_on_list",
            message="You're already on the list — we'll be in touch.",
            total=total_before,
        )

    db.add(
        LeadDB(
            email=email,
            full_name=(payload.full_name.strip() if payload.full_name else None),
            interest=(payload.interest.strip() if payload.interest else None),
            source=payload.source.strip()[:80] or "waitlist",
        )
    )
    db.commit()
    return LeadCaptureResponse(
        status="captured",
        message="You're on the list! We'll email you with early access.",
        total=total_before + 1,
    )


@router.get("/count", response_model=LeadCount)
def lead_count(db: Annotated[Session, Depends(get_db)]) -> LeadCount:
    return LeadCount(count=db.scalar(select(func.count()).select_from(LeadDB)) or 0)


@router.get("", response_model=list[LeadRead])
def list_leads(
    _principal: Annotated[Principal, Depends(get_current_principal)],
    db: Annotated[Session, Depends(get_db)],
) -> list[LeadRead]:
    leads = db.scalars(select(LeadDB).order_by(LeadDB.created_at.desc())).all()
    return [
        LeadRead(
            id=lead.id,
            email=lead.email,
            full_name=lead.full_name,
            interest=lead.interest,
            source=lead.source,
            created_at=lead.created_at,
        )
        for lead in leads
    ]
