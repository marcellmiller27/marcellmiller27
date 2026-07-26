// JHI-SIG: 69M2705M | Opportunity Scan edition (cross-asset) | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { useEffect, useState } from "react";
import { editionDate, fetchQuotes, fmt, type QuoteMap } from "@/lib/newsletter-format";
import { EditorialByline } from "@/components/editorial-byline";
import { NewsletterDownloadButton } from "@/components/newsletter-download-button";
import { NewsletterMethodology } from "@/components/newsletter-methodology";
import { UpgradeGate } from "@/components/upgrade-gate";
import { useRole } from "@/components/role-provider";
import { canFullNewsletter } from "@/lib/roles";

type Idea = { assetClass: string; signal: string; thesis: string };

function buildScan(map: QuoteMap): Idea[] {
  const ten = map.UST10Y;
  const ff = map.FED_FUNDS;
  const gold = map.GOLD;
  const btc = map.BTC;

  return [
    {
      assetClass: "Fixed Income",
      signal: `10Y ${fmt(ten)}`,
      thesis:
        "Real yields near multi-year highs — intermediate Treasuries and investment-grade credit offer carry now and convexity if disinflation resumes. Ladder duration rather than reaching for it."
    },
    {
      assetClass: "Equities",
      signal: `Fed Funds ${fmt(ff)}`,
      thesis:
        "With policy restrictive, favor quality compounders and free-cash-flow yield over long-duration, unprofitable growth until the cutting cycle is confirmed."
    },
    {
      assetClass: "Real Assets",
      signal: `Gold ${fmt(gold)}`,
      thesis:
        "Gold's strength reflects fiscal and real-rate hedging demand. Pair it with cash-flowing real estate where cap rates have repriced to the new rate regime."
    },
    {
      assetClass: "Private Markets / SMB",
      signal: `Debt cost ~${fmt(ff)}+`,
      thesis:
        "Higher leverage costs pressure LBO math — the edge is in lower-leverage, cash-flowing small businesses acquired at disciplined multiples (JHI's core hunting ground)."
    },
    {
      assetClass: "Digital Assets",
      signal: `BTC ${fmt(btc)}`,
      thesis:
        "A high-beta read on liquidity — size positions to volatility and treat as a satellite, not a core holding, until policy eases."
    }
  ];
}

export function OpportunityScan() {
  const { role } = useRole();
  const [map, setMap] = useState<QuoteMap>({});
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    fetchQuotes()
      .then(({ map: m }) => {
        if (!active) return;
        setMap(m);
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

  if (loading) return <p className="rec-empty">Scanning asset classes for opportunities…</p>;
  if (error) return <p className="rec-empty">Unable to reach the data service ({error}).</p>;

  const full = canFullNewsletter(role);
  const allIdeas = buildScan(map);
  const ideas = full ? allIdeas : allIdeas.slice(0, 2);

  return (
    <article className="news">
      <NewsletterDownloadButton slug="opportunity-scan" />

      <header className="news__masthead">
        <p className="eyebrow">JHI Research &amp; Analytics · Opportunity Scan</p>
        <h2>Cross-Asset Opportunity Scan</h2>
        <p className="news__edition">Edition of {editionDate()}</p>
        <EditorialByline />
      </header>

      <section className="news__lede">
        <p>
          Where the current regime — restrictive policy, above-target inflation, and a resilient
          but softening consumer — is creating opportunity across asset classes.
        </p>
      </section>

      <div className="scan-grid">
        {ideas.map((idea) => (
          <article className="scan-card" key={idea.assetClass}>
            <div className="scan-card__head">
              <span className="scan-card__class">{idea.assetClass}</span>
              <span className="scan-card__signal">{idea.signal}</span>
            </div>
            <p className="scan-card__thesis">{idea.thesis}</p>
          </article>
        ))}
      </div>

      {!full && <UpgradeGate />}

      <NewsletterMethodology />

      <footer className="news__footer">
        <p>
          Prepared by JHI Research &amp; Analytics Firm, Inc. Ideas are generated from public data
          (FRED · BLS · market feeds), written in JHI&apos;s independent professional perspective.
        </p>
        <p className="news__disclaimer">
          For research and educational purposes only. Not investment, legal, tax, or accounting advice.
        </p>
      </footer>
    </article>
  );
}
