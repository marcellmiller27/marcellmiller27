// JHI-SIG: 69M2705M | Home — the Aegira story | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { ModuleFooter } from "@/components/module-footer";
import { TeamShowcase } from "@/components/team-showcase";

// Home is the narrative front page: what Aegira is, what it does, who builds it.
// (The Dashboard is the working launchpad; this page tells the story.)

const bodyStyle = {
  maxWidth: "62rem",
  color: "var(--muted-strong)",
  fontSize: "var(--fs-lg)",
  lineHeight: 1.7
} as const;

const pillars = [
  {
    name: "Markets & Research",
    detail:
      "Economics (Federal Reserve, Treasury, BEA, BLS, IMF, OECD, World Bank), a fundamentals Screener, branded Reports, and the AI-authored Newsletters — one economic view across equities, credit, commodities, crypto, and forex."
  },
  {
    name: "Acquire & Diligence",
    detail:
      "For search-fund and SMB acquirers: a Limited Scope Review of a target's economics, a Quality-of-Earnings–style Earnings analysis, Document Review, and a Pipeline and Portfolio to move each target from screen to close."
  }
];

const family = [
  "Aegira Platform",
  "Aegira AI",
  "Aegira Markets",
  "Aegira Research",
  "Aegira Terminal",
  "Aegira API",
  "Aegira Mobile",
  "Aegira Studio",
  "Aegira Enterprise"
];

const principles = [
  {
    name: "Research, not advice",
    detail:
      "We deliver research, analytics, and decision-support — never investment advice or brokerage."
  },
  {
    name: "Radical transparency",
    detail:
      "We publish how our scores and methodologies work, and their limits. You see the work, not just the number."
  },
  {
    name: "Grounded, fact-locked AI",
    detail:
      "AI elevates the writing; it never invents a figure. Numbers are locked to the underlying data, with provenance."
  },
  {
    name: "Institutional standard",
    detail:
      "How we do anything is how we do everything — every detail, down to the smallest point, is held to a Tier-1 bar."
  }
];

export default function HomePage() {
  return (
    <AppShell
      eyebrow="The Aegira Story"
      title="See what Wall Street sees."
      description="Institutional-grade market, economic, and deal intelligence — for the independent investor and acquirer."
    >
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">What we do</p>
          <h2>The tools hedge funds pay six figures for — by subscription.</h2>
        </div>
        <p style={bodyStyle}>
          Aegira pulls live economic, market, and company data — the Fed, the Treasury, SEC
          filings, and prices across stocks, crypto, commodities, and forex — and turns it into
          decision-ready output: valuations, opportunity screens, technical trade setups, and
          branded research briefings. It&rsquo;s the capability hedge funds and PE firms pay six
          figures for, delivered to independent investors and acquirers by subscription. Named for
          the aegis — the shield.
        </p>
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">What you can do</p>
          <h2>Two pillars, one shared spine.</h2>
        </div>
        <div className="trust-grid">
          {pillars.map((p) => (
            <article className="trust-card" key={p.name}>
              <h3>{p.name}</h3>
              <p>{p.detail}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">The product family</p>
          <h2>Aegira grows with you.</h2>
        </div>
        <div className="tag-grid" style={{ marginTop: "1rem" }}>
          {family.map((f) => (
            <span className="tag" key={f}>
              {f}
            </span>
          ))}
        </div>
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">The team</p>
          <h2>A lean team of operators, augmented by AI.</h2>
        </div>
        <p style={{ ...bodyStyle, marginBottom: "1.25rem" }}>
          The platform is built and maintained by an AI engineering department and an AI
          editorial desk, supported 24/7 by five specialized AI agents — onboarding,
          subscriptions &amp; billing, account &amp; security, product &amp; markets, and
          technical triage (which escalates to the founder). Every agent works under human
          direction.
        </p>
        <TeamShowcase />
        <p style={{ ...bodyStyle, marginTop: "1.25rem", fontSize: "var(--fs-md)" }}>
          The same roster is on the dedicated <Link href="/team">Team page</Link>.
        </p>
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Our standard</p>
          <h2>How we do anything is how we do everything.</h2>
        </div>
        <div className="trust-grid">
          {principles.map((p) => (
            <article className="trust-card" key={p.name}>
              <h3>{p.name}</h3>
              <p>{p.detail}</p>
            </article>
          ))}
        </div>
        <p style={{ ...bodyStyle, marginTop: "1.5rem", fontSize: "var(--fs-md)" }}>
          Aegira is a product of JHI Research &amp; Analytics Firm, Inc. · JHI-SIG: 69M2705M.
        </p>
      </section>

      <ModuleFooter module="home" />
    </AppShell>
  );
}
