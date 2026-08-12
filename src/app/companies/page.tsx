// JHI-SIG: 69M2705M | Entity directory route | JHI Research & Analytics Firm, Inc. (proprietary)
import { AppShell } from "@/components/app-shell";
import { EntityDirectory } from "@/components/entity-directory";
import { ModuleFooter } from "@/components/module-footer";

export default async function CompaniesDirectoryPage({
  searchParams
}: {
  searchParams: Promise<{ q?: string }>;
}) {
  const { q } = await searchParams;

  return (
    <AppShell
      eyebrow="Directory"
      title="Companies & entities"
      description="Search the entity graph — companies, firms and advisors — and pivot across transactions and relationships."
    >
      <EntityDirectory initialQuery={q ?? ""} />
      <ModuleFooter module="companies" />
    </AppShell>
  );
}
