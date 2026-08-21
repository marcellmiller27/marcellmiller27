"use client";

import { useEffect, useState } from "react";
import { formatQuoteValue } from "@/lib/format";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api/v1";

// Default cross-asset set (crypto, indices, commodities, treasuries, ETF proxies,
// macro). All served by the existing /market/quotes endpoint. Override via prop.
const DEFAULT_SYMBOLS =
  "BTC,ETH,SPX,GOLD,UST10Y,VNQ,SMB_PROXY,PE_PROXY,BOND_HY,INFLATION";

type Quote = {
  symbol: string;
  name: string;
  price: number | null;
  unit: string;
  asset_class: string;
  change_percent: number | null;
  source: string;
  as_of: string | null;
  status: string;
};

function TickerItem({ quote }: { quote: Quote }) {
  const positive = (quote.change_percent ?? 0) >= 0;
  return (
    <span className="market-ticker__item">
      <span className="market-ticker__sym">{quote.symbol}</span>
      <span className="market-ticker__px">{formatQuoteValue(quote)}</span>
      {quote.change_percent !== null ? (
        <span
          className={
            positive ? "market-ticker__chg up" : "market-ticker__chg down"
          }
        >
          {positive ? "▲" : "▼"} {Math.abs(quote.change_percent).toFixed(2)}%
        </span>
      ) : null}
    </span>
  );
}

export function MarketTicker({ symbols = DEFAULT_SYMBOLS }: { symbols?: string }) {
  const [quotes, setQuotes] = useState<Quote[]>([]);

  useEffect(() => {
    let active = true;
    const pull = () => {
      fetch(`${API_BASE}/market/quotes?symbols=${encodeURIComponent(symbols)}`)
        .then((response) => {
          if (!response.ok) throw new Error(String(response.status));
          return response.json();
        })
        .then((data) => {
          if (!active) return;
          const live = (data.quotes ?? []).filter(
            (q: Quote) => q.price !== null,
          );
          setQuotes(live);
        })
        .catch(() => {
          /* keep last-known quotes on transient failure */
        });
    };
    pull();
    const timer = setInterval(pull, 30000);
    return () => {
      active = false;
      clearInterval(timer);
    };
  }, [symbols]);

  if (quotes.length === 0) return null;

  // Duplicate the row so the CSS translateX(-50%) loop is seamless.
  return (
    <div className="market-ticker" aria-label="Live cross-asset market prices">
      <div className="market-ticker__track">
        {quotes.map((quote) => (
          <TickerItem key={`a-${quote.symbol}`} quote={quote} />
        ))}
        {quotes.map((quote) => (
          <TickerItem key={`b-${quote.symbol}`} quote={quote} />
        ))}
      </div>
    </div>
  );
}
