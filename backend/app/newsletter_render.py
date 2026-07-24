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
from urllib.parse import urlparse

# The frontend origin the backend prints from. In the compose network the frontend
# service is reachable at http://frontend:3000; override for other environments.
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://frontend:3000")

_PDF_MARGIN = {"top": "0.5in", "bottom": "0.5in", "left": "0.5in", "right": "0.5in"}


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
                prefer_css_page_size=True,
            )
        finally:
            browser.close()
