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
      eyebrow="Our AI team"
      title="Meet the John Henry Investments customer-service team"
      description="Five specialized AI agents support every member 24/7 — onboarding, subscriptions, account security, product guidance, and technical triage that escalates to the founder."
    >
      <section className="team-grid">
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
      </section>
    </PlatformShell>
  );
}
