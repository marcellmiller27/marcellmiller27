// JHI-SIG: 69M2705M | Application Shell (left-sidebar TOC) | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import type { ReactNode } from "react";
import { Logo } from "@/components/logo";
import { MarketTicker } from "@/components/market-ticker";

// The application Table of Contents (left sidebar). Function-first, institutional
// nomenclature; grouped by job-to-be-done. Routes to existing modules today; the
// SEARCH entity set + full Tools taxonomy land in later phases.
type TocItem = { href: string; label: string };
type TocGroup = { section: string | null; items: TocItem[] };

const toc: TocGroup[] = [
  { section: null, items: [{ href: "/dashboard", label: "Dashboard" }] },
  {
    section: "Research & Intelligence",
    items: [
      { href: "/macro", label: "Macro Dashboard" },
      { href: "/opportunities", label: "Opportunity Screener" },
      { href: "/reports", label: "Reports" }
    ]
  },
  {
    section: "Diligence a Target",
    items: [
      { href: "/deal-xray", label: "Limited Scope Review" },
      { href: "/diligence-suite", label: "Quality of Earnings" },
      { href: "/due-diligence", label: "Document Review" }
    ]
  },
  {
    section: "Deal Workflow",
    items: [
      { href: "/pipeline", label: "Pipeline" },
      { href: "/portfolio", label: "Portfolio" }
    ]
  },
  {
    section: "Outputs & AI",
    items: [
      { href: "/assistant", label: "Ask JHI" },
      { href: "/downloads", label: "Documents" }
    ]
  },
  { section: "Firm Operations", items: [{ href: "/accounting", label: "Accounting" }] }
];

const utility: TocItem[] = [
  { href: "/account", label: "Account" },
  { href: "/support", label: "Help" }
];

type AppShellProps = {
  eyebrow: string;
  title: string;
  description: string;
  children: ReactNode;
};

export function AppShell({ eyebrow, title, description, children }: AppShellProps) {
  return (
    <div className="app-layout">
      <aside className="app-sidebar" aria-label="Platform navigation">
        <Link className="app-sidebar__brand" href="/dashboard">
          <Logo size={30} />
          <span>JHI Research &amp; Analytics</span>
        </Link>
        <nav className="app-toc">
          {toc.map((group, i) => (
            <div className="app-toc__group" key={group.section ?? `g${i}`}>
              {group.section && <p className="app-toc__section">{group.section}</p>}
              {group.items.map((item) => (
                <Link href={item.href} key={item.href}>
                  {item.label}
                </Link>
              ))}
            </div>
          ))}
          <div className="app-toc__group app-toc__group--utility">
            {utility.map((item) => (
              <Link href={item.href} key={item.href}>
                {item.label}
              </Link>
            ))}
          </div>
        </nav>
      </aside>

      <div className="app-main">
        <header className="app-topbar">
          <input
            className="app-search"
            type="search"
            placeholder="Search companies, transactions, filings…"
            aria-label="Global search"
          />
          <div className="app-topbar__actions">
            <Link className="app-topbar__ai" href="/assistant">
              Ask JHI
            </Link>
            <Link className="app-topbar__account" href="/account">
              Account
            </Link>
          </div>
        </header>

        <MarketTicker />

        <section className="app-hero app-hero--compact">
          <p className="eyebrow">{eyebrow}</p>
          <h1>{title}</h1>
          <p>{description}</p>
        </section>

        {children}
      </div>
    </div>
  );
}
