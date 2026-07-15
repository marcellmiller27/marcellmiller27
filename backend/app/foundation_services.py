import json
import re
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_models import AuditLogDB, MembershipDB, OrganizationDB, SubscriptionDB, UserDB
from app.foundation_models import (
    AuditLogRead,
    AuthResponse,
    BillingPlan,
    BillingWebhookEvent,
    CheckoutSessionRequest,
    CheckoutSessionResponse,
    LoginRequest,
    MeResponse,
    OrganizationRead,
    Principal,
    RegisterRequest,
    SubscriptionPlan,
    SubscriptionRead,
    SubscriptionStatus,
    UserRead,
    UserRole,
)
from app.security import create_access_token, hash_password, verify_password


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "organization"


def user_read(user: UserDB) -> UserRead:
    return UserRead(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        created_at=user.created_at,
    )


def organization_read(organization: OrganizationDB) -> OrganizationRead:
    return OrganizationRead(
        id=organization.id,
        name=organization.name,
        slug=organization.slug,
        created_at=organization.created_at,
    )


def subscription_read(subscription: SubscriptionDB) -> SubscriptionRead:
    return SubscriptionRead(
        id=subscription.id,
        organization_id=subscription.organization_id,
        plan=SubscriptionPlan(subscription.plan),
        status=SubscriptionStatus(subscription.status),
        provider=subscription.provider,
        provider_customer_id=subscription.provider_customer_id,
        provider_subscription_id=subscription.provider_subscription_id,
        current_period_end=subscription.current_period_end,
        created_at=subscription.created_at,
        updated_at=subscription.updated_at,
    )


