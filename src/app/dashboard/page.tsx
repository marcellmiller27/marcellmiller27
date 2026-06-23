import { PlatformShell } from "@/components/platform-shell";
import {
  dashboardMetrics,
  dashboardWidgets,
  marketSignals,
  opportunities
} from "@/lib/platform-data";

export default function DashboardPage() {
  const topOpportunities = opportunities.slice(0, 3);

  return (
    <PlatformShell
      eyebrow="Core platform"
      title="Investor command center"
      description="Monitor portfolio value, market alerts, economic indicators, acquisition opportunities, and AI recommendations from one operating dashboard."
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

      <section className="app-section app-section--split">
        <div>
          <p className="eyebrow">Market watch</p>
          <h2>Live intelligence widgets</h2>
          <div className="widget-strip">
            {dashboardWidgets.map((widget) => (
              <span key={widget}>{widget}</span>
            ))}
          </div>
        </div>
        <div className="signal-list">
          {marketSignals.map((signal) => (
            <article className="signal-card" key={signal.name}>
              <div>
                <span>{signal.name}</span>
                <strong>{signal.value}</strong>
              </div>
              <p>{signal.insight}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">AI recommendations</p>
          <h2>Highest priority opportunities</h2>
        </div>
        <div className="app-grid app-grid--three">
          {topOpportunities.map((opportunity) => (
            <article className="app-card" key={opportunity.name}>
              <span>{opportunity.category}</span>
              <strong>{opportunity.score}</strong>
              <h3>{opportunity.name}</h3>
              <p>{opportunity.thesis}</p>
              <div className="recommendation">{opportunity.recommendation}</div>
            </article>
          ))}
        </div>
      </section>
    </PlatformShell>
  );
}
