# JHI-SIG: 69M2705M | CRM | John Henry Investments (proprietary)
"""Durable, Postgres/SQLAlchemy-backed CRM service.

Migrated from the in-memory store so contacts/deals/activities persist across
restarts. The API contract (pydantic models, status codes, errors) is unchanged.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_models import CRMActivityDB, CRMContactDB, CRMDealDB
from app.models import (
    CRMActivity,
    CRMActivityCreate,
    CRMContact,
    CRMContactCreate,
    CRMDeal,
    CRMDealCreate,
    CRMSummary,
    DealStage,
)

_CLOSED_STAGES = {DealStage.CLOSED_WON.value, DealStage.CLOSED_LOST.value}


class CRMService:
    # -- contacts --------------------------------------------------------- #
    def list_contacts(self, db: Session) -> list[CRMContact]:
        rows = db.scalars(select(CRMContactDB).order_by(CRMContactDB.created_at)).all()
        return [self._contact(r) for r in rows]

    def create_contact(self, db: Session, payload: CRMContactCreate) -> CRMContact:
        row = CRMContactDB(**payload.model_dump())
        db.add(row)
        db.commit()
        db.refresh(row)
        return self._contact(row)

    # -- deals ------------------------------------------------------------ #
    def list_deals(self, db: Session) -> list[CRMDeal]:
        rows = db.scalars(select(CRMDealDB).order_by(CRMDealDB.created_at)).all()
        return [self._deal(r) for r in rows]

    def create_deal(self, db: Session, payload: CRMDealCreate) -> CRMDeal:
        if db.get(CRMContactDB, str(payload.contact_id)) is None:
            raise KeyError(f"Unknown contact_id: {payload.contact_id}")
        row = CRMDealDB(
            contact_id=str(payload.contact_id),
            name=payload.name,
            stage=payload.stage.value,
            expected_value=str(payload.expected_value),
            probability=payload.probability,
            next_step=payload.next_step,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return self._deal(row)

    # -- activities ------------------------------------------------------- #
    def list_activities(self, db: Session) -> list[CRMActivity]:
        rows = db.scalars(select(CRMActivityDB).order_by(CRMActivityDB.created_at)).all()
        return [self._activity(r) for r in rows]

    def create_activity(self, db: Session, payload: CRMActivityCreate) -> CRMActivity:
        if db.get(CRMContactDB, str(payload.contact_id)) is None:
            raise KeyError(f"Unknown contact_id: {payload.contact_id}")
        if payload.deal_id is not None and db.get(CRMDealDB, str(payload.deal_id)) is None:
            raise KeyError(f"Unknown deal_id: {payload.deal_id}")
        row = CRMActivityDB(
            contact_id=str(payload.contact_id),
            deal_id=str(payload.deal_id) if payload.deal_id is not None else None,
            activity_type=payload.activity_type,
            summary=payload.summary,
            due_date=payload.due_date,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return self._activity(row)

    # -- summary ---------------------------------------------------------- #
    def summary(self, db: Session) -> CRMSummary:
        deals = db.scalars(select(CRMDealDB)).all()
        total_contacts = len(db.scalars(select(CRMContactDB.id)).all())
        active = [d for d in deals if d.stage not in _CLOSED_STAGES]
        weighted = sum(
            (Decimal(d.expected_value) * Decimal(d.probability) / Decimal("100") for d in active),
            Decimal("0"),
        )
        return CRMSummary(
            total_contacts=total_contacts,
            active_deals=len(active),
            weighted_pipeline=weighted,
            next_actions=[d.next_step for d in active if d.next_step],
        )

    # -- seed ------------------------------------------------------------- #
    def seed_if_empty(self, db: Session) -> None:
        if db.scalar(select(CRMContactDB.id)) is not None:
            return
        contact = self.create_contact(
            db,
            CRMContactCreate(
                full_name="Avery Johnson",
                organization="Northstar Family Office",
                email="avery@example.com",
                phone="555-0100",
                role="Managing Partner",
                relationship_type="enterprise prospect",
                owner="Marcellus Miller",
            ),
        )
        deal = self.create_deal(
            db,
            CRMDealCreate(
                contact_id=contact.id,
                name="Family office enterprise platform subscription",
                stage=DealStage.DILIGENCE,
                expected_value=Decimal("24000.00"),
                probability=65,
                next_step="Send branded macro report sample",
            ),
        )
        self.create_activity(
            db,
            CRMActivityCreate(
                contact_id=contact.id,
                deal_id=deal.id,
                activity_type="follow_up",
                summary="Provide demo access and compliance overview.",
                due_date=date(2026, 6, 30),
            ),
        )

    # -- converters ------------------------------------------------------- #
    @staticmethod
    def _contact(row: CRMContactDB) -> CRMContact:
        return CRMContact(
            id=row.id, full_name=row.full_name, organization=row.organization, email=row.email,
            phone=row.phone, role=row.role, relationship_type=row.relationship_type,
            owner=row.owner, created_at=row.created_at,
        )

    @staticmethod
    def _deal(row: CRMDealDB) -> CRMDeal:
        return CRMDeal(
            id=row.id, contact_id=row.contact_id, name=row.name, stage=DealStage(row.stage),
            expected_value=Decimal(row.expected_value), probability=row.probability,
            next_step=row.next_step, created_at=row.created_at, updated_at=row.updated_at,
        )

    @staticmethod
    def _activity(row: CRMActivityDB) -> CRMActivity:
        return CRMActivity(
            id=row.id, contact_id=row.contact_id, deal_id=row.deal_id,
            activity_type=row.activity_type, summary=row.summary, due_date=row.due_date,
            created_at=row.created_at,
        )
