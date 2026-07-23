# JHI-SIG: 69M2705M | Newsletters router (server-side PDF) | JHI Research & Analytics Firm, Inc. (proprietary)
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Response

from app.market_services import MarketDataService
from app.newsletter_content import EDITION_SLUGS, NEWSLETTER_SYMBOLS, build_edition
from app.pdf_export import newsletter_pdf

router = APIRouter(prefix="/newsletters", tags=["newsletters"])


@router.get("/{edition}/pdf")
def newsletter_pdf_download(edition: str) -> Response:
    """Server-generated PDF for an editorial edition.

    Replaces the browser `window.print()` path (which crashed the forwarded/desktop
    viewer) and is reusable for the Step-B email attachment. Editions on-platform are
    currently public, so the PDF renders the full edition; when per-plan gating lands
    (Phase 6), pass full=False here for anonymous readers to mirror the on-screen teaser.
    """
    if edition not in EDITION_SLUGS:
        raise HTTPException(status_code=404, detail="Unknown newsletter edition.")

    data = MarketDataService().quotes(NEWSLETTER_SYMBOLS)
    now = datetime.now(timezone.utc)
    built = build_edition(edition, data.quotes, now, full=True)
    pdf_bytes = newsletter_pdf(built)

    filename = f"jhi-{edition}-{now:%Y-%m-%d}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
