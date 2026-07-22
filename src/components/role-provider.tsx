// JHI-SIG: 69M2705M | Role context (presentation layer) | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import type { Role } from "@/lib/roles";

// Presentation-layer role. Persisted in localStorage so the "preview role" survives
// navigation. Replaced by the real signed-in role (from the auth token) once RBAC lands.
const KEY = "jhi-preview-role";

type Ctx = { role: Role; setRole: (r: Role) => void };

const RoleContext = createContext<Ctx>({ role: "subscriber", setRole: () => {} });

function isRole(v: string | null): v is Role {
  return v === "public" || v === "free" || v === "subscriber" || v === "staff";
}

export function RoleProvider({ children }: { children: ReactNode }) {
  const [role, setRoleState] = useState<Role>("subscriber");

  useEffect(() => {
    try {
      const s = window.localStorage.getItem(KEY);
      // Hydrate the persisted preview role after mount (client-only; avoids SSR/window).
      // eslint-disable-next-line react-hooks/set-state-in-effect
      if (isRole(s)) setRoleState(s);
    } catch {
      /* ignore */
    }
  }, []);

  const setRole = (r: Role) => {
    setRoleState(r);
    try {
      window.localStorage.setItem(KEY, r);
    } catch {
      /* ignore */
    }
  };

  return <RoleContext.Provider value={{ role, setRole }}>{children}</RoleContext.Provider>;
}

export function useRole() {
  return useContext(RoleContext);
}
