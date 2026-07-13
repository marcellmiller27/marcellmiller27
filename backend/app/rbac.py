# JHI-SIG: 69M2705M | RBAC role -> permission map | John Henry Investments (proprietary)
"""Role-based access control: capability strings and per-role permission sets.

Gatekeeper P0 uses fixed, code-defined permission sets (seeded from the existing
UserRole values). A full editable role/permission matrix (DB-backed) is P1. The
platform super-admin (UserRole.ADMIN) holds every permission.
"""

from __future__ import annotations

from app.foundation_models import UserRole

# Capability catalog: "<resource>:<action>". Keep additive.
PERMISSIONS: tuple[str, ...] = (
    "admin:access",       # open the Admin control plane
    "users:read",
    "users:manage",       # invite / deactivate / change role / reset MFA
    "roles:read",
    "audit:read",
    "accounting:read",
    "accounting:post",
    "crm:read",
    "crm:write",
    "reports:read",
    "research:read",
    "deals:read",
    "deals:write",
    "integrations:manage",
)

# Common member permission set (read/use the product, no admin control plane).
_MEMBER: frozenset[str] = frozenset(
    {
        "accounting:read",
        "crm:read",
        "reports:read",
        "research:read",
        "deals:read",
        "deals:write",
    }
)

# Per-role permission sets. ADMIN = platform super-admin (all permissions).
ROLE_PERMISSIONS: dict[UserRole, frozenset[str]] = {
    UserRole.ADMIN: frozenset(PERMISSIONS),
    UserRole.INVESTOR: _MEMBER,
    UserRole.FAMILY_OFFICE: _MEMBER | {"crm:write"},
    UserRole.ENTERPRISE: _MEMBER | {"crm:write", "accounting:post", "integrations:manage"},
    UserRole.ADVISOR: _MEMBER | {"crm:write"},
    UserRole.CPA: _MEMBER | {"accounting:post"},
    UserRole.ATTORNEY: _MEMBER,
    UserRole.BANKER: _MEMBER,
}


def permissions_for(role: UserRole) -> frozenset[str]:
    return ROLE_PERMISSIONS.get(role, _MEMBER)


def role_has_permission(role: UserRole, permission: str) -> bool:
    return permission in permissions_for(role)


def is_super_admin(role: UserRole) -> bool:
    return role == UserRole.ADMIN
