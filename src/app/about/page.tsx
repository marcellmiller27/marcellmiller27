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
      eyebrow="About · JHI Research & Analytics Firm, Inc."
      title="We are a team of operators augmented by AI."
      description="At John Henry Investments, we combine a lean team of skilled operators with advanced AI to deliver the capabilities and output of a much larger firm. Rather than competing with technology, we leverage it to maximize our efficiency and results."
    >
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Why we exist</p>
          <h2>Institutional research shouldn&rsquo;t be locked behind a $30,000 contract.</h2>
        </div>
        <p style={bodyStyle}>
          Diligence data is often fragmented and expensive, and the initial review of a CIM can
          consume days of senior leadership&rsquo;s time — frequently on deals that do not move
          forward. We built JHI to provide independent investors and acquirers with
          institutional-grade research and diligence that is clear, transparent, and grounded in
          real data. We offer this at a fraction of the traditional cost, with a genuine trial
          period and no contract lock-in.
        </p>
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Who we are</p>
          <h2>Veteran-led. Combat-tested. Built to endure.</h2>
        </div>
        <p style={bodyStyle}>
          JHI is led by operators with 20+ years of experience building accounting systems,
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
