// JHI-SIG: 69M2705M | Company record route | JHI Research & Analytics Firm, Inc. (proprietary)
import { notFound } from "next/navigation";
import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { CompanyRecord } from "@/components/company-record";
import { companies, getCompany } from "@/lib/entities";

export function generateStaticParams() {
  return companies.map((c) => ({ slug: c.slug }));
}

export default async function CompanyRecordPage({
  params
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const company = getCompany(slug);
  if (!company) notFound();

  return (
    <AppShell eyebrow="Company" title={company.name} description={company.description}>
      <p className="rec-crumb">
        <Link href="/companies">Companies</Link> <span aria-hidden>›</span> {company.name}
      </p>
      <CompanyRecord company={company} />
    </AppShell>
  );
}
