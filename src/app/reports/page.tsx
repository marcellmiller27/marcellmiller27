import { LiveMarket } from "@/components/live-market";
import { LiveReports } from "@/components/live-reports";
import { PlatformShell } from "@/components/platform-shell";
import { intelligenceReports } from "@/lib/platform-data";

export default function ReportsPage() {
  return (
    <PlatformShell
      eyebrow="John Henry Intelligence Center"
      title="Generate branded investment intelligence reports"
      description="Package macro signals, crypto cycles, acquisition screens, and dividend opportunities into subscriber-ready newsletters and PDF reports."
    >
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Live financials</p>
          <h2>Executive snapshot &amp; income statement</h2>
        </div>
        <LiveReports />
      </section>

      <section className="app-grid app-grid--two">
        {intelligenceReports.map((report) => (
          <article className="report-card" key={report.title}>
            <div>
              <span>{report.cadence}</span>
              <h2>{report.title}</h2>
              <p>{report.audience}</p>
            </div>
            <ul>
              {report.highlights.map((highlight) => (
                <li key={highlight}>{highlight}</li>
              ))}
            </ul>
            <button type="button">Generate report preview</button>
          </article>
        ))}
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Macro dashboard feed</p>
          <h2>Live signals available for report generation</h2>
        </div>
        <LiveMarket symbols="SPX,UST10Y,GOLD,BTC,INFLATION" />
      </section>
    </PlatformShell>
  );
}
