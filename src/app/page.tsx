import Link from "next/link";
import { Logo } from "@/components/logo";
import { WaitlistForm } from "@/components/waitlist-form";
import { dashboardWidgets, pricingTiers } from "@/lib/platform-data";

// Customer-facing homepage. Internal figures (ARR targets, per-tier revenue,
// module blueprint, tech stack, enterprise valuation) live in the investor deck,
// never here. Legal entity: JHI Research & Analytics Firm, Inc.

const audiences = [
  "Search-Fund & SMB Acquirers",
  "Independent Sponsors",
  "Family Offices",
  "Investment Advisors (RIAs)",
  "CPAs",
  "Attorneys",
  "Business Brokers",
  "Executive Recruiters",
  "Self-Directed Investors"
];

const workflow = [
  {
    step: "01",
    name: "Screen",
    summary:
      "Surface and rank opportunities with the Opportunity Score across public markets, crypto, real assets, and private businesses."
  },
  {
    step: "02",
    name: "Deal X-Ray",
    summary:
      "X-ray a CIM in minutes: a Business Quality Assessment, an honest ethic rating, a per-deal valuation, and DSCR / SBA financing fit."
  },
  {
    step: "03",
    name: "Quality of Earnings",
    summary:
      "Software-accelerated QoE — proof-of-cash, normalized EBITDA, working capital, red flags — reviewed and signed by a partner CPA."
  },
  {
    step: "04",
    name: "Pipeline & Close",
    summary:
      "Track every target from screen to close, with interactive Excel models and branded PDF memos you can hand to lenders and sellers."
  }
];

const products = [
  {
    name: "Deal X-Ray (BQA)",
    summary:
      "A six-segment Business Quality Assessment, Deal Score, valuation, and financing options from a CIM's key figures."
  },
  {
    name: "Quality of Earnings",
    summary:
      "CPA-signed QoE at software speed — a fraction of the cost and time of a manual engagement."
  },
  {
    name: "Deal Pipeline",
    summary:
      "Save every analysis and move targets through Screen → Diligence → Financing → Offer → Close."
  },
  {
    name: "Interactive Excel & PDF",
    summary:
      "Live, editable models (DSCR, valuation, scenarios) and branded memos — yours to keep, no download limits."
  },
  {
    name: "Multi-Asset Research",
    summary:
      "Live data and macro signals across equities, ETFs, fixed income, crypto, commodities, and real assets."
  },
  {
    name: "Opportunity & Deal Score",
    summary:
      "A transparent 0–100 decision-support score — with published methodology, not a black box."
  }
];

const trust = [
  {
    name: "Research, not advice",
    detail:
      "We deliver research, analytics, and decision-support — not investment advice or brokerage."
  },
  {
    name: "Transparent methodology",
    detail:
      "We publish how our scores work and their validation limits. You can see the work, not just the number."
  },
  {
    name: "Licensed data",
    detail:
      "Point-in-time fundamentals and market data from licensed providers, with clear provenance."
  },
  {
    name: "Partner CPA network",
    detail:
      "Formal Quality-of-Earnings and attest work is delivered by licensed partner CPA firms."
  }
];

