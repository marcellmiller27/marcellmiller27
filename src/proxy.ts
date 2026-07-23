// JHI-SIG: 69M2705M | Route access enforcement (proxy) | JHI Research & Analytics Firm, Inc. (proprietary)
// Server-side enforcement: product routes require an auth token cookie. Unauthenticated
// visitors are redirected to /login (deep-links are blocked at the edge, not just hidden
// in the menu). The storefront and the Newsletter module (teaser) stay public.
//
// NOTE: this gates on token PRESENCE (set only by a real backend login). The backend APIs
// remain the hard guard (they verify the JWT signature); verifying the token here too
// (via /auth/me) is an optional hardening.
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PROTECTED_PREFIXES = [
  "/dashboard",
  "/macro",
  "/opportunities",
  "/deal-xray",
  "/diligence-suite",
  "/due-diligence",
  "/pipeline",
  "/portfolio",
  "/assistant",
  "/downloads",
  "/reports",
  "/companies",
  "/firms",
  "/advisors",
  "/accounting",
  "/account"
];

function isProtected(pathname: string): boolean {
  return PROTECTED_PREFIXES.some((p) => pathname === p || pathname.startsWith(`${p}/`));
}

export function proxy(req: NextRequest) {
  const { pathname } = req.nextUrl;
  if (!isProtected(pathname)) return NextResponse.next();

  const token = req.cookies.get("jhi_token")?.value;
  if (!token) {
    const url = req.nextUrl.clone();
    url.pathname = "/login";
    url.searchParams.set("next", pathname);
    return NextResponse.redirect(url);
  }
  return NextResponse.next();
}

export const config = {
  // Run on all app routes except Next internals and the API proxy.
  matcher: ["/((?!_next/static|_next/image|favicon.ico|icon.svg|api).*)"]
};
