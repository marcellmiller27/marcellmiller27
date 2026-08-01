"use client";
// JHI-SIG: 69M2705M | Purchase Flow — Phase A checkout (mock) | JHI Research & Analytics Firm, Inc. (proprietary)
// Phase A: plan/interval summary + transparent 7-day trial disclosure + a mock card
// form (test mode, no charge) that starts a trial via POST /billing/start-trial.
// Phase B replaces the mock form with Stripe Checkout + Subscriptions + webhooks.
import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { apiFetch } from "@/lib/api";
import { getCookie, TOKEN_COOKIE } from "@/lib/auth";
import { pricingTiers, type BillingInterval, type SubscriptionPlan } from "@/lib/platform-data";

const money = (n: number) => `$${n.toLocaleString("en-US")}`;
const PLANS: SubscriptionPlan[] = ["consumer", "professional", "enterprise"];

export function CheckoutFlow() {
  const router = useRouter();
  const params = useSearchParams();
  const planParam = (params.get("plan") ?? "consumer") as SubscriptionPlan;
  const plan: SubscriptionPlan = PLANS.includes(planParam) ? planParam : "consumer";
  const interval: BillingInterval = params.get("interval") === "monthly" ? "monthly" : "annual";
  const tier = pricingTiers.find((t) => t.plan === plan) ?? pricingTiers[0];

  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  const perMonth = interval === "annual" ? tier.annualPerMonth : tier.monthly;
  const dueToday = 0;

  async function startTrial(e: React.FormEvent) {
    e.preventDefault();
    setErr("");
    // Phase A funnel: an account exists only for paid/trial — require sign-in first.
    const token = getCookie(TOKEN_COOKIE);
    if (!token) {
      const next = encodeURIComponent(`/checkout?plan=${plan}&interval=${interval}`);
      router.push(`/login?next=${next}`);
      return;
    }
    setBusy(true);
    try {
      const r = await apiFetch("/billing/start-trial", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ plan, interval })
      });
      if (!r.ok) {
        const d = await r.json().catch(() => ({}));
        throw new Error(typeof d.detail === "string" ? d.detail : `Request failed (${r.status})`);
      }
      router.push(`/checkout/success?plan=${plan}&interval=${interval}`);
      router.refresh();
    } catch (e) {
      setErr(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="checkout">
      <section className="checkout__summary">
        <p className="checkout__eyebrow">Order summary</p>
        <h3>{tier.name}</h3>
        <p className="checkout__audience">{tier.audience}</p>
        <div className="checkout__price">
          <strong>{money(perMonth)}</strong>
          <span> / month</span>
        </div>
        <p className="checkout__billed">
          {interval === "annual"
            ? `Billed annually after trial — ${money(tier.annualTotal)}/yr (save ~10%)`
            : "Billed monthly after trial · cancel anytime"}
        </p>
        <p className="checkout__seats">{tier.seats}</p>
        <ul className="checkout__features">
          {tier.features.map((f) => (
            <li key={f}>{f}</li>
          ))}
        </ul>
        <p className="checkout__switch">
          <Link href="/pricing">← Change plan</Link>
        </p>
      </section>

      <section className="checkout__pay">
        <div className="checkout__trial">
          <h3>Start your 7-day free trial</h3>
          <ul>
            <li>
              <strong>Due today: {money(dueToday)}.</strong> Your card is saved but not charged
              during the trial.
            </li>
            <li>
              We&apos;ll email a reminder <strong>before</strong> your trial ends. It then
              auto-converts to {money(perMonth)}/month
              {interval === "annual" ? ` (billed ${money(tier.annualTotal)}/yr)` : ""}.
            </li>
            <li>
              <strong>One-click cancel</strong> anytime from your account — cancel before the
              trial ends and you won&apos;t be charged.
            </li>
          </ul>
        </div>

        <form className="checkout__form" onSubmit={startTrial}>
          <p className="checkout__testmode">Test mode — Phase A. No real charge is made.</p>
          <label>
            <span>Name on card</span>
            <input autoComplete="cc-name" placeholder="Jane Investor" defaultValue="" />
          </label>
          <label>
            <span>Card number</span>
            <input inputMode="numeric" placeholder="4242 4242 4242 4242" defaultValue="" />
          </label>
          <div className="checkout__row">
            <label>
              <span>Expiry</span>
              <input placeholder="MM / YY" defaultValue="" />
            </label>
            <label>
              <span>CVC</span>
              <input inputMode="numeric" placeholder="123" defaultValue="" />
            </label>
          </div>
          {err && <p className="auth-form__err">{err}</p>}
          <button type="submit" className="button button--primary" disabled={busy}>
            {busy ? "Starting trial…" : "Start 7-day free trial"}
          </button>
          <p className="checkout__fineprint">
            By starting your trial you agree to Aegira&apos;s terms. Live card processing (Stripe)
            activates in Phase B.
          </p>
        </form>
      </section>
    </div>
  );
}
