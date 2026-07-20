// JHI-SIG: 69M2705M | Dashboard workspace (launchpad + at-a-glance) | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import {
  ArrowUpRight,
  BarChart3,
  Briefcase,
  Calculator,
  Download,
  FileSearch,
  FileText,
  ScanSearch,
  Search,
  Sparkles,
  Workflow,
  type LucideIcon
} from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { LiveMarket } from "@/components/live-market";
import {
  coverageStats,
  dashboardLaunchpad,
  dashboardMetrics,
  watchlist
} from "@/lib/platform-data";

// Map each launchpad context to its line icon (shares the TOC iconography).
const launchIcons: Record<string, LucideIcon> = {
  Economics: BarChart3,
  Screener: Search,
  Reports: FileText,
  Scope: ScanSearch,
  Earnings: Calculator,
  "Document Review": FileSearch,
  Pipeline: Workflow,
  Portfolio: Briefcase,
  "Ask JHI": Sparkles,
  Documents: Download
};

export default function DashboardPage() {
  return (
    <AppShell
      eyebrow="Overview"
      title="Command center"
      description="Your launchpad into research, diligence and deal workflow — with portfolio, watch list and macro at a glance."
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

      <div className="dash-workspace">
        <div className="dash-main">
          {dashboardLaunchpad.map((group) => (
            <section className="launch-group" key={group.section}>
              <p className="eyebrow">{group.section}</p>
              <div className="launch-grid">
                {group.items.map((item) => {
                  const Icon = launchIcons[item.label] ?? ArrowUpRight;
                  return (
                    <Link className="launch-card" href={item.href} key={item.href}>
                      <span className="launch-card__icon">
                        <Icon size={20} strokeWidth={1.75} aria-hidden />
                      </span>
                      <span className="launch-card__body">
                        <span className="launch-card__title">
                          <h3>{item.label}</h3>
                          <ArrowUpRight className="launch-card__go" size={15} aria-hidden />
                        </span>
                        <p>{item.blurb}</p>
                        <span className="launch-card__meta">{item.meta}</span>
                      </span>
                    </Link>
                  );
                })}
              </div>
            </section>
          ))}
        </div>

        <aside className="dash-rail" aria-label="At a glance">
          <section className="rail-card">
            <p className="eyebrow">Coverage</p>
            <ul className="rail-stats">
              {coverageStats.map((stat) => (
                <li key={stat.label}>
                  <span>{stat.label}</span>
                  <strong>{stat.value}</strong>
                </li>
              ))}
            </ul>
          </section>

          <section className="rail-card">
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
          </section>

          <section className="rail-card">
            <p className="eyebrow">Market snapshot</p>
            <LiveMarket symbols="BTC,GOLD,SPX,UST10Y,INFLATION" />
          </section>
        </aside>
      </div>
    </AppShell>
  );
}
