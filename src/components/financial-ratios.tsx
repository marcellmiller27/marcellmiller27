// JHI-SIG: 69M2705M | Key Financial Ratios | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { useState } from "react";
import Link from "next/link";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api/v1";

type RatioResult = {
  key: string;
  name: string;
  category: string;
  unit: string;
  value: number | null;
  display: string;
  status: string;
  interpretation: string;
  benchmark: string;
};

type Report = { results: RatioResult[]; summary: string; disclaimer: string };

const FIELDS: { key: string; label: string }[] = [
  { key: "purchase_price", label: "Purchase price ($)" },
  { key: "sde", label: "SDE ($)" },
  { key: "ebitda", label: "EBITDA ($)" },
  { key: "revenue", label: "Revenue ($)" },
  { key: "cogs", label: "COGS ($)" },
  { key: "operating_expenses", label: "Operating expenses ($)" },
  { key: "net_income", label: "Net income ($)" },
  { key: "total_debt", label: "Total debt ($)" },
  { key: "annual_debt_service", label: "Annual debt service ($)" },
  { key: "total_equity", label: "Total equity ($)" },
  { key: "current_assets", label: "Current assets ($)" },
  { key: "current_liabilities", label: "Current liabilities ($)" },
  { key: "inventory", label: "Inventory ($)" }
];

const DEFAULTS: Record<string, number> = {
  purchase_price: 1000000,
  sde: 250000,
  ebitda: 200000,
  revenue: 1000000,
  cogs: 400000,
  operating_expenses: 400000,
  net_income: 120000,
  total_debt: 400000,
  annual_debt_service: 100000,
  total_equity: 600000,
  current_assets: 300000,
  current_liabilities: 150000,
  inventory: 100000
};

function statusColor(s: string): string {
  if (s === "strong") return "var(--growth, #35c46b)";
  if (s === "adequate") return "var(--premium, #d4af37)";
  if (s === "caution") return "#e0a15a";
  if (s === "weak") return "#e05a5a";
  return "var(--muted, #8a94a6)";
}

export function FinancialRatios() {
  const [form, setForm] = useState<Record<string, string | number>>(DEFAULTS);
  const [report, setReport] = useState<Report | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const set = (k: string, v: string) => setForm((p) => ({ ...p, [k]: v === "" ? "" : Number(v) }));

  const run = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      const payload: Record<string, number> = {};
      Object.entries(form).forEach(([k, v]) => {
        if (v !== "" && !Number.isNaN(Number(v))) payload[k] = Number(v);
      });
      const resp = await fetch(`${API_BASE}/framework/ratios/compute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!resp.ok) throw new Error(`Compute failed (${resp.status}).`);
      setReport(await resp.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Compute failed.");
    } finally {
      setBusy(false);
    }
  };

  const exportCsv = () => {
    if (!report) return;
    const rows = [["Ratio", "Category", "Value", "Status", "Benchmark", "Interpretation"]];
    report.results.forEach((r) =>
      rows.push([r.name, r.category, r.display, r.status, r.benchmark, r.interpretation])
    );
    const csv = rows.map((r) => r.map((v) => `"${v.replace(/"/g, '""')}"`).join(",")).join("\r\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "Aegira_key_financial_ratios.csv";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  };

  const grouped = report
    ? report.results.reduce<Record<string, RatioResult[]>>((acc, r) => {
        (acc[r.category] ||= []).push(r);
        return acc;
      }, {})
    : {};

  return (
    <div>
      <form onSubmit={run} className="app-card" style={{ marginBottom: "1.5rem" }}>
        <div className="app-grid app-grid--three" style={{ gap: "0.8rem" }}>
          {FIELDS.map((f) => (
            <label key={f.key} style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: "var(--fs-sm)" }}>
              <span>{f.label}</span>
              <input
                type="number"
                value={form[f.key] as number}
                onChange={(e) => set(f.key, e.target.value)}
                style={{ padding: "0.5rem", borderRadius: 6, border: "1px solid var(--border)", background: "transparent", color: "inherit" }}
              />
            </label>
          ))}
        </div>
        <button type="submit" className="button button--primary" disabled={busy} style={{ marginTop: "1rem" }}>
          {busy ? "Computing…" : "Compute ratios"}
        </button>
        {error ? (
          <p className="live-market__status" style={{ marginTop: "0.6rem" }}>
            <span className="live-market__dot live-market__dot--off" />
            {error}
          </p>
        ) : null}
      </form>

      {report ? (
        <div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: "1rem", flexWrap: "wrap", marginBottom: "0.8rem" }}>
            <p style={{ fontWeight: 700, margin: 0 }}>{report.summary}</p>
            <button type="button" className="button button--secondary" onClick={exportCsv}>
              Export ratios (CSV)
            </button>
          </div>

          {Object.entries(grouped).map(([category, items]) => (
            <section className="app-section" key={category}>
              <div className="app-section__heading">
                <p className="eyebrow">{category}</p>
              </div>
              <div className="app-grid app-grid--three">
                {items.map((r) => (
                  <article className="app-card" key={r.key} style={{ borderTop: `3px solid ${statusColor(r.status)}` }}>
                    <span>{r.name}</span>
                    <strong style={{ fontSize: "var(--fs-3xl)" }}>{r.display}</strong>
                    <p style={{ color: statusColor(r.status), fontWeight: 800, textTransform: "capitalize", margin: "0.2rem 0" }}>
                      {r.status}
                    </p>
                    <p style={{ fontSize: "var(--fs-sm)" }}>{r.interpretation}</p>
                    <p className="live-market__muted" style={{ fontSize: "var(--fs-xs, 0.72rem)" }}>{r.benchmark}</p>
                  </article>
                ))}
              </div>
            </section>
          ))}

          <div className="upgrade-gate" style={{ marginTop: "1rem" }}>
            <p className="eyebrow">Next step</p>
            <h3>Turn ratios into a valuation and a diligence plan</h3>
            <p>
              Ratios flag what to investigate. Run the earnings quality, model the value, and
              track the deal to close with the Aegira platform.
            </p>
            <div className="upgrade-gate__actions">
              <Link className="button button--primary" href="/diligence-suite">
                Run Earnings / QoE
              </Link>
              <Link className="button button--secondary" href="/valuation">
                Open Valuation
              </Link>
            </div>
          </div>

          <p className="live-market__muted" style={{ fontSize: "var(--fs-sm)", marginTop: "0.8rem" }}>{report.disclaimer}</p>
        </div>
      ) : null}
    </div>
  );
}
