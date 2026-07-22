// JHI-SIG: 69M2705M | Role preview switcher (temporary demo control) | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { useRole } from "@/components/role-provider";
import { ROLE_OPTIONS, type Role } from "@/lib/roles";

// TEMPORARY demo control so access tiers can be previewed before real sign-in / RBAC.
// Remove (or gate to staff) once server-side auth drives the role.
export function RolePreviewSwitcher() {
  const { role, setRole } = useRole();
  return (
    <label
      className="role-switcher"
      title="Preview the platform as a given access tier (temporary — until real sign-in / RBAC)"
    >
      <span>Preview</span>
      <select value={role} onChange={(e) => setRole(e.target.value as Role)} aria-label="Preview access tier">
        {ROLE_OPTIONS.map((o) => (
          <option key={o.id} value={o.id}>
            {o.label}
          </option>
        ))}
      </select>
    </label>
  );
}
