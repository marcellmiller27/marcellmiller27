# JHI-SIG: 69M2705M | Platform spine | John Henry Investments (proprietary)
from datetime import date
from decimal import Decimal

import pytest

from app.models import JournalEntryCreate
from app.services import AccountingService, CRMService, DashboardService, ReportingService
from app.store import InMemoryStore


def test_seeded_trial_balance_is_balanced() -> None:
    store = InMemoryStore()
    trial_balance = AccountingService(store).trial_balance(date(2026, 6, 1), date(2026, 6, 30))

    assert trial_balance.is_balanced is True
    assert trial_balance.total_debits == trial_balance.total_credits


def test_create_balanced_journal_entry_updates_trial_balance() -> None:
    store = InMemoryStore()
    entry = JournalEntryCreate(
        entry_date=date(2026, 6, 15),
        memo="Professional plan subscription payment",
        source_module="billing",
        created_by="test",
        lines=[
            {"account_code": "1000", "debit": Decimal("299.00")},
            {"account_code": "4000", "credit": Decimal("299.00")},
        ],
    )

    created = store.create_journal_entry(entry)
    trial_balance = AccountingService(store).trial_balance(date(2026, 6, 1), date(2026, 6, 30))

    assert created.memo == "Professional plan subscription payment"
    assert trial_balance.is_balanced is True


def test_unbalanced_journal_entry_is_rejected() -> None:
    with pytest.raises(ValueError):
        JournalEntryCreate(
            entry_date=date(2026, 6, 15),
            memo="Invalid entry",
            lines=[
                {"account_code": "1000", "debit": Decimal("100.00")},
                {"account_code": "4000", "credit": Decimal("99.00")},
            ],
        )


def test_reporting_services_return_financial_and_audit_reports() -> None:
    store = InMemoryStore()
    reporting = ReportingService(store)

    financial_report = reporting.financial_report(date(2026, 6, 1), date(2026, 6, 30))
    audit_report = reporting.audit_report(date(2026, 6, 1), date(2026, 6, 30))

    assert financial_report.income_statement
    assert financial_report.balance_sheet
    assert audit_report.findings


def test_dashboard_and_crm_summaries_use_seeded_pipeline() -> None:
    store = InMemoryStore()

    dashboard = DashboardService(store).executive_snapshot()
    crm_summary = CRMService(store).summary()

    assert dashboard.active_crm_deals == 1
    assert crm_summary.total_contacts == 1
    assert crm_summary.weighted_pipeline == Decimal("15600.00")
