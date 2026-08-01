"use client";
// JHI-SIG: 69M2705M | Purchase Flow — Phase A success | JHI Research & Analytics Firm, Inc. (proprietary)
// Confirms the trial started and shows the trial end date pulled from the live
// subscription record, with clear next steps (explore) and cancel (manage plan).
import { useEffect, useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";
import { pricingTiers, type SubscriptionPlan } from "@/lib/platform-data";
import { useSearchParams } from "next/navigation";

const money = (n: number) => `$${n.toLocaleString("en-US")}`;

export function CheckoutSuccess() {
  const params = useSearchParams();
  const plan = (params.get("plan") ?? "consumer") as SubscriptionPlan;
  const interval = params.get("interval") === "monthly" ? "monthly" : "annual";
  const tier = pricingTiers.find((t) => t.plan === plan) ?? pricingTiers[0];
  const perMonth = interval === "annual" ? tier.annualPerMonth : tier.monthly;

  const [trialEnd, setTrialEnd] = useState<string | null>(null);
  const [status, setStatus] = useState<string>("");

  useEffect(() => {
    let active = true;
    apiFetch("/billing/subscription")
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`))))
      .then((d) => {
        if (!active) return;
        setStatus(d.subscription?.status ?? "");
        setTrialEnd(d.subscription?.current_period_end ?? null);
      })
      .catch(() => active && setStatus(""));
    return () => {
      active = false;
    };
  }, []);

  const endLabel = trialEnd
    ? new Date(trialEnd).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })
    : null;

  return (
    <div className="checkout-success">
      <div className="checkout-success__badge" aria-hidden>
        ✓
      </div>
      <h3>Your free trial is active</h3>
      <p className="checkout-success__lede">
        Welcome to the <strong>{tier.name}</strong>. You have full access for the next 7 days.
      </p>
      <dl className="checkout-success__facts">
        <div>
          <dt>Plan</dt>
          <dd>{tier.name}</dd>
        </div>
        <div>
          <dt>After trial</dt>
          <dd>
            {money(perMonth)}/month{interval === "annual" ? ` (billed ${money(tier.annualTotal)}/yr)` : ""}
          </dd>
        </div>
        <div>
          <dt>Trial ends</dt>
          <dd>{endLabel ?? "in 7 days"}</dd>
        </div>
        <div>
          <dt>Status</dt>
          <dd>{status || "trialing"}</dd>
        </div>
      </dl>
      <p className="checkout-success__note">
        We&apos;ll remind you before your trial ends. Cancel anytime — one click, no charge if you
        cancel before {endLabel ?? "the trial ends"}.
      </p>
      <div className="checkout-success__actions">
        <Link className="button button--primary" href="/home">
          Explore the platform →
        </Link>
        <Link className="button button--ghost" href="/account">
          Manage or cancel plan
        </Link>
      </div>
    </div>
  );
}
