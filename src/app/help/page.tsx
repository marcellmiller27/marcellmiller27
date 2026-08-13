// JHI-SIG: 69M2705M | Help hub (public) | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import { StorefrontShell } from "@/components/storefront-shell";

const bodyStyle = {
  maxWidth: "62rem",
  color: "var(--muted-strong)",
  fontSize: "var(--fs-lg)",
  lineHeight: 1.7
} as const;

const topics = [
  {
    name: "Getting started",
    detail: "Create an account, pick a plan, and set up your first workspace.",
    href: "/register",
    cta: "Start free"
  },
  {
    name: "Plans & billing",
    detail: "Compare tiers, understand per-seat pricing, and manage your subscription.",
    href: "/pricing",
    cta: "See pricing"
  },
  {
    name: "Using the platform",
    detail: "Screen opportunities, run a Limited Scope Review, and read the Newsletters.",
    href: "/framework",
    cta: "Open the Framework"
  },
  {
    name: "Ask the AI support team",
    detail: "Instant answers on plans, security, market data, and the mobile app.",
    href: "/support",
    cta: "Open Support"
  }
];

export default function HelpPage() {
  return (
    <StorefrontShell
      eyebrow="Help · Aegira"
      title="How can we help?"
      description="Start here for setup, plans, and how-tos. For anything the guides don't cover, the AI support team on the Support page answers instantly."
    >
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Popular topics</p>
          <h2>Find your answer fast.</h2>
        </div>
        <div className="trust-grid">
          {topics.map((t) => (
            <article className="trust-card" key={t.name}>
              <h3>{t.name}</h3>
              <p>{t.detail}</p>
              <p style={{ marginTop: "0.6rem" }}>
                <Link href={t.href} style={{ color: "var(--growth)", fontWeight: 800 }}>
                  {t.cta} &rarr;
                </Link>
              </p>
            </article>
          ))}
        </div>
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Still stuck?</p>
          <h2>Reach a human.</h2>
        </div>
        <p style={bodyStyle}>
          The AI support team on the <Link href="/support">Support</Link> page handles most
          questions instantly and escalates to the founder when needed. For direct contact,
          see the <Link href="/contact">Contact</Link> page or email{" "}
          <a href="mailto:support@aegiraenterprise.com">support@aegiraenterprise.com</a>.
        </p>
        <p style={{ ...bodyStyle, marginTop: "1.25rem", fontSize: "var(--fs-md)" }}>
          Aegira is a product of JHI Research &amp; Analytics Firm, Inc. · JHI-SIG: 69M2705M.
        </p>
      </section>
    </StorefrontShell>
  );
}
