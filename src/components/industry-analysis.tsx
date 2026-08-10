// JHI-SIG: 69M2705M | Industry Analysis (derived benchmarks) | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api/v1";

type Sector = {
  sector: string;
  gross_margin_pct: number;
  operating_margin_pct: number;
  net_margin_pct: number;
  revenue_growth_pct: number;
  ev_ebitda_multiple: number;
  note: string;
};

type Benchmarks = { sectors: Sector[]; basis: string; disclaimer: string };

export function IndustryAnalysis() {
  const [data, setData] = useState<Benchmarks | null>(null);

  useEffect(() => {
    fetch(`${API_BASE}/framework/industry-benchmarks`)
      .then((r) => r.json())
      .then(setData)
      .catch(() => setData(null));
  }, []);

  if (!data) return <p className="live-market__muted">Loading benchmarks…</p>;

  return (
    <div>
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Derived sector aggregates</p>
          <h2>Benchmark a target against its sector</h2>
        </div>
        <div className="table-card">
          <article className="table-row" style={{ fontWeight: 800, fontSize: "var(--fs-sm)" }}>
            <div style={{ minWidth: 220 }}>Sector</div>
            <div style={{ minWidth: 90 }}>Gross</div>
            <div style={{ minWidth: 90 }}>Operating</div>
            <div style={{ minWidth: 70 }}>Net</div>
            <div style={{ minWidth: 80 }}>Growth</div>
            <div style={{ minWidth: 100 }}>EV/EBITDA</div>
          </article>
          {data.sectors.map((s) => (
            <article className="table-row" key={s.sector}>
              <div style={{ minWidth: 220 }}>
                <strong>{s.sector}</strong>
                <span style={{ display: "block", fontSize: "var(--fs-xs, 0.72rem)" }} className="live-market__muted">
                  {s.note}
                </span>
              </div>
              <div style={{ minWidth: 90 }}>{s.gross_margin_pct}%</div>
              <div style={{ minWidth: 90 }}>{s.operating_margin_pct}%</div>
              <div style={{ minWidth: 70 }}>{s.net_margin_pct}%</div>
              <div style={{ minWidth: 80 }}>{s.revenue_growth_pct}%</div>
              <div style={{ minWidth: 100 }}>{s.ev_ebitda_multiple}×</div>
            </article>
          ))}
        </div>
        <p className="live-market__muted" style={{ fontSize: "var(--fs-sm)", marginTop: "0.6rem" }}>
          <strong>Basis:</strong> {data.basis}
        </p>
      </section>

      <div className="upgrade-gate">
        <p className="eyebrow">Go deeper</p>
        <h3>Compare a specific target to its sector</h3>
        <p>
          Compute the target&apos;s own margins and multiple with the ratios tool, then screen and
          value it against the sector with the Aegira platform.
        </p>
        <div className="upgrade-gate__actions">
          <Link className="button button--primary" href="/framework/ratios">
            Compute the ratios
          </Link>
          <Link className="button button--secondary" href="/opportunities">
            Open the Screener
          </Link>
        </div>
      </div>

      <p className="live-market__muted" style={{ fontSize: "var(--fs-sm)", marginTop: "0.8rem" }}>{data.disclaimer}</p>
    </div>
  );
}
