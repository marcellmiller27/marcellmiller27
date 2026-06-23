import Link from "next/link";
import type { ReactNode } from "react";

const navigation = [
  { href: "/", label: "Home" },
  { href: "/dashboard", label: "Dashboard" },
  { href: "/opportunities", label: "Opportunities" },
  { href: "/due-diligence", label: "Due Diligence" },
  { href: "/portfolio", label: "Portfolio" },
  { href: "/reports", label: "Reports" },
  { href: "/assistant", label: "AI Assistant" }
];

type PlatformShellProps = {
  eyebrow: string;
  title: string;
  description: string;
  children: ReactNode;
};

export function PlatformShell({ eyebrow, title, description, children }: PlatformShellProps) {
  return (
    <main className="app-shell">
      <header className="app-header">
        <Link className="app-header__brand" href="/">
          <span>JH</span>
          John Henry Investments
        </Link>
        <nav className="app-nav" aria-label="Application navigation">
          {navigation.map((item) => (
            <Link href={item.href} key={item.href}>
              {item.label}
            </Link>
          ))}
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
