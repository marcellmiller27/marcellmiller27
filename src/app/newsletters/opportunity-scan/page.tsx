// JHI-SIG: 69M2705M | Opportunity Scan route | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { OpportunityScan } from "@/components/opportunity-scan";

export default function OpportunityScanPage() {
  return (
    <AppShell
      eyebrow="Reports"
      title="Cross-Asset Opportunity Scan"
      description="Idea generation across all asset classes, derived from the live data and written in JHI's professional perspective."
    >
      <p className="rec-crumb">
        <Link href="/newsletters">Newsletters</Link> <span aria-hidden>›</span> Opportunity Scan
      </p>
      <OpportunityScan />
    </AppShell>
  );
}
