import {
  dashboardWidgets,
  platformModules,
  pricingTiers,
  scoreCategories,
  techStack,
  userTypes
} from "@/lib/platform-data";

const keyMetrics = [
  { label: "Primary mission", value: "AI-powered opportunity discovery" },
  { label: "Target ARR scenario", value: "$90M" },
  { label: "Opportunity score", value: "0-100" },
  { label: "Platform model", value: "B2C + B2B SaaS" }
];

const reportExamples = [
  "John Henry Weekly Macro Report",
  "Crypto Intelligence Report",
  "Business Acquisition Report",
  "Dividend Opportunities Report"
];

export default function Home() {
  return (
    <main>
      <section className="hero section">
        <div className="hero__content">
          <p className="eyebrow">John Henry Investments, LLC</p>
          <h1>Investment intelligence for markets, acquisitions, and generational wealth.</h1>
          <p className="hero__lead">
            A subscription platform for investors, business owners, family offices, and acquisition
            entrepreneurs to discover opportunities, analyze risk, value assets, and manage portfolios.
          </p>
          <div className="hero__actions">
            <a className="button button--primary" href="#plans">
              View subscription plans
            </a>
            <a className="button button--secondary" href="#modules">
              Explore platform modules
            </a>
          </div>
        </div>
        <div className="hero__panel" aria-label="Platform summary">
          <div className="score-card">
            <span>John Henry Opportunity Score</span>
            <strong>87</strong>
            <p>Buy signal based on valuation, growth, liquidity, and macro conditions.</p>
          </div>
          <div className="mini-grid">
            {dashboardWidgets.map((widget) => (
              <span key={widget}>{widget}</span>
            ))}
          </div>
        </div>
      </section>

      <section className="metrics section" aria-label="Platform metrics">
        {keyMetrics.map((metric) => (
          <article className="metric-card" key={metric.label}>
            <span>{metric.label}</span>
            <strong>{metric.value}</strong>
          </article>
        ))}
      </section>

      <section className="section split">
        <div>
          <p className="eyebrow">Primary users</p>
          <h2>Built for individual investors and professional capital allocators.</h2>
        </div>
        <div className="tag-grid">
          {userTypes.map((type) => (
            <span className="tag" key={type}>
              {type}
            </span>
          ))}
        </div>
      </section>

      <section className="section" id="plans">
        <div className="section-heading">
          <p className="eyebrow">Revenue model</p>
          <h2>Subscription plans across consumer, professional, and enterprise markets.</h2>
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
              <footer>
                <span>{tier.target}</span>
                <span>{tier.revenue}</span>
              </footer>
            </article>
          ))}
        </div>
      </section>

      <section className="section" id="modules">
        <div className="section-heading">
          <p className="eyebrow">Application blueprint</p>
          <h2>Thirteen modules from user management to proprietary scoring.</h2>
        </div>
        <div className="module-grid">
          {platformModules.map((module) => (
            <article className="module-card" key={module.name}>
              <p className="module-card__phase">{module.phase}</p>
              <h3>{module.name}</h3>
              <p>{module.summary}</p>
              <ul>
                {module.features.map((feature) => (
                  <li key={feature}>{feature}</li>
                ))}
              </ul>
              {module.output ? <div className="module-card__output">{module.output}</div> : null}
            </article>
          ))}
        </div>
      </section>

      <section className="section intelligence">
        <div className="section-heading">
          <p className="eyebrow">John Henry Intelligence Center</p>
          <h2>Macro signals, weekly reports, and private AI research assistance.</h2>
        </div>
        <div className="intelligence__grid">
          <article>
            <h3>Global macro dashboard</h3>
            <p>
              Tracks central banks, treasury markets, oil, gold, Bitcoin, money supply, CPI, PPI,
              GDP, and unemployment to forecast recession probability and liquidity trends.
            </p>
          </article>
          <article>
            <h3>Automated reports</h3>
            <div className="report-list">
              {reportExamples.map((report) => (
                <span key={report}>{report}</span>
              ))}
            </div>
          </article>
          <article>
            <h3>Research assistant</h3>
            <p>
              Answers questions like Analyze Tesla, Evaluate this business, Compare SBA loans,
              Build a dividend portfolio, and Analyze the Bitcoin cycle.
            </p>
          </article>
        </div>
      </section>

      <section className="section score-section">
        <div>
          <p className="eyebrow">Proprietary IP</p>
          <h2>John Henry Opportunity Score</h2>
          <p>
            The scoring system creates a repeatable decision-support layer across public securities,
            private businesses, and digital assets.
          </p>
        </div>
        <div className="score-grid">
          {scoreCategories.map((category) => (
            <article key={category.assetClass}>
              <h3>{category.assetClass}</h3>
              <ul>
                {category.factors.map((factor) => (
                  <li key={factor}>{factor}</li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      </section>

      <section className="section">
        <div className="section-heading">
          <p className="eyebrow">Technology stack</p>
          <h2>Architecture selected for ownership, portability, and future enterprise value.</h2>
        </div>
        <div className="stack-grid">
          {techStack.map((layer) => (
            <article key={layer.layer}>
              <h3>{layer.layer}</h3>
              <p>{layer.tools.join(" / ")}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section vision">
        <p className="eyebrow">Five-year vision</p>
        <h2>From investment company to financial technology company.</h2>
        <p>
          The long-term platform can expand into an investment research platform, business
          acquisition marketplace, AI due diligence platform, family office operating system, and
          wealth intelligence network.
        </p>
        <div className="vision__valuation">
          <strong>$720M - $1.3B+</strong>
          <span>Potential enterprise value range at 8x-15x ARR if the platform reaches $90M ARR.</span>
        </div>
      </section>
    </main>
  );
}
