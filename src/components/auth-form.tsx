// JHI-SIG: 69M2705M | Auth form (real login / register) | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useRole } from "@/components/role-provider";
import { setCookie, TOKEN_COOKIE } from "@/lib/auth";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api/v1";

type Mode = "login" | "register";

export function AuthForm({ mode }: { mode: Mode }) {
  const router = useRouter();
  const { setRole } = useRole();
  const [form, setForm] = useState({
    email: "",
    password: "",
    full_name: "",
    organization_name: "",
    plan: "consumer"
  });
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");

  const set = (k: string, v: string) => setForm((f) => ({ ...f, [k]: v }));

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setErr("");
    try {
      const path = mode === "login" ? "/auth/login" : "/auth/register";
      const body =
        mode === "login"
          ? { email: form.email, password: form.password }
          : {
              organization_name: form.organization_name,
              full_name: form.full_name,
              email: form.email,
              password: form.password,
              plan: form.plan
            };
      const r = await fetch(`${API_BASE}${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
      if (!r.ok) {
        const d = await r.json().catch(() => ({}));
        const detail = typeof d.detail === "string" ? d.detail : `Request failed (${r.status})`;
        throw new Error(detail);
      }
      const d = await r.json();
      if (!d.access_token) throw new Error("No token returned.");
      setCookie(TOKEN_COOKIE, d.access_token);
      // Any authenticated customer maps to the subscriber tier. A dedicated JHI
      // "staff" tier (for Accounting/admin) requires a real backend staff role.
      setRole("subscriber");
      const next = new URLSearchParams(window.location.search).get("next") || "/dashboard";
      router.push(next);
      router.refresh();
    } catch (e) {
      setErr(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <form className="auth-form" onSubmit={submit}>
      {mode === "register" && (
        <>
          <label>
            <span>Organization</span>
            <input required value={form.organization_name} onChange={(e) => set("organization_name", e.target.value)} placeholder="Your firm or workspace" />
          </label>
          <label>
            <span>Full name</span>
            <input required value={form.full_name} onChange={(e) => set("full_name", e.target.value)} placeholder="Jane Investor" />
          </label>
        </>
      )}
      <label>
        <span>Email</span>
        <input type="email" required value={form.email} onChange={(e) => set("email", e.target.value)} placeholder="you@firm.com" />
      </label>
      <label>
        <span>Password</span>
        <input type="password" required minLength={8} value={form.password} onChange={(e) => set("password", e.target.value)} placeholder="At least 8 characters" />
      </label>
      {mode === "register" && (
        <label>
          <span>Plan</span>
          <select value={form.plan} onChange={(e) => set("plan", e.target.value)}>
            <option value="consumer">Consumer (Tier 3)</option>
            <option value="professional">Professional (Tier 2)</option>
            <option value="enterprise">Enterprise (Tier 1)</option>
          </select>
        </label>
      )}
      {err && <p className="auth-form__err">{err}</p>}
      <button type="submit" className="button button--primary" disabled={busy}>
        {busy ? "Please wait…" : mode === "login" ? "Sign in" : "Create account"}
      </button>
    </form>
  );
}
