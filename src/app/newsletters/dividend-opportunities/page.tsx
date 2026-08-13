// JHI-SIG: 69M2705M | Dividend Opportunities route | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { NewsletterEdition } from "@/components/newsletter-edition";

export default function DividendOpportunitiesPage() {
  return (
    <AppShell
      eyebrow="Reports"
      title="Dividend Opportunities"
      description="A monthly income read — dividend growth, balance-sheet quality, and covered income ideas, screened from point-in-time fundamentals (SF1 primary · SEC EDGAR fallback) plus live price. Every figure is derived and written in Aegira's professional perspective, ready to read on-platform or export to PDF."
    >
      <p className="rec-crumb">
        <Link href="/newsletters">Newsletters</Link> <span aria-hidden>›</span> Dividend Opportunities
      </p>
      <NewsletterEdition slug="dividend-opportunities" variant="brief" />
    </AppShell>
  );
}
