// JHI-SIG: 69M2705M | Market Analysis | JHI Research & Analytics Firm, Inc. (proprietary)
import { AppShell } from "@/components/app-shell";
import { MarketAnalysis } from "@/components/market-analysis";

export default function MarketAnalysisPage() {
  return (
    <AppShell
      eyebrow="Acquisition Intelligence"
      title="Market analysis"
      description="Size the market with an interactive TAM/SAM/SOM worksheet, work through the market with a structured framework, and assess competitive pressure with Porter's five forces."
    >
      <MarketAnalysis />
    </AppShell>
  );
}
