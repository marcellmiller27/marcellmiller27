// JHI-SIG: 69M2705M | Acquisition / Deal X-Ray | John Henry Investments (proprietary)
import { DealXRay } from "@/components/deal-xray";
import { PlatformShell } from "@/components/platform-shell";

export default function DealXRayPage() {
  return (
    <PlatformShell
      eyebrow="Acquisition intelligence"
      title="Deal X-Ray — analyze a CIM in minutes"
      description="For search-fund & SMB buyers: enter the target's key figures for a 7-part scorecard, an honest ethic/credibility rating, a per-deal DCF + multiple valuation, DSCR/SBA fit, and realistic financing offers."
    >
      <DealXRay />
    </PlatformShell>
  );
}
