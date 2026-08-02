import { StorefrontShell } from "@/components/storefront-shell";
import { PricingPlans } from "@/components/pricing-plans";

export default function PricingPage() {
  return (
    <StorefrontShell
      eyebrow="Plans & pricing"
      title="Simple, transparent plans"
      description="Pay monthly or annually, cancel anytime. Transparent per-seat pricing with no surprise fees."
    >
      <PricingPlans />
    </StorefrontShell>
  );
}
