// JHI-SIG: 69M2705M | Legal & disclosures (public) | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import { StorefrontShell } from "@/components/storefront-shell";

const bodyStyle = {
  maxWidth: "62rem",
  color: "var(--muted-strong)",
  fontSize: "var(--fs-md)",
  lineHeight: 1.7
} as const;

const disclosures = [
  {
    name: "Research, not advice",
    detail:
      "Aegira provides research, analytics, and decision-support tools. Nothing on the platform is investment advice, a recommendation, a solicitation, or an offer to buy or sell any security or other instrument. We are not a broker-dealer, investment adviser, or fiduciary. Consult a licensed professional before making any decision."
  },
  {
    name: "Informational purposes only",
    detail:
      "Scores, valuations, screens, and other outputs are estimates generated from data and published methodologies. They may contain errors, become stale, or prove inaccurate. You are solely responsible for your own decisions and for verifying any figure before you rely on it."
  },
  {
    name: "Data & provenance",
    detail:
      "Market and fundamentals data are sourced from third-party and licensed providers and presented on a point-in-time basis. Aegira does not guarantee the accuracy, completeness, or timeliness of any data, and is not liable for provider errors or delays."
  },
  {
    name: "AI-assisted content",
    detail:
      "Some content is authored with AI under human direction. AI elevates writing but does not invent figures; numbers are locked to underlying data with provenance. Automated output can still be wrong — treat it as one input, not a final answer."
  },
  {
    name: "Third-party CPA work",
    detail:
      "Formal Quality-of-Earnings and attest engagements are delivered by licensed partner CPA firms, not by Aegira. Software-accelerated analyses on the platform are decision-support tools and are not a substitute for a signed professional engagement."
  }
];

export default function LegalPage() {
  return (
    <StorefrontShell
      eyebrow="Legal · Aegira"
      title="Legal & disclosures"
      description="The important disclosures that govern your use of Aegira. Aegira is a product of JHI Research & Analytics Firm, Inc."
    >
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Disclosures</p>
          <h2>What Aegira is — and is not.</h2>
        </div>
        <div className="trust-grid">
          {disclosures.map((d) => (
            <article className="trust-card" key={d.name}>
              <h3>{d.name}</h3>
              <p>{d.detail}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">More</p>
          <h2>Related policies.</h2>
        </div>
        <p style={bodyStyle}>
          See our <Link href="/privacy">Privacy Policy</Link> and{" "}
          <Link href="/terms">Terms of Service</Link> for the full terms that govern your
          account and your use of the platform. Questions? Visit{" "}
          <Link href="/contact">Contact</Link> or email{" "}
          <a href="mailto:support@aegiraenterprise.com">support@aegiraenterprise.com</a>.
        </p>
        <p style={{ ...bodyStyle, marginTop: "1.25rem" }}>
          Aegira is a product of JHI Research &amp; Analytics Firm, Inc. · JHI-SIG: 69M2705M.
        </p>
      </section>
    </StorefrontShell>
  );
}
