// JHI-SIG: 69M2705M | Key Financial Ratios | JHI Research & Analytics Firm, Inc. (proprietary)
import { AppShell } from "@/components/app-shell";
import { FinancialRatios } from "@/components/financial-ratios";

export default function RatiosPage() {
  return (
    <AppShell
      eyebrow="Acquisition Intelligence"
      title="Key financial ratios"
      description="Compute the ratios that decide a deal — the valuation multiple, debt-service coverage, leverage, margins, liquidity, returns, and the working-capital peg — from your own figures, each with plain-English meaning and benchmark bands."
    >
      <FinancialRatios />
    </AppShell>
  );
}
