import { PlatformShell } from "@/components/platform-shell";
import { intelligenceReports, marketSignals } from "@/lib/platform-data";

export default function ReportsPage() {
  return (
    <PlatformShell
      eyebrow="John Henry Intelligence Center"
      title="Generate branded investment intelligence reports"
      description="Package macro signals, crypto cycles, acquisition screens, and dividend opportunities into subscriber-ready newsletters and PDF reports."
    >
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
          <h2>Signals available for report generation</h2>
        </div>
        <div className="app-grid app-grid--three">
          {marketSignals.map((signal) => (
            <article className="app-card" key={signal.name}>
              <span>{signal.name}</span>
              <strong>{signal.value}</strong>
              <p>{signal.insight}</p>
            </article>
          ))}
        </div>
      </section>
    </PlatformShell>
  );
}
