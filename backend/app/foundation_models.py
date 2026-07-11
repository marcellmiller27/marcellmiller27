from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class UserRole(StrEnum):
    ADMIN = "admin"
    INVESTOR = "investor"
    ADVISOR = "advisor"
    CPA = "cpa"
    ATTORNEY = "attorney"
    BANKER = "banker"
    FAMILY_OFFICE = "family_office"
    ENTERPRISE = "enterprise"


class SubscriptionPlan(StrEnum):
    CONSUMER = "consumer"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(StrEnum):
    TRIALING = "trialing"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    INCOMPLETE = "incomplete"


class OrganizationRead(BaseModel):
    id: str
    name: str
    slug: str
    created_at: datetime


class UserRead(BaseModel):
    id: str
    email: str
    full_name: str
    is_active: bool
    created_at: datetime


class SubscriptionRead(BaseModel):
    id: str
    organization_id: str
    plan: SubscriptionPlan
    status: SubscriptionStatus
    provider: str
    provider_customer_id: str | None = None
    provider_subscription_id: str | None = None
    current_period_end: datetime | None = None
    created_at: datetime
    updated_at: datetime


class RegisterRequest(BaseModel):
    organization_name: str
    full_name: str
    email: str
    password: str = Field(min_length=8)
    plan: SubscriptionPlan = SubscriptionPlan.CONSUMER


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead
    organization: OrganizationRead
    role: UserRole
    subscription: SubscriptionRead


class Principal(BaseModel):
    user_id: str
    organization_id: str
    role: UserRole
    email: str


class MeResponse(BaseModel):
    user: UserRead
    organization: OrganizationRead
    role: UserRole
    subscription: SubscriptionRead


class BillingPlan(BaseModel):
    plan: SubscriptionPlan
    name: str
    price_label: str
    stripe_price_env: str
    features: list[str]


class CheckoutSessionRequest(BaseModel):
    plan: SubscriptionPlan
    success_url: str
    cancel_url: str


class CheckoutSessionResponse(BaseModel):
    provider: str
    checkout_url: str
    plan: SubscriptionPlan
    status: str
    message: str


class BillingWebhookEvent(BaseModel):
    event_type: str
    organization_id: str
    plan: SubscriptionPlan | None = None
    status: SubscriptionStatus | None = None
    provider_customer_id: str | None = None
    provider_subscription_id: str | None = None


class AuditLogRead(BaseModel):
    id: str
    organization_id: str | None
    actor_user_id: str | None
    action: str
    resource_type: str
    resource_id: str | None
    event: dict[str, str]
    created_at: datetime
