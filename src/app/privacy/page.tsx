// JHI-SIG: 69M2705M | Privacy policy (public) | JHI Research & Analytics Firm, Inc. (proprietary)
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
    name: "What we collect",
    detail:
      "Account details (name, email, organization), billing information processed by our payment provider, and usage data such as pages viewed and features used. We collect only what we need to operate the platform and improve it."
  },
  {
    name: "How we use it",
    detail:
      "To provide and secure your account, deliver research and analytics, process payments, respond to support requests, and communicate service and product updates. We do not sell your personal information."
  },
  {
    name: "Data security",
    detail:
      "We apply a national-security discipline to the financial data our subscribers trust us with: encryption in transit and at rest, least-privilege access, and audit logging. Sensitive credentials (for example, wallet private keys) are never stored."
  },
  {
    name: "Your choices",
    detail:
      "You can access, correct, export, or delete your account data, and opt out of non-essential communications, by contacting us. We retain data only as long as needed to provide the service and meet legal obligations."
  },
  {
    name: "Third parties",
    detail:
      "We use vetted providers for hosting, payments, and market data. They process data on our behalf under contractual and confidentiality obligations, and only for the purposes we specify."
  }
];

export default function PrivacyPage() {
  return (
    <StorefrontShell
      eyebrow="Privacy · Aegira"
      title="Privacy Policy"
      description="How JHI Research & Analytics Firm, Inc. collects, uses, and protects your information when you use Aegira."
    >
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Summary</p>
          <h2>Your data, handled with discipline.</h2>
        </div>
        <p style={bodyStyle}>
          This policy explains what we collect and why. Aegira is a product of JHI Research
          &amp; Analytics Firm, Inc. We keep data collection minimal, protect it seriously,
          and never sell your personal information.
        </p>
        <div className="trust-grid" style={{ marginTop: "1.5rem" }}>
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
          <p className="eyebrow">Contact</p>
          <h2>Questions about your data?</h2>
        </div>
        <p style={bodyStyle}>
          Email <a href="mailto:support@aegiraenterprise.com">support@aegiraenterprise.com</a>{" "}
          or visit the <Link href="/contact">Contact</Link> page. See also our{" "}
          <Link href="/terms">Terms of Service</Link> and{" "}
          <Link href="/legal">Legal &amp; Disclosures</Link>.
        </p>
        <p style={{ ...bodyStyle, marginTop: "1.25rem" }}>
          Aegira is a product of JHI Research &amp; Analytics Firm, Inc. · JHI-SIG: 69M2705M.
        </p>
      </section>
    </StorefrontShell>
  );
}
