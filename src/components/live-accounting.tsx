"use client";
// JHI-SIG: 69M2705M | Accounting UI | John Henry Investments (proprietary)

import { Fragment, useCallback, useEffect, useState } from "react";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

type Account = { code: string; name: string; account_type: string; category?: string };

// Non-GL operational metrics (8000 series) — tracked for management insight only,
// deliberately NOT posted to the general ledger.
const MANAGEMENT_METRICS: [string, string][] = [
  ["8000", "Annual Recurring Revenue (ARR)"],
  ["8010", "Monthly Recurring Revenue (MRR)"],
  ["8020", "Churn"],
  ["8030", "Customer Acquisition Cost (CAC)"],
  ["8040", "Lifetime Value (LTV)"],
  ["8050", "Gross Revenue Retention"],
  ["8060", "Net Revenue Retention"],
  ["8070", "Active Subscribers"],
  ["8080", "Average Revenue Per User (ARPU)"]
];

const groupHeadStyle = {
  padding: "0.5rem 0.75rem",
  background: "var(--border)",
  fontWeight: 800,
  fontSize: "var(--fs-xs)",
  textTransform: "uppercase" as const,
  letterSpacing: "0.04em"
};
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

const cellStyle = { padding: "0.5rem 0.75rem", borderBottom: "1px solid var(--border)", fontSize: "var(--fs-sm)" } as const;
const headStyle = { ...cellStyle, textAlign: "left" as const, color: "var(--muted)", fontWeight: 800, fontSize: "var(--fs-xs)", textTransform: "uppercase" as const };

const PERIOD_START = "2020-01-01";
const PERIOD_END = "2030-12-31";

