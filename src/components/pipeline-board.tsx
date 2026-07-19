"use client";
// JHI-SIG: 69M2705M | Deal Pipeline | JHI Research & Analytics Firm, Inc. (proprietary)

import { useEffect, useState } from "react";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

type Deal = {
  id: string;
  business_name: string;
  deal_type: string;
  stage: string;
  score: number | null;
  recommendation: string;
  headline: string;
  notes: string;
  updated_at: string;
};

const STAGE_LABELS: Record<string, string> = {
  screen: "Screen",
  analysis: "Analysis (BQA)",
  qoe: "Quality of Earnings",
  financing: "Financing",
  offer: "Offer",
  closed: "Closed",
  passed: "Passed"
};

export function PipelineBoard() {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [stages, setStages] = useState<string[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const load = async () => {
    try {
      const [dRes, sRes] = await Promise.all([
        fetch(`${API_BASE}/pipeline/deals`),
        fetch(`${API_BASE}/pipeline/stages`)
      ]);
      if (!dRes.ok || !sRes.ok) throw new Error("Failed to load pipeline.");
      setDeals(await dRes.json());
      setStages(await sRes.json());
      setError("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load pipeline.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let active = true;
    Promise.all([
      fetch(`${API_BASE}/pipeline/deals`).then((r) => (r.ok ? r.json() : Promise.reject(r))),
      fetch(`${API_BASE}/pipeline/stages`).then((r) => (r.ok ? r.json() : Promise.reject(r)))
    ])
      .then(([d, s]) => {
        if (!active) return;
        setDeals(d);
        setStages(s);
        setError("");
        setLoading(false);
      })
      .catch(() => {
        if (!active) return;
        setError("Failed to load pipeline.");
        setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  const move = async (id: string, stage: string) => {
    try {
      const resp = await fetch(`${API_BASE}/pipeline/deals/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ stage })
      });
      if (!resp.ok) throw new Error("Update failed.");
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Update failed.");
    }
  };

  const remove = async (id: string) => {
    try {
      const resp = await fetch(`${API_BASE}/pipeline/deals/${id}`, { method: "DELETE" });
      if (!resp.ok) throw new Error("Delete failed.");
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Delete failed.");
    }
  };

  if (loading) {
    return <p className="live-market__muted">Loading pipeline…</p>;
  }

  return (
    <div>
      {error ? (
        <p className="live-market__status">
          <span className="live-market__dot live-market__dot--off" />
          {error}
        </p>
      ) : null}

      {deals.length === 0 ? (
        <article className="app-card">
          <span>No saved deals yet</span>
          <p>
            Run an analysis in <strong>Deal X-Ray</strong> or <strong>Quality of Earnings</strong>{" "}
            and click <strong>Save to Pipeline</strong> to track targets through your acquisition
            workflow.
          </p>
        </article>
      ) : (
        <div className="app-grid app-grid--three">
          {stages
            .filter((stage) => deals.some((d) => d.stage === stage))
            .map((stage) => (
              <div key={stage}>
                <div className="app-section__heading">
                  <p className="eyebrow">{STAGE_LABELS[stage] ?? stage}</p>
                </div>
                {deals
                  .filter((d) => d.stage === stage)
                  .map((d) => (
                    <article className="app-card" key={d.id} style={{ marginBottom: "0.8rem" }}>
                      <span>{d.deal_type === "qoe" ? "Quality of Earnings" : "Deal X-Ray (BQA)"}</span>
                      <strong>{d.business_name}</strong>
                      <p style={{ fontSize: "0.82rem", opacity: 0.85 }}>
                        {d.score != null ? `Score ${d.score} · ` : ""}
                        {d.recommendation}
                      </p>
                      {d.headline ? (
                        <p style={{ fontSize: "0.76rem", opacity: 0.7 }}>{d.headline}</p>
                      ) : null}
                      <div style={{ display: "flex", gap: "0.4rem", marginTop: "0.6rem", flexWrap: "wrap" }}>
                        <select
                          value={d.stage}
                          onChange={(e) => move(d.id, e.target.value)}
                          style={{ padding: "0.35rem", borderRadius: 6, border: "1px solid var(--border)", background: "transparent", color: "inherit", fontSize: "0.78rem" }}
                        >
                          {stages.map((s) => (
                            <option key={s} value={s}>
                              {STAGE_LABELS[s] ?? s}
                            </option>
                          ))}
                        </select>
                        <button
                          type="button"
                          className="button button--secondary"
                          style={{ fontSize: "0.75rem", padding: "0.3rem 0.6rem" }}
                          onClick={() => remove(d.id)}
                        >
                          Remove
                        </button>
                      </div>
                    </article>
                  ))}
              </div>
            ))}
        </div>
      )}
    </div>
  );
}
