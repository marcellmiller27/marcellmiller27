// JHI-SIG: 69M2705M | Canonical price formatter (magnitude-aware) | JHI Research & Analytics Firm, Inc. (proprietary)
// One canonical, magnitude-aware price-formatting standard for the whole frontend.
// This is the TypeScript twin of the backend's `app/price_format.py`; the two MUST
// stay behavior-identical so a price looks the same in the live UI, a newsletter PDF,
// and an Excel workbook label.
//
// THE STANDARD
// ------------
// Forex pairs / FX rates (EUR/USD, USD/JPY, GBP/USD, ...):
//   4 decimal places, NO `$` symbol, shown as the rate — ALWAYS 4dp regardless of
//   magnitude (USD/JPY is ~159 but still 4dp).
//
// Dollar-priced assets (crypto, commodities, equities, indices, ETFs):
//   `$` prefix + thousands comma separators, decimals BY MAGNITUDE of the absolute
//   value:
//     abs >= 100         -> 2 decimals  ($4,585.80, $72,909.88)
//     1 <= abs < 100     -> 3 decimals  ($1.264)
//     0.0001 <= abs < 1  -> 4 decimals  ($0.1811)
//     abs < 0.0001       -> 4 significant figures (safeguard so a tiny value is not
//                           shown as `$0.0000`); never changes any of the above.
//
// This is DISPLAY formatting only — it never mutates the stored/computed numeric value.

// Asset classes whose price renders as a dollar amount (`$` + magnitude rule).
export const DOLLAR_PRICE_CLASSES = new Set([
  "crypto",
  "commodity",
  "equity",
  "index",
  "reit",
  "etf",
  "bond_proxy",
  "pe_proxy",
  "smb_proxy",
]);

// Asset classes that are forex rates (4dp, no `$`).
export const FOREX_CLASSES = new Set(["fx", "forex"]);

export const EM_DASH = "—";

export type PriceFormatOptions = {
  assetClass?: string | null;
  forex?: boolean | null;
};

function isForex(assetClass?: string | null, forex?: boolean | null): boolean {
  if (forex !== undefined && forex !== null) return forex;
  if (assetClass !== undefined && assetClass !== null) {
    return FOREX_CLASSES.has(assetClass.trim().toLowerCase());
  }
  return false;
}

// Decimal places for a dollar-priced value, by magnitude of its absolute value.
function dollarDecimals(absValue: number): number {
  if (absValue >= 100) return 2;
  if (absValue >= 1) return 3;
  if (absValue >= 0.0001) return 4;
  if (absValue === 0) return 4;
  // Safeguard: sub-0.0001 -> 4 significant figures so it isn't shown as $0.0000.
  return Math.max(4, 3 - Math.floor(Math.log10(absValue)));
}

/**
 * Render `value` as a price string per the canonical standard.
 *
 * Pass `{ forex: true }` (or an `assetClass` of `"fx"`/`"forex"`) for FX rates
 * (4dp, no `$`); otherwise the value is treated as a dollar-priced asset and rendered
 * with a `$` prefix, thousands separators, and magnitude-based decimals.
 */
export function formatPrice(
  value: number | null | undefined,
  { assetClass, forex }: PriceFormatOptions = {},
): string {
  if (value === null || value === undefined || !Number.isFinite(value)) {
    return EM_DASH;
  }

  if (isForex(assetClass, forex)) {
    // Forex: always 4dp, no `$`, shown as the rate (no thousands separator).
    return value.toFixed(4);
  }

  const sign = value < 0 ? "-" : "";
  const absValue = Math.abs(value);
  const decimals = dollarDecimals(absValue);
  const body = absValue.toLocaleString("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
  return `${sign}$${body}`;
}

// A quote-shaped value: enough to decide forex vs dollar-price vs a non-price
// (rate / macro) reading. Mirrors the backend `Quote` fields the UI receives.
export type PriceQuote = {
  price: number | null;
  unit?: string | null;
  asset_class?: string | null;
};

/**
 * Format a market quote for display, dispatching on its asset class / unit.
 *
 * Prices (forex + dollar-priced asset classes) route through `formatPrice`; non-price
 * readings (rates as `%`, macro index levels, aggregate money-supply figures) keep
 * their established, purpose-built formatting since the price standard does not apply.
 */
export function formatQuoteValue(quote: PriceQuote | null | undefined): string {
  if (!quote || quote.price === null || quote.price === undefined) return EM_DASH;
  const value = quote.price;
  const assetClass = quote.asset_class ?? null;
  const unit = quote.unit ?? "";

  if (isForex(assetClass, null)) return formatPrice(value, { forex: true });
  if (assetClass && DOLLAR_PRICE_CLASSES.has(assetClass.trim().toLowerCase())) {
    return formatPrice(value, { assetClass });
  }

  // Non-price readings — preserve the existing, unit-appropriate rendering.
  if (unit === "%") return `${value.toFixed(2)}%`;
  if (unit === "index") return value.toFixed(1);
  if (unit === "USD bn") {
    return value >= 1000 ? `$${(value / 1000).toFixed(2)}T` : `$${value.toFixed(1)}B`;
  }
  if (unit === "USD mn") {
    return value >= 1000 ? `$${(value / 1000).toFixed(2)}B` : `$${value.toFixed(1)}M`;
  }
  if (unit === "USD/oz" || unit === "USD") return formatPrice(value, { assetClass });
  return value.toLocaleString("en-US", { maximumFractionDigits: 2 });
}