export function LiveAccounting() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [trial, setTrial] = useState<Trial | null>(null);
  const [entries, setEntries] = useState<JEntry[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const load = useCallback(
    () =>
      Promise.all([
        fetch(`${API_BASE}/accounting/chart-of-accounts`).then((r) => (r.ok ? r.json() : Promise.reject(r))),
        fetch(`${API_BASE}/accounting/trial-balance?period_start=${PERIOD_START}&period_end=${PERIOD_END}`).then((r) =>
          r.ok ? r.json() : Promise.reject(r)
        ),
        fetch(`${API_BASE}/accounting/journal-entries`).then((r) => (r.ok ? r.json() : Promise.reject(r)))
      ]).then(([acc, tb, je]) => {
        setAccounts(acc);
        setTrial(tb);
        setEntries(je);
        setError("");
      }),
    []
  );

  useEffect(() => {
    let active = true;
    load()
      .catch(() => {
        if (active) setError("Accounting data is unavailable — confirm the backend is running on :8000.");
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [load]);

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

  const categories: string[] = [];
  for (const a of accounts) {
    const c = a.category || "Other";
    if (!categories.includes(c)) categories.push(c);
  }

  return (
    <div>
      <JournalEntryForm accounts={accounts} onPosted={load} />

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
              {categories.map((cat) => (
                <Fragment key={cat}>
                  <tr>
                    <td colSpan={3} style={groupHeadStyle}>
                      {cat}
                    </td>
                  </tr>
                  {accounts
                    .filter((a) => (a.category || "Other") === cat)
                    .map((a) => (
                      <tr key={a.code}>
                        <td style={cellStyle}>{a.code}</td>
                        <td style={cellStyle}>{a.name}</td>
                        <td style={{ ...cellStyle, textTransform: "capitalize" }}>{a.account_type}</td>
                      </tr>
                    ))}
                </Fragment>
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
                  fontSize: "var(--fs-sm)",
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
                <span style={{ color: "var(--muted)", fontSize: "var(--fs-sm)" }}>
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

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Management metrics · non-GL</p>
          <h2>Operational metrics (8000 series)</h2>
        </div>
        <article className="app-card" style={{ overflowX: "auto" }}>
          <p style={{ color: "var(--muted)", fontSize: "var(--fs-sm)", marginTop: 0 }}>
            Tracked alongside the ledger for management insight — these are{" "}
            <span style={{ fontWeight: 700 }}>not</span> general-ledger accounts and do not post to the
            trial balance.
          </p>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th style={headStyle}>Ref</th>
                <th style={headStyle}>Metric</th>
              </tr>
            </thead>
            <tbody>
              {MANAGEMENT_METRICS.map(([code, name]) => (
                <tr key={code}>
                  <td style={cellStyle}>{code}</td>
                  <td style={cellStyle}>{name}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </article>
      </section>
    </div>
  );
}

const inputStyle = {
  padding: "0.45rem 0.55rem",
  borderRadius: "8px",
  border: "1px solid var(--border)",
  fontSize: "var(--fs-sm)",
  background: "var(--surface, #fff)",
  color: "inherit",
  width: "100%"
} as const;

type DraftLine = { account_code: string; description: string; debit: string; credit: string };

function emptyLine(): DraftLine {
  return { account_code: "", description: "", debit: "", credit: "" };
}

function toNumber(value: string): number {
  const n = parseFloat(value);
  return Number.isFinite(n) ? n : 0;
}

function lineIsValid(line: DraftLine): boolean {
  if (!line.account_code) return false;
  const debit = toNumber(line.debit);
  const credit = toNumber(line.credit);
  if (debit < 0 || credit < 0) return false;
  // exactly one side must be positive
  return (debit > 0) !== (credit > 0);
}

function JournalEntryForm({ accounts, onPosted }: { accounts: Account[]; onPosted: () => Promise<void> }) {
  const today = new Date().toISOString().slice(0, 10);
  const [open, setOpen] = useState(false);
  const [entryDate, setEntryDate] = useState(today);
  const [memo, setMemo] = useState("");
  const [lines, setLines] = useState<DraftLine[]>([emptyLine(), emptyLine()]);
  const [posting, setPosting] = useState(false);
  const [message, setMessage] = useState<{ ok: boolean; text: string } | null>(null);

  const totalDebit = lines.reduce((s, l) => s + toNumber(l.debit), 0);
  const totalCredit = lines.reduce((s, l) => s + toNumber(l.credit), 0);
  const balanced = totalDebit > 0 && Math.abs(totalDebit - totalCredit) < 0.005;
  const allLinesValid = lines.every(lineIsValid);
  const canPost = !posting && memo.trim().length > 0 && lines.length >= 2 && allLinesValid && balanced;

  function updateLine(index: number, field: keyof DraftLine, value: string) {
    setLines((prev) =>
      prev.map((line, i) => {
        if (i !== index) return line;
        const next = { ...line, [field]: value };
        // A line is debit XOR credit — entering one clears the other.
        if (field === "debit" && toNumber(value) > 0) next.credit = "";
        if (field === "credit" && toNumber(value) > 0) next.debit = "";
        return next;
      })
    );
  }

  function addLine() {
    setLines((prev) => [...prev, emptyLine()]);
  }

  function removeLine(index: number) {
    setLines((prev) => (prev.length <= 2 ? prev : prev.filter((_, i) => i !== index)));
  }

  function resetForm() {
    setEntryDate(today);
    setMemo("");
    setLines([emptyLine(), emptyLine()]);
  }

  async function submit() {
    setPosting(true);
    setMessage(null);
    try {
      const payload = {
        entry_date: entryDate,
        memo: memo.trim(),
        source_module: "manual",
        created_by: "founder",
        lines: lines.map((l) => ({
          account_code: l.account_code,
          description: l.description.trim(),
          debit: toNumber(l.debit).toFixed(2),
          credit: toNumber(l.credit).toFixed(2)
        }))
      };
      const res = await fetch(`${API_BASE}/accounting/journal-entries`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!res.ok) {
        let detail = `Post failed (HTTP ${res.status}).`;
        try {
          const body = await res.json();
          if (body?.detail) detail = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail);
        } catch {
          /* keep default */
        }
        setMessage({ ok: false, text: detail });
        return;
      }
      await onPosted();
      resetForm();
      setMessage({ ok: true, text: "Journal entry posted and ledger updated." });
    } catch {
      setMessage({ ok: false, text: "Could not reach the accounting API." });
    } finally {
      setPosting(false);
    }
  }

  return (
    <section className="app-section">
      <div className="app-section__heading" style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", flexWrap: "wrap", gap: "0.5rem" }}>
        <div>
          <p className="eyebrow">Journal</p>
          <h2>Post a journal entry</h2>
        </div>
        <button
          type="button"
          onClick={() => setOpen((v) => !v)}
          style={{
            padding: "0.45rem 0.9rem",
            borderRadius: "999px",
            border: "1px solid var(--border)",
            background: open ? "transparent" : "var(--growth, #1f7a4d)",
            color: open ? "inherit" : "#fff",
            fontWeight: 700,
            fontSize: "var(--fs-sm)",
            cursor: "pointer"
          }}
        >
          {open ? "Close" : "+ New entry"}
        </button>
      </div>

      {open ? (
        <article className="app-card">
          <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap", marginBottom: "0.75rem" }}>
            <label style={{ display: "flex", flexDirection: "column", gap: "0.25rem", fontSize: "var(--fs-xs)", fontWeight: 700, color: "var(--muted)", textTransform: "uppercase" }}>
              Date
              <input type="date" value={entryDate} onChange={(e) => setEntryDate(e.target.value)} style={{ ...inputStyle, width: "170px" }} />
            </label>
            <label style={{ display: "flex", flexDirection: "column", gap: "0.25rem", fontSize: "var(--fs-xs)", fontWeight: 700, color: "var(--muted)", textTransform: "uppercase", flex: 1, minWidth: "220px" }}>
              Memo
              <input
                type="text"
                value={memo}
                placeholder="e.g. July cloud infrastructure invoice"
                onChange={(e) => setMemo(e.target.value)}
                style={inputStyle}
              />
            </label>
          </div>

          <div style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  <th style={{ ...headStyle, minWidth: "200px" }}>Account</th>
                  <th style={headStyle}>Description</th>
                  <th style={{ ...headStyle, textAlign: "right", width: "130px" }}>Debit</th>
                  <th style={{ ...headStyle, textAlign: "right", width: "130px" }}>Credit</th>
                  <th style={{ ...headStyle, width: "40px" }} />
                </tr>
              </thead>
              <tbody>
                {lines.map((line, i) => (
                  <tr key={i}>
                    <td style={cellStyle}>
                      <select
                        value={line.account_code}
                        onChange={(e) => updateLine(i, "account_code", e.target.value)}
                        style={inputStyle}
                      >
                        <option value="">Select account…</option>
                        {accounts.map((a) => (
                          <option key={a.code} value={a.code}>
                            {a.code} · {a.name}
                          </option>
                        ))}
                      </select>
                    </td>
                    <td style={cellStyle}>
                      <input
                        type="text"
                        value={line.description}
                        placeholder="optional"
                        onChange={(e) => updateLine(i, "description", e.target.value)}
                        style={inputStyle}
                      />
                    </td>
                    <td style={cellStyle}>
                      <input
                        type="number"
                        min="0"
                        step="0.01"
                        value={line.debit}
                        onChange={(e) => updateLine(i, "debit", e.target.value)}
                        style={{ ...inputStyle, textAlign: "right" }}
                      />
                    </td>
                    <td style={cellStyle}>
                      <input
                        type="number"
                        min="0"
                        step="0.01"
                        value={line.credit}
                        onChange={(e) => updateLine(i, "credit", e.target.value)}
                        style={{ ...inputStyle, textAlign: "right" }}
                      />
                    </td>
                    <td style={{ ...cellStyle, textAlign: "center" }}>
                      <button
                        type="button"
                        onClick={() => removeLine(i)}
                        disabled={lines.length <= 2}
                        title="Remove line"
                        style={{
                          border: "none",
                          background: "transparent",
                          cursor: lines.length <= 2 ? "not-allowed" : "pointer",
                          color: lines.length <= 2 ? "var(--border)" : "#c0392b",
                          fontSize: "var(--fs-xl)",
                          lineHeight: 1
                        }}
                      >
                        ×
                      </button>
                    </td>
                  </tr>
                ))}
                <tr>
                  <td style={{ ...cellStyle, fontWeight: 800 }} colSpan={2}>
                    Totals
                  </td>
                  <td style={{ ...cellStyle, textAlign: "right", fontWeight: 800 }}>{money(totalDebit)}</td>
                  <td style={{ ...cellStyle, textAlign: "right", fontWeight: 800 }}>{money(totalCredit)}</td>
                  <td style={cellStyle} />
                </tr>
              </tbody>
            </table>
          </div>

          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "0.75rem", marginTop: "0.75rem" }}>
            <div style={{ display: "flex", gap: "0.75rem", alignItems: "center" }}>
              <button
                type="button"
                onClick={addLine}
                style={{
                  padding: "0.4rem 0.8rem",
                  borderRadius: "8px",
                  border: "1px solid var(--border)",
                  background: "transparent",
                  cursor: "pointer",
                  fontWeight: 700,
                  fontSize: "var(--fs-sm)"
                }}
              >
                + Add line
              </button>
              <span
                style={{
                  fontSize: "var(--fs-sm)",
                  fontWeight: 800,
                  color: balanced ? "var(--growth)" : "#c0392b"
                }}
              >
                {balanced ? "Balanced ✓" : `Out of balance by ${money(Math.abs(totalDebit - totalCredit))}`}
              </span>
            </div>
            <button
              type="button"
              onClick={submit}
              disabled={!canPost}
              style={{
                padding: "0.55rem 1.2rem",
                borderRadius: "999px",
                border: "none",
                background: canPost ? "var(--growth, #1f7a4d)" : "var(--border)",
                color: "#fff",
                fontWeight: 800,
                fontSize: "var(--fs-base)",
                cursor: canPost ? "pointer" : "not-allowed"
              }}
            >
              {posting ? "Posting…" : "Post entry"}
            </button>
          </div>

          {message ? (
            <p
              style={{
                marginTop: "0.75rem",
                fontSize: "var(--fs-sm)",
                fontWeight: 700,
                color: message.ok ? "var(--growth)" : "#c0392b"
              }}
            >
              {message.text}
            </p>
          ) : null}
        </article>
      ) : null}
    </section>
  );
}
