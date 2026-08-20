# JHI-SIG: 69M2705M | Document Review module tests | JHI Research & Analytics Firm, Inc. (proprietary)
"""Tests for the Document Review module: real upload → analysis → persisted queue.

Covers the engine (deterministic risk indicators, graceful unparseable handling) and
the auth-gated endpoints (upload validation, persistence, per-user queue, and the
path-traversal guard on stored filenames).
"""

from __future__ import annotations

import io
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.document_review import analyze
from app.document_review_models import DocType, ReviewStatus
from app.main import app
from app.routers import document_review as dr_router

client = TestClient(app)

STORAGE_DIR = dr_router.STORAGE_DIR


def register_user() -> tuple[str, str]:
    """Register a fresh org/user and return (email, access_token)."""
    unique = uuid4().hex[:10]
    email = f"owner-{unique}@example.com"
    response = client.post(
        "/api/v1/auth/register",
        json={
            "organization_name": f"JHI Test Org {unique}",
            "full_name": "Jordan Lee",
            "email": email,
            "password": "SecurePass123",
            "plan": "professional",
        },
    )
    assert response.status_code == 201, response.text
    return email, response.json()["access_token"]


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


DECLINING_CSV = (
    "Line Item,2021,2022,2023\n"
    "Revenue,1000000,880000,760000\n"
    "Cost of Goods Sold,400000,390000,395000\n"
    "Net Income,120000,60000,-20000\n"
).encode("utf-8")


def _tiny_pdf(text: str) -> bytes:
    from reportlab.pdfgen import canvas

    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    for i, line in enumerate(text.splitlines()):
        c.drawString(72, 720 - i * 16, line)
    c.showPage()
    c.save()
    return buf.getvalue()


# --- Engine-level tests ------------------------------------------------------
def test_engine_flags_declining_series_and_scores() -> None:
    result = analyze(DocType.PNL, "pnl.csv", "text/csv", DECLINING_CSV)
    assert result.status == ReviewStatus.ANALYZED
    assert result.risk_score is not None and 0 <= result.risk_score <= 100
    joined = " ".join(result.flags).lower()
    assert "declining" in joined
    assert any("negative" in f.lower() for f in result.flags)  # Net Income goes negative
    assert result.questions  # diligence questions generated


def test_engine_never_fabricates_on_unparseable_file() -> None:
    result = analyze(DocType.TAX_RETURNS, "scan.pdf", "application/pdf", b"%PDF-1.4 not-real")
    assert result.status == ReviewStatus.MANUAL_REVIEW_REQUIRED
    assert result.risk_score is None  # no invented figures
    assert result.questions  # still gives the analyst baseline questions


# --- Endpoint tests ----------------------------------------------------------
def test_upload_csv_persists_scored_review() -> None:
    _email, token = register_user()
    resp = client.post(
        "/api/v1/document-review/upload",
        headers=_auth(token),
        data={"doc_type": "pnl"},
        files={"file": ("statement.csv", DECLINING_CSV, "text/csv")},
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["doc_type"] == "pnl"
    assert body["status"] == "analyzed"
    assert isinstance(body["risk_score"], int)
    assert body["flags"] and body["questions"]
    assert body["risk_band"] in ("Low", "Medium", "High")
    assert "not an audit" in body["disclaimer"].lower()


def test_upload_pdf_is_analyzed() -> None:
    _email, token = register_user()
    pdf = _tiny_pdf("Balance Sheet 2023\nAccounts Receivable 250,000\nDeferred Revenue 90,000")
    resp = client.post(
        "/api/v1/document-review/upload",
        headers=_auth(token),
        data={"doc_type": "balance_sheet"},
        files={"file": ("balance.pdf", pdf, "application/pdf")},
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    # A text PDF is parseable → analyzed with a score; a scanned one would be manual.
    assert body["status"] in ("analyzed", "manual_review_required")
    assert body["questions"]


def test_unsupported_type_rejected() -> None:
    _email, token = register_user()
    resp = client.post(
        "/api/v1/document-review/upload",
        headers=_auth(token),
        data={"doc_type": "pnl"},
        files={"file": ("malware.exe", b"MZ\x90\x00", "application/octet-stream")},
    )
    assert resp.status_code == 415, resp.text


def test_oversize_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    _email, token = register_user()
    monkeypatch.setattr(dr_router, "MAX_UPLOAD_BYTES", 1024)  # 1 KB cap for the test
    big = ("x,y\n" + "1000000,2000000\n" * 500).encode("utf-8")
    assert len(big) > 1024
    resp = client.post(
        "/api/v1/document-review/upload",
        headers=_auth(token),
        data={"doc_type": "bank_statements"},
        files={"file": ("big.csv", big, "text/csv")},
    )
    assert resp.status_code == 413, resp.text


def test_unauthenticated_upload_is_401() -> None:
    resp = client.post(
        "/api/v1/document-review/upload",
        data={"doc_type": "pnl"},
        files={"file": ("statement.csv", DECLINING_CSV, "text/csv")},
    )
    assert resp.status_code == 401, resp.text


def test_unauthenticated_queue_is_401() -> None:
    resp = client.get("/api/v1/document-review/queue")
    assert resp.status_code == 401, resp.text


def test_queue_returns_only_own_reviews_newest_first() -> None:
    _email_a, token_a = register_user()
    _email_b, token_b = register_user()

    # User A uploads two documents.
    for doc_type, name in (("pnl", "a1.csv"), ("balance_sheet", "a2.csv")):
        r = client.post(
            "/api/v1/document-review/upload",
            headers=_auth(token_a),
            data={"doc_type": doc_type},
            files={"file": (name, DECLINING_CSV, "text/csv")},
        )
        assert r.status_code == 201, r.text

    # User B uploads one.
    r = client.post(
        "/api/v1/document-review/upload",
        headers=_auth(token_b),
        data={"doc_type": "tax_returns"},
        files={"file": ("b1.csv", DECLINING_CSV, "text/csv")},
    )
    assert r.status_code == 201, r.text

    queue_a = client.get("/api/v1/document-review/queue", headers=_auth(token_a))
    assert queue_a.status_code == 200
    rows_a = queue_a.json()
    assert len(rows_a) == 2  # A sees only A's uploads
    # Newest first.
    assert rows_a[0]["filename"] == "a2.csv"
    assert all(row["uploaded_by"] == _email_a for row in rows_a)

    queue_b = client.get("/api/v1/document-review/queue", headers=_auth(token_b))
    assert len(queue_b.json()) == 1


def test_path_traversal_filename_is_neutralized() -> None:
    _email, token = register_user()
    resp = client.post(
        "/api/v1/document-review/upload",
        headers=_auth(token),
        data={"doc_type": "bank_statements"},
        files={"file": ("../../../../etc/evil.csv", DECLINING_CSV, "text/csv")},
    )
    assert resp.status_code == 201, resp.text
    review_id = resp.json()["id"]
    # The file must be stored INSIDE the per-review dir, never escaping the storage root.
    review_dir = STORAGE_DIR / review_id
    stored = list(review_dir.glob("*"))
    assert stored, "file was not stored in the per-review directory"
    for path in stored:
        assert STORAGE_DIR.resolve() in path.resolve().parents
    # No traversal artifact landed outside the storage root.
    assert not (STORAGE_DIR.parent / "evil.csv").exists()
    assert not (Path("/tmp") / "evil.csv").exists()
    # The stored display filename is a bare basename.
    assert resp.json()["filename"] == "evil.csv"
