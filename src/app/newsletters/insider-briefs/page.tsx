// JHI-SIG: 69M2705M | Insider Briefs route | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { NewsletterEdition } from "@/components/newsletter-edition";

export default function InsiderBriefsPage() {
  return (
    <AppShell
      eyebrow="Reports"
      title="Insider Briefs"
      description="A rotating deep-dive on the most salient macro theme — the depth mandate. Auto-selected from the data we poll and written in Aegira's professional perspective, ready to read on-platform or export to PDF."
    >
      <p className="rec-crumb">
        <Link href="/newsletters">Newsletters</Link> <span aria-hidden>›</span> Insider Briefs
      </p>
      <NewsletterEdition slug="insider-briefs" variant="insider" />
    </AppShell>
  );
}
