"use client";
// JHI-SIG: 69M2705M | Pricing plans (monthly/annual toggle + purchase entry) | JHI Research & Analytics Firm, Inc. (proprietary)
// Storefront pricing with a Monthly/Annual toggle and tier selection. "Continue"
// hands off to the Purchase Flow (Phase A) checkout with the chosen plan + interval.
import { useState } from "react";
import { useRouter } from "next/navigation";
import { pricingTiers, type BillingInterval } from "@/lib/platform-data";

const money = (n: number) => `$${n.toLocaleString("en-US")}`;

export function PricingPlans() {
  const router = useRouter();
  const [interval, setInterval] = useState<BillingInterval>("annual");
  const [selected, setSelected] = useState(pricingTiers[0].plan);

  function continueToCheckout() {
    router.push(`/checkout?plan=${selected}&interval=${interval}`);
  }

  return (
    <div className="pricing">
      <div className="pricing-toggle" role="tablist" aria-label="Billing interval">
        <button
          type="button"
          role="tab"
          aria-selected={interval === "monthly"}
          className={`pricing-toggle__btn ${interval === "monthly" ? "is-active" : ""}`}
          onClick={() => setInterval("monthly")}
        >
          Monthly
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={interval === "annual"}
          className={`pricing-toggle__btn ${interval === "annual" ? "is-active" : ""}`}
          onClick={() => setInterval("annual")}
        >
          Annual <span className="pricing-toggle__save">save ~10%</span>
        </button>
      </div>

      <section className="pricing-grid">
        {pricingTiers.map((tier) => {
          const active = selected === tier.plan;
          const perMonth = interval === "annual" ? tier.annualPerMonth : tier.monthly;
          return (
            <label
              className={`pricing-card pricing-card--select ${active ? "is-selected" : ""}`}
              key={tier.plan}
            >
              <input
                type="radio"
                name="plan"
                value={tier.plan}
                checked={active}
                onChange={() => setSelected(tier.plan)}
                className="pricing-card__radio"
              />
              <div>
                <p className="pricing-card__audience">{tier.audience}</p>
                <h3>{tier.name}</h3>
                <strong className="pricing-card__price">
                  {money(perMonth)}
                  <span className="pricing-card__per"> / month</span>
                </strong>
                <p className="pricing-card__billed">
                  {interval === "annual"
                    ? `Billed annually — ${money(tier.annualTotal)}/yr`
                    : "Billed monthly · cancel anytime"}
                </p>
                <p className="pricing-card__seats">{tier.seats}</p>
              </div>
              <ul>
                {tier.features.map((feature) => (
                  <li key={feature}>{feature}</li>
                ))}
              </ul>
            </label>
          );
        })}
      </section>

      <div className="pricing-cta">
        <p className="pricing-cta__note">
          Every plan starts with a <strong>7-day free trial</strong>. Card required; cancel
          anytime before the trial ends and you won&apos;t be charged.
        </p>
        <button type="button" className="button button--primary" onClick={continueToCheckout}>
          Continue → Start free trial
        </button>
      </div>
    </div>
  );
}
