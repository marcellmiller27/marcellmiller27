// JHI-SIG: 69M2705M | Accounting UI | John Henry Investments (proprietary)
import { LiveAccounting } from "@/components/live-accounting";
import { PlatformShell } from "@/components/platform-shell";

export default function AccountingPage() {
  return (
    <PlatformShell
      eyebrow="Firm operations"
      title="Accounting"
      description="The firm's general ledger, live from the backend: chart of accounts, trial balance, and journal entries — balanced, double-entry, and durable in Postgres."
    >
      <LiveAccounting />
    </PlatformShell>
  );
}
