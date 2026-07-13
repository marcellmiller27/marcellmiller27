# JHI-SIG: 69M2705M | Admin (System Administrator) service | John Henry Investments (proprietary)
"""Gatekeeper P0 admin operations: user management, roles matrix, audit — all audited.

Guardrails: an admin cannot deactivate or demote their own account (prevents lockout).
Full org-admin scoping, invitations/approvals, and impersonation are P1.
"""

from __future__ import annotations

import json

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.admin_models import (
    AdminOverview,
    AdminUserCreate,
    AdminUserRead,
    RoleMatrixEntry,
)
from app.config import get_settings
from app.db_models import (
    AuditLogDB,
    MembershipDB,
    OrganizationDB,
    UserDB,
    UserSecurityDB,
)
from app.foundation_models import AuditLogRead, Principal, UserRole
from app.rbac import PERMISSIONS, is_super_admin, permissions_for
from app.security import hash_password


class AdminService:
    def __init__(self, db: Session) -> None:
        self.db = db

    # -- reads ------------------------------------------------------------ #
    def list_users(self, limit: int = 500) -> list[AdminUserRead]:
        users = self.db.scalars(select(UserDB).order_by(UserDB.created_at.desc()).limit(limit)).all()
        orgs = {o.id: o for o in self.db.scalars(select(OrganizationDB)).all()}
        roles = {m.user_id: m for m in self.db.scalars(select(MembershipDB)).all()}
        mfa = {s.user_id: s for s in self.db.scalars(select(UserSecurityDB)).all()}
        out: list[AdminUserRead] = []
        for u in users:
            m = roles.get(u.id)
            org = orgs.get(m.organization_id) if m else None
            sec = mfa.get(u.id)
            out.append(
                AdminUserRead(
                    id=u.id,
                    email=u.email,
                    full_name=u.full_name,
                    is_active=u.is_active,
                    role=UserRole(m.role) if m else UserRole.INVESTOR,
                    organization_id=org.id if org else None,
                    organization_name=org.name if org else None,
                    two_factor_enabled=bool(sec.two_factor_enabled) if sec else False,
                    created_at=u.created_at,
                )
            )
        return out

    def overview(self) -> AdminOverview:
        total = self.db.scalar(select(func.count()).select_from(UserDB)) or 0
        active = self.db.scalar(select(func.count()).select_from(UserDB).where(UserDB.is_active.is_(True))) or 0
        admins = self.db.scalar(
            select(func.count()).select_from(MembershipDB).where(MembershipDB.role == UserRole.ADMIN.value)
        ) or 0
        orgs = self.db.scalar(select(func.count()).select_from(OrganizationDB)) or 0
        mfa = self.db.scalar(
            select(func.count()).select_from(UserSecurityDB).where(UserSecurityDB.two_factor_enabled.is_(True))
        ) or 0
        admin_actions = self.db.scalar(
            select(func.count()).select_from(AuditLogDB).where(AuditLogDB.action.like("admin.%"))
        ) or 0
        return AdminOverview(
            total_users=total,
            active_users=active,
            admins=admins,
            organizations=orgs,
            two_factor_enabled=mfa,
            recent_admin_actions=admin_actions,
            enforce_auth=get_settings().enforce_auth,
        )

    def roles_matrix(self) -> list[RoleMatrixEntry]:
        return [
            RoleMatrixEntry(
                role=role,
                permissions=sorted(permissions_for(role)),
                is_super_admin=is_super_admin(role),
            )
            for role in UserRole
        ]

    def all_permissions(self) -> list[str]:
        return list(PERMISSIONS)

    def list_audit(self, limit: int = 200) -> list[AuditLogRead]:
        logs = self.db.scalars(
            select(AuditLogDB).order_by(AuditLogDB.created_at.desc()).limit(limit)
        ).all()
        return [
            AuditLogRead(
                id=x.id,
                organization_id=x.organization_id,
                actor_user_id=x.actor_user_id,
                action=x.action,
                resource_type=x.resource_type,
                resource_id=x.resource_id,
                event=json.loads(x.event_json),
                created_at=x.created_at,
            )
            for x in logs
        ]

    # -- mutations (audited) --------------------------------------------- #
    def create_user(self, payload: AdminUserCreate, actor: Principal) -> AdminUserRead:
        email = payload.email.lower().strip()
        if self.db.scalar(select(UserDB).where(UserDB.email == email)) is not None:
            raise ValueError("A user with this email already exists.")
        org_id = payload.organization_id or actor.organization_id
        if self.db.get(OrganizationDB, org_id) is None:
            raise ValueError("Unknown organization.")
        user = UserDB(email=email, full_name=payload.full_name, password_hash=hash_password(payload.password))
        self.db.add(user)
        self.db.flush()
        self.db.add(MembershipDB(organization_id=org_id, user_id=user.id, role=payload.role.value))
        self._audit(actor, "admin.user.created", "user", user.id, {"email": email, "role": payload.role.value})
        self.db.commit()
        return self._read_one(user.id)

    def set_active(self, user_id: str, is_active: bool, actor: Principal) -> AdminUserRead:
        if user_id == actor.user_id and not is_active:
            raise ValueError("You cannot deactivate your own account.")
        user = self.db.get(UserDB, user_id)
        if user is None:
            raise KeyError("User not found.")
        user.is_active = is_active
        self._audit(actor, "admin.user.active_changed", "user", user_id, {"is_active": str(is_active)})
        self.db.commit()
        return self._read_one(user_id)

    def change_role(self, user_id: str, role: UserRole, actor: Principal) -> AdminUserRead:
        if user_id == actor.user_id and role != UserRole.ADMIN:
            raise ValueError("You cannot remove your own admin role.")
        membership = self.db.scalar(select(MembershipDB).where(MembershipDB.user_id == user_id))
        if membership is None:
            raise KeyError("User membership not found.")
        old = membership.role
        membership.role = role.value
        self._audit(actor, "admin.user.role_changed", "user", user_id, {"from": old, "to": role.value})
        self.db.commit()
        return self._read_one(user_id)

    def reset_mfa(self, user_id: str, actor: Principal) -> AdminUserRead:
        user = self.db.get(UserDB, user_id)
        if user is None:
            raise KeyError("User not found.")
        sec = self.db.scalar(select(UserSecurityDB).where(UserSecurityDB.user_id == user_id))
        if sec is not None:
            sec.two_factor_enabled = False
            sec.totp_secret = None
        self._audit(actor, "admin.user.mfa_reset", "user", user_id, {})
        self.db.commit()
        return self._read_one(user_id)

    # -- internals -------------------------------------------------------- #
    def _read_one(self, user_id: str) -> AdminUserRead:
        for u in self.list_users():
            if u.id == user_id:
                return u
        raise KeyError("User not found.")

    def _audit(self, actor: Principal, action: str, resource_type: str, resource_id: str, event: dict) -> None:
        self.db.add(
            AuditLogDB(
                organization_id=actor.organization_id,
                actor_user_id=actor.user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                event_json=json.dumps(event),
            )
        )
