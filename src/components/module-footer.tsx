// JHI-SIG: 69M2705M | Module footer — actionable next-step CTAs | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { useRole } from "@/components/role-provider";
import { meetsAccess, type AccessLevel } from "@/lib/roles";

// A consistent "what to do next" block placed at the BOTTOM of each module page
// (in the spirit of Mergr / 42Macro / ARK Invest). CTAs are REAL in-app links,
// centralized here per module so the copy stays consistent, and each carries the
// same access tier used by the menu so staff-only / subscriber-only actions are
// never surfaced to a viewer who cannot use them.
type Cta = { href: string; label: string; hint: string; access: AccessLevel };
type ModuleId =
  | "dashboard"
  | "home"
  | "valuation"
  | "opportunities"
  | "macro"
  | "reports"
  | "newsletters"
  | "framework"
  | "deal-xray"
  | "diligence-suite"
  | "due-diligence"
  | "pipeline"
  | "portfolio"
  | "companies"
  | "assistant";

// Real, in-app CTAs per module. Access tiers mirror src/components/app-menu.tsx.
const MODULE_CTAS: Record<ModuleId, Cta[]> = {
  dashboard: [
    { href: "/opportunities", label: "Screen opportunities", hint: "Rank ideas by fundamentals", access: "subscriber" },
    { href: "/deal-xray", label: "Run a Limited Scope Review", hint: "Fast read of a target", access: "subscriber" },
    { href: "/macro", label: "View Economics", hint: "Fed, Treasury & global data", access: "subscriber" },
    { href: "/newsletters", label: "Read the latest Brief", hint: "This week's editions", access: "free" }
  ],
  home: [
    { href: "/dashboard", label: "Open the Dashboard", hint: "Your working launchpad", access: "subscriber" },
    { href: "/opportunities", label: "Explore the Screener", hint: "Rank ideas by fundamentals", access: "subscriber" },
    { href: "/deal-xray", label: "Run a Limited Scope Review", hint: "Fast read of a target", access: "subscriber" },
    { href: "/newsletters", label: "Read the Newsletter", hint: "This week's editions", access: "free" }
  ],
  valuation: [
    { href: "/deal-xray", label: "Run a Limited Scope Review", hint: "Take a target to diligence", access: "subscriber" },
    { href: "/opportunities", label: "See the Screener", hint: "Find the next name to value", access: "subscriber" },
    { href: "/newsletters/economic-brief", label: "Read the latest Brief", hint: "Cross-asset context", access: "free" },
    { href: "/assistant", label: "Ask Aegira", hint: "Security analysis on demand", access: "subscriber" }
  ],
  opportunities: [
    { href: "/valuation", label: "Value a company", hint: "DCF + implied return", access: "subscriber" },
    { href: "/deal-xray", label: "Run a Limited Scope Review", hint: "Fast read of a target", access: "subscriber" },
    { href: "/newsletters/opportunity-scan", label: "Read the Opportunity Scan", hint: "This week's screen write-up", access: "free" },
    { href: "/macro", label: "View Economics", hint: "The macro backdrop", access: "subscriber" }
  ],
  macro: [
    { href: "/opportunities", label: "View the Screener", hint: "Turn the read into ideas", access: "subscriber" },
    { href: "/newsletters/economic-brief", label: "Read the Economic Brief", hint: "The depth mandate", access: "free" },
    { href: "/reports", label: "See Reports", hint: "Branded economic intelligence", access: "subscriber" }
  ],
  reports: [
    { href: "/newsletters/economic-brief", label: "Read the Economic Brief", hint: "This week's edition", access: "free" },
    { href: "/macro", label: "View Economics", hint: "Live federal & global data", access: "subscriber" },
    { href: "/opportunities", label: "Open the Screener", hint: "Rank ideas by fundamentals", access: "subscriber" }
  ],
  newsletters: [
    { href: "/opportunities", label: "View the Screener", hint: "Rank ideas by fundamentals", access: "subscriber" },
    { href: "/deal-xray", label: "Run a Limited Scope Review", hint: "Fast read of a target", access: "subscriber" },
    { href: "/macro", label: "View Economics", hint: "Fed, Treasury & global data", access: "subscriber" }
  ],
  framework: [
    { href: "/framework/ratios", label: "Run the key-ratio tool", hint: "Screen a company's ratios", access: "free" },
    { href: "/framework/due-diligence", label: "Open the DD checklist", hint: "Structured diligence steps", access: "free" },
    { href: "/deal-xray", label: "Run a Limited Scope Review", hint: "Apply it to a target", access: "subscriber" }
  ],
  "deal-xray": [
    { href: "/diligence-suite", label: "Run Quality of Earnings", hint: "Normalize the earnings", access: "subscriber" },
    { href: "/due-diligence", label: "Review the documents", hint: "Flag risk in the file", access: "subscriber" },
    { href: "/pipeline", label: "Add to the Pipeline", hint: "Move it toward close", access: "subscriber" },
    { href: "/valuation", label: "Value the company", hint: "Cross-check the price", access: "subscriber" }
  ],
  "diligence-suite": [
    { href: "/deal-xray", label: "Run a Limited Scope Review", hint: "Score the whole deal", access: "subscriber" },
    { href: "/due-diligence", label: "Review the documents", hint: "Flag risk in the file", access: "subscriber" },
    { href: "/pipeline", label: "Track in the Pipeline", hint: "Move it toward close", access: "subscriber" }
  ],
  "due-diligence": [
    { href: "/deal-xray", label: "Run a Limited Scope Review", hint: "Score the whole deal", access: "subscriber" },
    { href: "/diligence-suite", label: "Run Quality of Earnings", hint: "Normalize the earnings", access: "subscriber" },
    { href: "/framework/due-diligence", label: "Open the DD checklist", hint: "Structured diligence steps", access: "free" }
  ],
  pipeline: [
    { href: "/portfolio", label: "View the Portfolio", hint: "Consolidated holdings", access: "subscriber" },
    { href: "/deal-xray", label: "Run a Limited Scope Review", hint: "Diligence a new target", access: "subscriber" },
    { href: "/opportunities", label: "Screen new targets", hint: "Refill the top of funnel", access: "subscriber" }
  ],
  portfolio: [
    { href: "/pipeline", label: "Open the Pipeline", hint: "Active targets to close", access: "subscriber" },
    { href: "/opportunities", label: "Screen opportunities", hint: "Find the next allocation", access: "subscriber" },
    { href: "/valuation", label: "Value a holding", hint: "Re-underwrite the price", access: "subscriber" }
  ],
  companies: [
    { href: "/valuation", label: "Value a company", hint: "DCF + implied return", access: "subscriber" },
    { href: "/opportunities", label: "Screen more names", hint: "Rank the universe", access: "subscriber" },
    { href: "/deal-xray", label: "Run a Limited Scope Review", hint: "Fast read of a target", access: "subscriber" }
  ],
  assistant: [
    { href: "/dashboard", label: "Open the Dashboard", hint: "Your working launchpad", access: "subscriber" },
    { href: "/opportunities", label: "Screen opportunities", hint: "Rank ideas by fundamentals", access: "subscriber" },
    { href: "/valuation", label: "Value a company", hint: "DCF + implied return", access: "subscriber" }
  ]
};

export function ModuleFooter({ module, heading = "Where to next" }: { module: ModuleId; heading?: string }) {
  const { role } = useRole();
  const actions = (MODULE_CTAS[module] ?? []).filter((cta) => meetsAccess(role, cta.access));
  if (actions.length === 0) return null;

  return (
    <section className="module-footer" aria-label="Suggested next actions">
      <p className="module-footer__eyebrow">{heading}</p>
      <div className="module-footer__grid">
        {actions.map((cta) => (
          <Link className="module-footer__cta" href={cta.href} key={cta.href}>
            <span className="module-footer__label">
              {cta.label}
              <ArrowRight size={14} strokeWidth={1.75} aria-hidden />
            </span>
            <span className="module-footer__hint">{cta.hint}</span>
          </Link>
        ))}
      </div>
    </section>
  );
}
