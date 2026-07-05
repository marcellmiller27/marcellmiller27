"use client";

import { useEffect, useState } from "react";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

type Quote = {
  symbol: string;
  name: string;
  price: number | null;
  unit: string;
  change_percent: number | null;
  source: string;
  as_of: string | null;
  status: string;
};

function formatPrice(quote: Quote): string {
  if (quote.price === null) return "—";
  const value = quote.price;
  if (quote.unit === "%") return `${value.toFixed(2)}%`;
  if (Math.abs(value) >= 1000) {
    return value.toLocaleString("en-US", { maximumFractionDigits: 0 });
  }
  if (Math.abs(value) >= 1) return value.toFixed(2);
  return value.toFixed(4);
}

export function LiveMarket({ symbols }: { symbols: string }) {
  const [quotes, setQuotes] = useState<Quote[]>([]);
  const [updated, setUpdated] = useState<string>("");
  const [error, setError] = useState<string>("");

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
          setQuotes(data.quotes ?? []);
          setUpdated(new Date().toLocaleTimeString());
          setError("");
        })
        .catch(() => {
          if (active) setError("Live market feed is unavailable right now.");
        });
    };
    pull();
    const timer = setInterval(pull, 15000);
    return () => {
      active = false;
      clearInterval(timer);
    };
  }, [symbols]);

  return (
    <div>
      <p className="live-market__status">
        {error ? (
          <span className="live-market__dot live-market__dot--off" />
        ) : (
          <span className="live-market__dot" />
        )}
        {error ? error : updated ? `Live · updated ${updated}` : "Connecting to live feed…"}
      </p>
      <div className="signal-list">
        {quotes.map((quote) => {
          const positive = (quote.change_percent ?? 0) >= 0;
          return (
            <article className="signal-card" key={quote.symbol}>
              <div>
                <span>
                  {quote.symbol} · {quote.source}
                </span>
                <strong>{formatPrice(quote)}</strong>
              </div>
              <p>
                {quote.status !== "ok" ? (
                  <span className="live-market__muted">No live data for this asset class.</span>
                ) : quote.change_percent !== null ? (
                  <span className={positive ? "live-market__up" : "live-market__down"}>
                    {positive ? "▲" : "▼"} {Math.abs(quote.change_percent).toFixed(2)}%
                  </span>
                ) : (
                  <span className="live-market__muted">{quote.name}</span>
                )}
              </p>
            </article>
          );
        })}
        {quotes.length === 0 && !error ? (
          <article className="signal-card">
            <div>
              <span>Loading</span>
              <strong>—</strong>
            </div>
            <p>Fetching live quotes…</p>
          </article>
        ) : null}
      </div>
    </div>
  );
}
