# JHI-SIG: 69M2705M | External Integrations | John Henry Investments (proprietary)
from datetime import date
from decimal import Decimal

from app.models import (
    BankingTransactionCreate,
    DataDirection,
    IntegrationConnectionCreate,
    OfficeDocumentType,
    OfficeExportRequest,
    SyncJobCreate,
    VendorBillCreate,
)
from app.services import IntegrationService
from app.store import InMemoryStore


def test_connector_registry_includes_banking_vendor_and_office() -> None:
    service = IntegrationService(InMemoryStore())
    connectors = {connector.key: connector for connector in service.connectors()}

    assert "plaid" in connectors
    assert "bill-com" in connectors
    assert "microsoft-365" in connectors


def test_create_connection_and_sync_job() -> None:
    store = InMemoryStore()
    service = IntegrationService(store)
    connection = service.create_connection(
        IntegrationConnectionCreate(
            connector_key="plaid",
            display_name="Operating bank account",
            credential_reference="secret://plaid/item/jhi-operating",
        )
    )

    job = service.create_sync_job(
        SyncJobCreate(
            connection_id=connection.id,
            object_type="bank_transactions",
            direction=DataDirection.IMPORT,
            requested_by="test",
        )
    )

    assert job.status == "completed"
    assert "Plaid Banking" in job.message


def test_import_banking_transaction_adds_accounting_suggestion() -> None:
    store = InMemoryStore()
    service = IntegrationService(store)

    transaction = service.import_banking_transaction(
        BankingTransactionCreate(
            transaction_date=date(2026, 6, 23),
            external_id="txn_001",
            account_name="Operating Checking",
            description="OpenAI API usage",
            amount=Decimal("-120.00"),
            counterparty="OpenAI",
            category="AI",
        )
    )

    assert transaction.suggested_account_code == "5100"
    assert transaction.suggested_journal_memo


def test_import_vendor_bill_creates_balanced_journal_suggestion() -> None:
    store = InMemoryStore()
    service = IntegrationService(store)

    bill = service.import_vendor_bill(
        VendorBillCreate(
            vendor_name="Microsoft",
            external_id="bill_001",
            bill_date=date(2026, 6, 23),
            lines=[
                {
                    "description": "Microsoft 365 subscription",
                    "account_code": "5000",
                    "amount": Decimal("320.00"),
                }
            ],
        )
    )

    total_debits = sum(line.debit for line in bill.suggested_journal_entry.lines)
    total_credits = sum(line.credit for line in bill.suggested_journal_entry.lines)
    assert bill.total_amount == Decimal("320.00")
    assert total_debits == total_credits


def test_office_export_package_for_excel_financial_report() -> None:
    service = IntegrationService(InMemoryStore())

    package = service.office_export_package(
        OfficeExportRequest(
            document_type=OfficeDocumentType.EXCEL_WORKBOOK,
            template_name="Monthly Financial Report",
            source_report="financial_report",
            period_start=date(2026, 6, 1),
            period_end=date(2026, 6, 30),
            requested_by="Marcellus Miller",
        )
    )

    assert package.file_name == "monthly-financial-report.xlsx"
    assert "Income Statement" in package.sheets_or_sections
    assert package.rows_preview
