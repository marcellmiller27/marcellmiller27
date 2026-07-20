// JHI-SIG: 69M2705M | Acquisition / Deal X-Ray | JHI Research & Analytics Firm, Inc. (proprietary)
import { DealXRay } from "@/components/deal-xray";
import { AppShell } from "@/components/app-shell";

export default function DealXRayPage() {
  return (
    <AppShell
      eyebrow="Acquisitions"
      title="Deal X-Ray — analyze a CIM in minutes"
      description="For search-fund & SMB buyers: enter the target's key figures for a 7-part scorecard, an honest ethic/credibility rating, a per-deal DCF + multiple valuation, DSCR/SBA fit, and realistic financing offers."
    >
      <DealXRay />
    </AppShell>
  );
}