export default function Home() {
  return (
    <main>
      <section className="hero section">
        <div className="hero__content">
          <Link className="hero__brand" href="/">
            <Logo size={44} />
            John Henry Investments
          </Link>
          <p className="eyebrow">JHI Research &amp; Analytics Firm, Inc.</p>
          <h1>Institutional research and deal diligence — without the institutional price.</h1>
          <p className="hero__lead">
            Screen opportunities, x-ray a CIM, run a CPA-signed Quality of Earnings, and track
            every deal to close. Multi-asset research and acquisition intelligence, built for
            independent investors and acquirers.
          </p>
          <div className="hero__actions">
            <a className="button button--primary" href="#waitlist">
              Start free — no sales call
            </a>
            <a className="button button--secondary" href="/dashboard">
              Open the platform
            </a>
          </div>
          <p className="hero__trust">No lock-in · Cancel anytime · No auto-renewal traps.</p>
        </div>
        <div className="hero__panel" aria-label="Platform summary">
          <div className="score-card">
            <span>John Henry Opportunity Score</span>
            <strong>87</strong>
            <p>Transparent 0–100 decision-support score with published methodology.</p>
          </div>
          <div className="mini-grid">
            {dashboardWidgets.map((widget) => (
              <span key={widget}>{widget}</span>
            ))}
          </div>
        </div>
      </section>

      <section className="section contrast-strip">
        <p>
          Institutional-grade research — <strong>without the $30,000 contract, the fake trial,
          or the renewal trap.</strong>
        </p>
      </section>

      <section className="section split">
        <div>
          <p className="eyebrow">Who it&rsquo;s for</p>
          <h2>Built for buyers and the professionals who advise them.</h2>
        </div>
        <div className="tag-grid">
          {audiences.map((a) => (
            <span className="tag" key={a}>
              {a}
            </span>
          ))}
        </div>
      </section>

      <section className="section" id="workflow">
        <div className="section-heading">
          <p className="eyebrow">How it works</p>
          <h2>From first look to closing — get to &ldquo;no&rdquo; fast, and &ldquo;yes&rdquo; with conviction.</h2>
        </div>
        <div className="module-grid">
          {workflow.map((s) => (
            <article className="module-card" key={s.name}>
              <p className="module-card__phase">{s.step}</p>
              <h3>{s.name}</h3>
              <p>{s.summary}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section" id="product">
        <div className="section-heading">
          <p className="eyebrow">What you get</p>
          <h2>One platform for research, diligence, and deal workflow.</h2>
        </div>
        <div className="module-grid">
          {products.map((p) => (
            <article className="module-card" key={p.name}>
              <h3>{p.name}</h3>
              <p>{p.summary}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section" id="plans">
        <div className="section-heading">
          <p className="eyebrow">Plans &amp; pricing</p>
          <h2>Simple, transparent pricing. Start free.</h2>
        </div>
        <div className="pricing-grid">
          {pricingTiers.map((tier) => (
            <article className="pricing-card" key={tier.name}>
              <div>
                <p className="pricing-card__audience">{tier.audience}</p>
                <h3>{tier.name}</h3>
                <strong>{tier.price}</strong>
              </div>
              <ul>
                {tier.features.map((feature) => (
                  <li key={feature}>{feature}</li>
                ))}
              </ul>
            </article>
          ))}
        </div>
        <p className="pricing-note">
          Month-to-month. Cancel anytime. No auto-renewal traps, no per-seat surprises.
        </p>
      </section>

      <section className="section split">
        <div>
          <p className="eyebrow">Why trust us</p>
          <h2>Institutional discipline, radical transparency.</h2>
        </div>
        <div className="trust-grid">
          {trust.map((t) => (
            <article className="trust-card" key={t.name}>
              <h3>{t.name}</h3>
              <p>{t.detail}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section split" id="mission">
        <div>
          <p className="eyebrow">Our mission</p>
          <h2>Institutional research for independent investors and acquirers.</h2>
        </div>
        <div className="mission">
          <p className="mission__statement">
            To put institutional-grade research and diligence in the hands of the investors and
            acquirers the big platforms overlook — so they can screen faster, buy smarter, and
            build durable wealth.
          </p>
          <p className="mission__story">
            <Link className="m-link" href="/team">
              Read our story &rarr;
            </Link>
          </p>
        </div>
      </section>

      <section className="section waitlist-section" id="waitlist">
        <div className="waitlist-section__inner">
          <p className="eyebrow">Get started</p>
          <h2>Start free — no sales call, no lock-in.</h2>
          <p className="waitlist-section__lead">
            Tell us who you are and we&rsquo;ll get you into the platform. Cancel anytime.
          </p>
          <WaitlistForm source="landing" />
        </div>
      </section>
    </main>
  );
}
