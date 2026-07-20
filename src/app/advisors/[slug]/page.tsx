// JHI-SIG: 69M2705M | Advisor record route | JHI Research & Analytics Firm, Inc. (proprietary)
import { notFound } from "next/navigation";
import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { advisors, entityHref, getAdvisor, resolveTransaction } from "@/lib/entities";

export function generateStaticParams() {
  return advisors.map((a) => ({ slug: a.slug }));
}

export default async function AdvisorRecordPage({
  params
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const advisor = getAdvisor(slug);
  if (!advisor) notFound();

  const facts = [
    { label: "Type", value: advisor.type },
    { label: "Headquarters", value: advisor.hq },
    { label: "Coverage", value: advisor.coverage }
  ];

  const deals = (advisor.transactionIds ?? [])
    .map((id) => resolveTransaction(id))
    .filter((t): t is NonNullable<typeof t> => Boolean(t));

  return (
    <AppShell eyebrow="Advisor" title={advisor.name} description={advisor.description}>
      <p className="rec-crumb">
        <Link href="/companies">Directory</Link> <span aria-hidden>›</span> {advisor.name}
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
          <p className="eyebrow">Engagements</p>
          <h2>Transactions advised</h2>
        </div>
        <div className="rec-txns">
          {deals.map(({ txn, target, acquirer }) => (
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
                {acquirer && (
                  <span>
                    Acquirer:{" "}
                    <Link href={entityHref(acquirer.kind, acquirer.entity.slug)}>
                      {acquirer.entity.name}
                    </Link>
                  </span>
                )}
              </div>
            </article>
          ))}
          {deals.length === 0 && <p className="rec-empty">No engagements on record.</p>}
        </div>
      </section>
    </AppShell>
  );
}
