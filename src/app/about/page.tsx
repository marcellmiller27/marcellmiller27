import { StorefrontShell } from "@/components/storefront-shell";

// About / "Our story" — deliberately anonymous. Credibility comes from problem
// clarity, method, focus, and a real entity — no personal names, photos, or bios.

const sectors = [
  "Defense & government finance",
  "Logistics & transportation",
  "Healthcare",
  "Restaurants & hospitality",
  "Retail & automotive",
  "Software",
  "Public housing",
  "Manufacturing"
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
      "We publish how our scores work and their limits. You see the work, not just the number."
  },
  {
    name: "Intentional focus",
    detail:
      "We don't try to be Bloomberg. We do research and acquisition diligence for independent buyers — deeply."
  },
  {
    name: "Licensed data",
    detail:
      "Point-in-time fundamentals and market data from licensed providers, with clear provenance."
  },
  {
    name: "Discipline & security",
    detail:
      "A national-security discipline around the financial data our subscribers trust us with."
  }
];

const bodyStyle = {
  maxWidth: "62rem",
  color: "var(--muted-strong)",
  fontSize: "var(--fs-lg)",
  lineHeight: 1.7
} as const;

export default function AboutPage() {
  return (
    <StorefrontShell
      eyebrow="About · Aegira"
      title="See what Wall Street sees."
      description="Institutional-grade market, economic, and deal intelligence — for the independent investor and acquirer."
    >
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">What we do</p>
          <h2>Institutional research shouldn&rsquo;t be locked behind a $30,000 contract.</h2>
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
          <p className="eyebrow">Who we are</p>
          <h2>Veteran-led. Combat-tested. Built to endure.</h2>
        </div>
        <p style={bodyStyle}>
          Aegira is built and published by JHI Research &amp; Analytics Firm, Inc., and led by
          operators with 20+ years of experience building accounting systems,
          internal controls, and financial reporting — plus hands-on experience running an
          accounting, tax, and audit practice. Our senior accounting and finance leadership
          includes a CPA candidate, with a career spent operating businesses across:
        </p>
        <div className="tag-grid" style={{ marginTop: "1rem" }}>
          {sectors.map((s) => (
            <span className="tag" key={s}>
              {s}
            </span>
          ))}
        </div>
        <p style={{ ...bodyStyle, marginTop: "1rem" }}>
          Our cross-sector depth allows us to thoroughly understand the businesses that people
          actually operate and acquire, rather than focusing solely on tech startups. Please note
          that formal Quality-of-Earnings and attest work is delivered through our network of
          licensed partner CPAs.
        </p>
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">How we work</p>
          <h2>Human judgment, machine speed.</h2>
        </div>
        <div className="trust-grid">
          {principles.map((p) => (
            <article className="trust-card" key={p.name}>
              <h3>{p.name}</h3>
              <p>{p.detail}</p>
            </article>
          ))}
        </div>
      </section>
    </StorefrontShell>
  );
}
