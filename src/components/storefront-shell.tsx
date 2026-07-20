// JHI-SIG: 69M2705M | Storefront Shell (public marketing) | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import type { ReactNode } from "react";
import { Logo } from "@/components/logo";
import { MarketTicker } from "@/components/market-ticker";

// Public marketing navigation only — kept separate from the authenticated
// Application shell (left-sidebar TOC). Segment/solution pages land in later phases.
const navigation = [
  { href: "/", label: "Home" },
  { href: "/pricing", label: "Pricing" },
  { href: "/about", label: "About" },
  { href: "/team", label: "Team" },
  { href: "/login", label: "Log in" }
];

type StorefrontShellProps = {
  eyebrow: string;
  title: string;
  description: string;
  children: ReactNode;
};

export function StorefrontShell({ eyebrow, title, description, children }: StorefrontShellProps) {
  return (
    <main className="app-shell">
      <MarketTicker />
      <header className="app-header">
        <Link className="app-header__brand" href="/">
          <Logo size={38} />
          JHI Research &amp; Analytics Firm, Inc.
        </Link>
        <nav className="app-nav" aria-label="Marketing navigation">
          {navigation.map((item) => (
            <Link href={item.href} key={item.href}>
              {item.label}
            </Link>
          ))}
          <Link className="app-nav__cta" href="/register">
            Start free
          </Link>
        </nav>
      </header>

      <section className="app-hero">
        <p className="eyebrow">{eyebrow}</p>
        <h1>{title}</h1>
        <p>{description}</p>
      </section>

      {children}
    </main>
  );
}
