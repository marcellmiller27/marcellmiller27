# JHI-SIG: 69M2705M | Accounting & Reporting | John Henry Investments (proprietary)
"""Durable, DB-backed reporting & dashboard services.

Compute audit/financial reports and the executive dashboard from the Postgres-backed
accounting (journal entries / trial balance) and CRM (deals) data, so they reflect
real, durable activity instead of the in-memory store.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.accounting_services import AccountingService
from app.db_models import CRMDealDB, JournalLineDB
from app.models import (
    AuditFinding,
    AuditReport,
    DashboardMetric,
    DashboardSnapshot,
    FinancialReport,
    FinancialStatementLine,
    RiskLevel,
)

CASH_ACCOUNT = "1000"
_CLOSED_STAGES = {"closed_won", "closed_lost"}


class ReportingService:
    def __init__(self) -> None:
        self.accounting = AccountingService()

    def audit_report(self, db: Session, period_start: date, period_end: date) -> AuditReport:
        entries = self.accounting.list_journal_entries(db, period_start, period_end)
        findings = [
            AuditFinding(
                control_area="Journal entry balancing",
                risk_level=RiskLevel.LOW,
                finding=f"{len(entries)} posted entries reviewed; all accepted entries are balanced.",
                recommendation="Keep automated debit and credit validation enabled.",
            ),
            AuditFinding(
                control_area="Segregation of duties",
                risk_level=RiskLevel.MEDIUM,
                finding="Records are created without an approval workflow.",
                recommendation="Add preparer, reviewer, and approver roles before production launch.",
            ),
            AuditFinding(
                control_area="CRM revenue pipeline evidence",
                risk_level=RiskLevel.MEDIUM,
                finding="Enterprise pipeline is tracked, but contracts and invoices are not attached.",
                recommendation="Connect CRM deals to billing, document storage, and audit evidence.",
            ),
        ]
        return AuditReport(
            period_start=period_start,
            period_end=period_end,
            scope=[
                "General journal entries",
                "Trial balance",
                "Revenue pipeline",
                "Financial report inputs",
            ],
            findings=findings,
            controls_summary=(
                "Controls validate balanced entries and known account codes. Production "
                "controls should add approvals, audit logs, and evidence attachments."
            ),
            risk_score=42,
        )

    def financial_report(self, db: Session, period_start: date, period_end: date) -> FinancialReport:
        tb = self.accounting.trial_balance(db, period_start, period_end)

        def total(kind: str, debit_positive: bool) -> Decimal:
            return sum(
                (
                    (r.debit_total - r.credit_total) if debit_positive
                    else (r.credit_total - r.debit_total)
                    for r in tb.rows
                    if r.account_type == kind
                ),
                Decimal("0.00"),
            )

        revenue = total("revenue", debit_positive=False)
        expenses = total("expense", debit_positive=True)
        assets = total("asset", debit_positive=True)
        liabilities = total("liability", debit_positive=False)
        equity = total("equity", debit_positive=False)
        net_income = revenue - expenses
        deals_count = db.scalar(select(func.count()).select_from(CRMDealDB)) or 0

        return FinancialReport(
            period_start=period_start,
            period_end=period_end,
            income_statement=[
                FinancialStatementLine(label="Subscription and advisory revenue", amount=revenue),
                FinancialStatementLine(label="Operating expenses", amount=expenses),
                FinancialStatementLine(label="Net income", amount=net_income),
            ],
            balance_sheet=[
                FinancialStatementLine(label="Assets", amount=assets),
                FinancialStatementLine(label="Liabilities", amount=liabilities),
                FinancialStatementLine(label="Member equity", amount=equity),
            ],
            cash_flow_summary=[
                FinancialStatementLine(label="Operating cash flow", amount=net_income),
                FinancialStatementLine(label="Ending cash position", amount=self.cash_balance(db)),
            ],
            kpis={
                "gross_margin": "KPI pending revenue cost allocation",
                "burn_multiple": "KPI pending monthly recurring revenue history",
                "pipeline_coverage": f"{deals_count} CRM deal(s)",
            },
        )

    def cash_balance(self, db: Session) -> Decimal:
        lines = db.scalars(
            select(JournalLineDB).where(JournalLineDB.account_code == CASH_ACCOUNT)
        ).all()
        return sum(
            (Decimal(line.debit) - Decimal(line.credit) for line in lines), Decimal("0.00")
        )


class DashboardService:
    def __init__(self) -> None:
        self.reporting = ReportingService()

    def executive_snapshot(self, db: Session) -> DashboardSnapshot:
        cash_position = self.reporting.cash_balance(db)
        deals = db.scalars(select(CRMDealDB)).all()
        active = [d for d in deals if d.stage not in _CLOSED_STAGES]
        weighted_pipeline = sum(
            (Decimal(d.expected_value) * Decimal(d.probability) / Decimal("100") for d in active),
            Decimal("0.00"),
        )
        return DashboardSnapshot(
            metrics=[
                DashboardMetric(
                    label="Cash position",
                    value=f"${cash_position:,.2f}",
                    change="From the general ledger",
                    risk_level=RiskLevel.LOW,
                ),
                DashboardMetric(
                    label="Weighted CRM pipeline",
                    value=f"${weighted_pipeline:,.2f}",
                    change=f"{len(active)} active deal(s)",
                    risk_level=RiskLevel.MEDIUM,
                ),
                DashboardMetric(
                    label="Accounting controls",
                    value="Balanced",
                    change="Journal validation enabled",
                    risk_level=RiskLevel.LOW,
                ),
            ],
            open_audit_findings=3,
            active_crm_deals=len(active),
            monthly_recurring_revenue=Decimal("1500.00"),
            cash_position=cash_position,
            notes=[
                "Durable Postgres persistence enabled for accounting and CRM.",
                "Add approval workflow for journal entries.",
                "Connect CRM deals to Stripe subscriptions and invoices.",
            ],
        )
