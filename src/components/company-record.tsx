// JHI-SIG: 69M2705M | Company record (flat-tab deep dive) | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { useState } from "react";
import Link from "next/link";
import {
  advisors as allAdvisors,
  entityHref,
  getAdvisor,
  getCompany,
  resolveTransaction,
  type Company
} from "@/lib/entities";

const TABS = [
  "Overview",
  "Financials & Ratios",
  "Valuation",
  "Filings",
  "Risk & Governance",
  "Transactions",
  "Relationships",
  "Advisors",
  "News",
  "Analytics"
] as const;

type Tab = (typeof TABS)[number];

function Empty({ children }: { children: React.ReactNode }) {
  return <p className="rec-empty">{children}</p>;
}

export function CompanyRecord({ company }: { company: Company }) {
  const [tab, setTab] = useState<Tab>("Overview");

  const facts: { label: string; value: string }[] = [
    { label: "Ownership", value: company.ownership },
    { label: "Sector", value: company.sector },
    { label: "Industry", value: company.industry },
    { label: "Headquarters", value: company.hq },
    { label: "Founded", value: company.founded },
    { label: "Employees", value: company.employees },
    ...(company.ticker ? [{ label: "Ticker", value: company.ticker }] : []),
    { label: "Status", value: company.status }
  ];

  const resolvedTxns = (company.transactionIds ?? [])
    .map((id) => resolveTransaction(id))
    .filter((t): t is NonNullable<typeof t> => Boolean(t));

  return (
    <div className="rec">
      <section className="rec-facts">
        {facts.map((f) => (
          <div className="rec-fact" key={f.label}>
            <span>{f.label}</span>
            <strong>{f.value}</strong>
          </div>
        ))}
      </section>

      <div className="rec-tabs" role="tablist" aria-label="Company record">
        {TABS.map((t) => (
          <button
            key={t}
            role="tab"
            aria-selected={tab === t}
            className={`rec-tab${tab === t ? " rec-tab--active" : ""}`}
            onClick={() => setTab(t)}
          >
            {t}
          </button>
        ))}
      </div>

      <div className="rec-panel" role="tabpanel">
        {tab === "Overview" && (
          <div className="app-grid app-grid--two">
            <article className="app-card">
              <span>Profile</span>
              <p>{company.description}</p>
            </article>
            <article className="app-card">
              <span>Key ratios</span>
              {company.ratios ? (
                <ul className="rec-kv">
                  {company.ratios.map((r) => (
                    <li key={r.label}>
                      <span>{r.label}</span>
                      <strong>{r.value}</strong>
                    </li>
                  ))}
                </ul>
              ) : (
                <Empty>Ratios not yet mapped.</Empty>
              )}
            </article>
          </div>
        )}

        {tab === "Financials & Ratios" && (
          <>
            {company.financials ? (
              <>
                <table className="rec-table">
                  <thead>
                    <tr>
                      <th>Metric</th>
                      {company.financials.years.map((y) => (
                        <th key={y}>{y}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {company.financials.rows.map((row) => (
                      <tr key={row.metric}>
                        <td>{row.metric}</td>
                        {row.values.map((v, i) => (
                          <td key={i}>{v}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
                <p className="rec-basis">Basis: {company.financials.basis}</p>
              </>
            ) : (
              <Empty>
                Detailed financials not yet mapped — lands with EDGAR / client-upload depth (Phase 5).
              </Empty>
            )}
            {company.ratios && (
              <ul className="rec-kv rec-kv--wide">
                {company.ratios.map((r) => (
                  <li key={r.label}>
                    <span>{r.label}</span>
                    <strong>{r.value}</strong>
                  </li>
                ))}
              </ul>
            )}
          </>
        )}

        {tab === "Valuation" && (
          <>
            {company.valuation ? (
              <>
                <ul className="rec-kv rec-kv--wide">
                  {company.valuation.rows.map((r) => (
                    <li key={r.label}>
                      <span>{r.label}</span>
                      <strong>{r.value}</strong>
                    </li>
                  ))}
                </ul>
                <p className="rec-basis">Basis: {company.valuation.basis}</p>
                {company.valuation.comps.length > 0 && (
                  <div className="rec-pivot">
                    <p className="eyebrow">Comparable companies</p>
                    {company.valuation.comps.map((slug) => {
                      const comp = getCompany(slug);
                      if (!comp) return null;
                      return (
                        <Link className="rec-pivot__card" href={entityHref("company", comp.slug)} key={slug}>
                          <strong>{comp.name}</strong>
                          <span>{comp.industry} · {comp.hq}</span>
                        </Link>
                      );
                    })}
                  </div>
                )}
              </>
            ) : (
              <Empty>Valuation not yet mapped.</Empty>
            )}
          </>
        )}

        {tab === "Filings" && (
          <>
            {company.filings && company.filings.length > 0 ? (
              <table className="rec-table">
                <thead>
                  <tr>
                    <th>Form</th>
                    <th>Date</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {company.filings.map((f, i) => (
                    <tr key={i}>
                      <td><span className="rec-badge">{f.form}</span></td>
                      <td>{f.date}</td>
                      <td>{f.description}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <Empty>
                No SEC filings — {company.ownership === "Public" ? "none on record." : "private company. Filing depth applies to public entities; private financials arrive via client upload (Phase 5)."}
              </Empty>
            )}
          </>
        )}

        {tab === "Risk & Governance" && (
          <div className="app-grid app-grid--two">
            <article className="app-card">
              <span>Governance</span>
              {company.governance ? (
                <ul className="rec-kv">
                  {company.governance.map((g) => (
                    <li key={g.label}>
                      <span>{g.label}</span>
                      <strong>{g.value}</strong>
                    </li>
                  ))}
                </ul>
              ) : (
                <Empty>Governance not yet mapped.</Empty>
              )}
            </article>
            <article className="app-card">
              <span>Risk flags</span>
              {company.riskFlags ? (
                <ul className="rec-flags">
                  {company.riskFlags.map((r) => (
                    <li key={r.area}>
                      <span className={`rec-flag__level rec-flag__level--${r.level.toLowerCase()}`}>
                        {r.level}
                      </span>
                      <span className="rec-flag__body">
                        <strong>{r.area}</strong>
                        <span>{r.note}</span>
                      </span>
                    </li>
                  ))}
                </ul>
              ) : (
                <Empty>Risk flags not yet mapped.</Empty>
              )}
            </article>
          </div>
        )}

        {tab === "Transactions" && (
          <>
            {resolvedTxns.length > 0 ? (
              <div className="rec-txns">
                {resolvedTxns.map(({ txn, acquirer, advisorList }) => (
                  <article className="rec-txn" key={txn.id}>
                    <div className="rec-txn__head">
                      <span className="rec-badge">{txn.type}</span>
                      <span className="rec-txn__date">{txn.date}</span>
                      <strong className="rec-txn__value">{txn.value}</strong>
                    </div>
                    <p>{txn.summary}</p>
                    <div className="rec-txn__meta">
                      <span>Stake: <strong>{txn.stake}</strong></span>
                      {acquirer && (
                        <span>
                          Acquirer:{" "}
                          <Link href={entityHref(acquirer.kind, acquirer.entity.slug)}>
                            {acquirer.entity.name}
                          </Link>
                        </span>
                      )}
                      {advisorList.map((a) => (
                        <span key={a.slug}>
                          Advisor: <Link href={entityHref("advisor", a.slug)}>{a.name}</Link>
                        </span>
                      ))}
                    </div>
                  </article>
                ))}
              </div>
            ) : (
              <Empty>No transactions on record.</Empty>
            )}
          </>
        )}

        {tab === "Relationships" && (
          <div className="rec-pivot">
            {resolvedTxns.map(({ txn, acquirer }) =>
              acquirer ? (
                <Link
                  className="rec-pivot__card"
                  href={entityHref(acquirer.kind, acquirer.entity.slug)}
                  key={`acq-${txn.id}`}
                >
                  <span className="rec-pivot__edge">
                    {txn.type === "Investment" ? "Investor" : "Acquired by"}
                  </span>
                  <strong>{acquirer.entity.name}</strong>
                  <span>{acquirer.kind === "firm" ? "Firm" : "Company"}</span>
                </Link>
              ) : null
            )}
            {(company.advisorSlugs ?? []).map((slug) => {
              const a = getAdvisor(slug);
              if (!a) return null;
              return (
                <Link className="rec-pivot__card" href={entityHref("advisor", a.slug)} key={`adv-${slug}`}>
                  <span className="rec-pivot__edge">Advised by</span>
                  <strong>{a.name}</strong>
                  <span>{a.type}</span>
                </Link>
              );
            })}
            {(company.valuation?.comps ?? []).map((slug) => {
              const c = getCompany(slug);
              if (!c) return null;
              return (
                <Link className="rec-pivot__card" href={entityHref("company", c.slug)} key={`comp-${slug}`}>
                  <span className="rec-pivot__edge">Comparable</span>
                  <strong>{c.name}</strong>
                  <span>{c.industry}</span>
                </Link>
              );
            })}
            {resolvedTxns.length === 0 &&
              (company.advisorSlugs ?? []).length === 0 &&
              (company.valuation?.comps ?? []).length === 0 && (
                <Empty>No relationships mapped.</Empty>
              )}
          </div>
        )}

        {tab === "Advisors" && (
          <>
            {(company.advisorSlugs ?? []).length > 0 ? (
              <div className="rec-pivot">
                {(company.advisorSlugs ?? []).map((slug) => {
                  const a = getAdvisor(slug) ?? allAdvisors.find((x) => x.slug === slug);
                  if (!a) return null;
                  return (
                    <Link className="rec-pivot__card" href={entityHref("advisor", a.slug)} key={slug}>
                      <span className="rec-pivot__edge">{a.type}</span>
                      <strong>{a.name}</strong>
                      <span>{a.coverage} · {a.hq}</span>
                    </Link>
                  );
                })}
              </div>
            ) : (
              <Empty>No advisors on record.</Empty>
            )}
          </>
        )}

        {tab === "News" && (
          <>
            {company.news && company.news.length > 0 ? (
              <ul className="rec-news">
                {company.news.map((n, i) => (
                  <li key={i}>
                    <span className="rec-news__date">{n.date}</span>
                    <span className="rec-news__body">
                      <strong>{n.headline}</strong>
                      <span>{n.source}</span>
                    </span>
                  </li>
                ))}
              </ul>
            ) : (
              <Empty>No news on record.</Empty>
            )}
          </>
        )}

        {tab === "Analytics" && (
          <>
            {company.analytics ? (
              <div className="app-grid app-grid--two">
                <article className="app-card">
                  <span>Signals</span>
                  <ul className="rec-kv">
                    {company.analytics.rows.map((r) => (
                      <li key={r.label}>
                        <span>{r.label}</span>
                        <strong>{r.value}</strong>
                      </li>
                    ))}
                  </ul>
                </article>
                <article className="app-card app-card--accent">
                  <span>Macro overlay</span>
                  <p>{company.analytics.macroOverlay}</p>
                  <p className="rec-basis">
                    JHI depth edge: financials + macro on one record.
                  </p>
                </article>
              </div>
            ) : (
              <Empty>Analytics not yet mapped.</Empty>
            )}
          </>
        )}
      </div>
    </div>
  );
}
