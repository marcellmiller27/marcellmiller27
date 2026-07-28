// JHI-SIG: 69M2705M | Economic Brief route | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { NewsletterEdition } from "@/components/newsletter-edition";

export default function EconomicBriefPage() {
  return (
    <AppShell
      eyebrow="Reports"
      title="Economic Tracking newsletter"
      description="Auto-generated from the economic data we poll — assembled and written in Aegira's professional perspective, ready to read on-platform or export to PDF."
    >
      <p className="rec-crumb">
        <Link href="/newsletters">Newsletters</Link> <span aria-hidden>›</span> The Economic Brief
      </p>
      <NewsletterEdition slug="economic-brief" variant="brief" />
    </AppShell>
  );
}
