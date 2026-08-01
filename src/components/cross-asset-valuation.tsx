"use client";
// JHI-SIG: 69M2705M | Cross-Asset Valuation module (equities, Phase 1) | JHI Research & Analytics Firm, Inc. (proprietary)
// On-screen DCF + expected-return + Enter/Accumulate/Sideline action, for a user-entered
// ticker and the large/mid-cap screen. Downloads the branded Excel workbook.
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Valuation = {
  ticker: string;
  name: string;
  price: number;
  market_cap: number;
  base_fcf: number;
  fcf_basis: string;
  growth_rate: number;
  terminal_growth: number;
  risk_free: number;
  equity_risk_premium: number;
  beta: number;
  discount_rate: number;
  projection_years: number;
  projected_fcf: number[];
  present_values: number[];
  terminal_value: number;
  pv_terminal_value: number;
  intrinsic_equity_value: number;
  intrinsic_per_share: number;
  upside_pct: number;
  expected_return: number;
  signal: string;
  rationale: string;
  sources: string[];
  disclaimer: string;
};

const pct = (x: number) => `${(x * 100).toFixed(1)}%`;
const usd = (x: number) =>
  x >= 1e12 ? `$${(x / 1e12).toFixed(2)}T` : x >= 1e9 ? `$${(x / 1e9).toFixed(2)}B` : x >= 1e6 ? `$${(x / 1e6).toFixed(1)}M` : `$${x.toFixed(2)}`;
const signalClass = (s: string) =>
  s === "Enter" ? "val-signal--enter" : s === "Sideline" ? "val-signal--sideline" : "val-signal--hold";

export function CrossAssetValuation() {
  const [ticker, setTicker] = useState("AAPL");
  const [data, setData] = useState<Valuation | null>(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  const [universe, setUniverse] = useState<Valuation[]>([]);

  useEffect(() => {
    let active = true;
    apiFetch("/valuation/equity?n=8")
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`))))
      .then((d: Valuation[]) => active && setUniverse(d))
      .catch(() => active && setUniverse([]));
    return () => {
      active = false;
    };
  }, []);

  async function run(sym: string) {
    const t = sym.trim().toUpperCase();
    if (!t) return;
    setBusy(true);
    setErr("");
    setData(null);
    try {
      const r = await apiFetch(`/valuation/equity/${encodeURIComponent(t)}`);
      if (!r.ok) {
        const d = await r.json().catch(() => ({}));
        throw new Error(typeof d.detail === "string" ? d.detail : `Request failed (${r.status})`);
      }
      setData(await r.json());
    } catch (e) {
      setErr(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      setBusy(false);
    }
  }

  async function downloadWorkbook() {
    if (!data) return;
    try {
      const r = await apiFetch(`/valuation/equity/${encodeURIComponent(data.ticker)}/xlsx`);
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const blob = await r.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `Aegira_${data.ticker}_DCF_Valuation.xlsx`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch {
      setErr("Could not download the workbook.");
    }
  }

  return (
    <div className="valuation">
      <form
        className="valuation__search"
        onSubmit={(e) => {
          e.preventDefault();
          run(ticker);
        }}
      >
        <label htmlFor="val-ticker">Ticker</label>
        <input
          id="val-ticker"
          name="ticker"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          placeholder="e.g. AAPL, MSFT, CAT"
          autoComplete="off"
        />
        <button type="submit" className="button button--primary" disabled={busy}>
          {busy ? "Valuing…" : "Value it →"}
        </button>
      </form>

      {err && <p className="auth-form__err">{err}</p>}

      {data && (
        <article className="val-card">
          <header className="val-card__head">
            <div>
              <h3>
                {data.name} <span className="val-card__tkr">{data.ticker}</span>
              </h3>
              <p className="val-card__sub">
                Price {usd(data.price)} · Intrinsic {usd(data.intrinsic_per_share)}/share · Market cap{" "}
                {usd(data.market_cap)}
              </p>
            </div>
            <span className={`val-signal ${signalClass(data.signal)}`}>{data.signal}</span>
          </header>

          <div className="val-metrics">
            <div>
              <span className="val-metrics__k">Margin of safety</span>
              <strong className={data.upside_pct >= 0 ? "val-pos" : "val-neg"}>{pct(data.upside_pct)}</strong>
            </div>
            <div>
              <span className="val-metrics__k">Implied expected return</span>
              <strong>{pct(data.expected_return)}</strong>
            </div>
            <div>
              <span className="val-metrics__k">Discount rate</span>
              <strong>{pct(data.discount_rate)}</strong>
            </div>
            <div>
              <span className="val-metrics__k">Growth (yrs 1–{data.projection_years})</span>
              <strong>{pct(data.growth_rate)}</strong>
            </div>
          </div>

          <p className="val-rationale">{data.rationale}</p>

          <details className="val-details">
            <summary>DCF assumptions &amp; projection</summary>
            <ul className="val-assumptions">
              <li>Base FCF: {usd(data.base_fcf)} — {data.fcf_basis}</li>
              <li>Risk-free (10Y): {pct(data.risk_free)} · ERP: {pct(data.equity_risk_premium)} · Beta: {data.beta.toFixed(2)}</li>
              <li>Terminal growth: {pct(data.terminal_growth)}</li>
            </ul>
            <table className="val-table">
              <thead>
                <tr>
                  <th>Year</th>
                  <th>Projected FCF</th>
                  <th>Present value</th>
                </tr>
              </thead>
              <tbody>
                {data.projected_fcf.map((f, i) => (
                  <tr key={i}>
                    <td>Year {i + 1}</td>
                    <td>{usd(f)}</td>
                    <td>{usd(data.present_values[i])}</td>
                  </tr>
                ))}
                <tr>
                  <td>Terminal value</td>
                  <td>{usd(data.terminal_value)}</td>
                  <td>{usd(data.pv_terminal_value)}</td>
                </tr>
                <tr className="val-table__total">
                  <td>Intrinsic equity value</td>
                  <td colSpan={2}>{usd(data.intrinsic_equity_value)}</td>
                </tr>
              </tbody>
            </table>
          </details>

          <div className="val-card__actions">
            <button type="button" className="button button--primary" onClick={downloadWorkbook}>
              Download Excel workbook
            </button>
          </div>
          <p className="news__source">{data.disclaimer}</p>
        </article>
      )}

      <section className="val-universe">
        <h3>Top of the screen — largest margin of safety</h3>
        <p className="news__source">
          Large/mid-cap US equities valued on the same DCF and ranked by upside. Research, not advice.
        </p>
        {universe.length === 0 ? (
          <p className="rec-empty">Loading the screen…</p>
        ) : (
          <table className="val-table val-table--rank">
            <thead>
              <tr>
                <th>Ticker</th>
                <th>Name</th>
                <th>Price</th>
                <th>Intrinsic</th>
                <th>Upside</th>
                <th>Signal</th>
              </tr>
            </thead>
            <tbody>
              {universe.map((u) => (
                <tr key={u.ticker} onClick={() => { setTicker(u.ticker); run(u.ticker); }} className="val-row">
                  <td><strong>{u.ticker}</strong></td>
                  <td>{u.name}</td>
                  <td>{usd(u.price)}</td>
                  <td>{usd(u.intrinsic_per_share)}</td>
                  <td className={u.upside_pct >= 0 ? "val-pos" : "val-neg"}>{pct(u.upside_pct)}</td>
                  <td><span className={`val-signal val-signal--sm ${signalClass(u.signal)}`}>{u.signal}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
}
