import { AppShell } from "@/components/app-shell";
import { DocumentReview } from "@/components/document-review";
import { ModuleFooter } from "@/components/module-footer";

export default function DueDiligencePage() {
  return (
    <AppShell
      eyebrow="Acquisitions"
      title="Document Review — analyze acquisition documents before capital is at risk"
      description="Upload financial records, normalize cash flow, detect risk indicators, and generate diligence questions for acquisition and lending decisions."
    >
      <DocumentReview />
      <ModuleFooter module="due-diligence" />
    </AppShell>
  );
}
