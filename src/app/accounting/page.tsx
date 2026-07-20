// JHI-SIG: 69M2705M | Accounting UI | JHI Research & Analytics Firm, Inc. (proprietary)
import { LiveAccounting } from "@/components/live-accounting";
import { AppShell } from "@/components/app-shell";

export default function AccountingPage() {
  return (
    <AppShell
      eyebrow="Firm operations"
      title="Accounting"
      description="The firm's general ledger, live from the backend: chart of accounts, trial balance, and journal entries — balanced, double-entry, and durable in Postgres."
    >
      <LiveAccounting />
    </AppShell>
  );
}
