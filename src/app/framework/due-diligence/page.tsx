// JHI-SIG: 69M2705M | Due-Diligence Framework | JHI Research & Analytics Firm, Inc. (proprietary)
import { AppShell } from "@/components/app-shell";
import { DueDiligenceFramework } from "@/components/due-diligence-framework";

export default function DueDiligenceFrameworkPage() {
  return (
    <AppShell
      eyebrow="Acquisition Intelligence"
      title="Due-diligence framework"
      description="A comprehensive, categorized diligence checklist across financial, legal, operational, commercial, HR, and IT workstreams. Track it, export it, and start a diligence deal in your Pipeline."
    >
      <DueDiligenceFramework />
    </AppShell>
  );
}
