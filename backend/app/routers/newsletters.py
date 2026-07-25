# JHI-SIG: 69M2705M | Newsletters router (server-side PDF) | JHI Research & Analytics Firm, Inc. (proprietary)
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Request, Response

from app.market_services import MarketDataService
from app.newsletter_content import EDITION_SLUGS, NEWSLETTER_SYMBOLS, build_edition
from app.newsletter_render import render_newsletter_pdf
from app.pdf_export import newsletter_pdf
from app.security import decode_access_token

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/newsletters", tags=["newsletters"])


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


def _reportlab_pdf(edition: str, full: bool) -> bytes:
    """Fallback: server-side reportlab edition (used only if the headless render fails)."""
    data = MarketDataService().quotes(NEWSLETTER_SYMBOLS)
    built = build_edition(edition, data.quotes, datetime.now(timezone.utc), full=full)
    return newsletter_pdf(built)


@router.get("/{edition}/pdf")
def newsletter_pdf_download(edition: str, request: Request) -> Response:
    """PDF of an editorial edition — **exactly as viewed on the site**.

    Primary path: print the real /newsletters/{edition} page with headless Chromium
    (masthead, VP-of-Editorial portrait, styling, sections; interactive controls omitted
    via @media print). Role-aware: a valid bearer token renders the full edition, else the
    teaser. Falls back to the reportlab edition only if the browser render fails, so a
    download never breaks.
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
        pdf_bytes = _reportlab_pdf(edition, full=token is not None)
        source = "reportlab-fallback"

    filename = f"jhi-{edition}-{now:%Y-%m-%d}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-PDF-Source": source,
        },
    )
