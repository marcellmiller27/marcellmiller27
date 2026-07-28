# JHI-SIG: 69M2705M | Newsletters router (server-side PDF) | JHI Research & Analytics Firm, Inc. (proprietary)
import logging
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.editorial_llm import elevate_edition, llm_enabled
from app.market_services import MarketDataService
from app.newsletter_content import EDITION_SLUGS, NEWSLETTER_SYMBOLS, build_edition
from app.newsletter_render import render_newsletter_pdf
from app.pdf_export import newsletter_pdf
from app.security import decode_access_token

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/newsletters", tags=["newsletters"])


@router.get("/{edition}")
def newsletter_edition(
    edition: str,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    """The edition content as JSON — the single source of truth for on-screen render,
    the PDF (which prints the page), and future email. Deterministic build, then E2 LLM
    elevation (flag-gated, fact-locked). Role-aware: a valid bearer token → full edition."""
    if edition not in EDITION_SLUGS:
        raise HTTPException(status_code=404, detail="Unknown newsletter edition.")

    token = _bearer_token(request)
    data = MarketDataService().quotes(NEWSLETTER_SYMBOLS)
    built = build_edition(edition, data.quotes, datetime.now(timezone.utc), full=token is not None)

    editorial = "deterministic"
    if llm_enabled():
        built, meta = elevate_edition(built, db=db)
        editorial = "llm" if meta.get("used_llm") else f"deterministic:{meta.get('reason')}"

    return {"edition": asdict(built), "as_of": data.as_of.isoformat(), "editorial": editorial}


def _bearer_token(request: Request) -> str | None:
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None
    token = header[len("Bearer ") :]
    try:
        decode_access_token(token)
        return token
    except ValueError:
        return None


def _reportlab_pdf(edition: str, full: bool, db: Session) -> tuple[bytes, str]:
    """Fallback: server-side reportlab edition (only if the headless render fails).

    Applies the E2 LLM elevation here too (flag-gated, fact-locked) so the fallback
    still benefits from the editorial voice when enabled.
    """
    data = MarketDataService().quotes(NEWSLETTER_SYMBOLS)
    built = build_edition(edition, data.quotes, datetime.now(timezone.utc), full=full)
    note = "reportlab-fallback"
    if llm_enabled():
        built, meta = elevate_edition(built, db=db)
        note = "reportlab-fallback-llm" if meta.get("used_llm") else "reportlab-fallback"
    return newsletter_pdf(built), note


@router.get("/{edition}/pdf")
def newsletter_pdf_download(
    edition: str,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    """PDF of an editorial edition — **exactly as viewed on the site**.

    Primary path: print the real /newsletters/{edition} page with headless Chromium
    (masthead, VP-of-Editorial portrait, styling, sections; interactive controls omitted
    via @media print). Role-aware: a valid bearer token renders the full edition, else the
    teaser. Falls back to the reportlab edition (with optional E2 elevation) only if the
    browser render fails, so a download never breaks.
    """
    if edition not in EDITION_SLUGS:
        raise HTTPException(status_code=404, detail="Unknown newsletter edition.")

    token = _bearer_token(request)
    now = datetime.now(timezone.utc)
    source = "render"
    try:
        pdf_bytes = render_newsletter_pdf(edition, token=token)
    except Exception as exc:  # resilience: never fail the download
        logger.warning("Headless newsletter render failed (%s); using reportlab fallback.", exc)
        pdf_bytes, source = _reportlab_pdf(edition, full=token is not None, db=db)

    filename = f"aegira-{edition}-{now:%Y-%m-%d}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-PDF-Source": source,
        },
    )
