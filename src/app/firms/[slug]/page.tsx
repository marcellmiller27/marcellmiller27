// JHI-SIG: 69M2705M | Firm record route | JHI Research & Analytics Firm, Inc. (proprietary)
import { notFound } from "next/navigation";
import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { entityHref, firms, getCompany, getFirm, resolveTransaction } from "@/lib/entities";

export function generateStaticParams() {
  return firms.map((f) => ({ slug: f.slug }));
}

export default async function FirmRecordPage({
  params
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const firm = getFirm(slug);
  if (!firm) notFound();

  const facts = [
    { label: "Type", value: firm.type },
    { label: "Headquarters", value: firm.hq },
    { label: "Founded", value: firm.founded },
    ...(firm.aum ? [{ label: "AUM", value: firm.aum }] : []),
    { label: "Strategy", value: firm.strategy }
  ];

  const deals = (firm.transactionIds ?? [])
    .map((id) => resolveTransaction(id))
    .filter((t): t is NonNullable<typeof t> => Boolean(t));

  return (
    <AppShell eyebrow="Firm" title={firm.name} description={firm.description}>
      <p className="rec-crumb">
        <Link href="/companies">Directory</Link> <span aria-hidden>›</span> {firm.name}
      </p>

      <section className="rec-facts">
        {facts.map((f) => (
          <div className="rec-fact" key={f.label}>
            <span>{f.label}</span>
            <strong>{f.value}</strong>
          </div>
        ))}
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Portfolio</p>
          <h2>Companies</h2>
        </div>
        <div className="rec-pivot">
          {(firm.portfolioCompanySlugs ?? []).map((s) => {
            const c = getCompany(s);
            if (!c) return null;
            return (
              <Link className="rec-pivot__card" href={entityHref("company", c.slug)} key={s}>
                <span className="rec-pivot__edge">Portfolio company</span>
                <strong>{c.name}</strong>
                <span>{c.industry} · {c.hq}</span>
              </Link>
            );
          })}
          {(firm.portfolioCompanySlugs ?? []).length === 0 && (
            <p className="rec-empty">No portfolio companies on record.</p>
          )}
        </div>
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Deal activity</p>
          <h2>Transactions</h2>
        </div>
        <div className="rec-txns">
          {deals.map(({ txn, target, advisorList }) => (
            <article className="rec-txn" key={txn.id}>
              <div className="rec-txn__head">
                <span className="rec-badge">{txn.type}</span>
                <span className="rec-txn__date">{txn.date}</span>
                <strong className="rec-txn__value">{txn.value}</strong>
              </div>
              <p>{txn.summary}</p>
              <div className="rec-txn__meta">
                {target && (
                  <span>
                    Target: <Link href={entityHref("company", target.slug)}>{target.name}</Link>
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
          {deals.length === 0 && <p className="rec-empty">No transactions on record.</p>}
        </div>
      </section>
    </AppShell>
  );
}
