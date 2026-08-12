// JHI-SIG: 69M2705M | Crypto Intelligence route | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { NewsletterEdition } from "@/components/newsletter-edition";

export default function CryptoIntelligencePage() {
  return (
    <AppShell
      eyebrow="Reports"
      title="Crypto Intelligence"
      description="A biweekly digital-asset read — the Bitcoin/crypto cycle, price action across the majors, and the liquidity & adoption backdrop. Assembled from public data (CoinGecko spot + FRED M2) and written in Aegira's professional perspective, ready to read on-platform or export to PDF."
    >
      <p className="rec-crumb">
        <Link href="/newsletters">Newsletters</Link> <span aria-hidden>›</span> Crypto Intelligence
      </p>
      <NewsletterEdition slug="crypto-intelligence" variant="brief" />
    </AppShell>
  );
}
