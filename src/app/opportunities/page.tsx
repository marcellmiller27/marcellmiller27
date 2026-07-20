import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { opportunities, scoreCategories } from "@/lib/platform-data";

export default function OpportunitiesPage() {
  return (
    <AppShell
      eyebrow="Research"
      title="Discover and score investable opportunities"
      description="Screen public securities, private companies, real estate, and digital assets with the John Henry Opportunity Score."
    >
      <p className="rec-crumb">
        <Link href="/companies">Browse the entity directory →</Link>
      </p>
      <section className="app-grid app-grid--two">
        {opportunities.map((opportunity) => (
          <article className="opportunity-card" key={opportunity.name}>
            <div className="opportunity-card__header">
              <div>
                <span>{opportunity.category}</span>
                <h2>{opportunity.name}</h2>
              </div>
              <div className="score-badge">
                <strong>{opportunity.score}</strong>
                <span>{opportunity.recommendation}</span>
              </div>
            </div>
            <p>{opportunity.thesis}</p>
            <ul>
              {opportunity.metrics.map((metric) => (
                <li key={metric}>{metric}</li>
              ))}
            </ul>
            {opportunity.recordSlug && (
              <Link className="opportunity-card__link" href={`/companies/${opportunity.recordSlug}`}>
                Open company record →
              </Link>
            )}
          </article>
        ))}
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Scoring model</p>
          <h2>Proprietary factors by asset class</h2>
        </div>
        <div className="app-grid app-grid--three">
          {scoreCategories.map((category) => (
            <article className="app-card" key={category.assetClass}>
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
    </AppShell>
  );
}
