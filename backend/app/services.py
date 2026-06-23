from collections import defaultdict
from datetime import date
from decimal import Decimal

from app.models import (
    AuditFinding,
    AuditReport,
    BankingTransaction,
    BankingTransactionCreate,
    CRMSummary,
    DataDirection,
    DashboardMetric,
    DashboardSnapshot,
    FinancialReport,
    FinancialStatementLine,
    IntegrationCategory,
    IntegrationConnection,
    IntegrationConnectionCreate,
    IntegrationConnector,
    JournalEntryCreate,
    RiskLevel,
    OfficeDocumentType,
    OfficeExportPackage,
    OfficeExportRequest,
    SyncJob,
    SyncJobCreate,
    TrialBalance,
    TrialBalanceRow,
    VendorBill,
    VendorBillCreate,
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


class IntegrationService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store
        self.reporting = ReportingService(store)

    def connectors(self) -> list[IntegrationConnector]:
        return [
            IntegrationConnector(
                key="plaid",
                name="Plaid Banking",
                category=IntegrationCategory.BANKING,
                direction=DataDirection.IMPORT,
                supported_objects=["bank_accounts", "bank_transactions", "balances"],
                auth_method="oauth",
                production_notes="Use Plaid Link and token exchange. Store access tokens in a secret manager.",
            ),
            IntegrationConnector(
                key="mx",
                name="MX Banking",
                category=IntegrationCategory.BANKING,
                direction=DataDirection.IMPORT,
                supported_objects=["bank_accounts", "bank_transactions", "balances"],
                auth_method="oauth",
                production_notes="Alternative banking aggregation provider for account and transaction sync.",
            ),
            IntegrationConnector(
                key="quickbooks",
                name="QuickBooks Online",
                category=IntegrationCategory.ACCOUNTING,
                direction=DataDirection.BIDIRECTIONAL,
                supported_objects=["vendors", "bills", "invoices", "journal_entries"],
                auth_method="oauth",
                production_notes="Map chart of accounts and sync approved journal entries to QuickBooks.",
            ),
            IntegrationConnector(
                key="netsuite",
                name="Oracle NetSuite",
                category=IntegrationCategory.VENDOR,
                direction=DataDirection.BIDIRECTIONAL,
                supported_objects=["vendors", "bills", "purchase_orders", "journal_entries"],
                auth_method="token_based_auth",
                production_notes="Enterprise ERP integration for vendor, bill, and accounting workflows.",
            ),
            IntegrationConnector(
                key="bill-com",
                name="Bill.com",
                category=IntegrationCategory.VENDOR,
                direction=DataDirection.BIDIRECTIONAL,
                supported_objects=["vendors", "bills", "payments", "approvals"],
                auth_method="api_key_or_oauth",
                production_notes="Use for vendor bill intake, approval routing, and payment status.",
            ),
            IntegrationConnector(
                key="microsoft-365",
                name="Microsoft 365 Excel and Word",
                category=IntegrationCategory.OFFICE,
                direction=DataDirection.EXPORT,
                supported_objects=["excel_workbooks", "word_documents", "csv_exports", "report_templates"],
                auth_method="microsoft_graph_oauth",
                production_notes="Use Microsoft Graph for Excel workbook and Word document storage/export.",
            ),
            IntegrationConnector(
                key="salesforce",
                name="Salesforce CRM",
                category=IntegrationCategory.CRM,
                direction=DataDirection.BIDIRECTIONAL,
                supported_objects=["contacts", "accounts", "opportunities", "activities"],
                auth_method="oauth",
                production_notes="Sync enterprise sales pipeline with internal CRM records.",
            ),
        ]

    def get_connector(self, connector_key: str) -> IntegrationConnector:
        for connector in self.connectors():
            if connector.key == connector_key:
                return connector
        raise KeyError(f"Unknown connector key: {connector_key}")

    def create_connection(self, payload: IntegrationConnectionCreate) -> IntegrationConnection:
        self.get_connector(payload.connector_key)
        return self.store.create_integration_connection(payload)

    def create_sync_job(self, payload: SyncJobCreate) -> SyncJob:
        connection = self.store.integration_connections.get(payload.connection_id)
        if connection is None:
            raise KeyError(f"Unknown integration connection id: {payload.connection_id}")
        connector = self.get_connector(connection.connector_key)
        if payload.object_type not in connector.supported_objects:
            raise ValueError(f"{connector.name} does not support object type: {payload.object_type}")
        job = self.store.create_sync_job(payload)
        return self.store.complete_sync_job(
            job.id,
            records_processed=self._count_records_for_object(payload.object_type),
            message=f"{payload.object_type} {payload.direction} completed for {connector.name}.",
        )

    def import_banking_transaction(
        self,
        payload: BankingTransactionCreate,
    ) -> BankingTransaction:
        suggested_account_code = self._suggest_account_code(payload.description, payload.amount)
        suggested_journal_memo = (
            f"Imported bank transaction {payload.external_id}: {payload.description}"
        )
        return self.store.create_banking_transaction(
            payload,
            suggested_account_code=suggested_account_code,
            suggested_journal_memo=suggested_journal_memo,
        )

    def import_vendor_bill(self, payload: VendorBillCreate) -> VendorBill:
        total_amount = sum(line.amount for line in payload.lines)
        suggested_entry = {
            "entry_date": payload.bill_date,
            "memo": f"Imported vendor bill {payload.external_id} from {payload.vendor_name}",
            "source_module": "vendor_integration",
            "created_by": "integration",
            "lines": [
                {
                    "account_code": line.account_code,
                    "description": line.description,
                    "debit": line.amount,
                    "credit": Decimal("0.00"),
                }
                for line in payload.lines
            ]
            + [
                {
                    "account_code": "2000",
                    "description": f"Accounts payable to {payload.vendor_name}",
                    "debit": Decimal("0.00"),
                    "credit": total_amount,
                }
            ],
        }
        return self.store.create_vendor_bill(
            payload,
            suggested_journal_entry=JournalEntryCreate(**suggested_entry),
        )

    def office_export_package(self, payload: OfficeExportRequest) -> OfficeExportPackage:
        mime_types = {
            OfficeDocumentType.EXCEL_WORKBOOK: (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
            OfficeDocumentType.WORD_DOCUMENT: (
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ),
            OfficeDocumentType.CSV: "text/csv",
            OfficeDocumentType.PDF: "application/pdf",
        }
        extension = {
            OfficeDocumentType.EXCEL_WORKBOOK: "xlsx",
            OfficeDocumentType.WORD_DOCUMENT: "docx",
            OfficeDocumentType.CSV: "csv",
            OfficeDocumentType.PDF: "pdf",
        }[payload.document_type]
        rows_preview = self._rows_preview(payload)
        return OfficeExportPackage(
            document_type=payload.document_type,
            template_name=payload.template_name,
            source_report=payload.source_report,
            file_name=f"{payload.template_name.lower().replace(' ', '-')}.{extension}",
            mime_type=mime_types[payload.document_type],
            sheets_or_sections=self._sections_for_document(payload.document_type),
            field_map={
                "company": "John Henry Investments, LLC",
                "period_start": "report.period_start",
                "period_end": "report.period_end",
                "generated_at": "export.generated_at",
                "prepared_by": payload.requested_by,
            },
            rows_preview=rows_preview,
        )

    def _suggest_account_code(self, description: str, amount: Decimal) -> str:
        text = description.lower()
        if amount > 0:
            return "4000"
        if "cloud" in text or "aws" in text or "vercel" in text:
            return "5000"
        if "openai" in text or "anthropic" in text or "ai" in text:
            return "5100"
        if "marketing" in text or "advertising" in text:
            return "5200"
        return "5000"

    def _count_records_for_object(self, object_type: str) -> int:
        counts = {
            "bank_transactions": len(self.store.banking_transactions),
            "vendors": len({bill.vendor_name for bill in self.store.vendor_bills.values()}),
            "bills": len(self.store.vendor_bills),
            "journal_entries": len(self.store.journal_entries),
            "contacts": len(self.store.contacts),
            "opportunities": len(self.store.deals),
            "activities": len(self.store.activities),
        }
        return counts.get(object_type, 0)

    def _sections_for_document(self, document_type: OfficeDocumentType) -> list[str]:
        if document_type == OfficeDocumentType.EXCEL_WORKBOOK:
            return ["Summary", "Income Statement", "Balance Sheet", "Audit Findings", "CRM Pipeline"]
        if document_type == OfficeDocumentType.WORD_DOCUMENT:
            return ["Cover Page", "Executive Summary", "Financial Review", "Audit Notes"]
        if document_type == OfficeDocumentType.CSV:
            return ["Rows"]
        return ["Report"]

    def _rows_preview(self, payload: OfficeExportRequest) -> list[dict[str, str]]:
        if payload.source_report == "crm_pipeline":
            return [
                {
                    "deal": deal.name,
                    "stage": deal.stage,
                    "expected_value": str(deal.expected_value),
                    "probability": str(deal.probability),
                }
                for deal in self.store.deals.values()
            ]
        if payload.source_report == "financial_report" and payload.period_start and payload.period_end:
            report = self.reporting.financial_report(payload.period_start, payload.period_end)
            return [
                {"line": line.label, "amount": str(line.amount)}
                for line in report.income_statement
            ]
        return [
            {
                "source_report": payload.source_report,
                "template": payload.template_name,
                "status": "ready_for_provider_export",
            }
        ]
