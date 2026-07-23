// JHI-SIG: 69M2705M | Application menu (role-aware click drawer) | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { useState } from "react";
import Link from "next/link";
import {
  BarChart3,
  Briefcase,
  Calculator,
  Download,
  FileSearch,
  FileText,
  Home,
  LifeBuoy,
  Menu,
  Newspaper,
  ScanSearch,
  Scale,
  Search,
  Sparkles,
  UserCircle,
  Workflow,
  X,
  type LucideIcon
} from "lucide-react";
import { useRole } from "@/components/role-provider";
import { meetsAccess, type AccessLevel } from "@/lib/roles";

// The application Table of Contents, presented as a click-to-open menu drawer.
// Each item carries an `access` tier: staff-only (back-end/firm ops), subscriber
// (the product), or free (Newsletter + account). The menu is filtered by the
// viewer's role — free-newsletter registrants see only the Newsletter module.
type TocItem = { href: string; label: string; icon: LucideIcon; access: AccessLevel };
type TocGroup = { section: string | null; items: TocItem[] };

const toc: TocGroup[] = [
  { section: null, items: [{ href: "/dashboard", label: "Dashboard", icon: Home, access: "subscriber" }] },
  {
    section: "Research & Intelligence",
    items: [
      { href: "/macro", label: "Economics", icon: BarChart3, access: "subscriber" },
      { href: "/opportunities", label: "Screener", icon: Search, access: "subscriber" },
      { href: "/reports", label: "Reports", icon: FileText, access: "subscriber" }
    ]
  },
  {
    section: "Diligence a Target",
    items: [
      { href: "/deal-xray", label: "Scope", icon: ScanSearch, access: "subscriber" },
      { href: "/diligence-suite", label: "Earnings", icon: Calculator, access: "subscriber" },
      { href: "/due-diligence", label: "Document Review", icon: FileSearch, access: "subscriber" }
    ]
  },
  {
    section: "Deal Workflow",
    items: [
      { href: "/pipeline", label: "Pipeline", icon: Workflow, access: "subscriber" },
      { href: "/portfolio", label: "Portfolio", icon: Briefcase, access: "subscriber" }
    ]
  },
  {
    section: "Outputs & AI",
    items: [
      { href: "/newsletters", label: "Newsletter", icon: Newspaper, access: "free" },
      { href: "/assistant", label: "Ask JHI", icon: Sparkles, access: "subscriber" },
      { href: "/downloads", label: "Documents", icon: Download, access: "subscriber" }
    ]
  },
  {
    section: "Firm Operations",
    items: [{ href: "/accounting", label: "Accounting", icon: Scale, access: "staff" }]
  }
];

const utility: TocItem[] = [
  { href: "/account", label: "Account", icon: UserCircle, access: "free" },
  { href: "/support", label: "Help", icon: LifeBuoy, access: "free" }
];

export function AppMenu() {
  const [open, setOpen] = useState(false);
  const { role } = useRole();
  const close = () => setOpen(false);

  const visibleToc = toc
    .map((g) => ({ ...g, items: g.items.filter((it) => meetsAccess(role, it.access)) }))
    .filter((g) => g.items.length > 0);
  const visibleUtil = utility.filter((it) => meetsAccess(role, it.access));

  return (
    <>
      <button
        type="button"
        className="app-menu-btn"
        aria-haspopup="menu"
        aria-expanded={open}
        onClick={() => setOpen(true)}
      >
        <Menu size={16} strokeWidth={2} aria-hidden />
        <span>Menu</span>
      </button>

      <div className={`app-drawer${open ? " app-drawer--open" : ""}`} aria-hidden={!open}>
        <button className="app-drawer__backdrop" aria-label="Close menu" onClick={close} />
        <aside className="app-drawer__panel" aria-label="Platform navigation">
          <div className="app-drawer__header">
            <span>Menu</span>
            <button
              type="button"
              className="app-drawer__close"
              aria-label="Close menu"
              onClick={close}
            >
              <X size={18} aria-hidden />
            </button>
          </div>
          <nav className="app-toc">
            {visibleToc.map((group, i) => (
              <div className="app-toc__group" key={group.section ?? `g${i}`}>
                {group.section && <p className="app-toc__section">{group.section}</p>}
                {group.items.map((item) => (
                  <Link href={item.href} key={item.href} onClick={close}>
                    <item.icon size={16} strokeWidth={1.75} aria-hidden />
                    <span>{item.label}</span>
                  </Link>
                ))}
              </div>
            ))}
            {visibleUtil.length > 0 && (
              <div className="app-toc__group app-toc__group--utility">
                {visibleUtil.map((item) => (
                  <Link href={item.href} key={item.href} onClick={close}>
                    <item.icon size={16} strokeWidth={1.75} aria-hidden />
                    <span>{item.label}</span>
                  </Link>
                ))}
              </div>
            )}
          </nav>
        </aside>
      </div>
    </>
  );
}
