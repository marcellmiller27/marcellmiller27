# JHI-SIG: 69M2705M | Platform spine | John Henry Investments (proprietary)
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
