// JHI-SIG: 69M2705M | Due-Diligence Framework | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api/v1";

type DDItem = { id: string; text: string; priority: string };
type DDCategory = { id: string; name: string; purpose: string; items: DDItem[] };
type Checklist = { categories: DDCategory[]; total_items: number; disclaimer: string };

export function DueDiligenceFramework() {
  const [data, setData] = useState<Checklist | null>(null);
  const [checked, setChecked] = useState<Record<string, boolean>>({});
  const [business, setBusiness] = useState("Target Co.");
  const [saved, setSaved] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/framework/due-diligence`)
      .then((r) => r.json())
      .then(setData)
      .catch(() => setData(null));
  }, []);

  const toggle = (id: string) => setChecked((p) => ({ ...p, [id]: !p[id] }));

  const doneCount = Object.values(checked).filter(Boolean).length;
  const total = data?.total_items ?? 0;

  const exportCsv = () => {
    if (!data) return;
    const rows = [["Category", "Priority", "Item", "Done"]];
    data.categories.forEach((c) =>
      c.items.forEach((it) => rows.push([c.name, it.priority, it.text, checked[it.id] ? "yes" : ""]))
    );
    const csv = rows.map((r) => r.map((v) => `"${v.replace(/"/g, '""')}"`).join(",")).join("\r\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `Aegira_due_diligence_${business.replace(/[^A-Za-z0-9]+/g, "_") || "target"}.csv`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  };

  const saveToPipeline = async () => {
    setError("");
    setSaved("");
    try {
      const resp = await fetch(`${API_BASE}/pipeline/deals`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          business_name: business || "Target Co.",
          deal_type: "due_diligence",
          stage: "screen",
          headline: `Due diligence — ${doneCount}/${total} items complete`,
          inputs: { checked }
        })
      });
      if (!resp.ok) throw new Error(`Save failed (${resp.status}).`);
      setSaved("Diligence deal created in Pipeline ✓");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Save failed.");
    }
  };

  if (!data) return <p className="live-market__muted">Loading checklist…</p>;

  return (
    <div>
      <div className="app-card" style={{ marginBottom: "1.5rem", display: "flex", gap: "0.8rem", alignItems: "flex-end", flexWrap: "wrap" }}>
        <label style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: "var(--fs-sm)", flex: "1 1 220px" }}>
          <span>Target business name</span>
          <input
            value={business}
            onChange={(e) => setBusiness(e.target.value)}
            style={{ padding: "0.5rem", borderRadius: 6, border: "1px solid var(--border)", background: "transparent", color: "inherit" }}
          />
        </label>
        <div style={{ fontWeight: 800, fontSize: "var(--fs-xl)" }}>
          {doneCount}/{total} complete
        </div>
        <button type="button" className="button button--secondary" onClick={exportCsv}>
          Export checklist (CSV)
        </button>
        <button type="button" className="button button--primary" onClick={saveToPipeline}>
          Start diligence deal in Pipeline
        </button>
        {saved ? <span style={{ color: "var(--growth)", fontWeight: 700 }}>{saved}</span> : null}
        {error ? <span style={{ color: "#e05a5a", fontWeight: 700 }}>{error}</span> : null}
      </div>

      {data.categories.map((c) => (
        <section className="app-section" key={c.id}>
          <div className="app-section__heading">
            <p className="eyebrow">{c.name}</p>
            <h2 style={{ fontSize: "var(--fs-lg)" }}>{c.purpose}</h2>
          </div>
          <div className="app-card">
            {c.items.map((it) => (
              <label
                key={it.id}
                style={{ display: "flex", gap: "0.6rem", alignItems: "flex-start", padding: "0.4rem 0", borderBottom: "1px solid var(--border)", cursor: "pointer" }}
              >
                <input type="checkbox" checked={!!checked[it.id]} onChange={() => toggle(it.id)} style={{ marginTop: "0.2rem" }} />
                <span style={{ textDecoration: checked[it.id] ? "line-through" : "none", opacity: checked[it.id] ? 0.6 : 1 }}>
                  {it.text}
                  {it.priority === "critical" ? (
                    <span className="tag" style={{ marginLeft: "0.5rem", fontSize: "var(--fs-xs, 0.7rem)", color: "#e05a5a", borderColor: "#e05a5a" }}>
                      critical
                    </span>
                  ) : null}
                </span>
              </label>
            ))}
          </div>
        </section>
      ))}

      <div className="upgrade-gate" style={{ marginTop: "1rem" }}>
        <p className="eyebrow">Accelerate diligence</p>
        <h3>Run the financial workstream at software speed</h3>
        <p>
          The financial items above are automated in the Earnings / QoE suite — proof-of-cash,
          add-back scrutiny, and the working-capital peg — then routed to a partner CPA when you
          need a signed report.
        </p>
        <div className="upgrade-gate__actions">
          <Link className="button button--primary" href="/diligence-suite">
            Open Earnings / QoE
          </Link>
          <Link className="button button--secondary" href="/pipeline">
            View Pipeline
          </Link>
        </div>
      </div>

      <p className="live-market__muted" style={{ fontSize: "var(--fs-sm)", marginTop: "0.8rem" }}>{data.disclaimer}</p>
    </div>
  );
}
