// JHI-SIG: 69M2705M | Application Shell (left-sidebar TOC) | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import type { ReactNode } from "react";
import {
  BarChart3,
  Briefcase,
  Calculator,
  Download,
  FileSearch,
  FileText,
  Home,
  LifeBuoy,
  ScanSearch,
  Scale,
  Search,
  Sparkles,
  UserCircle,
  Workflow,
  type LucideIcon
} from "lucide-react";
import { GlobalSearch } from "@/components/global-search";
import { Logo } from "@/components/logo";
import { MarketTicker } from "@/components/market-ticker";

// The application Table of Contents (left sidebar). Function-first, institutional
// nomenclature; grouped by job-to-be-done. Each context carries a line icon
// (lucide) mirroring the institutional-workspace convention. Routes to existing
// modules today; the SEARCH entity set + full Tools taxonomy land in later phases.
type TocItem = { href: string; label: string; icon: LucideIcon };
type TocGroup = { section: string | null; items: TocItem[] };

const toc: TocGroup[] = [
  { section: null, items: [{ href: "/dashboard", label: "Dashboard", icon: Home }] },
  {
    section: "Research & Intelligence",
    items: [
      { href: "/macro", label: "Economics", icon: BarChart3 },
      { href: "/opportunities", label: "Screener", icon: Search },
      { href: "/reports", label: "Reports", icon: FileText }
    ]
  },
  {
    section: "Diligence a Target",
    items: [
      { href: "/deal-xray", label: "Scope", icon: ScanSearch },
      { href: "/diligence-suite", label: "Earnings", icon: Calculator },
      { href: "/due-diligence", label: "Document Review", icon: FileSearch }
    ]
  },
  {
    section: "Deal Workflow",
    items: [
      { href: "/pipeline", label: "Pipeline", icon: Workflow },
      { href: "/portfolio", label: "Portfolio", icon: Briefcase }
    ]
  },
  {
    section: "Outputs & AI",
    items: [
      { href: "/assistant", label: "Ask JHI", icon: Sparkles },
      { href: "/downloads", label: "Documents", icon: Download }
    ]
  },
  { section: "Firm Operations", items: [{ href: "/accounting", label: "Accounting", icon: Scale }] }
];

const utility: TocItem[] = [
  { href: "/account", label: "Account", icon: UserCircle },
  { href: "/support", label: "Help", icon: LifeBuoy }
];

type AppShellProps = {
  eyebrow: string;
  title: string;
  description: string;
  children: ReactNode;
};

export function AppShell({ eyebrow, title, description, children }: AppShellProps) {
  return (
    <div className="app-root">
      <header className="app-topbar">
        <Link className="app-topbar__brand" href="/dashboard">
          <Logo size={26} />
          <span>JHI Research &amp; Analytics</span>
        </Link>
        <GlobalSearch />
        <div className="app-topbar__actions">
          <Link className="app-topbar__ai" href="/assistant">
            Ask JHI
          </Link>
          <Link className="app-topbar__account" href="/account">
            Account
          </Link>
        </div>
      </header>

      <div className="app-layout">
        <aside className="app-sidebar" aria-label="Platform navigation">
          <nav className="app-toc">
            {toc.map((group, i) => (
              <div className="app-toc__group" key={group.section ?? `g${i}`}>
                {group.section && <p className="app-toc__section">{group.section}</p>}
                {group.items.map((item) => (
                  <Link href={item.href} key={item.href}>
                    <item.icon size={16} strokeWidth={1.75} aria-hidden />
                    <span>{item.label}</span>
                  </Link>
                ))}
              </div>
            ))}
            <div className="app-toc__group app-toc__group--utility">
              {utility.map((item) => (
                <Link href={item.href} key={item.href}>
                  <item.icon size={16} strokeWidth={1.75} aria-hidden />
                  <span>{item.label}</span>
                </Link>
              ))}
            </div>
          </nav>
        </aside>

        <div className="app-main">
          <MarketTicker />
          <section className="app-hero app-hero--compact">
            <p className="eyebrow">{eyebrow}</p>
            <h1>{title}</h1>
            <p>{description}</p>
          </section>
          {children}
        </div>
      </div>
    </div>
  );
}
