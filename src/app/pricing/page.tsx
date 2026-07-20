import { StorefrontShell } from "@/components/storefront-shell";
import { pricingTiers } from "@/lib/platform-data";

export default function PricingPage() {
  return (
    <StorefrontShell
      eyebrow="Plans & pricing"
      title="Simple, transparent plans"
      description="Pay monthly or annually, cancel anytime. Transparent per-seat pricing with no surprise fees."
    >
      <section className="pricing-grid">
        {pricingTiers.map((tier) => (
          <article className="pricing-card" key={tier.name}>
            <div>
              <p className="pricing-card__audience">{tier.audience}</p>
              <h3>{tier.name}</h3>
              <strong>{tier.price}</strong>
              <p className="pricing-card__seats">{tier.seats}</p>
            </div>
            <ul>
              {tier.features.map((feature) => (
                <li key={feature}>{feature}</li>
              ))}
            </ul>
          </article>
        ))}
      </section>
    </StorefrontShell>
  );
}
