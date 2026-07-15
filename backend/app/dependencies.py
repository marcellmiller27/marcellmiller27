from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.db_models import UserDB
from app.foundation_models import Principal, UserRole
from app.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_principal(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> Principal:
    try:
        payload = decode_access_token(token)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token.",
        ) from exc

    user = db.get(UserDB, payload["sub"])
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")

    return Principal(
        user_id=payload["sub"],
        organization_id=payload["organization_id"],
        role=UserRole(payload["role"]),
        email=payload["email"],
    )


def require_admin(principal: Annotated[Principal, Depends(get_current_principal)]) -> Principal:
    if principal.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required.")
    return principal


def require_premium(
    principal: Annotated[Principal, Depends(get_current_principal)],
    db: Annotated[Session, Depends(get_db)],
) -> Principal:
    """Gate premium features to the paid tiers: T1 (Enterprise) and T2 (Professional).
    T3 (Consumer / individual) is denied."""
    from app.foundation_models import SubscriptionPlan
    from app.foundation_services import FoundationService

    subscription = FoundationService(db).me(principal).subscription
    if subscription.plan not in (SubscriptionPlan.PROFESSIONAL, SubscriptionPlan.ENTERPRISE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="A Professional (T2) or Enterprise (T1) plan is required for this feature.",
        )
    return principal
