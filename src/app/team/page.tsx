"use client";

import { useEffect, useState } from "react";
import { PlatformShell } from "@/components/platform-shell";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

type Agent = {
  key: string;
  name: string;
  role: string;
  persona: string;
  expertise: string[];
  background: string;
  avatar: string;
  escalates: boolean;
};

const monogramStyle = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  background: "linear-gradient(135deg, #0c1f33, #1a3a5c)",
  color: "#e3b765",
  fontSize: "5rem",
  fontWeight: 900,
  letterSpacing: "0.12em"
} as const;

export default function TeamPage() {
  const [agents, setAgents] = useState<Agent[]>([]);

  useEffect(() => {
    fetch(`${API_BASE}/agents`)
      .then((r) => r.json())
      .then((d) => setAgents(d.agents ?? []))
      .catch(() => setAgents([]));
  }, []);

  return (
    <PlatformShell
      eyebrow="Our team"
      title="Meet the John Henry Investments team"
      description="An AI engineering teammate builds and maintains the platform, and five specialized AI agents support every member 24/7 — onboarding, subscriptions, account security, product guidance, and technical triage that escalates to the founder."
    >
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Platform engineering</p>
          <h2>Who builds &amp; maintains the platform</h2>
        </div>
        <div className="team-grid">
          <article className="team-card">
            <div className="team-card__photo" style={monogramStyle}>
              CY
            </div>
            <div className="team-card__body">
              <span className="team-card__role">VP, Software Engineering · AI Teammate</span>
              <h3 className="team-card__name">Cy Henry</h3>
              <p className="team-card__persona">
                The founder&apos;s AI build partner — designs, ships, tests, and documents the platform.
              </p>
              <div className="output-tags">
                {["Full-stack engineering", "Architecture & security", "Testing & QA", "Docs & board minutes"].map(
                  (tag) => (
                    <span className="tag" key={tag}>
                      {tag}
                    </span>
                  )
                )}
              </div>
              <p className="team-card__bg">
                Cy is JHI&apos;s AI software-engineering teammate — building and hardening the platform
                end-to-end (frontend, backend, data, and developer experience), running tests, and
                keeping the board minutes with the founder. Cy works under human direction; every change
                is reviewed and shipped as a pull request.
              </p>
              <span className="m-pill m-pill--on">Human-directed · shipped via pull request</span>
            </div>
          </article>
        </div>
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Customer-service team</p>
          <h2>Five specialized AI support agents</h2>
        </div>
        <div className="team-grid">
          {agents.map((agent) => (
            <article className="team-card" key={agent.key}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img className="team-card__photo" src={agent.avatar} alt={agent.name} />
              <div className="team-card__body">
                <span className="team-card__role">{agent.role}</span>
                <h3 className="team-card__name">{agent.name}</h3>
                <p className="team-card__persona">{agent.persona}</p>
                <div className="output-tags">
                  {agent.expertise.map((tag) => (
                    <span className="tag" key={tag}>
                      {tag}
                    </span>
                  ))}
                </div>
                <p className="team-card__bg">{agent.background}</p>
                {agent.escalates ? (
                  <span className="m-pill m-pill--on">Escalates to founder</span>
                ) : null}
              </div>
            </article>
          ))}
          {agents.length === 0 ? <p>Loading the team…</p> : null}
        </div>
      </section>
    </PlatformShell>
  );
}
