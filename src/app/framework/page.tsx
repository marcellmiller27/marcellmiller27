// JHI-SIG: 69M2705M | Acquisition Intelligence Framework | JHI Research & Analytics Firm, Inc. (proprietary)
import { AppShell } from "@/components/app-shell";
import { FrameworkHub } from "@/components/framework-hub";
import { ModuleFooter } from "@/components/module-footer";

export default function FrameworkPage() {
  return (
    <AppShell
      eyebrow="Acquisition Intelligence"
      title="The Aegira Acquisition Intelligence Framework"
      description="A practical, educational guide for search-fund, ETA, and SMB acquirers — the ten elements of a rigorous acquisition analysis, each with a how-to, an Aegira tool to run it, and an exportable checklist. Research, not advice."
    >
      <FrameworkHub />
      <ModuleFooter module="framework" />
    </AppShell>
  );
}
