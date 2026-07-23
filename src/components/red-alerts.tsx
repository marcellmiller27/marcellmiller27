// JHI-SIG: 69M2705M | Red Alerts edition (threshold-triggered) | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { useEffect, useState } from "react";
import { editionDate, fetchQuotes, type QuoteMap } from "@/lib/newsletter-format";
import { EditorialByline } from "@/components/editorial-byline";
import { NewsletterDownloadButton } from "@/components/newsletter-download-button";
import { UpgradeGate } from "@/components/upgrade-gate";
import { useRole } from "@/components/role-provider";
import { canFullNewsletter } from "@/lib/roles";

type Severity = "High" | "Medium" | "Low";
type Alert = { severity: Severity; title: string; detail: string; classes: string[] };

const RANK: Record<Severity, number> = { High: 0, Medium: 1, Low: 2 };

// Deterministic, threshold-triggered alerts derived from the live feed.
function buildAlerts(map: QuoteMap): Alert[] {
  const alerts: Alert[] = [];
  const price = (s: string) => map[s]?.price ?? null;

  const cpi = price("INFLATION");
  if (cpi != null && cpi > 3)
    alerts.push({
      severity: cpi > 4 ? "High" : "Medium",
      title: `Inflation elevated at ${cpi.toFixed(2)}%`,
      detail:
        "Above the 3% line — the last mile of disinflation is stalling, constraining the Fed's room to cut and pressuring long-duration valuations.",
      classes: ["Rates", "Equities", "Fixed income"]
    });

  const ff = price("FED_FUNDS");
  if (ff != null && ff >= 4)
    alerts.push({
      severity: "Medium",
      title: `Policy restrictive — Fed Funds at ${ff.toFixed(2)}%`,
      detail:
        "Financing costs stay high; rate-sensitive sectors, leverage-dependent deals, and refinancings remain under pressure.",
      classes: ["Private markets", "Real assets", "Equities"]
    });

  const ten = price("UST10Y");
  if (ten != null && ten >= 4.5)
    alerts.push({
      severity: "Medium",
      title: `Long rates elevated — 10Y at ${ten.toFixed(2)}%`,
      detail:
        "Higher discount rates compress valuations and raise the bar for new capital; watch duration exposure and cap-rate expansion.",
      classes: ["Fixed income", "Real assets", "Equities"]
    });

  const un = price("UNEMPLOYMENT");
  if (un != null && un >= 4.5)
    alerts.push({
      severity: un >= 5.5 ? "High" : "Medium",
      title: `Labor softening — unemployment at ${un.toFixed(2)}%`,
      detail:
        "A rising jobless rate flags cyclical demand risk to consumer spending, credit performance, and small-business cash flows.",
      classes: ["Equities", "Credit", "Private markets"]
    });

  const sent = price("CONSUMER_SENTIMENT");
  if (sent != null && sent < 60)
    alerts.push({
      severity: "Low",
      title: `Subdued consumer sentiment (${sent.toFixed(1)})`,
      detail:
        "Cautious households can foreshadow softer discretionary demand even while headline spending holds.",
      classes: ["Equities", "Consumer"]
    });

  for (const sym of ["SPX", "GOLD", "BTC", "UST10Y"]) {
    const q = map[sym];
    const chg = q?.change_percent;
    if (q && chg != null && Math.abs(chg) >= 2)
      alerts.push({
        severity: Math.abs(chg) >= 4 ? "High" : "Medium",
        title: `${q.name} moved ${chg > 0 ? "+" : ""}${chg.toFixed(1)}% on the session`,
        detail: `A sharp ${chg > 0 ? "advance" : "decline"} signals a shift in risk appetite worth monitoring for follow-through.`,
        classes: ["Markets"]
      });
  }

  return alerts.sort((a, b) => RANK[a.severity] - RANK[b.severity]);
}

export function RedAlerts() {
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

  if (loading) return <p className="rec-empty">Scanning the live feed for triggered alerts…</p>;
  if (error) return <p className="rec-empty">Unable to reach the data service ({error}).</p>;

  const full = canFullNewsletter(role);
  const allAlerts = buildAlerts(map);
  const alerts = full ? allAlerts : allAlerts.slice(0, 1);

  return (
    <article className="news">
      <NewsletterDownloadButton slug="red-alerts" />

      <header className="news__masthead">
        <p className="eyebrow">JHI Research &amp; Analytics · Red Alerts</p>
        <h2>Red Alerts</h2>
        <p className="news__edition">Edition of {editionDate()}</p>
        <EditorialByline />
      </header>

      {alerts.length === 0 ? (
        <p className="rec-empty">
          All clear — no red alerts. Tracked indicators are within normal bands.
        </p>
      ) : (
        <ul className="alert-list">
          {alerts.map((a, i) => (
            <li className={`alert alert--${a.severity.toLowerCase()}`} key={i}>
              <div className="alert__head">
                <span className="alert__sev">{a.severity}</span>
                <strong className="alert__title">{a.title}</strong>
              </div>
              <p className="alert__detail">{a.detail}</p>
              <div className="output-tags">
                {a.classes.map((c) => (
                  <span className="tag" key={c}>
                    {c}
                  </span>
                ))}
              </div>
            </li>
          ))}
        </ul>
      )}

      {!full && allAlerts.length > 0 && <UpgradeGate />}

      <footer className="news__footer">
        <p>
          Prepared by JHI Research &amp; Analytics Firm, Inc. Triggered from public data
          (FRED · BLS · market feeds). Thresholds are indicative, not trading signals.
        </p>
        <p className="news__disclaimer">
          For research and educational purposes only. Not investment, legal, tax, or accounting advice.
        </p>
      </footer>
    </article>
  );
}
