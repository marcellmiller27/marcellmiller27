from datetime import date, datetime, timezone
from decimal import Decimal
from enum import StrEnum
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

Money = Annotated[Decimal, Field(max_digits=18, decimal_places=2)]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AccountType(StrEnum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"


class JournalStatus(StrEnum):
    DRAFT = "draft"
    POSTED = "posted"


class DealStage(StrEnum):
    LEAD = "lead"
    QUALIFIED = "qualified"
    DILIGENCE = "diligence"
    PROPOSAL = "proposal"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Account(BaseModel):
    code: str
    name: str
    account_type: AccountType


class JournalLineCreate(BaseModel):
    account_code: str
    description: str = ""
    debit: Money = Decimal("0.00")
    credit: Money = Decimal("0.00")
    entity: str = "John Henry Investments, LLC"
    department: str = "Platform"

    @model_validator(mode="after")
    def validate_debit_or_credit(self) -> "JournalLineCreate":
        if self.debit < 0 or self.credit < 0:
            raise ValueError("Debit and credit amounts must be zero or greater.")
        if self.debit == 0 and self.credit == 0:
            raise ValueError("A journal line must include a debit or credit amount.")
        if self.debit > 0 and self.credit > 0:
            raise ValueError("A journal line cannot include both debit and credit amounts.")
        return self


class JournalLine(JournalLineCreate):
    account_name: str
    account_type: AccountType


class JournalEntryCreate(BaseModel):
    entry_date: date
    memo: str
    source_module: str = "manual"
    created_by: str = "system"
    lines: list[JournalLineCreate] = Field(min_length=2)

    @model_validator(mode="after")
    def validate_balanced_entry(self) -> "JournalEntryCreate":
        total_debits = sum(line.debit for line in self.lines)
        total_credits = sum(line.credit for line in self.lines)
        if total_debits != total_credits:
            raise ValueError("Journal entry must balance: total debits must equal total credits.")
        return self


class JournalEntry(JournalEntryCreate):
    id: UUID = Field(default_factory=uuid4)
    status: JournalStatus = JournalStatus.POSTED
    lines: list[JournalLine]
    created_at: datetime = Field(default_factory=utc_now)
    posted_at: datetime | None = Field(default_factory=utc_now)


class TrialBalanceRow(BaseModel):
    account_code: str
    account_name: str
    account_type: AccountType
    debit_total: Money
    credit_total: Money
    net_balance: Money


class TrialBalance(BaseModel):
    period_start: date
    period_end: date
    rows: list[TrialBalanceRow]
    total_debits: Money
    total_credits: Money
    is_balanced: bool


class AuditFinding(BaseModel):
    control_area: str
    risk_level: RiskLevel
    finding: str
    recommendation: str


class AuditReport(BaseModel):
    report_id: UUID = Field(default_factory=uuid4)
    generated_at: datetime = Field(default_factory=utc_now)
    period_start: date
    period_end: date
    scope: list[str]
    findings: list[AuditFinding]
    controls_summary: str
    risk_score: int = Field(ge=0, le=100)


class FinancialStatementLine(BaseModel):
    label: str
    amount: Money


class FinancialReport(BaseModel):
    report_id: UUID = Field(default_factory=uuid4)
    generated_at: datetime = Field(default_factory=utc_now)
    period_start: date
    period_end: date
    income_statement: list[FinancialStatementLine]
    balance_sheet: list[FinancialStatementLine]
    cash_flow_summary: list[FinancialStatementLine]
    kpis: dict[str, str]


class DashboardMetric(BaseModel):
    label: str
    value: str
    change: str
    risk_level: RiskLevel


class DashboardSnapshot(BaseModel):
    generated_at: datetime = Field(default_factory=utc_now)
    metrics: list[DashboardMetric]
    open_audit_findings: int
    active_crm_deals: int
    monthly_recurring_revenue: Money
    cash_position: Money
    notes: list[str]


class CRMContactCreate(BaseModel):
    full_name: str
    organization: str
    email: str
    phone: str = ""
    role: str = ""
    relationship_type: str = "prospect"
    owner: str = "platform"


class CRMContact(CRMContactCreate):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=utc_now)


class CRMDealCreate(BaseModel):
    contact_id: UUID
    name: str
    stage: DealStage = DealStage.LEAD
    expected_value: Money = Decimal("0.00")
    probability: int = Field(default=10, ge=0, le=100)
    next_step: str = ""


class CRMDeal(CRMDealCreate):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class CRMActivityCreate(BaseModel):
    contact_id: UUID
    deal_id: UUID | None = None
    activity_type: str
    summary: str
    due_date: date | None = None


class CRMActivity(CRMActivityCreate):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=utc_now)


class CRMSummary(BaseModel):
    total_contacts: int
    active_deals: int
    weighted_pipeline: Money
    next_actions: list[str]
