"use client";

import { useEffect, useState } from "react";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api/v1";

type Indicator = {
  key: string;
  label: string;
  value: number | null;
  unit: string;
  period: string | null;
  status: string;
  note?: string | null;
};

type MacroSeries = {
  source: string;
  country?: string | null;
  indicators: Indicator[];
};

type Quote = {
  symbol: string;
  name: string;
  price: number | null;
  unit: string;
  change_percent: number | null;
  status: string;
};

const MACRO_PANELS = [
  { path: "/macro/bea", title: "US National Accounts · BEA" },
  { path: "/macro/treasury", title: "US Treasury · Fiscal" },
  { path: "/macro/world-bank", title: "World Bank · WDI (US)" },
  { path: "/macro/imf", title: "IMF · WEO (US)" },
  { path: "/macro/oecd", title: "OECD · Leading Indicator (US)" },
];

const FRED_SYMBOLS =
  "GDP,FED_FUNDS,UNEMPLOYMENT,CONSUMER_CREDIT,CC_DELINQUENCY,RETAIL_SALES,CONSUMER_SENTIMENT,INDUSTRIAL_PRODUCTION";

function fmtValue(value: number | null, unit: string): string {
  if (value === null || value === undefined) return "—";
  if (unit === "%") return `${value.toFixed(2)}%`;
  if (unit === "index") return value.toFixed(1);
  let dollars: number | null = null;
  if (unit === "USD mn") dollars = value * 1e6;
  else if (unit === "USD" || unit === "USD bn") dollars = unit === "USD bn" ? value * 1e9 : value;
  if (dollars !== null) {
    const abs = Math.abs(dollars);
    if (abs >= 1e12) return `$${(dollars / 1e12).toFixed(2)}T`;
    if (abs >= 1e9) return `$${(dollars / 1e9).toFixed(2)}B`;
    if (abs >= 1e6) return `$${(dollars / 1e6).toFixed(1)}M`;
    return `$${dollars.toLocaleString("en-US", { maximumFractionDigits: 0 })}`;
  }
  return value.toLocaleString("en-US", { maximumFractionDigits: 0 });
}

function IndicatorRow({ indicator }: { indicator: Indicator }) {
  const ok = indicator.status === "ok";
  return (
    <div className="macro-row">
      <span className="macro-row__label">{indicator.label}</span>
      <span className="macro-row__value">
        {ok ? fmtValue(indicator.value, indicator.unit) : "—"}
        {indicator.period ? <span className="macro-row__period"> {indicator.period}</span> : null}
      </span>
    </div>
  );
}

export function LiveMacro() {
  const [panels, setPanels] = useState<MacroSeries[]>([]);
  const [fred, setFred] = useState<Quote[]>([]);
  const [updated, setUpdated] = useState<string>("");
  const [error, setError] = useState<string>("");

  useEffect(() => {
    let active = true;
    const load = () => {
      Promise.all(
        MACRO_PANELS.map((p) =>
          fetch(`${API_BASE}${p.path}`)
            .then((r) => (r.ok ? r.json() : null))
            .then((d) => (d ? { ...d, source: p.title } : null))
            .catch(() => null),
        ),
      ).then((results) => {
        if (!active) return;
        setPanels(results.filter(Boolean) as MacroSeries[]);
        setUpdated(new Date().toLocaleTimeString());
      });
      fetch(`${API_BASE}/market/quotes?symbols=${encodeURIComponent(FRED_SYMBOLS)}`)
        .then((r) => (r.ok ? r.json() : null))
        .then((d) => {
          if (active && d) setFred(d.quotes ?? []);
        })
        .catch(() => {
          if (active) setError("Some feeds are unavailable right now.");
        });
    };
    load();
    const timer = setInterval(load, 60000);
    return () => {
      active = false;
      clearInterval(timer);
    };
  }, []);

  return (
    <div>
      <p className="live-market__status">
        <span className={error ? "live-market__dot live-market__dot--off" : "live-market__dot"} />
        {updated ? `Live · updated ${updated}` : "Connecting to live feeds…"}
      </p>
      <div className="app-grid app-grid--three">
        <article className="app-card">
          <span>US Macro · FRED</span>
          <div className="macro-panel">
            {fred.length === 0 ? (
              <p className="live-market__muted">Loading…</p>
            ) : (
              fred.map((q) => (
                <div className="macro-row" key={q.symbol}>
                  <span className="macro-row__label">{q.name}</span>
                  <span className="macro-row__value">
                    {q.status === "ok" ? fmtValue(q.price, q.unit) : "—"}
                  </span>
                </div>
              ))
            )}
          </div>
        </article>

        {panels.map((panel) => (
          <article className="app-card" key={panel.source}>
            <span>{panel.source}</span>
            <div className="macro-panel">
              {panel.indicators.map((ind) => (
                <IndicatorRow indicator={ind} key={ind.key} />
              ))}
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
