// JHI-SIG: 69M2705M | Entity directory (search + pivot) | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { searchEntities, type EntityKind } from "@/lib/entities";

const FILTERS: { label: string; kind: EntityKind | "all" }[] = [
  { label: "All", kind: "all" },
  { label: "Companies", kind: "company" },
  { label: "Firms", kind: "firm" },
  { label: "Advisors", kind: "advisor" }
];

const KIND_LABEL: Record<EntityKind, string> = {
  company: "Company",
  firm: "Firm",
  advisor: "Advisor",
  transaction: "Transaction"
};

export function EntityDirectory({ initialQuery = "" }: { initialQuery?: string }) {
  const [query, setQuery] = useState(initialQuery);
  const [kind, setKind] = useState<EntityKind | "all">("all");

  const results = useMemo(() => {
    const all = searchEntities(query);
    return kind === "all" ? all : all.filter((r) => r.kind === kind);
  }, [query, kind]);

  return (
    <div className="dir">
      <div className="dir-controls">
        <input
          className="dir-search"
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search companies, firms, advisors…"
          aria-label="Search entities"
        />
        <div className="dir-filters">
          {FILTERS.map((f) => (
            <button
              key={f.kind}
              className={`dir-filter${kind === f.kind ? " dir-filter--active" : ""}`}
              onClick={() => setKind(f.kind)}
            >
              {f.label}
            </button>
          ))}
        </div>
      </div>

      <p className="dir-count">{results.length} result{results.length === 1 ? "" : "s"}</p>

      {results.length > 0 ? (
        <ul className="dir-list">
          {results.map((r) => (
            <li key={`${r.kind}-${r.slug}`}>
              <Link className="dir-row" href={r.href}>
                <span className={`rec-badge rec-badge--${r.kind}`}>{KIND_LABEL[r.kind]}</span>
                <span className="dir-row__body">
                  <strong>{r.name}</strong>
                  <span>{r.sub}</span>
                </span>
                <span className="dir-row__go" aria-hidden>›</span>
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p className="rec-empty">No entities match “{query}”.</p>
      )}
    </div>
  );
}
