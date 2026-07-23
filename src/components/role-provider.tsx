// JHI-SIG: 69M2705M | Role context (derived from real auth) | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import type { Role } from "@/lib/roles";
import { FREE_COOKIE, getCookie, TOKEN_COOKIE } from "@/lib/auth";
import { apiFetch } from "@/lib/api";

// The presentation role is DERIVED from real auth state:
//   auth token cookie  → subscriber (product + full newsletters)
//   free cookie only   → free (newsletter teaser only)
//   neither            → public
// Server-side route enforcement lives in src/middleware.ts. (A distinct "staff"
// tier for Accounting/admin needs a real backend staff role — see feedback.)
type Ctx = { role: Role; setRole: (r: Role) => void };

const RoleContext = createContext<Ctx>({ role: "public", setRole: () => {} });

function deriveRole(): Role {
  if (getCookie(TOKEN_COOKIE)) return "subscriber";
  if (getCookie(FREE_COOKIE)) return "free";
  return "public";
}

export function RoleProvider({ children }: { children: ReactNode }) {
  const [role, setRoleState] = useState<Role>("public");

  useEffect(() => {
    let active = true;
    // Derive from cookies after mount (client-only; avoids SSR/hydration mismatch).
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setRoleState(deriveRole());
    // If authenticated, confirm real role/staff status from the backend (source of truth).
    if (getCookie(TOKEN_COOKIE)) {
      apiFetch("/auth/me")
        .then((r) => (r.ok ? r.json() : null))
        .then((d) => {
          if (active && d?.is_staff) setRoleState("staff");
        })
        .catch(() => {
          /* keep derived role */
        });
    }
    return () => {
      active = false;
    };
  }, []);

  return <RoleContext.Provider value={{ role, setRole: setRoleState }}>{children}</RoleContext.Provider>;
}

export function useRole() {
  return useContext(RoleContext);
}
