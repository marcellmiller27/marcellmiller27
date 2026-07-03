"use client";
// JHI-SIG: 69M2705M | Identity, Auth & Security | John Henry Investments (proprietary)

import { useEffect, useState } from "react";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";
const TOKEN_KEY = "jhi_token";

type Me = {
  user: { email: string; full_name: string; is_active: boolean };
  organization: { name: string; slug: string };
  role: string;
  subscription: { plan: string; status: string; provider: string };
};

function fetchMe(tok: string): Promise<Me> {
  return fetch(`${API_BASE}/auth/me`, { headers: { Authorization: `Bearer ${tok}` } }).then((r) => {
    if (!r.ok) throw new Error(String(r.status));
    return r.json();
  });
}

export function LiveAccount() {
  const [me, setMe] = useState<Me | null>(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    let active = true;
    const stored = localStorage.getItem(TOKEN_KEY);
    if (!stored) return;
    fetchMe(stored)
      .then((data) => active && setMe(data))
      .catch(() => {
        localStorage.removeItem(TOKEN_KEY);
      });
    return () => {
      active = false;
    };
  }, []);

  const signIn = async (event: React.FormEvent) => {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim(), password })
      });
      if (!response.ok) throw new Error("Invalid email or password.");
      const data = await response.json();
      localStorage.setItem(TOKEN_KEY, data.access_token);
      setPassword("");
      setMe(await fetchMe(data.access_token));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Sign-in failed.");
    } finally {
      setBusy(false);
    }
  };

  const signOut = () => {
    localStorage.removeItem(TOKEN_KEY);
    setMe(null);
  };

  if (me) {
    return (
      <div>
        <p className="live-market__status">
          <span className="live-market__dot" />
          Signed in · live account
          <button
            type="button"
            onClick={signOut}
            style={{ marginLeft: "1rem", background: "none", border: "1px solid var(--border)", color: "inherit", borderRadius: 6, padding: "0.2rem 0.6rem", cursor: "pointer", font: "inherit" }}
          >
            Sign out
          </button>
        </p>
        <div className="app-grid app-grid--four">
          <article className="app-card">
            <span>User</span>
            <strong>{me.user.full_name}</strong>
            <p>{me.user.email}</p>
          </article>
          <article className="app-card">
            <span>Organization</span>
            <strong>{me.organization.name}</strong>
            <p>{me.organization.slug}</p>
          </article>
          <article className="app-card">
            <span>Role</span>
            <strong style={{ textTransform: "capitalize" }}>{me.role}</strong>
            <p>Access level for platform routes.</p>
          </article>
          <article className="app-card">
            <span>Subscription</span>
            <strong style={{ textTransform: "capitalize" }}>{me.subscription.plan}</strong>
            <p>
              Status: {me.subscription.status} · {me.subscription.provider}
            </p>
          </article>
        </div>
      </div>
    );
  }

  return (
    <div className="app-card" style={{ maxWidth: 420 }}>
      <span>Sign in</span>
      <strong>View your live account</strong>
      <p>Enter your credentials to load your live user, organization, role, and subscription.</p>
      <form onSubmit={signIn} className="support-form" style={{ flexDirection: "column", gap: "0.6rem", alignItems: "stretch" }}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          aria-label="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          aria-label="Password"
          required
        />
        <button type="submit" disabled={busy}>
          {busy ? "Signing in…" : "Sign in"}
        </button>
      </form>
      {error ? (
        <p className="live-market__status" style={{ marginTop: "0.6rem" }}>
          <span className="live-market__dot live-market__dot--off" />
          {error}
        </p>
      ) : null}
    </div>
  );
}
