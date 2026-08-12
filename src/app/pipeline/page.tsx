// JHI-SIG: 69M2705M | Deal Pipeline | JHI Research & Analytics Firm, Inc. (proprietary)
import { PipelineBoard } from "@/components/pipeline-board";
import { AppShell } from "@/components/app-shell";
import { ModuleFooter } from "@/components/module-footer";

export default function PipelinePage() {
  return (
    <AppShell
      eyebrow="Acquisitions"
      title="Deal Pipeline — track every target to close"
      description="Save Limited Scope Review (LSR) and Quality of Earnings analyses, then move each target through your workflow: Screen → Analysis → QoE → Financing → Offer → Closed."
    >
      <PipelineBoard />
      <ModuleFooter module="pipeline" />
    </AppShell>
  );
}
