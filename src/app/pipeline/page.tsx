// JHI-SIG: 69M2705M | Deal Pipeline | JHI Research & Analytics Firm, Inc. (proprietary)
import { PipelineBoard } from "@/components/pipeline-board";
import { PlatformShell } from "@/components/platform-shell";

export default function PipelinePage() {
  return (
    <PlatformShell
      eyebrow="Acquisitions"
      title="Deal Pipeline — track every target to close"
      description="Save Deal X-Ray (BQA) and Quality of Earnings analyses, then move each target through your workflow: Screen → Analysis → QoE → Financing → Offer → Closed."
    >
      <PipelineBoard />
    </PlatformShell>
  );
}
