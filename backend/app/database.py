# JHI-SIG: 69M2705M | Platform spine | John Henry Investments (proprietary)
import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./john_henry_platform.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def init_db() -> None:
    import app.db_models  # noqa: F401

    Base.metadata.create_all(bind=engine)

    # Seed durable demo data if empty (keeps the CRM + accounting API contracts).
    from app.accounting_services import AccountingService
    from app.crm_services import CRMService

    db = SessionLocal()
    try:
        CRMService().seed_if_empty(db)
        AccountingService().seed_if_empty(db)
    finally:
        db.close()


def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
