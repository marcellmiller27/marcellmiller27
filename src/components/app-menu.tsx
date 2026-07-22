// JHI-SIG: 69M2705M | Application menu (click drawer) | JHI Research & Analytics Firm, Inc. (proprietary)
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
  ScanSearch,
  Scale,
  Search,
  Sparkles,
  UserCircle,
  Workflow,
  X,
  type LucideIcon
} from "lucide-react";

// The application Table of Contents, presented as a click-to-open menu drawer
// (mirrors the institutional "☰ MENU" pattern). Function-first nomenclature,
// grouped by job-to-be-done; each context carries a line icon.
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

export function AppMenu() {
  const [open, setOpen] = useState(false);
  const close = () => setOpen(false);

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
            {toc.map((group, i) => (
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
            <div className="app-toc__group app-toc__group--utility">
              {utility.map((item) => (
                <Link href={item.href} key={item.href} onClick={close}>
                  <item.icon size={16} strokeWidth={1.75} aria-hidden />
                  <span>{item.label}</span>
                </Link>
              ))}
            </div>
          </nav>
        </aside>
      </div>
    </>
  );
}
