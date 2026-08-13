// JHI-SIG: 69M2705M | Contact page (public) | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import { StorefrontShell } from "@/components/storefront-shell";

const bodyStyle = {
  maxWidth: "62rem",
  color: "var(--muted-strong)",
  fontSize: "var(--fs-lg)",
  lineHeight: 1.7
} as const;

const channels = [
  {
    name: "General & support",
    detail: "support@aegiraenterprise.com",
    hint: "Questions about plans, data, accounts, or the platform."
  },
  {
    name: "Entity",
    detail: "JHI Research & Analytics Firm, Inc.",
    hint: "Aegira is a product of JHI Research & Analytics Firm, Inc."
  },
  {
    name: "Help center",
    detail: "Browse the Help hub",
    hint: "Self-serve answers and how-tos before you write in."
  }
];

export default function ContactPage() {
  return (
    <StorefrontShell
      eyebrow="Contact · Aegira"
      title="Talk to us."
      description="We keep it simple: one inbox, real answers, no phone-tree runaround. Reach the team directly or start with the Help hub."
    >
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">How to reach us</p>
          <h2>One inbox for everything.</h2>
        </div>
        <div className="trust-grid">
          {channels.map((c) => (
            <article className="trust-card" key={c.name}>
              <h3>{c.name}</h3>
              <p style={{ fontWeight: 700, color: "var(--text)", margin: "0 0 0.35rem" }}>{c.detail}</p>
              <p>{c.hint}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Before you write</p>
          <h2>Fastest paths to an answer.</h2>
        </div>
        <p style={bodyStyle}>
          Most questions are answered instantly by the AI support team on the{" "}
          <Link href="/support">Support</Link> page, or in the{" "}
          <Link href="/help">Help</Link> hub. For anything else — billing, security,
          partnerships, or press — email{" "}
          <a href="mailto:support@aegiraenterprise.com">support@aegiraenterprise.com</a>{" "}
          and we&rsquo;ll route you to the right specialist.
        </p>
        <p style={{ ...bodyStyle, marginTop: "1.25rem", fontSize: "var(--fs-md)" }}>
          Aegira is a product of JHI Research &amp; Analytics Firm, Inc. · JHI-SIG: 69M2705M.
        </p>
      </section>
    </StorefrontShell>
  );
}
