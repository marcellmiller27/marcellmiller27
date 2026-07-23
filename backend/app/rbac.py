"""JHI-SIG: 69M2705M | RBAC foundation | JHI Research & Analytics Firm, Inc. (proprietary)

Access control primitives. Staff (JHI Founder + employees) are identified by an email
allowlist (`JHI_STAFF_EMAILS`, comma-separated) until a dedicated staff role/column lands.
Back-office modules (Accounting, Admin, etc.) require staff; product APIs require an
authenticated subscriber (+ `require_premium` for T1/T2 features).
"""
import os
from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.dependencies import get_current_principal
from app.foundation_models import Principal


def staff_emails() -> set[str]:
    raw = os.getenv("JHI_STAFF_EMAILS", "")
    return {e.strip().lower() for e in raw.split(",") if e.strip()}


def is_staff(principal: Principal) -> bool:
    return principal.email.lower() in staff_emails()


def require_staff(
    principal: Annotated[Principal, Depends(get_current_principal)],
) -> Principal:
    """Gate back-office / firm-operations modules to JHI staff only."""
    if not is_staff(principal):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff access required.",
        )
    return principal
