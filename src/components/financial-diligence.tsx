"use client";
// JHI-SIG: 69M2705M | Financial Diligence Suite | JHI Research & Analytics Firm, Inc. (proprietary)

import { useState } from "react";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

type Report = {
  business_name: string;
  period_label: string;
  financial_integrity_score: number;
  adjusted_ebitda: number;
  reported_ebitda: number;
  ebitda_adjustment: number;
  proof_of_cash: {
    checked: boolean;
    reported_revenue: number;
    bank_deposits: number | null;
    variance_pct: number | null;
    flag: string;
  };
  working_capital: {
    net_working_capital: number;
    nwc_pct_of_revenue: number;
    note: string;
  };
  revenue_quality: { score: number; note: string };
  debt_like_items: number;
  procedures_performed: string[];
  red_flags: string[];
  recommended_tier: string;
  recommended_action: string;
  add_on_pricing: {
    band: string;
    manual_low: number;
    manual_high: number;
    platform_low: number;
    platform_high: number;
  };
  disclaimer: string;
};

type Quote = {
  reference: string;
  tier_name: string;
  estimated_price_low: number;
  estimated_price_high: number;
  turnaround_estimate: string;
  partner_match_status: string;
  next_steps: string[];
};

const DEFAULTS = {
  business_name: "Carrollton Design Build",
  industry: "construction_management",
  revenue: 12962195,
  reported_ebitda: 2381009,
  addbacks_claimed: 58745,
  questionable_addbacks: 23517,
  one_time_items: 0,
  bank_deposits: 12800000,
  accounts_receivable: 0,
  inventory: 0,
  accounts_payable: 0,
  recurring_revenue_pct: 15,
  customer_concentration_pct: 64,
  debt_like_items: 0,
  asking_price: 6200000,
  post_loi: true
};

function money(n: number | null): string {
  if (n === null || n === undefined) return "—";
  return `$${Math.round(n).toLocaleString("en-US")}`;
}

function scoreColor(n: number): string {
  if (n >= 75) return "var(--growth, #35c46b)";
  if (n >= 55) return "var(--premium, #d4af37)";
  return "#e05a5a";
}

