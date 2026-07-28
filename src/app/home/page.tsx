// JHI-SIG: 69M2705M | Home — the Aegira story | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";
import { AppShell } from "@/components/app-shell";

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

const team = [
  {
    name: "Cy Henry",
    role: "VP of Software Engineering (AI)",
    detail: "Builds and hardens the platform end-to-end — human-directed, shipped via review."
  },
  {
    name: "Ellery Vance",
    role: "VP of Editorial (AI)",
    detail: "Leads the editorial desk — turning polled data into grounded, institutional-grade intelligence."
  }
];

export default function HomePage() {
  return (
    <AppShell
      eyebrow="The Aegira Story"
      title="Institutional intelligence for global markets."
      description="Aegira is an operating system for economic and deal intelligence — built so independent investors and acquirers can see further, and act with conviction."
    >
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">What Aegira is</p>
          <h2>One platform for the whole decision — research through diligence.</h2>
        </div>
        <p style={bodyStyle}>
          Institutional-grade research and diligence have long been locked behind five- and
          six-figure contracts. Aegira brings that capability to independent investors and
          acquirers: live economic data, cross-asset market intelligence, fundamentals screening,
          and acquisition diligence — clear, transparent, grounded in real data, and delivered on a
          fixed, honest cadence. Two connected pillars carry the work.
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
        <div className="trust-grid">
          {team.map((t) => (
            <article className="trust-card" key={t.name}>
              <h3>{t.name}</h3>
              <p>
                <strong>{t.role}</strong>
                <br />
                {t.detail}
              </p>
            </article>
          ))}
        </div>
        <p style={{ ...bodyStyle, marginTop: "1rem" }}>
          Meet the full team, including leadership and the AI desk, on the{" "}
          <Link href="/team">Team page</Link>.
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
    </AppShell>
  );
}
