# JHI-SIG: 69M2705M | ORM models | John Henry Investments (proprietary)
from datetime import date, datetime, timezone
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def new_id() -> str:
    return str(uuid4())


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class OrganizationDB(Base):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    memberships: Mapped[list["MembershipDB"]] = relationship(back_populates="organization")
    subscriptions: Mapped[list["SubscriptionDB"]] = relationship(back_populates="organization")


class UserDB(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    memberships: Mapped[list["MembershipDB"]] = relationship(back_populates="user")


class MembershipDB(Base):
    __tablename__ = "organization_memberships"
    __table_args__ = (UniqueConstraint("organization_id", "user_id"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(80), nullable=False, default="admin")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    organization: Mapped[OrganizationDB] = relationship(back_populates="memberships")
    user: Mapped[UserDB] = relationship(back_populates="memberships")


class SubscriptionDB(Base):
    __tablename__ = "subscriptions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    plan: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(80), nullable=False, default="trialing")
    provider: Mapped[str] = mapped_column(String(80), nullable=False, default="stripe")
    provider_customer_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    provider_subscription_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    current_period_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    organization: Mapped[OrganizationDB] = relationship(back_populates="subscriptions")


class UserSecurityDB(Base):
    __tablename__ = "user_security"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)
    totp_secret: Mapped[str | None] = mapped_column(String(64), nullable=True)
    two_factor_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class DeviceCredentialDB(Base):
    __tablename__ = "device_credentials"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    credential_id: Mapped[str] = mapped_column(String(512), nullable=False, unique=True, index=True)
    public_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    label: Mapped[str] = mapped_column(String(120), nullable=False, default="Mobile device")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class CRMContactDB(Base):
    """Durable CRM contact (migrated from the in-memory store)."""

    __tablename__ = "crm_contacts"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    organization: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    phone: Mapped[str] = mapped_column(String(40), nullable=False, default="")
    role: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    relationship_type: Mapped[str] = mapped_column(String(80), nullable=False, default="prospect")
    owner: Mapped[str] = mapped_column(String(120), nullable=False, default="platform")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class CRMDealDB(Base):
    __tablename__ = "crm_deals"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    contact_id: Mapped[str] = mapped_column(ForeignKey("crm_contacts.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    stage: Mapped[str] = mapped_column(String(40), nullable=False, default="lead")
    expected_value: Mapped[str] = mapped_column(String(40), nullable=False, default="0.00")
    probability: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    next_step: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class CRMActivityDB(Base):
    __tablename__ = "crm_activities"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    contact_id: Mapped[str] = mapped_column(ForeignKey("crm_contacts.id"), nullable=False, index=True)
    deal_id: Mapped[str | None] = mapped_column(ForeignKey("crm_deals.id"), nullable=True)
    activity_type: Mapped[str] = mapped_column(String(80), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class AccountDB(Base):
    """Chart-of-accounts entry (durable)."""

    __tablename__ = "accounts"

    code: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    account_type: Mapped[str] = mapped_column(String(20), nullable=False)
    # Sub-section for statement grouping (e.g. "Current Assets", "Cost of Revenue").
    category: Mapped[str] = mapped_column(String(120), nullable=False, default="")


class JournalEntryDB(Base):
    __tablename__ = "journal_entries"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    entry_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    memo: Mapped[str] = mapped_column(String(500), nullable=False)
    source_module: Mapped[str] = mapped_column(String(80), nullable=False, default="manual")
    created_by: Mapped[str] = mapped_column(String(120), nullable=False, default="system")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="posted")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=utc_now)


class JournalLineDB(Base):
    __tablename__ = "journal_lines"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    entry_id: Mapped[str] = mapped_column(ForeignKey("journal_entries.id"), nullable=False, index=True)
    line_no: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    account_code: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    debit: Mapped[str] = mapped_column(String(40), nullable=False, default="0.00")
    credit: Mapped[str] = mapped_column(String(40), nullable=False, default="0.00")
    entity: Mapped[str] = mapped_column(String(120), nullable=False, default="John Henry Investments, LLC")
    department: Mapped[str] = mapped_column(String(120), nullable=False, default="Platform")
    account_name: Mapped[str] = mapped_column(String(255), nullable=False)
    account_type: Mapped[str] = mapped_column(String(20), nullable=False)


class SupportTicketDB(Base):
    """An escalated support ticket forwarded to the founder for further action."""

    __tablename__ = "support_tickets"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    user_email: Mapped[str | None] = mapped_column(String(320), nullable=True, index=True)
    agent: Mapped[str] = mapped_column(String(80), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str | None] = mapped_column(String(80), nullable=True)
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="normal")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="open")
    assigned_to: Mapped[str] = mapped_column(String(80), nullable=False, default="founder")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class LeadDB(Base):
    """A marketing waitlist / lead captured from the GTM funnel (public)."""

    __tablename__ = "leads"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    email: Mapped[str] = mapped_column(String(320), nullable=False, index=True)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    interest: Mapped[str | None] = mapped_column(String(80), nullable=True)
    source: Mapped[str] = mapped_column(String(80), nullable=False, default="waitlist")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class AuditLogDB(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    organization_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    actor_user_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(160), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(120), nullable=False)
    resource_id: Mapped[str | None] = mapped_column(String, nullable=True)
    event_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class DealRecordDB(Base):
    """A saved acquisition target in the Deal Pipeline (Deal X-Ray or QoE analysis).

    Turns the stateless analyzers into a workflow: save a run, move it through stages,
    revisit and compare. (Single-tenant for now; scope by organization when auth is
    wired into these module endpoints.)
    """

    __tablename__ = "pipeline_deals"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    business_name: Mapped[str] = mapped_column(String(255), nullable=False)
    deal_type: Mapped[str] = mapped_column(String(40), nullable=False, default="deal_xray")
    stage: Mapped[str] = mapped_column(String(40), nullable=False, default="screen", index=True)
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    recommendation: Mapped[str] = mapped_column(String(60), nullable=False, default="")
    headline: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    inputs_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    notes: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )


class IntegrationConnectionDB(Base):
    """Durable external-integration connection (migrated from the in-memory store)."""

    __tablename__ = "integration_connections"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    connector_key: Mapped[str] = mapped_column(String(80), nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    credential_reference: Mapped[str] = mapped_column(String(255), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="connected")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class SyncJobDB(Base):
    __tablename__ = "integration_sync_jobs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    connection_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    object_type: Mapped[str] = mapped_column(String(80), nullable=False)
    direction: Mapped[str] = mapped_column(String(40), nullable=False)
    requested_by: Mapped[str] = mapped_column(String(120), nullable=False, default="system")
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="queued")
    records_processed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    message: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class BankingTransactionDB(Base):
    __tablename__ = "integration_banking_transactions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    connection_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    external_id: Mapped[str] = mapped_column(String(120), nullable=False)
    account_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    amount: Mapped[str] = mapped_column(String(40), nullable=False, default="0.00")
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    counterparty: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    category: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    imported_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    suggested_account_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    suggested_journal_memo: Mapped[str | None] = mapped_column(String(500), nullable=True)


class VendorBillDB(Base):
    __tablename__ = "integration_vendor_bills"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    connection_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    vendor_name: Mapped[str] = mapped_column(String(255), nullable=False)
    external_id: Mapped[str] = mapped_column(String(120), nullable=False)
    bill_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    lines_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    total_amount: Mapped[str] = mapped_column(String(40), nullable=False, default="0.00")
    imported_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
