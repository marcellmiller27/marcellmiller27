# JHI-SIG: 69M2705M | Admin (System Administrator) API | John Henry Investments (proprietary)
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.admin_models import (
    ActiveChangeRequest,
    AdminOverview,
    AdminUserCreate,
    AdminUserRead,
    RoleChangeRequest,
    RoleMatrixEntry,
)
from app.admin_services import AdminService
from app.database import get_db
from app.dependencies import require_permission
from app.foundation_models import AuditLogRead, Principal

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/overview", response_model=AdminOverview)
def overview(
    _p: Annotated[Principal, Depends(require_permission("admin:access"))],
    db: Annotated[Session, Depends(get_db)],
) -> AdminOverview:
    return AdminService(db).overview()


@router.get("/users", response_model=list[AdminUserRead])
def list_users(
    _p: Annotated[Principal, Depends(require_permission("users:read"))],
    db: Annotated[Session, Depends(get_db)],
) -> list[AdminUserRead]:
    return AdminService(db).list_users()


@router.post("/users", response_model=AdminUserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: AdminUserCreate,
    principal: Annotated[Principal, Depends(require_permission("users:manage"))],
    db: Annotated[Session, Depends(get_db)],
) -> AdminUserRead:
    try:
        return AdminService(db).create_user(payload, principal)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.patch("/users/{user_id}/active", response_model=AdminUserRead)
def set_active(
    user_id: str,
    payload: ActiveChangeRequest,
    principal: Annotated[Principal, Depends(require_permission("users:manage"))],
    db: Annotated[Session, Depends(get_db)],
) -> AdminUserRead:
    try:
        return AdminService(db).set_active(user_id, payload.is_active, principal)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.patch("/users/{user_id}/role", response_model=AdminUserRead)
def change_role(
    user_id: str,
    payload: RoleChangeRequest,
    principal: Annotated[Principal, Depends(require_permission("users:manage"))],
    db: Annotated[Session, Depends(get_db)],
) -> AdminUserRead:
    try:
        return AdminService(db).change_role(user_id, payload.role, principal)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/users/{user_id}/reset-mfa", response_model=AdminUserRead)
def reset_mfa(
    user_id: str,
    principal: Annotated[Principal, Depends(require_permission("users:manage"))],
    db: Annotated[Session, Depends(get_db)],
) -> AdminUserRead:
    try:
        return AdminService(db).reset_mfa(user_id, principal)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/roles", response_model=list[RoleMatrixEntry])
def roles_matrix(
    _p: Annotated[Principal, Depends(require_permission("roles:read"))],
    db: Annotated[Session, Depends(get_db)],
) -> list[RoleMatrixEntry]:
    return AdminService(db).roles_matrix()


@router.get("/audit-logs", response_model=list[AuditLogRead])
def audit_logs(
    _p: Annotated[Principal, Depends(require_permission("audit:read"))],
    db: Annotated[Session, Depends(get_db)],
) -> list[AuditLogRead]:
    return AdminService(db).list_audit()
