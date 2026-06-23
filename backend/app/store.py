from datetime import date
from decimal import Decimal
from uuid import UUID

from app.models import (
    Account,
    AccountType,
    CRMActivity,
    CRMActivityCreate,
    CRMContact,
    CRMContactCreate,
    CRMDeal,
    CRMDealCreate,
    DealStage,
    JournalEntry,
    JournalEntryCreate,
    JournalLine,
)


class InMemoryStore:
    """Simple repository for the prototype backend until PostgreSQL is connected."""

    def __init__(self) -> None:
        self.accounts: dict[str, Account] = self._seed_chart_of_accounts()
        self.journal_entries: list[JournalEntry] = []
        self.contacts: dict[UUID, CRMContact] = {}
        self.deals: dict[UUID, CRMDeal] = {}
        self.activities: dict[UUID, CRMActivity] = {}
        self._seed_records()

    def _seed_chart_of_accounts(self) -> dict[str, Account]:
        accounts = [
            Account(code="1000", name="Cash and Cash Equivalents", account_type=AccountType.ASSET),
            Account(code="1100", name="Accounts Receivable", account_type=AccountType.ASSET),
            Account(code="1200", name="Prepaid Software", account_type=AccountType.ASSET),
            Account(code="1500", name="Platform Development Asset", account_type=AccountType.ASSET),
            Account(code="2000", name="Accounts Payable", account_type=AccountType.LIABILITY),
            Account(code="2100", name="Deferred Revenue", account_type=AccountType.LIABILITY),
            Account(code="3000", name="Member Equity", account_type=AccountType.EQUITY),
            Account(code="4000", name="Subscription Revenue", account_type=AccountType.REVENUE),
            Account(code="4100", name="Advisory Revenue", account_type=AccountType.REVENUE),
            Account(code="5000", name="Cloud Infrastructure Expense", account_type=AccountType.EXPENSE),
            Account(code="5100", name="AI Data Processing Expense", account_type=AccountType.EXPENSE),
            Account(code="5200", name="Sales and Marketing Expense", account_type=AccountType.EXPENSE),
        ]
        return {account.code: account for account in accounts}

    def _seed_records(self) -> None:
        seed_entries = [
            JournalEntryCreate(
                entry_date=date(2026, 6, 1),
                memo="Seed member capital contribution",
                source_module="accounting",
                created_by="system",
                lines=[
                    {"account_code": "1000", "debit": Decimal("250000.00")},
                    {"account_code": "3000", "credit": Decimal("250000.00")},
                ],
            ),
            JournalEntryCreate(
                entry_date=date(2026, 6, 5),
                memo="Enterprise subscription invoice",
                source_module="billing",
                created_by="system",
                lines=[
                    {"account_code": "1100", "debit": Decimal("1500.00")},
                    {"account_code": "4000", "credit": Decimal("1500.00")},
                ],
            ),
            JournalEntryCreate(
                entry_date=date(2026, 6, 10),
                memo="Cloud and AI platform operating costs",
                source_module="operations",
                created_by="system",
                lines=[
                    {"account_code": "5000", "debit": Decimal("4200.00")},
                    {"account_code": "5100", "debit": Decimal("1800.00")},
                    {"account_code": "1000", "credit": Decimal("6000.00")},
                ],
            ),
        ]
        for entry in seed_entries:
            self.create_journal_entry(entry)

        contact = self.create_contact(
            CRMContactCreate(
                full_name="Avery Johnson",
                organization="Northstar Family Office",
                email="avery@example.com",
                phone="555-0100",
                role="Managing Partner",
                relationship_type="enterprise prospect",
                owner="Marcellus Miller",
            )
        )
        deal = self.create_deal(
            CRMDealCreate(
                contact_id=contact.id,
                name="Family office enterprise platform subscription",
                stage=DealStage.DILIGENCE,
                expected_value=Decimal("24000.00"),
                probability=65,
                next_step="Send branded macro report sample",
            )
        )
        self.create_activity(
            CRMActivityCreate(
                contact_id=contact.id,
                deal_id=deal.id,
                activity_type="follow_up",
                summary="Provide demo access and compliance overview.",
                due_date=date(2026, 6, 30),
            )
        )

    def create_journal_entry(self, payload: JournalEntryCreate) -> JournalEntry:
        lines: list[JournalLine] = []
        for line in payload.lines:
            account = self.accounts.get(line.account_code)
            if account is None:
                raise KeyError(f"Unknown account code: {line.account_code}")
            lines.append(
                JournalLine(
                    **line.model_dump(),
                    account_name=account.name,
                    account_type=account.account_type,
                )
            )
        entry = JournalEntry(**payload.model_dump(exclude={"lines"}), lines=lines)
        self.journal_entries.append(entry)
        return entry

    def list_journal_entries(
        self,
        period_start: date | None = None,
        period_end: date | None = None,
    ) -> list[JournalEntry]:
        entries = self.journal_entries
        if period_start is not None:
            entries = [entry for entry in entries if entry.entry_date >= period_start]
        if period_end is not None:
            entries = [entry for entry in entries if entry.entry_date <= period_end]
        return entries

    def create_contact(self, payload: CRMContactCreate) -> CRMContact:
        contact = CRMContact(**payload.model_dump())
        self.contacts[contact.id] = contact
        return contact

    def create_deal(self, payload: CRMDealCreate) -> CRMDeal:
        if payload.contact_id not in self.contacts:
            raise KeyError(f"Unknown contact id: {payload.contact_id}")
        deal = CRMDeal(**payload.model_dump())
        self.deals[deal.id] = deal
        return deal

    def create_activity(self, payload: CRMActivityCreate) -> CRMActivity:
        if payload.contact_id not in self.contacts:
            raise KeyError(f"Unknown contact id: {payload.contact_id}")
        if payload.deal_id is not None and payload.deal_id not in self.deals:
            raise KeyError(f"Unknown deal id: {payload.deal_id}")
        activity = CRMActivity(**payload.model_dump())
        self.activities[activity.id] = activity
        return activity


store = InMemoryStore()
