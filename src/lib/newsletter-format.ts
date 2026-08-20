// JHI-SIG: 69M2705M | Newsletter data helpers | JHI Research & Analytics Firm, Inc. (proprietary)
// Shared fetch + formatting for the editorial editions (Economic Brief, Red Alerts,
// Opportunity Scan). All read the same live /market/quotes feed via the same-origin proxy.

import { formatQuoteValue } from "@/lib/format";

export const NEWSLETTER_API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api/v1";

// The full indicator + market set the editions draw from.
export const NEWSLETTER_SYMBOLS =
  "GDP,FED_FUNDS,UNEMPLOYMENT,RETAIL_SALES,CONSUMER_SENTIMENT,INDUSTRIAL_PRODUCTION,INFLATION,SPX,GOLD,UST10Y,BTC";

export type Quote = {
  symbol: string;
  name: string;
  price: number | null;
  unit: string;
  asset_class?: string | null;
  change_percent: number | null;
  status: string;
  note: string | null;
  as_of: string | null;
};

export type QuoteMap = Record<string, Quote>;

// Consolidated onto the canonical magnitude-aware formatter (src/lib/format.ts) so a
// price renders identically here, in the live ticker, and in the backend twin. Prices
// route through the standard; non-price readings (rates, macro levels) keep their
// unit-appropriate rendering inside `formatQuoteValue`.
export function fmt(q: Quote | undefined): string {
  return formatQuoteValue(q ?? null);
}

export async function fetchQuotes(
  symbols: string = NEWSLETTER_SYMBOLS
): Promise<{ map: QuoteMap; asOf: string }> {
  const r = await fetch(
    `${NEWSLETTER_API_BASE}/market/quotes?symbols=${encodeURIComponent(symbols)}`
  );
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  const d = await r.json();
  const map: QuoteMap = {};
  for (const q of d.quotes ?? []) map[q.symbol] = q;
  return { map, asOf: d.as_of ?? new Date().toISOString() };
}

// Download the server-generated PDF for an edition. Replaces window.print() (which
// crashed the forwarded/desktop viewer). Uses apiFetch so the auth token is
// forwarded — subscribers/staff get the full edition, everyone else the teaser,
// matching the on-screen role gate.
export async function downloadNewsletterPdf(slug: string): Promise<void> {
  const { apiFetch } = await import("@/lib/api");
  const res = await apiFetch(`/newsletters/${slug}/pdf`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `aegira-${slug}-${new Date().toISOString().slice(0, 10)}.pdf`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

export function editionDate(): string {
  return new Date().toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric"
  });
}
