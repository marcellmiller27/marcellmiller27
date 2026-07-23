// JHI-SIG: 69M2705M | Auth cookie helpers (client) | JHI Research & Analytics Firm, Inc. (proprietary)
// The auth token is issued by the backend (/api/v1/auth/login|register) and stored in a
// cookie so Next.js middleware can enforce route access server-side. A separate "free"
// cookie marks free-newsletter registrants (no login) for the teaser tier.

export const TOKEN_COOKIE = "jhi_token";
export const FREE_COOKIE = "jhi_free";

export function setCookie(name: string, value: string, days = 7): void {
  try {
    document.cookie = `${name}=${encodeURIComponent(value)}; path=/; max-age=${days * 86400}; samesite=lax`;
  } catch {
    /* ignore */
  }
}

export function clearCookie(name: string): void {
  try {
    document.cookie = `${name}=; path=/; max-age=0`;
  } catch {
    /* ignore */
  }
}

export function getCookie(name: string): string | null {
  try {
    const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
    return match ? decodeURIComponent(match[1]) : null;
  } catch {
    return null;
  }
}
