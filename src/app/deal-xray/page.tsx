// JHI-SIG: 69M2705M | Acquisition / Deal X-Ray | JHI Research & Analytics Firm, Inc. (proprietary)
import { DealXRay } from "@/components/deal-xray";
import { AppShell } from "@/components/app-shell";
import { ModuleFooter } from "@/components/module-footer";

export default function DealXRayPage() {
  return (
    <AppShell
      eyebrow="Acquisitions"
      title="Limited Scope Review — CIM analysis in Excel"
      description="For search-fund & SMB acquisitions: enter the company's data for a 7-part scorecard and an honest, ethical credibility rating — with a per-deal DCF + multiple valuation, DSCR/SBA fit, and realistic financing offers, all exportable to Excel."
    >
      <DealXRay />
      <ModuleFooter module="deal-xray" />
    </AppShell>
  );
}
