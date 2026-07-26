// JHI-SIG: 69M2705M | Authenticated API fetch | JHI Research & Analytics Firm, Inc. (proprietary)
// Same-origin API client that forwards the auth token (from the jhi_token cookie) as a
// Bearer header, so RBAC-protected backend endpoints receive the caller's identity.
import { getCookie, TOKEN_COOKIE } from "@/lib/auth";

export const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api/v1";

export function apiFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const headers = new Headers(init.headers);
  const token = getCookie(TOKEN_COOKIE);
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const url = path.startsWith("http")
    ? path
    : `${API_BASE}${path.startsWith("/") ? "" : "/"}${path}`;
  return fetch(url, { ...init, headers });
}
