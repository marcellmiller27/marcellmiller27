// JHI-SIG: 69M2705M | Access tiers (presentation layer) | JHI Research & Analytics Firm, Inc. (proprietary)
// NOTE: This is the PRESENTATION layer only — it drives what the UI shows. It is NOT
// security. True enforcement (blocking API/route access) lands with server-side RBAC
// (the Gatekeeper / Phase 6). Until then, menu-hiding + content gating are UX, not a
// security boundary.

export type Role = "public" | "free" | "subscriber" | "staff";

// Minimum tier required to see a thing.
export type AccessLevel = "public" | "free" | "subscriber" | "staff";

const RANK: Record<Role, number> = { public: 0, free: 1, subscriber: 2, staff: 3 };

export function meetsAccess(role: Role, level: AccessLevel): boolean {
  return RANK[role] >= RANK[level];
}

// Free-newsletter registrants get a teaser; subscribers and staff get the full edition.
export function canFullNewsletter(role: Role): boolean {
  return RANK[role] >= RANK["subscriber"];
}

export const ROLE_OPTIONS: { id: Role; label: string }[] = [
  { id: "public", label: "Public (not signed in)" },
  { id: "free", label: "Free newsletter" },
  { id: "subscriber", label: "Subscriber (Tier 1–3)" },
  { id: "staff", label: "Founder / employee" }
];
