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

# Full GAAP-style chart of accounts for JHI Research & Analytics Firm, Inc.
# Each row: (code, name, account_type, category). Category drives statement grouping;
# account_type (asset/liability/equity/revenue/expense) drives debit/credit normalization.
# Contra accounts keep their parent type (e.g. Accumulated Depreciation is an asset).
_SEED_ACCOUNTS = [
    # --- 1000 Assets: Current ---
    ("1010", "Cash - Operating", "asset", "Current Assets"),
    ("1020", "Cash - Payroll", "asset", "Current Assets"),
    ("1030", "Money Market", "asset", "Current Assets"),
    ("1100", "Accounts Receivable", "asset", "Current Assets"),
    ("1110", "Allowance for Doubtful Accounts", "asset", "Current Assets"),  # contra-asset
    ("1200", "Prepaid Insurance", "asset", "Current Assets"),
    ("1210", "Prepaid Software Licenses", "asset", "Current Assets"),
    ("1220", "Prepaid Marketing", "asset", "Current Assets"),
    ("1230", "Employee Advances", "asset", "Current Assets"),
    ("1240", "Deposits", "asset", "Current Assets"),
    # --- 1500 Assets: Fixed ---
    ("1500", "Computer Equipment", "asset", "Fixed Assets"),
    ("1510", "Office Equipment", "asset", "Fixed Assets"),
    ("1520", "Furniture & Fixtures", "asset", "Fixed Assets"),
    ("1530", "Leasehold Improvements", "asset", "Fixed Assets"),
    ("1590", "Accumulated Depreciation", "asset", "Fixed Assets"),  # contra-asset
    # --- 1700 Assets: Intangible ---
    ("1700", "Capitalized Software Development", "asset", "Intangible Assets"),
    ("1710", "Internally Developed Platform IP", "asset", "Intangible Assets"),
    ("1720", "Trademarks", "asset", "Intangible Assets"),
    ("1730", "Copyrights", "asset", "Intangible Assets"),
    ("1740", "Patents", "asset", "Intangible Assets"),
    ("1750", "Domain Names", "asset", "Intangible Assets"),
    ("1760", "Goodwill", "asset", "Intangible Assets"),
    ("1770", "Customer Lists (Acquired)", "asset", "Intangible Assets"),
    ("1790", "Accumulated Amortization", "asset", "Intangible Assets"),  # contra-asset
    # --- 2000 Liabilities: Current ---
    ("2000", "Accounts Payable", "liability", "Current Liabilities"),
    ("2010", "Credit Cards Payable", "liability", "Current Liabilities"),
    ("2020", "Payroll Liabilities", "liability", "Current Liabilities"),
    ("2030", "Federal Payroll Taxes", "liability", "Current Liabilities"),
    ("2040", "State Payroll Taxes", "liability", "Current Liabilities"),
    ("2050", "Sales Tax Payable", "liability", "Current Liabilities"),
    ("2060", "Deferred Revenue (Subscriptions)", "liability", "Current Liabilities"),
    ("2070", "Customer Deposits", "liability", "Current Liabilities"),
    ("2080", "Accrued Expenses", "liability", "Current Liabilities"),
    # --- 2500 Liabilities: Long-Term ---
    ("2500", "SBA Loan", "liability", "Long-Term Liabilities"),
    ("2510", "Notes Payable", "liability", "Long-Term Liabilities"),
    ("2520", "Equipment Loan", "liability", "Long-Term Liabilities"),
    ("2530", "Deferred Tax Liability", "liability", "Long-Term Liabilities"),
    # --- 3000 Shareholders' Equity ---
    ("3000", "Common Stock", "equity", "Shareholders' Equity"),
    ("3010", "Additional Paid-In Capital", "equity", "Shareholders' Equity"),
    ("3020", "Treasury Stock", "equity", "Shareholders' Equity"),  # contra-equity
    ("3100", "Retained Earnings", "equity", "Shareholders' Equity"),
    ("3200", "Current Year Earnings", "equity", "Shareholders' Equity"),
    # --- 4000 Revenue: Subscription ---
    ("4000", "Enterprise Subscriptions", "revenue", "Subscription Revenue"),
    ("4010", "Professional Subscriptions", "revenue", "Subscription Revenue"),
    ("4020", "Individual Subscriptions", "revenue", "Subscription Revenue"),
    ("4030", "Monthly Subscription Revenue", "revenue", "Subscription Revenue"),
    ("4040", "Annual Subscription Revenue", "revenue", "Subscription Revenue"),
    # --- 4100 Revenue: Research ---
    ("4100", "Institutional Research", "revenue", "Research Revenue"),
    ("4110", "Business Acquisition Research", "revenue", "Research Revenue"),
    ("4120", "Search Fund Due Diligence", "revenue", "Research Revenue"),
    ("4130", "Financial Education Revenue", "revenue", "Research Revenue"),
    # --- 4200 Revenue: Other ---
    ("4200", "Licensing Revenue", "revenue", "Other Revenue"),
    ("4210", "API Revenue", "revenue", "Other Revenue"),
    ("4220", "Advertising Revenue", "revenue", "Other Revenue"),
    ("4230", "Affiliate Revenue", "revenue", "Other Revenue"),
    ("4300", "Interest Income", "revenue", "Other Revenue"),
    ("4310", "Other Income", "revenue", "Other Revenue"),
    # --- 5000 Cost of Revenue ---
    ("5000", "Cloud Hosting", "expense", "Cost of Revenue"),
    ("5010", "API Data Providers", "expense", "Cost of Revenue"),
    ("5020", "Financial Market Data Licenses", "expense", "Cost of Revenue"),
    ("5030", "Software Infrastructure", "expense", "Cost of Revenue"),
    ("5040", "AI Processing Costs", "expense", "Cost of Revenue"),
    ("5050", "Payment Processing Fees", "expense", "Cost of Revenue"),
    ("5060", "Customer Support", "expense", "Cost of Revenue"),
    # --- 6000 Operating Expenses: Payroll ---
    ("6000", "Officer Salaries", "expense", "Payroll"),
    ("6010", "Employee Salaries", "expense", "Payroll"),
    ("6020", "Payroll Taxes", "expense", "Payroll"),
    ("6030", "Employee Benefits", "expense", "Payroll"),
    ("6040", "Retirement Contributions", "expense", "Payroll"),
    # --- 6100 Operating Expenses: Research & Development ---
    ("6100", "Software Development", "expense", "Research & Development"),
    ("6110", "Contractors", "expense", "Research & Development"),
    ("6120", "Software Testing", "expense", "Research & Development"),
    ("6130", "Product Design", "expense", "Research & Development"),
    ("6140", "AI Development", "expense", "Research & Development"),
    # --- 6200 Operating Expenses: Sales & Marketing ---
    ("6200", "Advertising", "expense", "Sales & Marketing"),
    ("6210", "Digital Marketing", "expense", "Sales & Marketing"),
    ("6220", "SEO", "expense", "Sales & Marketing"),
    ("6230", "Conferences", "expense", "Sales & Marketing"),
    ("6240", "Promotional Materials", "expense", "Sales & Marketing"),
    # --- 6300 Operating Expenses: General & Administrative ---
    ("6300", "Rent", "expense", "General & Administrative"),
    ("6310", "Utilities", "expense", "General & Administrative"),
    ("6320", "Internet", "expense", "General & Administrative"),
    ("6330", "Office Supplies", "expense", "General & Administrative"),
    ("6340", "Telephone", "expense", "General & Administrative"),
    ("6350", "Insurance", "expense", "General & Administrative"),
    ("6360", "Bank Charges", "expense", "General & Administrative"),
    ("6370", "Legal Fees", "expense", "General & Administrative"),
    ("6380", "Accounting & Audit Fees", "expense", "General & Administrative"),
    ("6390", "Board of Directors Expense", "expense", "General & Administrative"),
    ("6400", "Travel", "expense", "General & Administrative"),
    ("6410", "Meals", "expense", "General & Administrative"),
    ("6420", "Dues & Subscriptions", "expense", "General & Administrative"),
    ("6430", "Training", "expense", "General & Administrative"),
    # --- 6500 Operating Expenses: Technology ---
    ("6500", "Microsoft 365", "expense", "Technology"),
    ("6510", "AWS/Azure Hosting", "expense", "Technology"),
    ("6520", "Google Cloud", "expense", "Technology"),
    ("6530", "GitHub", "expense", "Technology"),
    ("6540", "Atlassian", "expense", "Technology"),
    ("6550", "Cybersecurity", "expense", "Technology"),
    ("6560", "Software Licenses", "expense", "Technology"),
    # --- 6600 Operating Expenses: Depreciation & Amortization ---
    ("6600", "Depreciation Expense", "expense", "Depreciation & Amortization"),
    ("6610", "Amortization Expense", "expense", "Depreciation & Amortization"),
    # --- 6700 Operating Expenses: Taxes ---
    ("6700", "State Franchise Tax", "expense", "Taxes"),
    ("6710", "Federal Income Tax", "expense", "Taxes"),
    ("6720", "State Income Tax", "expense", "Taxes"),
    ("6730", "Property Tax", "expense", "Taxes"),
    # --- 6800 Operating Expenses: Other ---
    ("6800", "Charitable Contributions", "expense", "Other Expenses"),
    ("6810", "Miscellaneous Expense", "expense", "Other Expenses"),
    # --- 7000 Non-Operating Items ---
    ("7000", "Interest Expense", "expense", "Non-Operating"),
    ("7010", "Gain on Asset Disposal", "revenue", "Non-Operating"),
    ("7020", "Loss on Asset Disposal", "expense", "Non-Operating"),
]


