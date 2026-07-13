# JHI-SIG: 69M2705M | Admin (System Administrator) models | John Henry Investments (proprietary)
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.foundation_models import UserRole


class AdminUserRead(BaseModel):
    id: str
    email: str
    full_name: str
    is_active: bool
    role: UserRole
    organization_id: str | None = None
    organization_name: str | None = None
    two_factor_enabled: bool = False
    created_at: datetime


class AdminUserCreate(BaseModel):
    email: str
    full_name: str
    role: UserRole = UserRole.INVESTOR
    password: str = Field(min_length=8)
    organization_id: str | None = None  # defaults to the acting admin's org


class RoleChangeRequest(BaseModel):
    role: UserRole


class ActiveChangeRequest(BaseModel):
    is_active: bool


class RoleMatrixEntry(BaseModel):
    role: UserRole
    permissions: list[str]
    is_super_admin: bool = False


class AdminOverview(BaseModel):
    total_users: int
    active_users: int
    admins: int
    organizations: int
    two_factor_enabled: int
    recent_admin_actions: int
    enforce_auth: bool
