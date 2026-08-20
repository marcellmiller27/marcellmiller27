# JHI-SIG: 69M2705M | Document Review module | JHI Research & Analytics Firm, Inc. (proprietary)
"""Document Review API — real upload → analysis → risk-scored, persisted queue.

These are sensitive tax/bank documents, so every route is AUTH-GATED
(``Depends(get_current_principal)``): an anonymous caller gets 401. Uploaded files
are validated (extension + content-type + size) and stored SECURELY OUTSIDE the
Next.js ``public/`` web root, under ``backend/app/data/document_review/<review_id>/``
with a sanitized, bare filename (path-traversal safe). Each upload is analyzed by the
deterministic engine and persisted as a ``DocumentReviewDB`` row; the queue returns
the caller's own reviews, newest first.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.db_models import DocumentReviewDB, new_id
from app.dependencies import get_current_principal
from app.document_review import (
    ALLOWED_CONTENT_TYPES,
    ALLOWED_EXTENSIONS,
    DISCLAIMER,
    MAX_UPLOAD_BYTES,
    _extension,
    analyze,
)
from app.document_review_models import (
    DOC_TYPE_LABELS,
    DocType,
    DocumentReviewResult,
    ReviewStatus,
)
from app.foundation_models import Principal

router = APIRouter(prefix="/document-review", tags=["document-review"])

# Uploaded documents live OUTSIDE the Next.js public/ web root.
STORAGE_DIR = (Path(__file__).resolve().parent.parent / "data" / "document_review").resolve()


def _safe_stored_name(filename: str) -> str:
    """Reduce any client-supplied name to a safe, bare filename (no path parts)."""
    bare = Path(filename or "").name
    bare = bare.replace("\x00", "")
    # Keep only a conservative character set; fall back to a generic name.
    cleaned = "".join(c for c in bare if c.isalnum() or c in ("-", "_", ".", " ")).strip()
    return cleaned or "upload"


def _to_result(row: DocumentReviewDB) -> DocumentReviewResult:
    return DocumentReviewResult(
        id=row.id,
        doc_type=DocType(row.doc_type),
        doc_type_label=DOC_TYPE_LABELS.get(row.doc_type, row.doc_type),
        filename=row.filename,
        content_type=row.content_type,
        size_bytes=row.size_bytes,
        uploaded_by=row.uploaded_by,
        status=ReviewStatus(row.status),
        risk_score=row.risk_score,
        risk_band=(
            ""
            if row.risk_score is None
            else ("High" if row.risk_score >= 67 else "Medium" if row.risk_score >= 34 else "Low")
        ),
        summary=row.summary,
        flags=json.loads(row.flags_json or "[]"),
        questions=json.loads(row.questions_json or "[]"),
        disclaimer=DISCLAIMER,
        uploaded_at=row.uploaded_at,
    )


@router.post("/upload", response_model=DocumentReviewResult, status_code=status.HTTP_201_CREATED)
async def upload_document(
    principal: Annotated[Principal, Depends(get_current_principal)],
    db: Annotated[Session, Depends(get_db)],
    doc_type: Annotated[DocType, Form(description="tax_returns | pnl | balance_sheet | bank_statements")],
    file: Annotated[UploadFile, File(description="PDF, CSV, or XLSX financial document.")],
) -> DocumentReviewResult:
    """Upload one financial document → validate → analyze → persist a risk-scored review."""
    filename = file.filename or "upload"
    ext = _extension(filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type '{ext or 'unknown'}'. Accepted: PDF, CSV, XLSX.",
        )
    if file.content_type and file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported content type '{file.content_type}'. Accepted: PDF, CSV, XLSX.",
        )

    raw = await file.read()
    if len(raw) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Empty file — nothing to analyze."
        )
    if len(raw) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,  # Content Too Large
            detail=f"File exceeds the {MAX_UPLOAD_BYTES // (1024 * 1024)} MB limit.",
        )

    record = DocumentReviewDB(
        id=new_id(),  # generate up front so the storage dir can key on the review id
        doc_type=doc_type.value,
        filename=Path(filename).name,
        uploaded_by=principal.email,
        organization_id=principal.organization_id,
        content_type=file.content_type or "",
        size_bytes=len(raw),
    )

    # Persist bytes to a per-review directory OUTSIDE the web root (path-traversal safe).
    stored_name = _safe_stored_name(filename)
    review_dir = (STORAGE_DIR / record.id).resolve()
    if not str(review_dir).startswith(str(STORAGE_DIR)):  # defense-in-depth
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid storage path.")
    review_dir.mkdir(parents=True, exist_ok=True)
    dest = (review_dir / stored_name).resolve()
    if dest.parent != review_dir:  # bare-name guarantee
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid filename.")
    dest.write_bytes(raw)
    record.stored_name = stored_name

    # Analyze (deterministic; never raises, never fabricates figures).
    result = analyze(doc_type, filename, file.content_type or "", raw)
    record.status = result.status.value
    record.risk_score = result.risk_score
    record.summary = result.summary
    record.flags_json = json.dumps(result.flags)
    record.questions_json = json.dumps(result.questions)

    db.add(record)
    db.commit()
    db.refresh(record)
    return _to_result(record)


@router.get("/queue", response_model=list[DocumentReviewResult])
def list_queue(
    principal: Annotated[Principal, Depends(get_current_principal)],
    db: Annotated[Session, Depends(get_db)],
) -> list[DocumentReviewResult]:
    """Return the authenticated user's persisted document reviews, newest first."""
    rows = db.scalars(
        select(DocumentReviewDB)
        .where(DocumentReviewDB.uploaded_by == principal.email)
        .order_by(DocumentReviewDB.uploaded_at.desc())
    ).all()
    return [_to_result(r) for r in rows]
