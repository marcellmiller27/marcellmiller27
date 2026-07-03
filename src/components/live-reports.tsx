"use client";

import { useEffect, useState } from "react";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

type Metric = { label: string; value: string; change: string; risk_level: string };
type Line = { label: string; amount: string };
type Executive = {
  metrics: Metric[];
  open_audit_findings: number;
  active_crm_deals: number;
  monthly_recurring_revenue: string;
  cash_position: string;
  notes: string[];
};
type Financial = {
  period_start: string;
  period_end: string;
  income_statement: Line[];
  kpis: Record<string, string>;
};

export function LiveReports() {
  const [exec, setExec] = useState<Executive | null>(null);
  const [fin, setFin] = useState<Financial | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    const end = new Date().toISOString().slice(0, 10);
    const start = "2020-01-01";
    Promise.all([
      fetch(`${API_BASE}/dashboards/executive`).then((r) => {
        if (!r.ok) throw new Error(String(r.status));
        return r.json();
      }),
      fetch(`${API_BASE}/reports/financial?period_start=${start}&period_end=${end}`).then((r) => {
        if (!r.ok) throw new Error(String(r.status));
        return r.json();
      })
    ])
      .then(([execData, finData]) => {
        if (!active) return;
        setExec(execData);
        setFin(finData);
        setError("");
      })
      .catch(() => active && setError("Live report data is unavailable right now."));
    return () => {
      active = false;
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
  if (!exec || !fin) {
    return (
      <p className="live-market__status">
        <span className="live-market__dot" />
        Loading live financials…
      </p>
    );
  }

  return (
    <div>
      <p className="live-market__status">
        <span className="live-market__dot" />
        Live · from the durable ledger &amp; CRM
      </p>
      <div className="app-grid app-grid--four">
        <article className="app-card">
          <span>Monthly recurring revenue</span>
          <strong>${exec.monthly_recurring_revenue}</strong>
          <p>Computed from active subscriptions.</p>
        </article>
        <article className="app-card">
          <span>Cash position</span>
          <strong>${exec.cash_position}</strong>
          <p>From the posted general ledger.</p>
        </article>
        <article className="app-card">
          <span>Active CRM deals</span>
          <strong>{exec.active_crm_deals}</strong>
          <p>Open pipeline opportunities.</p>
        </article>
        <article className="app-card">
          <span>Open audit findings</span>
          <strong>{exec.open_audit_findings}</strong>
          <p>Controls requiring attention.</p>
        </article>
      </div>

      <div className="app-section__heading" style={{ marginTop: "1.5rem" }}>
        <p className="eyebrow">Income statement</p>
        <h3 style={{ margin: "0.2rem 0" }}>
          {fin.period_start} → {fin.period_end}
        </h3>
      </div>
      <div className="table-card">
        {fin.income_statement.map((line) => (
          <article className="table-row" key={line.label}>
            <div>
              <span>Line</span>
              <strong>{line.label}</strong>
            </div>
            <p style={{ textAlign: "right", fontWeight: 800 }}>${line.amount}</p>
          </article>
        ))}
        {fin.income_statement.length === 0 ? (
          <article className="table-row">
            <div>
              <span>Line</span>
              <strong>No posted entries in range</strong>
            </div>
            <p>—</p>
          </article>
        ) : null}
      </div>
    </div>
  );
}
