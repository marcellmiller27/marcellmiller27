# JHI-SIG: 69M2705M | External Integrations | JHI Research & Analytics Firm, Inc. (proprietary)
"""Durable, Postgres/SQLAlchemy-backed integrations service.

Migrated from the in-memory store so integration connections, sync jobs, banking
transactions, and vendor bills persist across restarts. The API contract
(pydantic models, status codes, errors) is unchanged. The connector registry and
Office export package are derived/static and need no persistence.
"""

from __future__ import annotations

import json
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_models import (
    BankingTransactionDB,
    CRMDealDB,
    IntegrationConnectionDB,
    SyncJobDB,
    VendorBillDB,
    utc_now,
)
from app.models import (
    BankingTransaction,
    BankingTransactionCreate,
    DataDirection,
    IntegrationCategory,
    IntegrationConnection,
    IntegrationConnectionCreate,
    IntegrationConnector,
    IntegrationStatus,
    JournalEntryCreate,
    OfficeDocumentType,
    OfficeExportPackage,
    OfficeExportRequest,
    SyncJob,
    SyncJobCreate,
    SyncStatus,
    VendorBill,
    VendorBillCreate,
    VendorBillLine,
)
from app.reporting_services import ReportingService

_CONNECTORS: list[IntegrationConnector] = [
    IntegrationConnector(
        key="plaid", name="Plaid Banking", category=IntegrationCategory.BANKING,
        direction=DataDirection.IMPORT,
        supported_objects=["bank_accounts", "bank_transactions", "balances"],
        auth_method="oauth",
        production_notes="Use Plaid Link and token exchange. Store access tokens in a secret manager.",
    ),
    IntegrationConnector(
        key="mx", name="MX Banking", category=IntegrationCategory.BANKING,
        direction=DataDirection.IMPORT,
        supported_objects=["bank_accounts", "bank_transactions", "balances"],
        auth_method="oauth",
        production_notes="Alternative banking aggregation provider for account and transaction sync.",
    ),
    IntegrationConnector(
        key="quickbooks", name="QuickBooks Online", category=IntegrationCategory.ACCOUNTING,
        direction=DataDirection.BIDIRECTIONAL,
        supported_objects=["vendors", "bills", "invoices", "journal_entries"],
        auth_method="oauth",
        production_notes="Map chart of accounts and sync approved journal entries to QuickBooks.",
    ),
    IntegrationConnector(
        key="netsuite", name="Oracle NetSuite", category=IntegrationCategory.VENDOR,
        direction=DataDirection.BIDIRECTIONAL,
        supported_objects=["vendors", "bills", "purchase_orders", "journal_entries"],
        auth_method="token_based_auth",
        production_notes="Enterprise ERP integration for vendor, bill, and accounting workflows.",
    ),
    IntegrationConnector(
        key="bill-com", name="Bill.com", category=IntegrationCategory.VENDOR,
        direction=DataDirection.BIDIRECTIONAL,
        supported_objects=["vendors", "bills", "payments", "approvals"],
        auth_method="api_key_or_oauth",
        production_notes="Use for vendor bill intake, approval routing, and payment status.",
    ),
    IntegrationConnector(
        key="microsoft-365", name="Microsoft 365 Excel and Word",
        category=IntegrationCategory.OFFICE, direction=DataDirection.EXPORT,
        supported_objects=["excel_workbooks", "word_documents", "csv_exports", "report_templates"],
        auth_method="microsoft_graph_oauth",
        production_notes="Use Microsoft Graph for Excel workbook and Word document storage/export.",
    ),
    IntegrationConnector(
        key="salesforce", name="Salesforce CRM", category=IntegrationCategory.CRM,
        direction=DataDirection.BIDIRECTIONAL,
        supported_objects=["contacts", "accounts", "opportunities", "activities"],
        auth_method="oauth",
        production_notes="Sync enterprise sales pipeline with internal CRM records.",
    ),
]


