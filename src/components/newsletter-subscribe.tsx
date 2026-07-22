// JHI-SIG: 69M2705M | Newsletter subscribe opt-in (Step B) | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api/v1";

type Status = "idle" | "sending" | "ok" | "error";

export function NewsletterSubscribe() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [msg, setMsg] = useState("");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("sending");
    try {
      const r = await fetch(`${API_BASE}/leads`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          full_name: "",
          interest: "Newsletter",
          source: "newsletter-subscribe"
        })
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      setStatus("ok");
      setMsg("You're on the list. Editions will be emailed once delivery is enabled.");
      setEmail("");
    } catch {
      setStatus("error");
      setMsg("Couldn't subscribe right now — please try again shortly.");
    }
  }

  return (
    <form className="news-subscribe" onSubmit={submit}>
      <div>
        <p className="eyebrow">Subscribe</p>
        <h3>Get the editions by email</h3>
        <p className="news-subscribe__blurb">
          The Economic Brief, Red Alerts, and Opportunity Scans — delivered as they publish.
        </p>
      </div>
      <div className="news-subscribe__row">
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@firm.com"
          aria-label="Email address"
          className="dir-search"
        />
        <button type="submit" className="button button--primary" disabled={status === "sending"}>
          {status === "sending" ? "Subscribing…" : "Subscribe"}
        </button>
      </div>
      {status === "ok" && <p className="news-subscribe__ok">{msg}</p>}
      {status === "error" && <p className="news-subscribe__err">{msg}</p>}
    </form>
  );
}
