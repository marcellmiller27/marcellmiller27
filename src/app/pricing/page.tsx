import { PlatformShell } from "@/components/platform-shell";
import { pricingTiers } from "@/lib/platform-data";

export default function PricingPage() {
  return (
    <PlatformShell
      eyebrow="Plans & pricing"
      title="Simple, transparent plans"
      description="The backend exposes billing plans, checkout-session contracts, subscription status, and webhook update endpoints for a Stripe-based billing foundation."
    >
      <section className="pricing-grid">
        {pricingTiers.map((tier) => (
          <article className="pricing-card" key={tier.name}>
            <div>
              <p className="pricing-card__audience">{tier.audience}</p>
              <h3>{tier.name}</h3>
              <strong>{tier.price}</strong>
            </div>
            <ul>
              {tier.features.map((feature) => (
                <li key={feature}>{feature}</li>
              ))}
            </ul>
            <footer>
              <span>{tier.target}</span>
              <span>{tier.revenue}</span>
            </footer>
          </article>
        ))}
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Billing API contracts</p>
          <h2>Ready for Stripe product and price IDs</h2>
        </div>
        <div className="app-grid app-grid--three">
          <article className="app-card">
            <span>Plans</span>
            <strong>/api/v1/billing/plans</strong>
            <p>Lists Consumer, Professional, and Enterprise plan entitlements.</p>
          </article>
          <article className="app-card">
            <span>Checkout</span>
            <strong>/api/v1/billing/checkout-session</strong>
            <p>Creates a checkout-session contract and records billing intent.</p>
          </article>
          <article className="app-card">
            <span>Webhook</span>
            <strong>/api/v1/billing/webhook</strong>
            <p>Updates subscription plan, status, customer ID, and subscription ID.</p>
          </article>
        </div>
      </section>
    </PlatformShell>
  );
}