class FoundationService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def register(self, payload: RegisterRequest) -> AuthResponse:
        email = payload.email.lower().strip()
        existing_user = self.db.scalar(select(UserDB).where(UserDB.email == email))
        if existing_user is not None:
            raise ValueError("A user with this email already exists.")

        base_slug = slugify(payload.organization_name)
        slug = base_slug
        index = 2
        while self.db.scalar(select(OrganizationDB).where(OrganizationDB.slug == slug)) is not None:
            slug = f"{base_slug}-{index}"
            index += 1

        organization = OrganizationDB(name=payload.organization_name, slug=slug)
        user = UserDB(
            email=email,
            full_name=payload.full_name,
            password_hash=hash_password(payload.password),
        )
        self.db.add_all([organization, user])
        self.db.flush()

        membership = MembershipDB(
            organization_id=organization.id,
            user_id=user.id,
            role=UserRole.ADMIN.value,
        )
        subscription = SubscriptionDB(
            organization_id=organization.id,
            plan=payload.plan.value,
            status=SubscriptionStatus.TRIALING.value,
            provider="stripe",
        )
        self.db.add_all([membership, subscription])
        self.audit(
            action="organization.registered",
            resource_type="organization",
            resource_id=organization.id,
            organization_id=organization.id,
            actor_user_id=user.id,
            event={"plan": payload.plan.value, "email": email},
        )
        self.db.commit()
        return self._auth_response(user, organization, membership, subscription)

    def login(self, payload: LoginRequest) -> AuthResponse:
        email = payload.email.lower().strip()
        user = self.db.scalar(select(UserDB).where(UserDB.email == email))
        if user is None or not verify_password(payload.password, user.password_hash):
            raise ValueError("Invalid email or password.")
        if not user.is_active:
            raise ValueError("User account is inactive.")
        membership = self._primary_membership(user.id)
        organization = self.db.get(OrganizationDB, membership.organization_id)
        subscription = self._current_subscription(organization.id)
        self.audit(
            action="auth.login",
            resource_type="user",
            resource_id=user.id,
            organization_id=organization.id,
            actor_user_id=user.id,
            event={"email": email},
        )
        self.db.commit()
        return self._auth_response(user, organization, membership, subscription)

    def me(self, principal: Principal) -> MeResponse:
        user = self.db.get(UserDB, principal.user_id)
        organization = self.db.get(OrganizationDB, principal.organization_id)
        subscription = self._current_subscription(principal.organization_id)
        return MeResponse(
            user=user_read(user),
            organization=organization_read(organization),
            role=principal.role,
            subscription=subscription_read(subscription),
        )

    def billing_plans(self) -> list[BillingPlan]:
        return [
            BillingPlan(
                plan=SubscriptionPlan.CONSUMER,
                name="Consumer Plan",
                price_label="$50/month",
                stripe_price_env="STRIPE_CONSUMER_PRICE_ID",
                features=["Dashboard", "Market intelligence", "AI assistant", "Opportunity scanner"],
                seats="1 user seat",
            ),
            BillingPlan(
                plan=SubscriptionPlan.PROFESSIONAL,
                name="Professional Plan",
                price_label="$299/month",
                stripe_price_env="STRIPE_PROFESSIONAL_PRICE_ID",
                features=["Acquisition engine", "Due diligence", "Financial reports", "CRM pipeline"],
                seats="1 user seat",
            ),
            BillingPlan(
                plan=SubscriptionPlan.ENTERPRISE,
                name="Enterprise / Family Office Plan",
                price_label="$1,500/month (5 seats) + $99/additional seat",
                stripe_price_env="STRIPE_ENTERPRISE_PRICE_ID",
                features=[
                    "Team accounts & role permissions",
                    "5 user seats included",
                    "Additional seats — $99 / seat / month",
                    "Integrations, branded reports & advanced controls",
                ],
                seats="5 seats included · +$99 / additional seat",
            ),
        ]

    def create_checkout_session(
        self,
        principal: Principal,
        payload: CheckoutSessionRequest,
    ) -> CheckoutSessionResponse:
        subscription = self._current_subscription(principal.organization_id)
        subscription.plan = payload.plan.value
        subscription.status = SubscriptionStatus.INCOMPLETE.value
        subscription.updated_at = datetime.now(timezone.utc)
        self.audit(
            action="billing.checkout_requested",
            resource_type="subscription",
            resource_id=subscription.id,
            organization_id=principal.organization_id,
            actor_user_id=principal.user_id,
            event={"plan": payload.plan.value},
        )
        self.db.commit()
        return CheckoutSessionResponse(
            provider="stripe",
            checkout_url=(
                f"{payload.success_url}?checkout=mock&plan={payload.plan.value}"
                if payload.success_url
                else "https://billing.example.test/checkout"
            ),
            plan=payload.plan,
            status="checkout_session_created",
            message="Stripe checkout contract is ready; configure Stripe SDK and price IDs for live billing.",
        )

    def apply_billing_webhook(self, payload: BillingWebhookEvent) -> SubscriptionRead:
        subscription = self._current_subscription(payload.organization_id)
        if payload.plan is not None:
            subscription.plan = payload.plan.value
        if payload.status is not None:
            subscription.status = payload.status.value
        if payload.provider_customer_id is not None:
            subscription.provider_customer_id = payload.provider_customer_id
        if payload.provider_subscription_id is not None:
            subscription.provider_subscription_id = payload.provider_subscription_id
        subscription.updated_at = datetime.now(timezone.utc)
        self.audit(
            action=f"billing.webhook.{payload.event_type}",
            resource_type="subscription",
            resource_id=subscription.id,
            organization_id=payload.organization_id,
            actor_user_id=None,
            event={"status": subscription.status, "plan": subscription.plan},
        )
        self.db.commit()
        return subscription_read(subscription)

    def list_audit_logs(self, principal: Principal) -> list[AuditLogRead]:
        logs = self.db.scalars(
            select(AuditLogDB)
            .where(AuditLogDB.organization_id == principal.organization_id)
            .order_by(AuditLogDB.created_at.desc())
        ).all()
        return [
            AuditLogRead(
                id=log.id,
                organization_id=log.organization_id,
                actor_user_id=log.actor_user_id,
                action=log.action,
                resource_type=log.resource_type,
                resource_id=log.resource_id,
                event=json.loads(log.event_json),
                created_at=log.created_at,
            )
            for log in logs
        ]

    def audit(
        self,
        action: str,
        resource_type: str,
        resource_id: str | None,
        organization_id: str | None,
        actor_user_id: str | None,
        event: dict[str, str],
    ) -> None:
        self.db.add(
            AuditLogDB(
                organization_id=organization_id,
                actor_user_id=actor_user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                event_json=json.dumps(event),
            )
        )

    def _primary_membership(self, user_id: str) -> MembershipDB:
        membership = self.db.scalar(select(MembershipDB).where(MembershipDB.user_id == user_id))
        if membership is None:
            raise ValueError("User does not belong to an organization.")
        return membership

    def _current_subscription(self, organization_id: str) -> SubscriptionDB:
        subscription = self.db.scalar(
            select(SubscriptionDB).where(SubscriptionDB.organization_id == organization_id)
        )
        if subscription is None:
            subscription = SubscriptionDB(
                organization_id=organization_id,
                plan=SubscriptionPlan.CONSUMER.value,
                status=SubscriptionStatus.TRIALING.value,
                provider="stripe",
            )
            self.db.add(subscription)
            self.db.flush()
        return subscription

    def _auth_response(
        self,
        user: UserDB,
        organization: OrganizationDB,
        membership: MembershipDB,
        subscription: SubscriptionDB,
    ) -> AuthResponse:
        token = create_access_token(
            {
                "sub": user.id,
                "organization_id": organization.id,
                "role": membership.role,
                "email": user.email,
            }
        )
        return AuthResponse(
            access_token=token,
            user=user_read(user),
            organization=organization_read(organization),
            role=UserRole(membership.role),
            subscription=subscription_read(subscription),
        )
