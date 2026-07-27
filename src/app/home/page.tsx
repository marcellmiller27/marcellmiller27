// JHI-SIG: 69M2705M | Home (front-door launchpad) | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import {
  ArrowUpRight,
  BarChart3,
  Briefcase,
  Calculator,
  Download,
  FileSearch,
  FileText,
  ScanSearch,
  Search,
  Sparkles,
  Workflow,
  type LucideIcon
} from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { dashboardLaunchpad } from "@/lib/platform-data";

// Map each launchpad context to its line icon (shares the TOC iconography).
const launchIcons: Record<string, LucideIcon> = {
  Economics: BarChart3,
  Screener: Search,
  Reports: FileText,
  Scope: ScanSearch,
  Earnings: Calculator,
  "Document Review": FileSearch,
  Pipeline: Workflow,
  Portfolio: Briefcase,
  "Ask Aegira": Sparkles,
  Documents: Download
};

export default function HomePage() {
  return (
    <AppShell
      eyebrow="Aegira"
      title="Home"
      description="Your launchpad — jump into any module below."
    >
      <div className="home-launch">
        {dashboardLaunchpad.map((group) => (
          <section className="launch-group" key={group.section}>
            <p className="eyebrow">{group.section}</p>
            <div className="launch-grid">
              {group.items.map((item) => {
                const Icon = launchIcons[item.label] ?? ArrowUpRight;
                return (
                  <Link className="launch-card" href={item.href} key={item.href}>
                    <span className="launch-card__icon">
                      <Icon size={20} strokeWidth={1.75} aria-hidden />
                    </span>
                    <span className="launch-card__body">
                      <span className="launch-card__title">
                        <h3>{item.label}</h3>
                        <ArrowUpRight className="launch-card__go" size={15} aria-hidden />
                      </span>
                      <p>{item.blurb}</p>
                      <span className="launch-card__meta">{item.meta}</span>
                    </span>
                  </Link>
                );
              })}
            </div>
          </section>
        ))}
      </div>
    </AppShell>
  );
}
