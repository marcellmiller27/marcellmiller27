// JHI-SIG: 69M2705M | Global entity search (top bar) | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export function GlobalSearch() {
  const router = useRouter();
  const [q, setQ] = useState("");

  return (
    <form
      className="app-search-form"
      role="search"
      onSubmit={(e) => {
        e.preventDefault();
        const term = q.trim();
        router.push(term ? `/companies?q=${encodeURIComponent(term)}` : "/companies");
      }}
    >
      <input
        className="app-search"
        type="search"
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Search companies, transactions, filings…"
        aria-label="Global search"
      />
    </form>
  );
}