export function FinancialDiligence() {
  const [form, setForm] = useState<Record<string, string | number | boolean>>(DEFAULTS);
  const [report, setReport] = useState<Report | null>(null);
  const [quote, setQuote] = useState<Quote | null>(null);
  const [busy, setBusy] = useState(false);
  const [quoting, setQuoting] = useState(false);
  const [error, setError] = useState("");
  const [saved, setSaved] = useState("");

  const set = (k: string, v: string | number | boolean) => setForm((p) => ({ ...p, [k]: v }));

  const run = async (event: React.FormEvent) => {
    event.preventDefault();
    setBusy(true);
    setError("");
    setQuote(null);
    setSaved("");
    try {
      const resp = await fetch(`${API_BASE}/financial-diligence/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form)
      });
      if (!resp.ok) throw new Error(`Analysis failed (${resp.status}).`);
      setReport(await resp.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed.");
    } finally {
      setBusy(false);
    }
  };

  const requestQoE = async () => {
    if (!report) return;
    setQuoting(true);
    setError("");
    try {
      const resp = await fetch(`${API_BASE}/financial-diligence/engagement`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          business_name: report.business_name,
          tier: "qoe",
          target_ebitda: report.adjusted_ebitda || report.reported_ebitda,
          state: "",
          contact_email: "subscriber@johnhenry.example"
        })
      });
      if (!resp.ok) throw new Error(`Engagement request failed (${resp.status}).`);
      setQuote(await resp.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Engagement request failed.");
    } finally {
      setQuoting(false);
    }
  };

  const download = async (path: string, ext: string) => {
    setError("");
    try {
      const resp = await fetch(`${API_BASE}/financial-diligence/${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form)
      });
      if (!resp.ok) throw new Error(`Export failed (${resp.status}).`);
      const blob = await resp.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `JHI_QoE_${String(form.business_name ?? "target").replace(/[^A-Za-z0-9]+/g, "_")}.${ext}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Export failed.");
    }
  };

  const saveToPipeline = async () => {
    if (!report) return;
    setError("");
    try {
      const resp = await fetch(`${API_BASE}/pipeline/deals`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          business_name: report.business_name,
          deal_type: "qoe",
          stage: "qoe",
          score: report.financial_integrity_score,
          recommendation: `Tier ${report.recommended_tier}`,
          headline: report.recommended_action,
          inputs: form
        })
      });
      if (!resp.ok) throw new Error(`Save failed (${resp.status}).`);
      setSaved("Saved to pipeline ✓");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Save failed.");
    }
  };

  const num = (k: keyof typeof DEFAULTS, label: string) => (
    <label style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: "var(--fs-sm)" }}>
      <span>{label}</span>
      <input
        type="number"
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
          <label style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: "var(--fs-sm)" }}>
            <span>Business name</span>
            <input value={form.business_name as string} onChange={(e) => set("business_name", e.target.value)}
              style={{ padding: "0.5rem", borderRadius: 6, border: "1px solid var(--border)", background: "transparent", color: "inherit" }} />
          </label>
          {num("revenue", "Revenue ($)")}
          {num("reported_ebitda", "Reported EBITDA/SDE ($)")}
          {num("addbacks_claimed", "Add-backs claimed ($)")}
          {num("questionable_addbacks", "Questionable add-backs ($)")}
          {num("one_time_items", "One-time items ($)")}
          {num("bank_deposits", "Bank deposits ($, proof of cash)")}
          {num("accounts_receivable", "Accounts receivable ($)")}
          {num("inventory", "Inventory ($)")}
          {num("accounts_payable", "Accounts payable ($)")}
          {num("recurring_revenue_pct", "Recurring revenue %")}
          {num("customer_concentration_pct", "Top-customer %")}
          {num("debt_like_items", "Debt-like items ($)")}
          {num("asking_price", "Asking price ($)")}
        </div>
        <button type="submit" className="button button--primary" disabled={busy} style={{ marginTop: "1rem" }}>
          {busy ? "Running diligence…" : "Run Financial Diligence"}
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
          <div style={{ display: "flex", gap: "0.5rem", justifyContent: "flex-end", alignItems: "center", marginBottom: "0.8rem" }}>
            {saved ? <span style={{ color: "var(--growth)", fontSize: "var(--fs-sm)", fontWeight: 700 }}>{saved}</span> : null}
            <button type="button" className="button button--secondary" onClick={saveToPipeline}>
              Save to Pipeline
            </button>
            <button type="button" className="button button--secondary" onClick={() => download("export.xlsx", "xlsx")}>
              Export to Excel
            </button>
            <button type="button" className="button button--secondary" onClick={() => download("export.pdf", "pdf")}>
              Export to PDF
            </button>
          </div>
          <section className="app-grid app-grid--three">
            <article className="app-card" style={{ borderTop: `3px solid ${scoreColor(report.financial_integrity_score)}` }}>
              <span>Financial Integrity Score</span>
              <strong style={{ fontSize: "var(--fs-5xl)" }}>{report.financial_integrity_score}</strong>
              <p style={{ color: scoreColor(report.financial_integrity_score), fontWeight: 800 }}>
                Recommended: Tier {report.recommended_tier}
              </p>
            </article>
            <article className="app-card">
              <span>Adjusted EBITDA</span>
              <strong style={{ fontSize: "var(--fs-3xl)" }}>{money(report.adjusted_ebitda)}</strong>
              <p>Reported {money(report.reported_ebitda)} · adjustment −{money(report.ebitda_adjustment)}</p>
            </article>
            <article className="app-card">
              <span>Recommended action</span>
              <p style={{ fontWeight: 600 }}>{report.recommended_action}</p>
            </article>
          </section>

          <section className="app-section">
            <div className="app-section__heading"><p className="eyebrow">QoE procedures</p><h2>What we ran</h2></div>
            <div className="app-grid app-grid--three">
              <article className="app-card">
                <span>Proof of cash</span>
                <strong style={{ fontSize: "var(--fs-xl)" }}>
                  {report.proof_of_cash.checked ? `${report.proof_of_cash.variance_pct}% variance` : "Not performed"}
                </strong>
                <p>{report.proof_of_cash.flag}</p>
              </article>
              <article className="app-card">
                <span>Net working capital</span>
                <strong style={{ fontSize: "var(--fs-xl)" }}>{money(report.working_capital.net_working_capital)} ({report.working_capital.nwc_pct_of_revenue}%)</strong>
                <p>{report.working_capital.note}</p>
              </article>
              <article className="app-card">
                <span>Quality of revenue</span>
                <strong style={{ fontSize: "var(--fs-xl)" }}>{report.revenue_quality.score}/100</strong>
                <p>{report.revenue_quality.note}</p>
              </article>
            </div>
          </section>

          {report.red_flags.length ? (
            <section className="app-section">
              <div className="app-section__heading"><p className="eyebrow">Red flags</p><h2>Resolve before you offer</h2></div>
              <ul>{report.red_flags.map((f) => <li key={f}>{f}</li>)}</ul>
            </section>
          ) : null}

          <section className="app-section">
            <div className="app-section__heading"><p className="eyebrow">Add-on pricing</p><h2>Partner-CPA QoE vs. the manual market</h2></div>
            <div className="table-card">
              <article className="table-row">
                <div style={{ minWidth: 220 }}>
                  <span>{report.add_on_pricing.band}</span>
                  <strong>Quality of Earnings (Tier B)</strong>
                </div>
                <p style={{ fontSize: "var(--fs-sm)" }}>
                  Manual market: {money(report.add_on_pricing.manual_low)}–{money(report.add_on_pricing.manual_high)}<br />
                  <strong style={{ color: "var(--growth,#35c46b)" }}>
                    JHI platform: {money(report.add_on_pricing.platform_low)}–{money(report.add_on_pricing.platform_high)}
                  </strong>
                </p>
                <button className="button button--primary" disabled={quoting} onClick={requestQoE}>
                  {quoting ? "Requesting…" : "Request CPA-signed QoE"}
                </button>
              </article>
            </div>
          </section>

          {quote ? (
            <section className="app-section">
              <div className="app-section__heading"><p className="eyebrow">Engagement quote</p><h2>{quote.reference}</h2></div>
              <article className="app-card">
                <p style={{ fontWeight: 700 }}>
                  {quote.tier_name}: {money(quote.estimated_price_low)}–{money(quote.estimated_price_high)} · {quote.turnaround_estimate} · status: {quote.partner_match_status}
                </p>
                <ol style={{ marginTop: "0.5rem" }}>
                  {quote.next_steps.map((s) => <li key={s}>{s}</li>)}
                </ol>
              </article>
            </section>
          ) : null}

          <p className="live-market__muted" style={{ fontSize: "var(--fs-sm)" }}>{report.disclaimer}</p>
        </div>
      ) : null}
    </div>
  );
}
