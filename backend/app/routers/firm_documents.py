"""JHI-SIG: 69M2705M | Firm Documents (staff-only) | JHI Research & Analytics Firm, Inc. (proprietary)

Confidential firm documents (internal models, handbooks, competitor audits) are NOT
served statically from the Next.js `public/` tree. They live outside the web root
(`backend/app/data/firm_documents/`) and are streamed only through this endpoint,
which is gated to JHI staff (`Depends(require_staff)`). A non-staff or anonymous
request therefore receives 401/403 and never touches the file bytes.
"""
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

from app.foundation_models import Principal
from app.rbac import require_staff

router = APIRouter(prefix="/firm-documents", tags=["firm-documents"])

# Confidential documents live outside the Next.js `public/` web root.
DOCUMENTS_DIR = (Path(__file__).resolve().parent.parent / "data" / "firm_documents").resolve()

_MEDIA_TYPES = {
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


@router.get("/{name}")
def get_firm_document(
    name: str,
    _staff: Annotated[Principal, Depends(require_staff)],
) -> FileResponse:
    """Stream a confidential firm document to an authenticated staff member.

    `require_staff` runs first: anonymous callers get 401, non-staff subscribers get 403,
    so the file bytes are never reached without staff authorization.
    """
    # Reject anything that is not a bare filename (defense-in-depth against path traversal).
    if name != Path(name).name or name in (".", "..") or name.startswith("."):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    path = (DOCUMENTS_DIR / name).resolve()
    if DOCUMENTS_DIR != path.parent or not path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    media_type = _MEDIA_TYPES.get(path.suffix.lower(), "application/octet-stream")
    return FileResponse(path, media_type=media_type, filename=name)
