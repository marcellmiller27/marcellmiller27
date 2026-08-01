// JHI-SIG: 69M2705M | Checkout success route (Purchase Flow — Phase A) | JHI Research & Analytics Firm, Inc. (proprietary)
import { Suspense } from "react";
import { AppShell } from "@/components/app-shell";
import { CheckoutSuccess } from "@/components/checkout-success";

export default function CheckoutSuccessPage() {
  return (
    <AppShell
      eyebrow="Checkout"
      title="Trial started"
      description="Your 7-day free trial is now active."
    >
      <Suspense fallback={<p className="rec-empty">Confirming your trial…</p>}>
        <CheckoutSuccess />
      </Suspense>
    </AppShell>
  );
}
