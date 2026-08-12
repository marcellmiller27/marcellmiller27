"""JHI-SIG: 69M2705M | Firm Documents staff-gate tests | JHI Research & Analytics Firm, Inc.

Verifies that confidential firm documents are streamed ONLY to authenticated staff:
anonymous -> 401, non-staff subscriber -> 403, staff -> 200 with the file bytes. Also
verifies the files no longer live in the public web root and that path traversal is blocked.
"""
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCUMENTS_DIR = REPO_ROOT / "backend" / "app" / "data" / "firm_documents"
SAMPLE_DOC = "Aegira_Data_Sources_Comparison.xlsx"


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


def test_documents_are_not_in_public_web_root() -> None:
    # The confidential files must NOT be statically served from Next.js public/.
    public_downloads = REPO_ROOT / "public" / "downloads"
    static_files = list(public_downloads.glob("*.xlsx")) + list(public_downloads.glob("*.docx"))
    assert static_files == [], f"Confidential files still statically served: {static_files}"
    # They live in the non-public backend data dir instead.
    assert (DOCUMENTS_DIR / SAMPLE_DOC).is_file()


def test_anonymous_request_is_unauthorized() -> None:
    res = client.get(f"/api/v1/firm-documents/{SAMPLE_DOC}")
    assert res.status_code == 401


def test_non_staff_subscriber_is_forbidden(monkeypatch: pytest.MonkeyPatch) -> None:
    # No staff allowlist -> a normal, authenticated subscriber is still denied.
    monkeypatch.setenv("JHI_STAFF_EMAILS", "founder@johnhenry.example")
    _email, token = register_user()
    res = client.get(
        f"/api/v1/firm-documents/{SAMPLE_DOC}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403


def test_staff_can_download(monkeypatch: pytest.MonkeyPatch) -> None:
    email, token = register_user()
    # Put THIS user's email on the staff allowlist (require_staff reads the env at call time).
    monkeypatch.setenv("JHI_STAFF_EMAILS", email)
    res = client.get(
        f"/api/v1/firm-documents/{SAMPLE_DOC}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert (
        res.headers["content-type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    # A real .xlsx is a zip archive -> starts with the PK signature.
    assert res.content[:2] == b"PK"
    assert len(res.content) > 0


def test_staff_missing_document_returns_404(monkeypatch: pytest.MonkeyPatch) -> None:
    email, token = register_user()
    monkeypatch.setenv("JHI_STAFF_EMAILS", email)
    res = client.get(
        "/api/v1/firm-documents/does_not_exist.xlsx",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404


def test_path_traversal_is_blocked(monkeypatch: pytest.MonkeyPatch) -> None:
    email, token = register_user()
    monkeypatch.setenv("JHI_STAFF_EMAILS", email)
    # URL-encoded traversal that survives to the path param must not escape the dir.
    res = client.get(
        "/api/v1/firm-documents/..%2f..%2fmain.py",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404