class AccountingService:
    def list_accounts(self, db: Session) -> list[Account]:
        rows = db.scalars(select(AccountDB).order_by(AccountDB.code)).all()
        return [
            Account(
                code=r.code,
                name=r.name,
                account_type=AccountType(r.account_type),
                category=r.category or "",
            )
            for r in rows
        ]

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
        # Idempotent upsert of the chart of accounts: add any missing codes and keep
        # the name/type/category authoritative for existing codes (so a previously
        # seeded database converges to the current chart without manual migration).
        existing = {a.code: a for a in db.scalars(select(AccountDB)).all()}
        changed = False
        for code, name, atype, category in _SEED_ACCOUNTS:
            acc = existing.get(code)
            if acc is None:
                db.add(AccountDB(code=code, name=name, account_type=atype, category=category))
                changed = True
            elif acc.name != name or acc.account_type != atype or (acc.category or "") != category:
                acc.name = name
                acc.account_type = atype
                acc.category = category
                changed = True
        if changed:
            db.commit()
        if db.scalar(select(JournalEntryDB.id)) is None:
            for entry in self._seed_entries():
                self.create_journal_entry(db, entry)

    @staticmethod
    def _seed_entries() -> list[JournalEntryCreate]:
        return [
            JournalEntryCreate(
                entry_date=date(2026, 6, 1), memo="Seed founder capital contribution",
                source_module="accounting", created_by="system",
                lines=[
                    {"account_code": "1010", "debit": Decimal("250000.00")},
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
                    {"account_code": "5040", "debit": Decimal("1800.00")},
                    {"account_code": "1010", "credit": Decimal("6000.00")},
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
