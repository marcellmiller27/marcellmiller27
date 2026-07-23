# JHI-SIG: 69M2705M | Newsletters router (server-side PDF) | JHI Research & Analytics Firm, Inc. (proprietary)
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.editorial_llm import elevate_edition, llm_enabled
from app.market_services import MarketDataService
from app.newsletter_content import EDITION_SLUGS, NEWSLETTER_SYMBOLS, build_edition
from app.pdf_export import newsletter_pdf
from app.security import decode_access_token

router = APIRouter(prefix="/newsletters", tags=["newsletters"])


def _is_authenticated(request: Request) -> bool:
    """Optional auth: a valid bearer token unlocks the full edition; otherwise the
    reader gets the same teaser they'd see on screen. No 401 — the preview is public."""
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return False
    try:
        decode_access_token(header[len("Bearer ") :])
        return True
    except ValueError:
        return False


@router.get("/{edition}/pdf")
def newsletter_pdf_download(
    edition: str,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    """Server-generated PDF for an editorial edition.

    Replaces the browser `window.print()` path (which crashed the forwarded/desktop
    viewer) and is reusable for the Step-B email attachment. Role-aware to mirror the
    on-screen gate: an authenticated (subscriber/staff) reader gets the full edition;
    anonymous/free readers get the teaser.
    """
    if edition not in EDITION_SLUGS:
        raise HTTPException(status_code=404, detail="Unknown newsletter edition.")

    full = _is_authenticated(request)
    data = MarketDataService().quotes(NEWSLETTER_SYMBOLS)
    now = datetime.now(timezone.utc)
    built = build_edition(edition, data.quotes, now, full=full)

    # E2 (flag-gated, off by default): elevate the prose with the LLM, fact-locked, with
    # deterministic fallback. Numeric fields are never sent to the model.
    source = "deterministic"
    if llm_enabled():
        built, meta = elevate_edition(built, db=db)
        source = "llm" if meta.get("used_llm") else f"deterministic:{meta.get('reason')}"

    pdf_bytes = newsletter_pdf(built)
    filename = f"jhi-{edition}-{now:%Y-%m-%d}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-Editorial-Source": source,
        },
    )
