// JHI-SIG: 69M2705M | Red Alerts route | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { RedAlerts } from "@/components/red-alerts";

export default function RedAlertsPage() {
  return (
    <AppShell
      eyebrow="Reports"
      title="Red Alerts"
      description="Time-sensitive, threshold-triggered signals from the live data — surfaced the moment an indicator trips a line worth acting on."
    >
      <p className="rec-crumb">
        <Link href="/newsletters">Newsletters</Link> <span aria-hidden>›</span> Red Alerts
      </p>
      <RedAlerts />
    </AppShell>
  );
}
