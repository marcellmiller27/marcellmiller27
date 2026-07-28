// JHI-SIG: 69M2705M | Full-team showcase (leadership + AI agents) | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api/v1";

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

type Leader = {
  photo: string;
  fallback: string;
  role: string;
  name: string;
  persona: string;
  tags: string[];
  background: string;
  pill: string;
};

const leadership: Leader[] = [
  {
    photo: "/team/vp-software-engineer.png",
    fallback: "CY",
    role: "VP of Software Engineering",
    name: "Cy Henry",
    persona: "The founder's AI build partner — designs, ships, tests, and documents the platform.",
    tags: ["Full-stack engineering", "Architecture & security", "Testing & QA", "Docs & board minutes"],
    background:
      "Cy leads Aegira's AI engineering department — building and hardening the platform end-to-end " +
      "(frontend, backend, data, and developer experience), running tests, and keeping the board minutes " +
      "with the founder. Cy works under human direction; every change is reviewed and shipped as a pull request.",
    pill: "Human-directed · shipped via pull request"
  },
  {
    photo: "/team/vp-editorial.png",
    fallback: "EV",
    role: "VP of Editorial",
    name: "Ellery Vance",
    persona:
      "The firm's AI editorial lead — authors every newsletter, insider brief, and red alert, with depth across all asset classes.",
    tags: ["Newsletters & updates", "Insider briefs", "Red alerts", "Cross-asset opportunities", "Depth research"],
    background:
      "Ellery leads Aegira's editorial desk — turning the data the platform polls into published intelligence: " +
      "recurring updates, deep-dive insider briefs, time-sensitive red alerts, and opportunity scans that surface " +
      "unforeseen ideas across equities, credit, real assets, private markets, and digital assets. Written in " +
      "Aegira's independent professional perspective; human-directed and published via review.",
    pill: "Human-directed · published via review"
  }
];

function LeaderCard({ leader }: { leader: Leader }) {
  const [photoOk, setPhotoOk] = useState(true);
  return (
    <article className="team-card">
      {photoOk ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          className="team-card__photo"
          src={leader.photo}
          alt={`${leader.name}, ${leader.role}`}
          onError={() => setPhotoOk(false)}
        />
      ) : (
        <div
          className="team-card__photo"
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            background: "linear-gradient(135deg, #0c1f33, #1a3a5c)",
            color: "#e3b765",
            fontSize: "3.5rem",
            fontWeight: 900,
            letterSpacing: "0.12em"
          }}
        >
          {leader.fallback}
        </div>
      )}
      <div className="team-card__body">
        <span className="team-card__role">{leader.role}</span>
        <h3 className="team-card__name">{leader.name}</h3>
        <p className="team-card__persona">{leader.persona}</p>
        <div className="output-tags">
          {leader.tags.map((tag) => (
            <span className="tag" key={tag}>
              {tag}
            </span>
          ))}
        </div>
        <p className="team-card__bg">{leader.background}</p>
        <span className="m-pill m-pill--on">{leader.pill}</span>
      </div>
    </article>
  );
}

export function TeamShowcase() {
  const [agents, setAgents] = useState<Agent[]>([]);

  useEffect(() => {
    let active = true;
    fetch(`${API_BASE}/agents`)
      .then((r) => r.json())
      .then((d) => active && setAgents(d.agents ?? []))
      .catch(() => active && setAgents([]));
    return () => {
      active = false;
    };
  }, []);

  return (
    <>
      <p className="eyebrow" style={{ marginTop: "0.5rem" }}>
        Leadership
      </p>
      <div className="team-grid">
        {leadership.map((leader) => (
          <LeaderCard key={leader.name} leader={leader} />
        ))}
      </div>

      <p className="eyebrow" style={{ marginTop: "2rem" }}>
        AI support agents — 24/7
      </p>
      <div className="team-grid">
        {agents.map((agent) => (
          <article className="team-card" key={agent.key}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img className="team-card__photo" src={agent.avatar} alt={`${agent.name}, ${agent.role}`} />
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
              {agent.escalates ? <span className="m-pill m-pill--on">Escalates to founder</span> : null}
            </div>
          </article>
        ))}
        {agents.length === 0 ? <p className="rec-empty">Loading the team…</p> : null}
      </div>
    </>
  );
}
