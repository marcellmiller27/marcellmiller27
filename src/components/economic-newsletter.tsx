// JHI-SIG: 69M2705M | Economic Tracking newsletter (auto-generated) | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { useEffect, useState } from "react";
import {
  editionDate,
  fetchQuotes,
  fmt,
  type QuoteMap
} from "@/lib/newsletter-format";
import { EditorialByline } from "@/components/editorial-byline";

type Section = { heading: string; blurb: string; symbols: string[] };

// Grouping of the polled indicators into an institutional newsletter structure.
const SECTIONS: Section[] = [
  {
    heading: "Monetary Policy & Rates",
    blurb: "The policy rate and the long end frame the cost of capital across the economy.",
    symbols: ["FED_FUNDS", "UST10Y"]
  },
  {
    heading: "Inflation",
    blurb: "The pace of price growth relative to the Federal Reserve's 2% objective.",
    symbols: ["INFLATION"]
  },
  {
    heading: "Labor & the Consumer",
    blurb: "Employment slack and household demand — the engine of two-thirds of output.",
    symbols: ["UNEMPLOYMENT", "RETAIL_SALES", "CONSUMER_SENTIMENT"]
  },
  {
    heading: "Growth & Output",
    blurb: "Aggregate activity and the industrial base.",
    symbols: ["GDP", "INDUSTRIAL_PRODUCTION"]
  },
  {
    heading: "Markets",
    blurb: "Cross-asset read on risk appetite and safe-haven demand.",
    symbols: ["SPX", "GOLD", "BTC"]
  }
];

const ALL_SYMBOLS = Array.from(new Set(SECTIONS.flatMap((s) => s.symbols))).join(",");

// JHI professional-voice commentary, derived deterministically from the data.
function commentary(symbol: string, v: number | null): string {
  if (v === null) return "Awaiting the next release.";
  switch (symbol) {
    case "FED_FUNDS":
      return v >= 4
        ? "A restrictive stance that continues to weigh on rate-sensitive demand."
        : v >= 2.5
          ? "A moderately restrictive stance; policy is not yet neutral."
          : "An accommodative stance supportive of credit and risk assets.";
    case "UST10Y":
      return v >= 4.5
        ? "Long rates remain elevated, keeping borrowing costs and discount rates high."
        : "Long rates are easing, a tailwind for valuations and refinancing.";
    case "INFLATION":
      return v <= 2.5
        ? "At or near the Fed's 2% target — consistent with an easing bias."
        : v <= 4
          ? "Running above the 2% target; the last mile of disinflation is proving sticky."
          : "Elevated and above target, constraining the path to rate cuts.";
    case "UNEMPLOYMENT":
      return v < 4.5
        ? "The labor market remains firm, underpinning consumer resilience."
        : v <= 5.5
          ? "A softening labor market that bears watching for demand risk."
          : "A weak labor market signaling cyclical downside.";
    case "RETAIL_SALES":
      return "Headline household spending — the clearest read on consumer demand.";
    case "CONSUMER_SENTIMENT":
      return v < 60
        ? "Subdued sentiment; households remain cautious despite steady spending."
        : "Improving sentiment supports the demand outlook.";
    case "GDP":
      return "Aggregate output; the denominator for leverage, valuation and deficit ratios.";
    case "INDUSTRIAL_PRODUCTION":
      return "The industrial base — a cyclical tell for goods demand and capex.";
    case "SPX":
      return "Broad equity risk appetite and the equity cost of capital.";
    case "GOLD":
      return "Safe-haven demand and a hedge against real-rate and fiscal risk.";
    case "BTC":
      return "A high-beta read on liquidity and speculative risk appetite.";
    default:
      return "";
  }
}

function headline(map: QuoteMap): string {
  const ff = map.FED_FUNDS?.price;
  const cpi = map.INFLATION?.price;
  const un = map.UNEMPLOYMENT?.price;
  const stance = ff == null ? "current" : ff >= 4 ? "restrictive" : ff >= 2.5 ? "moderately restrictive" : "accommodative";
  const infl = cpi == null ? "" : cpi <= 2.5 ? "with inflation back near target" : `with inflation at ${cpi.toFixed(1)}%, still above the 2% target`;
  const labor = un == null ? "" : un < 4.5 ? "and the labor market holding firm" : "as the labor market softens";
  return `Policy remains ${stance} ${infl} ${labor}. The picture below balances a resilient consumer against still-elevated financing costs — the central tension for allocators and acquirers this cycle.`;
}

export function EconomicNewsletter() {
  const [map, setMap] = useState<QuoteMap>({});
  const [asOf, setAsOf] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    fetchQuotes(ALL_SYMBOLS)
      .then(({ map: m, asOf: a }) => {
        if (!active) return;
        setMap(m);
        setAsOf(a);
        setLoading(false);
      })
      .catch((e) => {
        if (!active) return;
        setError(String(e.message ?? e));
        setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  const edition = editionDate();

  if (loading) return <p className="rec-empty">Generating the latest edition from live data…</p>;
  if (error)
    return <p className="rec-empty">Unable to reach the data service ({error}). Try again shortly.</p>;

  return (
    <article className="news">
      <div className="news__actions">
        <button type="button" className="button button--secondary" onClick={() => window.print()}>
          Print / Save as PDF
        </button>
      </div>

      <header className="news__masthead">
        <p className="eyebrow">JHI Research &amp; Analytics · Economic Tracking</p>
        <h2>The Economic Brief</h2>
        <p className="news__edition">Edition of {edition}</p>
        <EditorialByline />
      </header>

      <section className="news__lede">
        <h3>Executive summary</h3>
        <p>{headline(map)}</p>
      </section>

      {SECTIONS.map((section) => (
        <section className="news__section" key={section.heading}>
          <h3>{section.heading}</h3>
          <p className="news__blurb">{section.blurb}</p>
          <ul className="news__rows">
            {section.symbols.map((sym) => {
              const q = map[sym];
              if (!q) return null;
              return (
                <li className="news__row" key={sym}>
                  <div className="news__row-head">
                    <span className="news__metric">{q.name}</span>
                    <strong className="news__value">{fmt(q)}</strong>
                  </div>
                  <p className="news__note">{commentary(sym, q.price)}</p>
                  {q.note ? <p className="news__source">{q.note}</p> : null}
                </li>
              );
            })}
          </ul>
        </section>
      ))}

      <footer className="news__footer">
        <p>
          Prepared by JHI Research &amp; Analytics Firm, Inc. Sourced from public data —
          Federal Reserve (FRED), U.S. Bureau of Labor Statistics, and market feeds. Figures
          are as last released; as of {new Date(asOf).toLocaleString("en-US")}.
        </p>
        <p className="news__disclaimer">
          For research and educational purposes only. Not investment, legal, tax, or
          accounting advice. Written in JHI&apos;s independent professional perspective.
        </p>
      </footer>
    </article>
  );
}
