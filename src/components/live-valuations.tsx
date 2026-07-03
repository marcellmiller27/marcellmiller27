"use client";
// JHI-SIG: 69M2705M | Valuations | John Henry Investments (proprietary)

import { useEffect, useState } from "react";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

type Estimate = {
  asset_class: string;
  method: string;
  estimated_value: number | null;
  unit: string;
  live_inputs: Record<string, number>;
  assumptions: Record<string, number>;
  status: string;
  note: string | null;
};
type Report = { as_of: string; disclaimer: string; estimates: Estimate[] };

function fmt(value: number | null): string {
  if (value === null) return "—";
  if (Math.abs(value) >= 1000)
    return value.toLocaleString("en-US", { maximumFractionDigits: 0 });
  return value.toFixed(2);
}

export function LiveValuations({
  noi = 100000,
  ebitda = 1000000,
  peCommitted = 1000000
}: {
  noi?: number;
  ebitda?: number;
  peCommitted?: number;
}) {
  const [report, setReport] = useState<Report | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    const qs = `noi=${noi}&ebitda=${ebitda}&pe_committed=${peCommitted}`;
    const pull = () =>
      fetch(`${API_BASE}/valuations/estimate?${qs}`)
        .then((r) => {
          if (!r.ok) throw new Error(String(r.status));
          return r.json();
        })
        .then((data) => {
          if (!active) return;
          setReport(data);
          setError("");
        })
        .catch(() => active && setError("Live modeled valuations are unavailable right now."));
    pull();
    const timer = setInterval(pull, 60000);
    return () => {
      active = false;
      clearInterval(timer);
    };
  }, [noi, ebitda, peCommitted]);

  if (error) {
    return (
      <p className="live-market__status">
        <span className="live-market__dot live-market__dot--off" />
        {error}
      </p>
    );
  }
  if (!report) {
    return (
      <p className="live-market__status">
        <span className="live-market__dot" />
        Modeling valuations from live inputs…
      </p>
    );
  }

  return (
    <div>
      <p className="live-market__status">
        <span className="live-market__dot" />
        Live · modeled from public market inputs
      </p>
      <div className="app-grid app-grid--three">
        {report.estimates.map((est) => (
          <article className="app-card" key={est.asset_class}>
            <span>{est.asset_class}</span>
            <strong>
              {est.estimated_value === null ? "—" : `$${fmt(est.estimated_value)}`}
            </strong>
            <p>{est.method}</p>
            {est.note ? (
              <p className="live-market__muted" style={{ fontSize: "0.8rem" }}>
                {est.note}
              </p>
            ) : null}
          </article>
        ))}
      </div>
      <p className="live-market__muted" style={{ fontSize: "0.78rem", marginTop: "0.75rem" }}>
        {report.disclaimer}
      </p>
    </div>
  );
}
