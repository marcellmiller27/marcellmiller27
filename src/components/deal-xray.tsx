"use client";
// JHI-SIG: 69M2705M | Acquisition / Deal X-Ray | John Henry Investments (proprietary)

import { useState } from "react";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

type Segment = { segment: string; score: number; weight: number; findings: string[] };
type Financing = {
  label: string;
  equity_required: number;
  loan_amount: number;
  seller_note: number;
  annual_debt_service: number;
  dscr: number | null;
  sba_fit: boolean;
  note: string;
};
type Report = {
  business_name: string;
  industry: string;
  deal_score: number;
  recommendation: string;
  ethic_rating: number;
  ethic_note: string;
  segments: Segment[];
  valuation: {
    normalized_ebitda: number;
    basis_note: string;
    industry_multiple_base: number;
    multiple_value_low: number;
    multiple_value_base: number;
    multiple_value_high: number;
    dcf_enterprise_value: number;
    asking_price: number;
    verdict: string;
  };
  financing_options: Financing[];
  key_metrics: Record<string, string>;
  diligence_questions: string[];
  disclaimer: string;
};

const INDUSTRIES = [
  "hvac", "plumbing", "electrical", "landscaping", "restaurant", "ecommerce",
  "manufacturing", "healthcare_services", "professional_services", "logistics", "saas",
  "construction", "construction_management", "general"
];
const OWNER = ["absentee", "semi_absentee", "owner_operated", "owner_critical"];

// Pre-loaded with the real Carrollton Design Build CIM so a reviewer can run it in one click.
const DEFAULTS = {
  business_name: "Carrollton Design Build",
  industry: "construction_management",
  revenue: 12962195,
  revenue_prior: 11701091,
  reported_ebitda: 2381009,
  addbacks: 58745,
  annual_depreciation: 56362,
  earnings_history: "2381009, 1612599, 827662, 866690, 1345480",
  employees: 14,
  owner_involvement: "owner_operated",
  equipment_age_years: 5,
  customer_concentration_pct: 64,
  recurring_revenue_pct: 15,
  asking_price: 6200000,
  down_payment_pct: 10,
  seller_note_pct: 0,
  loan_rate_pct: 11.5,
  loan_term_years: 10
};

function money(n: number): string {
  return `$${Math.round(n).toLocaleString("en-US")}`;
}

function recColor(rec: string): string {
  if (rec === "Buy") return "var(--growth, #35c46b)";
  if (rec === "Watch") return "var(--premium, #d4af37)";
  return "#e05a5a";
}

