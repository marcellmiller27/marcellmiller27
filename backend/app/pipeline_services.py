# JHI-SIG: 69M2705M | Deal Pipeline | JHI Research & Analytics Firm, Inc. (proprietary)
"""Durable service for the Deal Pipeline — save, list, advance, and remove deals."""

from __future__ import annotations

import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_models import DealRecordDB
from app.pipeline_models import (
    DEAL_TYPES,
    STAGES,
    DealRecord,
    DealRecordCreate,
    DealRecordUpdate,
)


class PipelineError(ValueError):
    """Raised on invalid pipeline operations (bad stage/type or missing record)."""


class PipelineService:
    @staticmethod
    def _to_model(row: DealRecordDB) -> DealRecord:
        try:
            inputs = json.loads(row.inputs_json) if row.inputs_json else {}
        except json.JSONDecodeError:
            inputs = {}
        return DealRecord(
            id=row.id, business_name=row.business_name, deal_type=row.deal_type,
            stage=row.stage, score=row.score, recommendation=row.recommendation,
            headline=row.headline, inputs=inputs, notes=row.notes,
            created_at=row.created_at, updated_at=row.updated_at,
        )

    def create(self, db: Session, payload: DealRecordCreate) -> DealRecord:
        if payload.deal_type not in DEAL_TYPES:
            raise PipelineError(f"Unknown deal_type '{payload.deal_type}'.")
        if payload.stage not in STAGES:
            raise PipelineError(f"Unknown stage '{payload.stage}'.")
        row = DealRecordDB(
            business_name=payload.business_name, deal_type=payload.deal_type,
            stage=payload.stage, score=payload.score, recommendation=payload.recommendation,
            headline=payload.headline, notes=payload.notes,
            inputs_json=json.dumps(payload.inputs or {}),
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return self._to_model(row)

    def list(self, db: Session) -> list[DealRecord]:
        rows = db.execute(
            select(DealRecordDB).order_by(DealRecordDB.updated_at.desc())
        ).scalars().all()
        return [self._to_model(r) for r in rows]

    def get(self, db: Session, deal_id: str) -> DealRecord:
        row = db.get(DealRecordDB, deal_id)
        if row is None:
            raise PipelineError("Deal not found.")
        return self._to_model(row)

    def update(self, db: Session, deal_id: str, payload: DealRecordUpdate) -> DealRecord:
        row = db.get(DealRecordDB, deal_id)
        if row is None:
            raise PipelineError("Deal not found.")
        if payload.stage is not None:
            if payload.stage not in STAGES:
                raise PipelineError(f"Unknown stage '{payload.stage}'.")
            row.stage = payload.stage
        if payload.notes is not None:
            row.notes = payload.notes
        if payload.headline is not None:
            row.headline = payload.headline
        db.commit()
        db.refresh(row)
        return self._to_model(row)

    def delete(self, db: Session, deal_id: str) -> None:
        row = db.get(DealRecordDB, deal_id)
        if row is None:
            raise PipelineError("Deal not found.")
        db.delete(row)
        db.commit()
