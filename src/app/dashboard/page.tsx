// JHI-SIG: 69M2705M | Dashboard workspace (at-a-glance cockpit) | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { LiveMarket } from "@/components/live-market";
import {
  coverageStats,
  dashboardMetrics,
  watchlist
} from "@/lib/platform-data";

export default function DashboardPage() {
  return (
    <AppShell
      eyebrow="Overview"
      title="Dashboard"
      description="At-a-glance portfolio, watch list, and market signals."
    >
      <section className="app-grid app-grid--four">
        {dashboardMetrics.map((metric) => (
          <article className={`app-card app-card--${metric.tone}`} key={metric.label}>
            <span>{metric.label}</span>
            <strong>{metric.value}</strong>
            <p>{metric.change}</p>
          </article>
        ))}
      </section>

      <section className="app-grid app-grid--three" style={{ marginTop: "var(--space-5)" }}>
        <div className="rail-card">
          <p className="eyebrow">Coverage</p>
          <ul className="rail-stats">
            {coverageStats.map((stat) => (
              <li key={stat.label}>
                <span>{stat.label}</span>
                <strong>{stat.value}</strong>
              </li>
            ))}
          </ul>
        </div>

        <div className="rail-card">
          <div className="rail-card__head">
            <p className="eyebrow">Watch list</p>
            <Link href="/opportunities">View all</Link>
          </div>
          <ul className="rail-watch">
            {watchlist.map((item) => (
              <li key={item.name}>
                <span className={`rail-dot rail-dot--${item.tone}`} aria-hidden />
                <span className="rail-watch__body">
                  <span className="rail-watch__name">{item.name}</span>
                  <span className="rail-watch__meta">{item.meta}</span>
                </span>
              </li>
            ))}
          </ul>
        </div>

        <div className="rail-card">
          <p className="eyebrow">Market snapshot</p>
          <LiveMarket symbols="BTC,GOLD,SPX,UST10Y,INFLATION" />
        </div>
      </section>
    </AppShell>
  );
}
