// JHI-SIG: 69M2705M | The Main Street Acquirer route | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { NewsletterEdition } from "@/components/newsletter-edition";

export default function MainStreetAcquirerPage() {
  return (
    <AppShell
      eyebrow="Reports"
      title="The Main Street Acquirer"
      description="For SMB, search-fund, and ETA buyers: SBA lending intelligence, a recession-resilient industry spotlight, a rotating acquisition playbook, and a fact-locked deal teardown — assembled from public data and written in Aegira's professional perspective."
    >
      <p className="rec-crumb">
        <Link href="/newsletters">Newsletters</Link> <span aria-hidden>›</span> The Main Street Acquirer
      </p>
      <NewsletterEdition slug="main-street-acquirer" variant="brief" />
    </AppShell>
  );
}
