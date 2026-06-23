from collections import defaultdict
from datetime import date
from decimal import Decimal

from app.models import (
    AuditFinding,
    AuditReport,
    CRMSummary,
    DashboardMetric,
    DashboardSnapshot,
    FinancialReport,
    FinancialStatementLine,
    RiskLevel,
    TrialBalance,
    TrialBalanceRow,
)
from app.store import InMemoryStore


class AccountingService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def trial_balance(self, period_start: date, period_end: date) -> TrialBalance:
        totals: dict[str, dict[str, Decimal]] = defaultdict(
            lambda: {"debit": Decimal("0.00"), "credit": Decimal("0.00")}
        )

        for entry in self.store.list_journal_entries(period_start, period_end):
            for line in entry.lines:
                totals[line.account_code]["debit"] += line.debit
                totals[line.account_code]["credit"] += line.credit

        rows: list[TrialBalanceRow] = []
        for account_code in sorted(totals):
            account = self.store.accounts[account_code]
            debit_total = totals[account_code]["debit"]
            credit_total = totals[account_code]["credit"]
            rows.append(
                TrialBalanceRow(
                    account_code=account.code,
                    account_name=account.name,
                    account_type=account.account_type,
                    debit_total=debit_total,
                    credit_total=credit_total,
                    net_balance=debit_total - credit_total,
                )
            )

        total_debits = sum(row.debit_total for row in rows)
        total_credits = sum(row.credit_total for row in rows)
        return TrialBalance(
            period_start=period_start,
            period_end=period_end,
            rows=rows,
            total_debits=total_debits,
            total_credits=total_credits,
            is_balanced=total_debits == total_credits,
        )


class ReportingService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store
        self.accounting = AccountingService(store)

    def audit_report(self, period_start: date, period_end: date) -> AuditReport:
        entries = self.store.list_journal_entries(period_start, period_end)
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
                finding="Prototype records are created by system users without approval workflow.",
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
            controls_summary="Prototype controls validate balanced entries and known account codes. Production controls should add approvals, audit logs, and evidence attachments.",
            risk_score=42,
        )

    def financial_report(self, period_start: date, period_end: date) -> FinancialReport:
        trial_balance = self.accounting.trial_balance(period_start, period_end)

        revenue = sum(
            row.credit_total - row.debit_total
            for row in trial_balance.rows
            if row.account_type == "revenue"
        )
        expenses = sum(
            row.debit_total - row.credit_total
            for row in trial_balance.rows
            if row.account_type == "expense"
        )
        assets = sum(
            row.debit_total - row.credit_total
            for row in trial_balance.rows
            if row.account_type == "asset"
        )
        liabilities = sum(
            row.credit_total - row.debit_total
            for row in trial_balance.rows
            if row.account_type == "liability"
        )
        equity = sum(
            row.credit_total - row.debit_total
            for row in trial_balance.rows
            if row.account_type == "equity"
        )
        net_income = revenue - expenses

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
                FinancialStatementLine(label="Ending cash position", amount=self._cash_balance()),
            ],
            kpis={
                "gross_margin": "Prototype KPI pending revenue cost allocation",
                "burn_multiple": "Prototype KPI pending monthly recurring revenue history",
                "pipeline_coverage": f"{len(self.store.deals)} active CRM deal(s)",
            },
        )

    def _cash_balance(self) -> Decimal:
        cash = Decimal("0.00")
        for entry in self.store.journal_entries:
            for line in entry.lines:
                if line.account_code == "1000":
                    cash += line.debit - line.credit
        return cash


class DashboardService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store
        self.reporting = ReportingService(store)

    def executive_snapshot(self) -> DashboardSnapshot:
        cash_position = self.reporting._cash_balance()
        active_deals = [
            deal
            for deal in self.store.deals.values()
            if deal.stage not in {"closed_won", "closed_lost"}
        ]
        weighted_pipeline = sum(
            deal.expected_value * Decimal(deal.probability) / Decimal("100")
            for deal in active_deals
        )
        return DashboardSnapshot(
            metrics=[
                DashboardMetric(
                    label="Cash position",
                    value=f"${cash_position:,.2f}",
                    change="Seeded from general ledger",
                    risk_level=RiskLevel.LOW,
                ),
                DashboardMetric(
                    label="Weighted CRM pipeline",
                    value=f"${weighted_pipeline:,.2f}",
                    change=f"{len(active_deals)} active deal(s)",
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
            active_crm_deals=len(active_deals),
            monthly_recurring_revenue=Decimal("1500.00"),
            cash_position=cash_position,
            notes=[
                "Connect backend to PostgreSQL before production use.",
                "Add approval workflow for journal entries.",
                "Connect CRM deals to Stripe subscriptions and invoices.",
            ],
        )


class CRMService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def summary(self) -> CRMSummary:
        active_deals = [
            deal
            for deal in self.store.deals.values()
            if deal.stage not in {"closed_won", "closed_lost"}
        ]
        weighted_pipeline = sum(
            deal.expected_value * Decimal(deal.probability) / Decimal("100")
            for deal in active_deals
        )
        next_actions = [
            deal.next_step
            for deal in active_deals
            if deal.next_step
        ]
        return CRMSummary(
            total_contacts=len(self.store.contacts),
            active_deals=len(active_deals),
            weighted_pipeline=weighted_pipeline,
            next_actions=next_actions,
        )
