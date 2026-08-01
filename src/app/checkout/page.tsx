// JHI-SIG: 69M2705M | Checkout route (Purchase Flow — Phase A) | JHI Research & Analytics Firm, Inc. (proprietary)
import { Suspense } from "react";
import { StorefrontShell } from "@/components/storefront-shell";
import { CheckoutFlow } from "@/components/checkout-flow";

export default function CheckoutPage() {
  return (
    <StorefrontShell
      eyebrow="Checkout"
      title="Start your free trial"
      description="Review your plan and start a 7-day free trial. Card required; cancel anytime before it ends and you won't be charged."
    >
      <Suspense fallback={<p className="rec-empty">Loading checkout…</p>}>
        <CheckoutFlow />
      </Suspense>
    </StorefrontShell>
  );
}
