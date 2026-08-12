import { LiveMacro } from "@/components/live-macro";
import { AppShell } from "@/components/app-shell";
import { ModuleFooter } from "@/components/module-footer";

export default function MacroPage() {
  return (
    <AppShell
      eyebrow="Economy"
      title="Economics"
      description="Live federal and global economic data in one view — the Federal Reserve (FRED), BEA national accounts, US Treasury, World Bank, IMF, and OECD."
    >
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Live economic indicators</p>
          <h2>Federal Policy &amp; Global Economic Data</h2>
        </div>
        <LiveMacro />
      </section>

      <ModuleFooter module="macro" />
    </AppShell>
  );
}
