# JHI-SIG: 69M2705M | Exact-as-viewed newsletter PDF (headless render) | JHI Research & Analytics Firm, Inc. (proprietary)
"""Render the *actual* newsletter web page to PDF with headless Chromium, so the
download is pixel-identical to what the reader sees on the site (masthead, the VP of
Editorial portrait, styling, sections) — not a reportlab approximation.

Interactive controls (the Download button, etc.) are omitted via the site's @media
print rules. A caller's auth token is forwarded as the `jhi_token` cookie so the page
renders the full edition for subscribers/staff (teaser otherwise), mirroring on-screen.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from urllib.parse import urlparse

# The frontend origin the backend prints from. In the compose network the frontend
# service is reachable at http://frontend:3000; override for other environments.
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://frontend:3000")

# Institutional document margins — leave room for the running letterhead + footer.
_PDF_MARGIN = {"top": "0.95in", "bottom": "0.75in", "left": "0.6in", "right": "0.6in"}

# Running letterhead (every page) — firm mark + desk.
_HEADER_TEMPLATE = (
    '<div style="width:100%;font-size:8px;color:#0C1F33;font-family:Georgia,\'Times New Roman\',serif;'
    'padding:0 0.6in;display:flex;justify-content:space-between;align-items:center;'
    '-webkit-print-color-adjust:exact;">'
    '<span style="font-weight:bold;letter-spacing:0.02em;">JHI Research &amp; Analytics Firm, Inc.</span>'
    '<span style="color:#5A6B7D;letter-spacing:0.08em;text-transform:uppercase;font-size:7px;">'
    "Institutional Research &middot; Economic Tracking</span></div>"
)


def _footer_template(year: int) -> str:
    # Running footer (every page): provenance + confidentiality + page numbers.
    return (
        '<div style="width:100%;font-size:7px;color:#5A6B7D;font-family:Helvetica,Arial,sans-serif;'
        'padding:0 0.6in;display:flex;justify-content:space-between;align-items:center;'
        '-webkit-print-color-adjust:exact;">'
        f"<span>&copy; {year} JHI Research &amp; Analytics Firm, Inc. &middot; "
        "Confidential &mdash; not for redistribution</span>"
        '<span>JHI-SIG: 69M2705M &middot; Page <span class="pageNumber"></span> of '
        '<span class="totalPages"></span></span></div>'
    )


def render_newsletter_pdf(slug: str, token: str | None = None, origin: str | None = None) -> bytes:
    """Print /newsletters/{slug} to PDF via headless Chromium. Raises on failure so the
    caller can fall back to the server-side (reportlab) edition."""
    from playwright.sync_api import sync_playwright

    base = (origin or FRONTEND_ORIGIN).rstrip("/")
    url = f"{base}/newsletters/{slug}"
    host = urlparse(base).hostname or "localhost"

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
        try:
            context = browser.new_context(viewport={"width": 900, "height": 1200})
            if token:
                # jhi_token cookie → RoleProvider derives subscriber/staff → full edition.
                context.add_cookies(
                    [{"name": "jhi_token", "value": token, "domain": host, "path": "/"}]
                )
            page = context.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            # Masthead is always present; wait for it, then let live data + the portrait settle.
            page.wait_for_selector(".news__masthead", timeout=20000)
            page.wait_for_timeout(600)
            page.emulate_media(media="print")
            return page.pdf(
                print_background=True,
                format="Letter",
                margin=_PDF_MARGIN,
                display_header_footer=True,
                header_template=_HEADER_TEMPLATE,
                footer_template=_footer_template(datetime.now(timezone.utc).year),
            )
        finally:
            browser.close()
