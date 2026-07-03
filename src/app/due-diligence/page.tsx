import { LiveValuations } from "@/components/live-valuations";
import { PlatformShell } from "@/components/platform-shell";
import { dueDiligenceQueue } from "@/lib/platform-data";

const uploadTypes = ["Tax returns", "P&L statements", "Balance sheets", "Bank statements"];

export default function DueDiligencePage() {
  return (
    <PlatformShell
      eyebrow="AI due diligence center"
      title="Analyze acquisition documents before capital is at risk"
      description="Upload financial records, normalize cash flow, detect risk indicators, and generate diligence questions for acquisition and lending decisions."
    >
      <section className="app-section app-section--split">
        <div>
          <p className="eyebrow">Document intake</p>
          <h2>Financial upload workflow</h2>
          <p>
            The production build will connect secure storage, document extraction, AI review, and
            analyst approval before generating recommendations.
          </p>
        </div>
        <div className="upload-grid">
          {uploadTypes.map((type) => (
            <article key={type}>
              <span>Upload</span>
              <strong>{type}</strong>
            </article>
          ))}
        </div>
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Live acquisition valuation</p>
          <h2>Modeled target value from live market inputs</h2>
        </div>
        <LiveValuations ebitda={1500000} />
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Sample diligence queue</p>
          <h2>Automated analysis results</h2>
        </div>
        <div className="table-card">
          {dueDiligenceQueue.map((item) => (
            <article className="table-row" key={item.document}>
              <div>
                <span>{item.status}</span>
                <strong>{item.document}</strong>
              </div>
              <p>{item.finding}</p>
              <div className={`risk risk--${item.risk.toLowerCase()}`}>{item.risk} risk</div>
            </article>
          ))}
        </div>
      </section>
    </PlatformShell>
  );
}
