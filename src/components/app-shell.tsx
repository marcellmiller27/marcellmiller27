// JHI-SIG: 69M2705M | Application Shell (menu-drawer nav) | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import type { ReactNode } from "react";
import { AppMenu } from "@/components/app-menu";
import { GlobalSearch } from "@/components/global-search";
import { Logo } from "@/components/logo";
import { MarketTicker } from "@/components/market-ticker";

type AppShellProps = {
  eyebrow?: string;
  title?: string;
  description?: string;
  children: ReactNode;
};

export function AppShell({ eyebrow, title, description, children }: AppShellProps) {
  return (
    <div className="app-root">
      <header className="app-topbar">
        <AppMenu />
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

      <main className="app-main">
        <MarketTicker />
        {title && (
          <section className="app-hero app-hero--compact">
            {eyebrow && <p className="eyebrow">{eyebrow}</p>}
            <h1>{title}</h1>
            {description && <p>{description}</p>}
          </section>
        )}
        {children}
      </main>
    </div>
  );
}
