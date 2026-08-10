// JHI-SIG: 69M2705M | Industry Analysis | JHI Research & Analytics Firm, Inc. (proprietary)
import { AppShell } from "@/components/app-shell";
import { IndustryAnalysis } from "@/components/industry-analysis";

export default function IndustryAnalysisPage() {
  return (
    <AppShell
      eyebrow="Acquisition Intelligence"
      title="Industry analysis"
      description="Derived sector benchmarks — median margins, growth, and EV/EBITDA multiples compiled from public EDGAR and SF1 aggregates — to place a target in its industry. Derived-only reference bands, not valuations."
    >
      <IndustryAnalysis />
    </AppShell>
  );
}
