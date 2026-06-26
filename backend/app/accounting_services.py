"""Durable, SQLAlchemy/Postgres-backed accounting service.

Migrated from the in-memory store: chart of accounts, balanced double-entry journal
entries, and trial balance now persist across restarts. API contract unchanged
(balanced-entry validation lives in the pydantic model; unknown account codes raise
KeyError -> HTTP 400).
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_models import AccountDB, JournalEntryDB, JournalLineDB
from app.models import (
    Account,
    AccountType,
    JournalEntry,
    JournalEntryCreate,
    JournalLine,
    JournalStatus,
    TrialBalance,
    TrialBalanceRow,
)

_SEED_ACCOUNTS = [
    ("1000", "Cash and Cash Equivalents", "asset"),
    ("1100", "Accounts Receivable", "asset"),
    ("1200", "Prepaid Software", "asset"),
    ("1500", "Platform Development Asset", "asset"),
    ("2000", "Accounts Payable", "liability"),
    ("2100", "Deferred Revenue", "liability"),
    ("3000", "Member Equity", "equity"),
    ("4000", "Subscription Revenue", "revenue"),
    ("4100", "Advisory Revenue", "revenue"),
    ("5000", "Cloud Infrastructure Expense", "expense"),
    ("5100", "AI Data Processing Expense", "expense"),
    ("5200", "Sales and Marketing Expense", "expense"),
]


class AccountingService:
    def list_accounts(self, db: Session) -> list[Account]:
        rows = db.scalars(select(AccountDB).order_by(AccountDB.code)).all()
        return [Account(code=r.code, name=r.name, account_type=AccountType(r.account_type)) for r in rows]

    def list_journal_entries(
        self, db: Session, period_start: date | None = None, period_end: date | None = None
    ) -> list[JournalEntry]:
        stmt = select(JournalEntryDB).order_by(JournalEntryDB.entry_date, JournalEntryDB.created_at)
        if period_start is not None:
            stmt = stmt.where(JournalEntryDB.entry_date >= period_start)
        if period_end is not None:
            stmt = stmt.where(JournalEntryDB.entry_date <= period_end)
        return [self._entry(db, e) for e in db.scalars(stmt).all()]

    def create_journal_entry(self, db: Session, payload: JournalEntryCreate) -> JournalEntry:
        accounts = {a.code: a for a in db.scalars(select(AccountDB)).all()}
        for line in payload.lines:
            if line.account_code not in accounts:
                raise KeyError(f"Unknown account code: {line.account_code}")
        entry = JournalEntryDB(
            entry_date=payload.entry_date,
            memo=payload.memo,
            source_module=payload.source_module,
            created_by=payload.created_by,
            status=JournalStatus.POSTED.value,
        )
        db.add(entry)
        db.flush()
        for index, line in enumerate(payload.lines):
            account = accounts[line.account_code]
            db.add(
                JournalLineDB(
                    entry_id=entry.id,
                    line_no=index,
                    account_code=line.account_code,
                    description=line.description,
                    debit=str(line.debit),
                    credit=str(line.credit),
                    entity=line.entity,
                    department=line.department,
                    account_name=account.name,
                    account_type=account.account_type,
                )
            )
        db.commit()
        db.refresh(entry)
        return self._entry(db, entry)

    def trial_balance(self, db: Session, period_start: date, period_end: date) -> TrialBalance:
        accounts = {a.code: a for a in db.scalars(select(AccountDB)).all()}
        totals: dict[str, dict[str, Decimal]] = defaultdict(
            lambda: {"debit": Decimal("0.00"), "credit": Decimal("0.00")}
        )
        entry_ids = db.scalars(
            select(JournalEntryDB.id).where(
                JournalEntryDB.entry_date >= period_start,
                JournalEntryDB.entry_date <= period_end,
            )
        ).all()
        if entry_ids:
            lines = db.scalars(
                select(JournalLineDB).where(JournalLineDB.entry_id.in_(entry_ids))
            ).all()
            for line in lines:
                totals[line.account_code]["debit"] += Decimal(line.debit)
                totals[line.account_code]["credit"] += Decimal(line.credit)

        rows: list[TrialBalanceRow] = []
        for code in sorted(totals):
            account = accounts[code]
            debit_total = totals[code]["debit"]
            credit_total = totals[code]["credit"]
            rows.append(
                TrialBalanceRow(
                    account_code=account.code,
                    account_name=account.name,
                    account_type=AccountType(account.account_type),
                    debit_total=debit_total,
                    credit_total=credit_total,
                    net_balance=debit_total - credit_total,
                )
            )
        total_debits = sum((r.debit_total for r in rows), Decimal("0.00"))
        total_credits = sum((r.credit_total for r in rows), Decimal("0.00"))
        return TrialBalance(
            period_start=period_start,
            period_end=period_end,
            rows=rows,
            total_debits=total_debits,
            total_credits=total_credits,
            is_balanced=total_debits == total_credits,
        )

    def seed_if_empty(self, db: Session) -> None:
        if db.scalar(select(AccountDB.code)) is None:
            db.add_all(
                [AccountDB(code=c, name=n, account_type=t) for c, n, t in _SEED_ACCOUNTS]
            )
            db.commit()
        if db.scalar(select(JournalEntryDB.id)) is None:
            for entry in self._seed_entries():
                self.create_journal_entry(db, entry)

    @staticmethod
    def _seed_entries() -> list[JournalEntryCreate]:
        return [
            JournalEntryCreate(
                entry_date=date(2026, 6, 1), memo="Seed member capital contribution",
                source_module="accounting", created_by="system",
                lines=[
                    {"account_code": "1000", "debit": Decimal("250000.00")},
                    {"account_code": "3000", "credit": Decimal("250000.00")},
                ],
            ),
            JournalEntryCreate(
                entry_date=date(2026, 6, 5), memo="Enterprise subscription invoice",
                source_module="billing", created_by="system",
                lines=[
                    {"account_code": "1100", "debit": Decimal("1500.00")},
                    {"account_code": "4000", "credit": Decimal("1500.00")},
                ],
            ),
            JournalEntryCreate(
                entry_date=date(2026, 6, 10), memo="Cloud and AI platform operating costs",
                source_module="operations", created_by="system",
                lines=[
                    {"account_code": "5000", "debit": Decimal("4200.00")},
                    {"account_code": "5100", "debit": Decimal("1800.00")},
                    {"account_code": "1000", "credit": Decimal("6000.00")},
                ],
            ),
        ]

    @staticmethod
    def _entry(db: Session, entry: JournalEntryDB) -> JournalEntry:
        line_rows = db.scalars(
            select(JournalLineDB)
            .where(JournalLineDB.entry_id == entry.id)
            .order_by(JournalLineDB.line_no)
        ).all()
        lines = [
            JournalLine(
                account_code=line.account_code,
                description=line.description,
                debit=Decimal(line.debit),
                credit=Decimal(line.credit),
                entity=line.entity,
                department=line.department,
                account_name=line.account_name,
                account_type=AccountType(line.account_type),
            )
            for line in line_rows
        ]
        return JournalEntry(
            id=entry.id,
            entry_date=entry.entry_date,
            memo=entry.memo,
            source_module=entry.source_module,
            created_by=entry.created_by,
            status=JournalStatus(entry.status),
            created_at=entry.created_at,
            posted_at=entry.posted_at,
            lines=lines,
        )
