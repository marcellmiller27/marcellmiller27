// JHI-SIG: 69M2705M | Financial Diligence Suite | JHI Research & Analytics Firm, Inc. (proprietary)
import { FinancialDiligence } from "@/components/financial-diligence";
import { AppShell } from "@/components/app-shell";

export default function DiligenceSuitePage() {
  return (
    <AppShell
      eyebrow="Acquisitions"
      title="Quality of Earnings — at software speed, CPA-signed"
      description="Run software-accelerated QoE procedures on a target: proof-of-cash, EBITDA normalization, net-working-capital peg, quality-of-revenue, and debt-like items — with a Financial Integrity Score, then route to a licensed partner CPA for a signed report at a fraction of the manual cost."
    >
      <FinancialDiligence />
    </AppShell>
  );
}