class IntegrationService:
    # -- connectors (static) --------------------------------------------- #
    def connectors(self) -> list[IntegrationConnector]:
        return list(_CONNECTORS)

    def get_connector(self, connector_key: str) -> IntegrationConnector:
        for connector in _CONNECTORS:
            if connector.key == connector_key:
                return connector
        raise KeyError(f"Unknown connector key: {connector_key}")

    # -- connections ------------------------------------------------------ #
    def list_connections(self, db: Session) -> list[IntegrationConnection]:
        rows = db.scalars(
            select(IntegrationConnectionDB).order_by(IntegrationConnectionDB.created_at)
        ).all()
        return [self._connection(r) for r in rows]

    def create_connection(
        self, db: Session, payload: IntegrationConnectionCreate
    ) -> IntegrationConnection:
        self.get_connector(payload.connector_key)  # validates connector exists
        row = IntegrationConnectionDB(
            connector_key=payload.connector_key,
            display_name=payload.display_name,
            credential_reference=payload.credential_reference,
            enabled=payload.enabled,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return self._connection(row)

    # -- sync jobs -------------------------------------------------------- #
    def list_sync_jobs(self, db: Session) -> list[SyncJob]:
        rows = db.scalars(select(SyncJobDB).order_by(SyncJobDB.created_at)).all()
        return [self._sync_job(r) for r in rows]

    def create_sync_job(self, db: Session, payload: SyncJobCreate) -> SyncJob:
        connection = db.get(IntegrationConnectionDB, str(payload.connection_id))
        if connection is None:
            raise KeyError(f"Unknown integration connection id: {payload.connection_id}")
        connector = self.get_connector(connection.connector_key)
        if payload.object_type not in connector.supported_objects:
            raise ValueError(f"{connector.name} does not support object type: {payload.object_type}")
        row = SyncJobDB(
            connection_id=str(payload.connection_id),
            object_type=payload.object_type,
            direction=payload.direction.value,
            requested_by=payload.requested_by,
            status=SyncStatus.COMPLETED.value,
            records_processed=self._count_records_for_object(db, payload.object_type),
            message=f"{payload.object_type} {payload.direction.value} completed for {connector.name}.",
            completed_at=utc_now(),
        )
        connection.last_sync_at = utc_now()
        db.add(row)
        db.commit()
        db.refresh(row)
        return self._sync_job(row)

    # -- banking ---------------------------------------------------------- #
    def list_banking_transactions(self, db: Session) -> list[BankingTransaction]:
        rows = db.scalars(
            select(BankingTransactionDB).order_by(BankingTransactionDB.imported_at)
        ).all()
        return [self._banking(r) for r in rows]

    def import_banking_transaction(
        self, db: Session, payload: BankingTransactionCreate
    ) -> BankingTransaction:
        if payload.connection_id is not None and (
            db.get(IntegrationConnectionDB, str(payload.connection_id)) is None
        ):
            raise KeyError(f"Unknown integration connection id: {payload.connection_id}")
        row = BankingTransactionDB(
            connection_id=str(payload.connection_id) if payload.connection_id else None,
            transaction_date=payload.transaction_date,
            external_id=payload.external_id,
            account_name=payload.account_name,
            description=payload.description,
            amount=str(payload.amount),
            currency=payload.currency,
            counterparty=payload.counterparty,
            category=payload.category,
            suggested_account_code=self._suggest_account_code(payload.description, payload.amount),
            suggested_journal_memo=(
                f"Imported bank transaction {payload.external_id}: {payload.description}"
            ),
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return self._banking(row)

    # -- vendor bills ----------------------------------------------------- #
    def list_vendor_bills(self, db: Session) -> list[VendorBill]:
        rows = db.scalars(select(VendorBillDB).order_by(VendorBillDB.imported_at)).all()
        return [self._vendor_bill(r) for r in rows]

    def import_vendor_bill(self, db: Session, payload: VendorBillCreate) -> VendorBill:
        if payload.connection_id is not None and (
            db.get(IntegrationConnectionDB, str(payload.connection_id)) is None
        ):
            raise KeyError(f"Unknown integration connection id: {payload.connection_id}")
        total_amount = sum((line.amount for line in payload.lines), Decimal("0.00"))
        lines_json = json.dumps(
            [
                {"description": line.description, "account_code": line.account_code,
                 "amount": str(line.amount)}
                for line in payload.lines
            ]
        )
        row = VendorBillDB(
            connection_id=str(payload.connection_id) if payload.connection_id else None,
            vendor_name=payload.vendor_name,
            external_id=payload.external_id,
            bill_date=payload.bill_date,
            due_date=payload.due_date,
            currency=payload.currency,
            lines_json=lines_json,
            total_amount=str(total_amount),
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return self._vendor_bill(row)

    # -- office export (derived; no persistence) -------------------------- #
    def office_export_package(self, db: Session, payload: OfficeExportRequest) -> OfficeExportPackage:
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
            rows_preview=self._rows_preview(db, payload),
        )

    # -- helpers ---------------------------------------------------------- #
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

    def _count_records_for_object(self, db: Session, object_type: str) -> int:
        if object_type in ("bank_transactions", "balances", "bank_accounts"):
            return len(db.scalars(select(BankingTransactionDB.id)).all())
        if object_type == "bills":
            return len(db.scalars(select(VendorBillDB.id)).all())
        if object_type == "vendors":
            return len({b.vendor_name for b in db.scalars(select(VendorBillDB)).all()})
        if object_type in ("opportunities", "contacts", "activities"):
            return len(db.scalars(select(CRMDealDB.id)).all())
        return 0

    def _sections_for_document(self, document_type: OfficeDocumentType) -> list[str]:
        if document_type == OfficeDocumentType.EXCEL_WORKBOOK:
            return ["Summary", "Income Statement", "Balance Sheet", "Audit Findings", "CRM Pipeline"]
        if document_type == OfficeDocumentType.WORD_DOCUMENT:
            return ["Cover Page", "Executive Summary", "Financial Review", "Audit Notes"]
        if document_type == OfficeDocumentType.CSV:
            return ["Rows"]
        return ["Report"]

    def _rows_preview(self, db: Session, payload: OfficeExportRequest) -> list[dict[str, str]]:
        if payload.source_report == "crm_pipeline":
            deals = db.scalars(select(CRMDealDB)).all()
            return [
                {"deal": d.name, "stage": d.stage, "expected_value": str(d.expected_value),
                 "probability": str(d.probability)}
                for d in deals
            ]
        if payload.source_report == "financial_report" and payload.period_start and payload.period_end:
            report = ReportingService().financial_report(db, payload.period_start, payload.period_end)
            return [
                {"line": line.label, "amount": str(line.amount)}
                for line in report.income_statement
            ]
        return [
            {"source_report": payload.source_report, "template": payload.template_name,
             "status": "ready_for_provider_export"}
        ]

    # -- converters ------------------------------------------------------- #
    @staticmethod
    def _connection(row: IntegrationConnectionDB) -> IntegrationConnection:
        return IntegrationConnection(
            id=row.id, connector_key=row.connector_key, display_name=row.display_name,
            credential_reference=row.credential_reference, enabled=row.enabled,
            status=IntegrationStatus(row.status), created_at=row.created_at,
            last_sync_at=row.last_sync_at,
        )

    @staticmethod
    def _sync_job(row: SyncJobDB) -> SyncJob:
        return SyncJob(
            id=row.id, connection_id=row.connection_id, object_type=row.object_type,
            direction=DataDirection(row.direction), requested_by=row.requested_by,
            status=SyncStatus(row.status), records_processed=row.records_processed,
            message=row.message, created_at=row.created_at, completed_at=row.completed_at,
        )

    @staticmethod
    def _banking(row: BankingTransactionDB) -> BankingTransaction:
        return BankingTransaction(
            id=row.id, connection_id=row.connection_id, transaction_date=row.transaction_date,
            external_id=row.external_id, account_name=row.account_name, description=row.description,
            amount=Decimal(row.amount), currency=row.currency, counterparty=row.counterparty,
            category=row.category, imported_at=row.imported_at,
            suggested_account_code=row.suggested_account_code,
            suggested_journal_memo=row.suggested_journal_memo,
        )

    @staticmethod
    def _vendor_bill(row: VendorBillDB) -> VendorBill:
        lines = [
            VendorBillLine(
                description=line["description"], account_code=line["account_code"],
                amount=Decimal(line["amount"]),
            )
            for line in json.loads(row.lines_json)
        ]
        total_amount = Decimal(row.total_amount)
        suggested_entry = JournalEntryCreate(
            entry_date=row.bill_date,
            memo=f"Imported vendor bill {row.external_id} from {row.vendor_name}",
            source_module="vendor_integration",
            created_by="integration",
            lines=[
                {"account_code": line.account_code, "description": line.description,
                 "debit": line.amount, "credit": Decimal("0.00")}
                for line in lines
            ]
            + [
                {"account_code": "2000",
                 "description": f"Accounts payable to {row.vendor_name}",
                 "debit": Decimal("0.00"), "credit": total_amount}
            ],
        )
        return VendorBill(
            id=row.id, connection_id=row.connection_id, vendor_name=row.vendor_name,
            external_id=row.external_id, bill_date=row.bill_date, due_date=row.due_date,
            currency=row.currency, lines=lines, imported_at=row.imported_at,
            total_amount=total_amount, suggested_journal_entry=suggested_entry,
        )
