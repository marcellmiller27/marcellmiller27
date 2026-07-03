"use client";
// JHI-SIG: 69M2705M | Research & Opportunity Score | John Henry Investments (proprietary)

import { useEffect, useState } from "react";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

type AssetScore = { symbol: string; opportunity_score: number };
type Snapshot = {
  as_of: string;
  score_definition: string;
  n_assets: number;
  scores: AssetScore[];
  status: string;
};

export function LiveOpportunities() {
  const [snap, setSnap] = useState<Snapshot | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    const pull = () =>
      fetch(`${API_BASE}/research/opportunity-scores`)
        .then((r) => {
          if (!r.ok) throw new Error(String(r.status));
          return r.json();
        })
        .then((data) => {
          if (!active) return;
          setSnap(data);
          setError("");
        })
        .catch(() => active && setError("Live opportunity scores are unavailable right now."));
    pull();
    const timer = setInterval(pull, 60000);
    return () => {
      active = false;
      clearInterval(timer);
    };
  }, []);

  if (error) {
    return (
      <p className="live-market__status">
        <span className="live-market__dot live-market__dot--off" />
        {error}
      </p>
    );
  }
  if (!snap) {
    return (
      <p className="live-market__status">
        <span className="live-market__dot" />
        Computing live opportunity scores…
      </p>
    );
  }

  const ranked = [...snap.scores].sort((a, b) => b.opportunity_score - a.opportunity_score);

  return (
    <div>
      <p className="live-market__status">
        <span className="live-market__dot" />
        Live · {snap.n_assets} assets scored from market data
      </p>
      <p style={{ color: "var(--muted, #9fb3c8)", fontSize: "0.9rem", marginTop: 0 }}>
        {snap.score_definition}
      </p>
      <div className="table-card">
        {ranked.map((row, index) => {
          const score = Math.round(row.opportunity_score);
          const bar = Math.max(0, Math.min(100, score));
          return (
            <article className="table-row" key={row.symbol}>
              <div>
                <span>#{index + 1}</span>
                <strong>{row.symbol}</strong>
              </div>
              <div style={{ flex: 1, margin: "0 1rem" }}>
                <div style={{ background: "rgba(255,255,255,0.08)", borderRadius: 6, height: 8 }}>
                  <div
                    style={{
                      width: `${bar}%`,
                      height: 8,
                      borderRadius: 6,
                      background: "var(--growth, #35c46b)"
                    }}
                  />
                </div>
              </div>
              <div className="score-badge">
                <strong>{score}</strong>
                <span>/ 100</span>
              </div>
            </article>
          );
        })}
      </div>
    </div>
  );
}
