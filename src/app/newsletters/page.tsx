// JHI-SIG: 69M2705M | Newsletters index | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { NewsletterSubscribe } from "@/components/newsletter-subscribe";

type Edition = { href: string; name: string; cadence: string; blurb: string; ready: boolean };

const EDITIONS: Edition[] = [
  {
    href: "/newsletters/economic-brief",
    name: "The Economic Brief",
    cadence: "Recurring update",
    blurb: "The standing read on the economy and markets — policy, inflation, labor, growth, and cross-asset markets.",
    ready: true
  },
  {
    href: "/newsletters/red-alerts",
    name: "Red Alerts",
    cadence: "Time-sensitive",
    blurb: "Threshold-triggered signals when the data trips a line worth acting on — rate moves, inflation, dislocations.",
    ready: true
  },
  {
    href: "/newsletters/opportunity-scan",
    name: "Cross-Asset Opportunity Scan",
    cadence: "Recurring / triggered",
    blurb: "Idea generation across equities, credit, real assets, private markets, and digital assets.",
    ready: true
  },
  {
    href: "/newsletters",
    name: "Insider Briefs",
    cadence: "As-warranted",
    blurb: "Deep-dive analysis on a theme, sector, or target — the depth mandate. Coming soon.",
    ready: false
  }
];

export default function NewslettersPage() {
  return (
    <AppShell
      eyebrow="Reports"
      title="Newsletters"
      description="Published intelligence, auto-generated from the data we poll and written in JHI's professional perspective by the VP of Editorial. Read on-platform or export to PDF."
    >
      <div className="app-grid app-grid--two">
        {EDITIONS.map((e) => (
          <article className="app-card" key={e.name}>
            <span>{e.cadence}</span>
            <h3>{e.name}</h3>
            <p>{e.blurb}</p>
            {e.ready ? (
              <Link className="opportunity-card__link" href={e.href}>
                Generate / read →
              </Link>
            ) : (
              <span className="news__source">In development</span>
            )}
          </article>
        ))}
      </div>

      <p className="news__source" style={{ marginTop: "0.75rem" }}>
        Previous editions are archived weekly — free registrants can open any edition as a
        preview; subscribers (Tier 1–3) get the full archive. Rolling out with email delivery.
      </p>

      <section className="app-section">
        <NewsletterSubscribe />
      </section>
    </AppShell>
  );
}
