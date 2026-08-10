// JHI-SIG: 69M2705M | Market Analysis Template | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api/v1";

type Section = { id: string; name: string; guidance: string; prompts: string[] };
type Field = { key: string; label: string; hint: string };
type Template = {
  sections: Section[];
  tam_worksheet: Field[];
  five_forces: string[];
  disclaimer: string;
};

function money(n: number): string {
  if (!isFinite(n) || n <= 0) return "—";
  return `$${Math.round(n).toLocaleString("en-US")}`;
}

export function MarketAnalysis() {
  const [data, setData] = useState<Template | null>(null);
  const [w, setW] = useState<Record<string, number>>({
    total_customers: 50000,
    avg_annual_spend: 5000,
    serviceable_pct: 20,
    obtainable_pct: 5
  });

  useEffect(() => {
    fetch(`${API_BASE}/framework/market-analysis`)
      .then((r) => r.json())
      .then(setData)
      .catch(() => setData(null));
  }, []);

  const { tam, sam, som } = useMemo(() => {
    const t = (w.total_customers || 0) * (w.avg_annual_spend || 0);
    const s = t * ((w.serviceable_pct || 0) / 100);
    const o = s * ((w.obtainable_pct || 0) / 100);
    return { tam: t, sam: s, som: o };
  }, [w]);

  if (!data) return <p className="live-market__muted">Loading template…</p>;

  return (
    <div>
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Sizing worksheet</p>
          <h2>TAM / SAM / SOM</h2>
        </div>
        <div className="app-card" style={{ marginBottom: "1rem" }}>
          <div className="app-grid app-grid--two" style={{ gap: "0.8rem" }}>
            {data.tam_worksheet.map((f) => (
              <label key={f.key} style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: "var(--fs-sm)" }}>
                <span>{f.label}</span>
                <input
                  type="number"
                  value={w[f.key] ?? ""}
                  onChange={(e) => setW((p) => ({ ...p, [f.key]: Number(e.target.value) }))}
                  style={{ padding: "0.5rem", borderRadius: 6, border: "1px solid var(--border)", background: "transparent", color: "inherit" }}
                />
                <span className="live-market__muted" style={{ fontSize: "var(--fs-xs, 0.72rem)" }}>{f.hint}</span>
              </label>
            ))}
          </div>
        </div>
        <div className="app-grid app-grid--three">
          <article className="app-card">
            <span>TAM — total addressable</span>
            <strong style={{ fontSize: "var(--fs-3xl)" }}>{money(tam)}</strong>
          </article>
          <article className="app-card">
            <span>SAM — serviceable</span>
            <strong style={{ fontSize: "var(--fs-3xl)" }}>{money(sam)}</strong>
          </article>
          <article className="app-card">
            <span>SOM — obtainable</span>
            <strong style={{ fontSize: "var(--fs-3xl)" }}>{money(som)}</strong>
          </article>
        </div>
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Framework</p>
          <h2>Work through the market</h2>
        </div>
        <div className="app-grid app-grid--two">
          {data.sections.map((s) => (
            <article className="app-card" key={s.id}>
              <h3 style={{ margin: "0 0 0.3rem" }}>{s.name}</h3>
              <p style={{ fontSize: "var(--fs-sm)" }}>{s.guidance}</p>
              <ul style={{ fontSize: "var(--fs-sm)", margin: "0.4rem 0 0", paddingLeft: "1.1rem" }}>
                {s.prompts.map((p) => (
                  <li key={p}>{p}</li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Competitive pressure</p>
          <h2>Porter&apos;s five forces</h2>
        </div>
        <div className="app-card">
          <ul style={{ margin: 0, paddingLeft: "1.1rem" }}>
            {data.five_forces.map((f) => (
              <li key={f} style={{ padding: "0.2rem 0" }}>{f}</li>
            ))}
          </ul>
        </div>
      </section>

      <div className="upgrade-gate">
        <p className="eyebrow">Take it live</p>
        <h3>Connect market sizing to the deal</h3>
        <p>Benchmark the sector, screen the target, and model the value on the Aegira platform.</p>
        <div className="upgrade-gate__actions">
          <Link className="button button--primary" href="/framework/industry-analysis">
            Industry benchmarks
          </Link>
          <Link className="button button--secondary" href="/pricing">
            Upgrade to Professional
          </Link>
        </div>
      </div>

      <p className="live-market__muted" style={{ fontSize: "var(--fs-sm)", marginTop: "0.8rem" }}>{data.disclaimer}</p>
    </div>
  );
}
