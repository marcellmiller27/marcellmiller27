"use client";
// JHI-SIG: 69M2705M | Accounting UI | John Henry Investments (proprietary)

import { useEffect, useState } from "react";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

type Account = { code: string; name: string; account_type: string };
type TrialRow = {
  account_code: string;
  account_name: string;
  account_type: string;
  debit_total: string | number;
  credit_total: string | number;
  net_balance: string | number;
};
type Trial = {
  period_start: string;
  period_end: string;
  rows: TrialRow[];
  total_debits: string | number;
  total_credits: string | number;
  is_balanced: boolean;
};
type JLine = {
  account_code: string;
  account_name: string;
  debit: string | number;
  credit: string | number;
  description: string;
};
type JEntry = {
  id: string;
  entry_date: string;
  memo: string;
  source_module: string;
  lines: JLine[];
};

function money(v: string | number): string {
  const n = typeof v === "string" ? parseFloat(v) : v;
  if (!Number.isFinite(n)) return "$0.00";
  return `$${n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

const cellStyle = { padding: "0.5rem 0.75rem", borderBottom: "1px solid var(--border)", fontSize: "0.85rem" } as const;
const headStyle = { ...cellStyle, textAlign: "left" as const, color: "var(--muted)", fontWeight: 800, fontSize: "0.75rem", textTransform: "uppercase" as const };

export function LiveAccounting() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [trial, setTrial] = useState<Trial | null>(null);
  const [entries, setEntries] = useState<JEntry[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    const start = "2020-01-01";
    const end = "2030-12-31";
    Promise.all([
      fetch(`${API_BASE}/accounting/chart-of-accounts`).then((r) => (r.ok ? r.json() : Promise.reject(r))),
      fetch(`${API_BASE}/accounting/trial-balance?period_start=${start}&period_end=${end}`).then((r) =>
        r.ok ? r.json() : Promise.reject(r)
      ),
      fetch(`${API_BASE}/accounting/journal-entries`).then((r) => (r.ok ? r.json() : Promise.reject(r)))
    ])
      .then(([acc, tb, je]) => {
        if (!active) return;
        setAccounts(acc);
        setTrial(tb);
        setEntries(je);
        setError("");
        setLoading(false);
      })
      .catch(() => {
        if (!active) return;
        setError("Accounting data is unavailable — confirm the backend is running on :8000.");
        setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  if (loading) {
    return <p className="live-market__muted">Loading accounting…</p>;
  }

  if (error) {
    return (
      <p className="live-market__status">
        <span className="live-market__dot live-market__dot--off" />
        {error}
      </p>
    );
  }

  return (
    <div>
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">General ledger</p>
          <h2>Chart of accounts</h2>
        </div>
        <article className="app-card" style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th style={headStyle}>Code</th>
                <th style={headStyle}>Account</th>
                <th style={headStyle}>Type</th>
              </tr>
            </thead>
            <tbody>
              {accounts.map((a) => (
                <tr key={a.code}>
                  <td style={cellStyle}>{a.code}</td>
                  <td style={cellStyle}>{a.name}</td>
                  <td style={{ ...cellStyle, textTransform: "capitalize" }}>{a.account_type}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </article>
      </section>

      {trial ? (
        <section className="app-section">
          <div className="app-section__heading">
            <p className="eyebrow">Trial balance</p>
            <h2>
              Balances{" "}
              <span
                style={{
                  fontSize: "0.8rem",
                  fontWeight: 800,
                  color: trial.is_balanced ? "var(--growth)" : "#c0392b"
                }}
              >
                {trial.is_balanced ? "· Balanced ✓" : "· Out of balance"}
              </span>
            </h2>
          </div>
          <article className="app-card" style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  <th style={headStyle}>Code</th>
                  <th style={headStyle}>Account</th>
                  <th style={{ ...headStyle, textAlign: "right" }}>Debit</th>
                  <th style={{ ...headStyle, textAlign: "right" }}>Credit</th>
                  <th style={{ ...headStyle, textAlign: "right" }}>Net</th>
                </tr>
              </thead>
              <tbody>
                {trial.rows.map((r) => (
                  <tr key={r.account_code}>
                    <td style={cellStyle}>{r.account_code}</td>
                    <td style={cellStyle}>{r.account_name}</td>
                    <td style={{ ...cellStyle, textAlign: "right" }}>{money(r.debit_total)}</td>
                    <td style={{ ...cellStyle, textAlign: "right" }}>{money(r.credit_total)}</td>
                    <td style={{ ...cellStyle, textAlign: "right" }}>{money(r.net_balance)}</td>
                  </tr>
                ))}
                <tr>
                  <td style={{ ...cellStyle, fontWeight: 800 }} colSpan={2}>
                    Totals
                  </td>
                  <td style={{ ...cellStyle, textAlign: "right", fontWeight: 800 }}>{money(trial.total_debits)}</td>
                  <td style={{ ...cellStyle, textAlign: "right", fontWeight: 800 }}>{money(trial.total_credits)}</td>
                  <td style={cellStyle} />
                </tr>
              </tbody>
            </table>
          </article>
        </section>
      ) : null}

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Journal</p>
          <h2>Recent journal entries</h2>
        </div>
        {entries.length === 0 ? (
          <p className="live-market__muted">No journal entries yet.</p>
        ) : (
          entries.slice(0, 12).map((e) => (
            <article className="app-card" key={e.id} style={{ marginBottom: "0.8rem" }}>
              <div style={{ display: "flex", justifyContent: "space-between", flexWrap: "wrap", gap: "0.5rem" }}>
                <strong>{e.memo}</strong>
                <span style={{ color: "var(--muted)", fontSize: "0.8rem" }}>
                  {e.entry_date} · {e.source_module}
                </span>
              </div>
              <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "0.5rem" }}>
                <tbody>
                  {e.lines.map((l, i) => (
                    <tr key={`${e.id}-${i}`}>
                      <td style={cellStyle}>
                        {l.account_code} · {l.account_name}
                      </td>
                      <td style={{ ...cellStyle, textAlign: "right" }}>
                        {parseFloat(String(l.debit)) > 0 ? money(l.debit) : ""}
                      </td>
                      <td style={{ ...cellStyle, textAlign: "right" }}>
                        {parseFloat(String(l.credit)) > 0 ? money(l.credit) : ""}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </article>
          ))
        )}
      </section>
    </div>
  );
}
