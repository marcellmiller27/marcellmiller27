// JHI-SIG: 69M2705M | Terms of service (public) | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import { StorefrontShell } from "@/components/storefront-shell";

const bodyStyle = {
  maxWidth: "62rem",
  color: "var(--muted-strong)",
  fontSize: "var(--fs-md)",
  lineHeight: 1.7
} as const;

const sections = [
  {
    name: "Acceptance",
    detail:
      "By creating an account or using Aegira, you agree to these Terms. Aegira is operated by JHI Research & Analytics Firm, Inc. If you do not agree, do not use the platform."
  },
  {
    name: "The service",
    detail:
      "Aegira provides research, analytics, and decision-support tools by subscription. Features, plans, and pricing may change. We aim for high availability but do not guarantee uninterrupted or error-free service."
  },
  {
    name: "Not investment advice",
    detail:
      "All content is informational only and is not investment advice, a recommendation, or an offer to buy or sell any security. You are solely responsible for your decisions. See our Legal & Disclosures for the full disclaimer."
  },
  {
    name: "Subscriptions & billing",
    detail:
      "Plans are billed monthly or annually and can be cancelled anytime — no lock-in and no auto-renewal traps. Fees are charged in advance; access continues through the paid period after cancellation."
  },
  {
    name: "Acceptable use",
    detail:
      "You may not resell, scrape, reverse-engineer, or redistribute the platform or its data, misuse credentials, or attempt to disrupt or gain unauthorized access to the service. Accounts are for the named subscriber and permitted seats."
  },
  {
    name: "Limitation of liability",
    detail:
      "The service is provided \u201cas is.\u201d To the maximum extent permitted by law, JHI Research & Analytics Firm, Inc. is not liable for indirect or consequential damages, or for decisions made in reliance on platform output."
  }
];

export default function TermsPage() {
  return (
    <StorefrontShell
      eyebrow="Terms · Aegira"
      title="Terms of Service"
      description="The terms that govern your use of Aegira, a product of JHI Research & Analytics Firm, Inc."
    >
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Agreement</p>
          <h2>The terms of using Aegira.</h2>
        </div>
        <div className="trust-grid">
          {sections.map((s) => (
            <article className="trust-card" key={s.name}>
              <h3>{s.name}</h3>
              <p>{s.detail}</p>
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
          Review our <Link href="/privacy">Privacy Policy</Link> and{" "}
          <Link href="/legal">Legal &amp; Disclosures</Link>. Questions about these terms?
          Visit <Link href="/contact">Contact</Link> or email{" "}
          <a href="mailto:support@aegiraenterprise.com">support@aegiraenterprise.com</a>.
        </p>
        <p style={{ ...bodyStyle, marginTop: "1.25rem" }}>
          Aegira is a product of JHI Research &amp; Analytics Firm, Inc. · JHI-SIG: 69M2705M.
        </p>
      </section>
    </StorefrontShell>
  );
}
