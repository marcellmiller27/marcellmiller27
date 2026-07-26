// JHI-SIG: 69M2705M | Register route | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import { StorefrontShell } from "@/components/storefront-shell";
import { AuthForm } from "@/components/auth-form";

export default function RegisterPage() {
  return (
    <StorefrontShell
      eyebrow="Get started"
      title="Create your JHI workspace"
      description="Register an organization workspace with a plan. You can start on Consumer (Tier 3) and upgrade anytime."
    >
      <section className="auth-layout">
        <div className="auth-panel">
          <AuthForm mode="register" />
          <p className="auth-alt">
            Already have an account? <Link href="/login">Sign in →</Link>
          </p>
        </div>
        <article className="app-card">
          <span>Plans</span>
          <strong>Tier 1–3</strong>
          <p>
            Consumer, Professional, and Enterprise plans unlock the platform and the full
            newsletter editions. Compare on the pricing page.
          </p>
          <Link className="opportunity-card__link" href="/pricing">
            Compare plans →
          </Link>
        </article>
      </section>
    </StorefrontShell>
  );
}
