// JHI-SIG: 69M2705M | Login route | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import { StorefrontShell } from "@/components/storefront-shell";
import { AuthForm } from "@/components/auth-form";

export default function LoginPage() {
  return (
    <StorefrontShell
      eyebrow="Secure access"
      title="Sign in"
      description="Sign in to the JHI platform. Access to research, records, and diligence tools is reserved for subscribers; the newsletter preview is open to all."
    >
      <section className="auth-layout">
        <div className="auth-panel">
          <AuthForm mode="login" />
          <p className="auth-alt">
            New to JHI? <Link href="/register">Create an account →</Link>
          </p>
        </div>
        <article className="app-card">
          <span>What you get</span>
          <strong>Subscriber access</strong>
          <p>
            Dashboard, Economics, Screener, records, and diligence tools — plus the full
            editions of The Economic Brief, Red Alerts, and the Cross-Asset Opportunity Scan.
          </p>
          <Link className="opportunity-card__link" href="/pricing">
            See plans &amp; pricing →
          </Link>
        </article>
      </section>
    </StorefrontShell>
  );
}
