// JHI-SIG: 69M2705M | Cancel subscription route | JHI Research & Analytics Firm, Inc. (proprietary)
import { AppShell } from "@/components/app-shell";
import { CancelSubscription } from "@/components/cancel-subscription";

export default function CancelSubscriptionPage() {
  return (
    <AppShell
      eyebrow="Subscription"
      title="Cancel subscription"
      description="Cancel in two steps. Your access continues until the end of your billing period, then deactivates automatically — with no auto-renewal traps."
    >
      <CancelSubscription />
    </AppShell>
  );
}
