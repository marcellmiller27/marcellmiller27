"use client";

import { useEffect, useState } from "react";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api/v1";

const INTERESTS = [
  "Individual investor",
  "Financial advisor",
  "Family office",
  "Business buyer",
  "Other"
];

export function WaitlistForm({ source = "landing" }: { source?: string }) {
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [interest, setInterest] = useState(INTERESTS[0]);
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState("");
  const [error, setError] = useState("");
  const [count, setCount] = useState<number | null>(null);

  const refreshCount = () => {
    fetch(`${API_BASE}/leads/count`)
      .then((r) => r.json())
      .then((d) => setCount(d.count ?? null))
      .catch(() => setCount(null));
  };

  useEffect(refreshCount, []);

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!email.trim() || busy) return;
    setBusy(true);
    setError("");
    try {
      const response = await fetch(`${API_BASE}/leads`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, full_name: fullName, interest, source })
      });
      const data = await response.json();
      if (!response.ok) {
        setError(data?.detail ?? "Something went wrong. Please try again.");
      } else {
        setDone(data.message);
        refreshCount();
      }
    } catch {
      setError("Couldn't reach the server. Please try again.");
    } finally {
      setBusy(false);
    }
  };

  if (done) {
    return (
      <div className="waitlist waitlist--done">
        <strong>✓ {done}</strong>
        {count !== null ? (
          <p>You&rsquo;re one of {count.toLocaleString()} on the list.</p>
        ) : null}
      </div>
    );
  }

  return (
    <form className="waitlist" onSubmit={submit}>
      <div className="waitlist__row">
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
          aria-label="Email"
        />
        <button className="button button--primary" type="submit" disabled={busy || !email.trim()}>
          {busy ? "Joining…" : "Join the waitlist"}
        </button>
      </div>
      <div className="waitlist__row">
        <input
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          placeholder="Full name (optional)"
          aria-label="Full name"
        />
        <select value={interest} onChange={(e) => setInterest(e.target.value)} aria-label="I am a">
          {INTERESTS.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      </div>
      {error ? <p className="waitlist__error">{error}</p> : null}
      <p className="waitlist__note">
        {count !== null && count > 0
          ? `Join ${count.toLocaleString()} others getting early access. No spam.`
          : "Be first to get early access. No spam."}
      </p>
    </form>
  );
}