export function DealXRay() {
  const [form, setForm] = useState<Record<string, string | number>>(DEFAULTS);
  const [report, setReport] = useState<Report | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const set = (k: string, v: string | number) => setForm((p) => ({ ...p, [k]: v }));

  const run = async (event: React.FormEvent) => {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      const history = String(form.earnings_history ?? "")
        .split(",")
        .map((s) => Number(s.trim()))
        .filter((n) => Number.isFinite(n) && n > 0);
      const payload = { ...form, earnings_history: history.length ? history : null };
      const resp = await fetch(`${API_BASE}/deal-xray/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!resp.ok) throw new Error(`Analysis failed (${resp.status}).`);
      setReport(await resp.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed.");
    } finally {
      setBusy(false);
    }
  };

  const exportExcel = async () => {
    setError("");
    try {
      const history = String(form.earnings_history ?? "")
        .split(",")
        .map((s) => Number(s.trim()))
        .filter((n) => Number.isFinite(n) && n > 0);
      const payload = { ...form, earnings_history: history.length ? history : null };
      const resp = await fetch(`${API_BASE}/deal-xray/export.xlsx`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!resp.ok) throw new Error(`Export failed (${resp.status}).`);
      const blob = await resp.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `JHI_BQA_${String(form.business_name ?? "deal").replace(/[^A-Za-z0-9]+/g, "_")}.xlsx`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Export failed.");
    }
  };

  const num = (k: keyof typeof DEFAULTS, label: string, step = "1") => (
    <label style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: "0.8rem" }}>
      <span>{label}</span>
      <input
        type="number"
        step={step}
        value={form[k] as number}
        onChange={(e) => set(k, e.target.value === "" ? "" : Number(e.target.value))}
        style={{ padding: "0.5rem", borderRadius: 6, border: "1px solid var(--border)", background: "transparent", color: "inherit" }}
      />
    </label>
  );

  return (
    <div>
      <form onSubmit={run} className="app-card" style={{ marginBottom: "1.5rem" }}>
        <div className="app-grid app-grid--three" style={{ gap: "0.8rem" }}>
          <label style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: "0.8rem" }}>
            <span>Business name</span>
            <input value={form.business_name as string} onChange={(e) => set("business_name", e.target.value)}
              style={{ padding: "0.5rem", borderRadius: 6, border: "1px solid var(--border)", background: "transparent", color: "inherit" }} />
          </label>
          <label style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: "0.8rem" }}>
            <span>Industry</span>
            <select value={form.industry as string} onChange={(e) => set("industry", e.target.value)}
              style={{ padding: "0.5rem", borderRadius: 6, border: "1px solid var(--border)", background: "transparent", color: "inherit" }}>
              {INDUSTRIES.map((i) => <option key={i} value={i}>{i.replace(/_/g, " ")}</option>)}
            </select>
          </label>
          <label style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: "0.8rem" }}>
            <span>Owner involvement</span>
            <select value={form.owner_involvement as string} onChange={(e) => set("owner_involvement", e.target.value)}
              style={{ padding: "0.5rem", borderRadius: 6, border: "1px solid var(--border)", background: "transparent", color: "inherit" }}>
              {OWNER.map((o) => <option key={o} value={o}>{o.replace(/_/g, " ")}</option>)}
            </select>
          </label>
          {num("revenue", "Revenue ($)")}
          {num("revenue_prior", "Prior-year revenue ($)")}
          {num("reported_ebitda", "Reported EBITDA/SDE ($)")}
          {num("addbacks", "Add-backs ($)")}
          {num("annual_depreciation", "Depreciation ($, capex proxy)")}
          <label style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: "0.8rem" }}>
            <span>Earnings history (recent first, comma-sep)</span>
            <input
              value={form.earnings_history as string}
              onChange={(e) => set("earnings_history", e.target.value)}
              placeholder="2381009, 1612599, 827662"
              style={{ padding: "0.5rem", borderRadius: 6, border: "1px solid var(--border)", background: "transparent", color: "inherit" }}
            />
          </label>
          {num("employees", "Employees")}
          {num("equipment_age_years", "Equipment age (yrs)")}
          {num("customer_concentration_pct", "Top-customer %")}
          {num("recurring_revenue_pct", "Recurring revenue %")}
          {num("asking_price", "Asking price ($)")}
          {num("down_payment_pct", "Down payment %")}
          {num("seller_note_pct", "Seller note %")}
          {num("loan_rate_pct", "Loan APR %", "0.1")}
        </div>
        <button type="submit" className="button button--primary" disabled={busy} style={{ marginTop: "1rem" }}>
          {busy ? "Analyzing…" : "Run Deal X-Ray"}
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
          <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: "0.8rem" }}>
            <button type="button" className="button button--secondary" onClick={exportExcel}>
              Export to Excel
            </button>
          </div>
          <section className="app-grid app-grid--three">
            <article className="app-card" style={{ borderTop: `3px solid ${recColor(report.recommendation)}` }}>
              <span>Deal Score</span>
              <strong style={{ fontSize: "2.4rem" }}>{report.deal_score}</strong>
              <p style={{ color: recColor(report.recommendation), fontWeight: 800 }}>{report.recommendation}</p>
            </article>
            <article className="app-card">
              <span>Honest Ethic Rating</span>
              <strong style={{ fontSize: "2.4rem" }}>{report.ethic_rating}</strong>
              <p>{report.ethic_note}</p>
            </article>
            <article className="app-card">
              <span>Valuation verdict</span>
              <strong style={{ textTransform: "capitalize" }}>{report.valuation.verdict}</strong>
              <p>
                Asking {money(report.valuation.asking_price)} vs. base {money(report.valuation.multiple_value_base)} ·
                DCF {money(report.valuation.dcf_enterprise_value)}
              </p>
              {report.valuation.basis_note ? (
                <p style={{ fontSize: "0.75rem", opacity: 0.8, marginTop: "0.35rem" }}>
                  Basis: {report.valuation.basis_note}
                </p>
              ) : null}
            </article>
          </section>

          <section className="app-section">
            <div className="app-section__heading"><p className="eyebrow">Six-segment scorecard</p><h2>Business Quality Assessment</h2></div>
            <div className="table-card">
              {report.segments.map((s) => (
                <article className="table-row" key={s.segment}>
                  <div style={{ minWidth: 160 }}>
                    <span>weight {Math.round(s.weight * 100)}%</span>
                    <strong>{s.segment}</strong>
                  </div>
                  <div style={{ flex: 1, margin: "0 1rem" }}>
                    <div style={{ background: "rgba(15,39,68,0.08)", borderRadius: 6, height: 8 }}>
                      <div style={{ width: `${s.score}%`, height: 8, borderRadius: 6, background: "var(--growth, #35c46b)" }} />
                    </div>
                    <p style={{ fontSize: "0.78rem", margin: "0.35rem 0 0", opacity: 0.85 }}>{s.findings.join(" ")}</p>
                  </div>
                  <div className="score-badge"><strong>{s.score}</strong><span>/100</span></div>
                </article>
              ))}
            </div>
          </section>

          <section className="app-section">
            <div className="app-section__heading"><p className="eyebrow">Financing / offer alternatives</p><h2>Realistic structures &amp; DSCR</h2></div>
            <div className="table-card">
              {report.financing_options.map((f) => (
                <article className="table-row" key={f.label}>
                  <div style={{ minWidth: 220 }}>
                    <span>{f.sba_fit ? "SBA-eligible" : "Review"}</span>
                    <strong>{f.label}</strong>
                    <p style={{ fontSize: "0.78rem", opacity: 0.85, margin: "0.25rem 0 0" }}>{f.note}</p>
                  </div>
                  <p style={{ fontSize: "0.82rem" }}>
                    Equity {money(f.equity_required)} · Loan {money(f.loan_amount)} · Seller note {money(f.seller_note)}<br />
                    Debt service {money(f.annual_debt_service)}/yr
                  </p>
                  <div className="score-badge">
                    <strong style={{ color: (f.dscr ?? 0) >= 1.25 ? "var(--growth,#35c46b)" : "#e05a5a" }}>
                      {f.dscr ?? "—"}
                    </strong>
                    <span>DSCR</span>
                  </div>
                </article>
              ))}
            </div>
          </section>

          <section className="app-section">
            <div className="app-section__heading"><p className="eyebrow">Key metrics</p><h2>At a glance</h2></div>
            <div className="app-grid app-grid--three">
              {Object.entries(report.key_metrics).map(([k, v]) => (
                <article className="app-card" key={k}><span>{k}</span><strong>{v}</strong></article>
              ))}
            </div>
          </section>

          <section className="app-section">
            <div className="app-section__heading"><p className="eyebrow">Diligence questions</p><h2>Ask before you offer</h2></div>
            <ul>
              {report.diligence_questions.map((q) => <li key={q}>{q}</li>)}
            </ul>
          </section>

          <p className="live-market__muted" style={{ fontSize: "0.78rem" }}>{report.disclaimer}</p>
        </div>
      ) : null}
    </div>
  );
}
