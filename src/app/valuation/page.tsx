// JHI-SIG: 69M2705M | Cross-Asset Valuation route | JHI Research & Analytics Firm, Inc. (proprietary)
import { AppShell } from "@/components/app-shell";
import { CrossAssetValuation } from "@/components/cross-asset-valuation";
import { ModuleFooter } from "@/components/module-footer";

export default function ValuationPage() {
  return (
    <AppShell
      eyebrow="Research & Intelligence"
      title="Cross-Asset Valuation"
      description="Discounted-cash-flow intrinsic value, implied expected return, and an Enter / Accumulate / Sideline call for any US equity — grounded in SEC EDGAR fundamentals and live prices. Export the full model to Excel."
    >
      <CrossAssetValuation />
      <ModuleFooter module="valuation" />
    </AppShell>
  );
}
