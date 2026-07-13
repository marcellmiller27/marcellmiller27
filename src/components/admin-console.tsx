"use client";
// JHI-SIG: 69M2705M | Admin console (Gatekeeper P0) | John Henry Investments (proprietary)

import { useCallback, useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";
const TOKEN_KEY = "jhi_token";

const ROLES = [
  "admin",
  "investor",
  "advisor",
  "cpa",
  "attorney",
  "banker",
  "family_office",
  "enterprise"
];

type Overview = {
  total_users: number;
  active_users: number;
  admins: number;
  organizations: number;
  two_factor_enabled: number;
  recent_admin_actions: number;
  enforce_auth: boolean;
};
type AdminUser = {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  role: string;
  organization_name: string | null;
  two_factor_enabled: boolean;
};
type RoleEntry = { role: string; permissions: string[]; is_super_admin: boolean };
type AuditEntry = {
  id: string;
  actor_user_id: string | null;
  action: string;
  resource_type: string;
  resource_id: string | null;
  created_at: string;
};

const cell = { padding: "0.5rem 0.7rem", borderBottom: "1px solid var(--border)", fontSize: "0.85rem" } as const;
const head = { ...cell, textAlign: "left" as const, color: "var(--muted)", fontWeight: 800, fontSize: "0.72rem", textTransform: "uppercase" as const };
const btn = { padding: "0.3rem 0.6rem", borderRadius: "7px", border: "1px solid var(--border)", background: "transparent", cursor: "pointer", fontSize: "0.78rem", fontWeight: 700 } as const;

export function AdminConsole() {
  const [token, setToken] = useState<string | null>(null);
  const [overview, setOverview] = useState<Overview | null>(null);
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [roles, setRoles] = useState<RoleEntry[]>([]);
  const [audit, setAudit] = useState<AuditEntry[]>([]);
  const [forbidden, setForbidden] = useState(false);
  const [error, setError] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [ready, setReady] = useState(false);

  const authHeader = useCallback(
    (t: string) => ({ Authorization: `Bearer ${t}`, "Content-Type": "application/json" }),
    []
  );

  const load = useCallback(
    (t: string) =>
      Promise.all([
        fetch(`${API_BASE}/admin/overview`, { headers: authHeader(t) }),
        fetch(`${API_BASE}/admin/users`, { headers: authHeader(t) }),
        fetch(`${API_BASE}/admin/roles`, { headers: authHeader(t) }),
        fetch(`${API_BASE}/admin/audit-logs`, { headers: authHeader(t) })
      ]).then(async ([o, u, r, a]) => {
        if (o.status === 403) {
          setForbidden(true);
          return;
        }
        if (!o.ok) throw new Error("load failed");
        setForbidden(false);
        setOverview(await o.json());
        setUsers(await u.json());
        setRoles(await r.json());
        setAudit(await a.json());
      }),
    [authHeader]
  );

  useEffect(() => {
    const t = typeof window !== "undefined" ? localStorage.getItem(TOKEN_KEY) : null;
    Promise.resolve().then(() => {
      setToken(t);
      if (t) {
        load(t)
          .catch(() => setError("Could not load admin data."))
          .finally(() => setReady(true));
      } else {
        setReady(true);
      }
    });
  }, [load]);

  async function signIn(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      if (!res.ok) {
        setError("Invalid email or password.");
        return;
      }
      const body = await res.json();
      localStorage.setItem(TOKEN_KEY, body.access_token);
      setToken(body.access_token);
      await load(body.access_token);
    } catch {
      setError("Could not reach the API.");
    }
  }

  function signOut() {
    localStorage.removeItem(TOKEN_KEY);
    setToken(null);
    setOverview(null);
    setUsers([]);
    setForbidden(false);
  }

  const act = useCallback(
    async (url: string, method: string, body?: object) => {
      if (!token) return;
      const res = await fetch(`${API_BASE}${url}`, {
        method,
        headers: authHeader(token),
        body: body ? JSON.stringify(body) : undefined
      });
      if (!res.ok) {
        const d = await res.json().catch(() => ({}));
        setError(d.detail ?? "Action failed.");
        return;
      }
      setError("");
      await load(token);
    },
    [token, authHeader, load]
  );

  if (!ready) return <p className="live-market__muted">Loading…</p>;

  if (!token) {
    return (
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Restricted</p>
          <h2>Admin sign-in</h2>
        </div>
        <article className="app-card" style={{ maxWidth: 420 }}>
          <form onSubmit={signIn} style={{ display: "flex", flexDirection: "column", gap: "0.6rem" }}>
            <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required style={{ padding: "0.5rem", borderRadius: 8, border: "1px solid var(--border)" }} />
            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required style={{ padding: "0.5rem", borderRadius: 8, border: "1px solid var(--border)" }} />
            <button type="submit" style={{ ...btn, background: "var(--growth, #1f7a4d)", color: "#fff", border: "none", padding: "0.55rem" }}>Sign in</button>
            {error ? <p style={{ color: "#c0392b", fontSize: "0.85rem" }}>{error}</p> : null}
          </form>
        </article>
      </section>
    );
  }

  if (forbidden) {
    return (
      <section className="app-section">
        <article className="app-card">
          <strong>Admin access required.</strong>
          <p style={{ color: "var(--muted)" }}>Your account does not have the <code>admin:access</code> permission.</p>
          <button type="button" onClick={signOut} style={btn}>Sign out</button>
        </article>
      </section>
    );
  }

  return (
    <div>
      <section className="app-section">
        <div className="app-section__heading" style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", flexWrap: "wrap", gap: "0.5rem" }}>
          <div>
            <p className="eyebrow">Control plane</p>
            <h2>Overview</h2>
          </div>
          <button type="button" onClick={signOut} style={btn}>Sign out</button>
        </div>
        {overview ? (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))", gap: "0.8rem" }}>
            {[
              ["Users", overview.total_users],
              ["Active", overview.active_users],
              ["Admins", overview.admins],
              ["Organizations", overview.organizations],
              ["MFA enabled", overview.two_factor_enabled],
              ["Admin actions", overview.recent_admin_actions]
            ].map(([label, val]) => (
              <article className="app-card" key={String(label)}>
                <span style={{ color: "var(--muted)", fontSize: "0.72rem", fontWeight: 800, textTransform: "uppercase" }}>{label}</span>
                <strong style={{ display: "block", fontSize: "1.6rem" }}>{val}</strong>
              </article>
            ))}
          </div>
        ) : null}
        <p style={{ marginTop: "0.6rem", fontSize: "0.82rem", color: overview?.enforce_auth ? "var(--growth)" : "var(--muted)" }}>
          Endpoint enforcement (<code>ENFORCE_AUTH</code>): <strong>{overview?.enforce_auth ? "ON" : "OFF (demo)"}</strong>
        </p>
        {error ? <p style={{ color: "#c0392b", fontSize: "0.85rem" }}>{error}</p> : null}
      </section>

      <section className="app-section">
        <div className="app-section__heading"><p className="eyebrow">Identity</p><h2>Users</h2></div>
        <article className="app-card" style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th style={head}>User</th><th style={head}>Role</th><th style={head}>MFA</th><th style={head}>Status</th><th style={head}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id}>
                  <td style={cell}><strong style={{ display: "block" }}>{u.full_name}</strong><span style={{ color: "var(--muted)", fontSize: "0.78rem" }}>{u.email}</span></td>
                  <td style={cell}>
                    <select value={u.role} onChange={(e) => act(`/admin/users/${u.id}/role`, "PATCH", { role: e.target.value })} style={{ padding: "0.25rem", borderRadius: 6, border: "1px solid var(--border)" }}>
                      {ROLES.map((r) => <option key={r} value={r}>{r}</option>)}
                    </select>
                  </td>
                  <td style={cell}>{u.two_factor_enabled ? "✓" : "—"}</td>
                  <td style={cell}><span style={{ color: u.is_active ? "var(--growth)" : "#c0392b", fontWeight: 700 }}>{u.is_active ? "Active" : "Inactive"}</span></td>
                  <td style={{ ...cell, whiteSpace: "nowrap" }}>
                    <button type="button" style={btn} onClick={() => act(`/admin/users/${u.id}/active`, "PATCH", { is_active: !u.is_active })}>{u.is_active ? "Deactivate" : "Reactivate"}</button>{" "}
                    <button type="button" style={btn} onClick={() => act(`/admin/users/${u.id}/reset-mfa`, "POST")}>Reset MFA</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </article>
      </section>

      <section className="app-section">
        <div className="app-section__heading"><p className="eyebrow">Access control</p><h2>Roles &amp; permissions</h2></div>
        <article className="app-card" style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead><tr><th style={head}>Role</th><th style={head}>Permissions</th></tr></thead>
            <tbody>
              {roles.map((r) => (
                <tr key={r.role}>
                  <td style={cell}><strong>{r.role}</strong>{r.is_super_admin ? <span style={{ color: "var(--gold, #9a6b12)", fontSize: "0.7rem", fontWeight: 800 }}> · SUPER-ADMIN</span> : null}</td>
                  <td style={{ ...cell, fontSize: "0.78rem", color: "var(--muted)" }}>{r.permissions.join(" · ")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </article>
      </section>

      <section className="app-section">
        <div className="app-section__heading"><p className="eyebrow">Audit</p><h2>Recent activity</h2></div>
        <article className="app-card" style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead><tr><th style={head}>When</th><th style={head}>Action</th><th style={head}>Resource</th></tr></thead>
            <tbody>
              {audit.slice(0, 40).map((a) => (
                <tr key={a.id}>
                  <td style={{ ...cell, whiteSpace: "nowrap", color: "var(--muted)", fontSize: "0.78rem" }}>{a.created_at.replace("T", " ").slice(0, 19)}</td>
                  <td style={cell}>{a.action}</td>
                  <td style={{ ...cell, color: "var(--muted)", fontSize: "0.78rem" }}>{a.resource_type}{a.resource_id ? ` · ${a.resource_id.slice(0, 8)}` : ""}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </article>
      </section>
    </div>
  );
}
