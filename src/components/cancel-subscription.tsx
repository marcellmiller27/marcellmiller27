"use client";
// JHI-SIG: 69M2705M | Subscription cancellation flow | JHI Research & Analytics Firm, Inc. (proprietary)
import { useMemo, useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";

type Step = "intent" | "reason" | "done";

type CancelResponse = {
  effective_date: string;
  reason: string;
  subscription: { status: string; plan: string };
};

// A "complete sentence" gate: the reason must be substantive (>= 4 words, >= 15
// characters) and close with sentence-ending punctuation. This is the rule that
// turns the field from red (invalid) to green (valid).
function isFullSentence(value: string): boolean {
  const cleaned = value.trim();
  const words = cleaned.split(/\s+/).filter(Boolean);
  return cleaned.length >= 15 && words.length >= 4 && /[.!?]$/.test(cleaned);
}

function formatDate(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
}

export function CancelSubscription() {
  const [step, setStep] = useState<Step>("intent");
  const [reason, setReason] = useState("");
  const [touched, setTouched] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<CancelResponse | null>(null);

  const valid = useMemo(() => isFullSentence(reason), [reason]);
  const showInvalid = touched && !valid;

  async function completeCancellation() {
    if (!valid || submitting) return;
    setSubmitting(true);
    setError(null);
    try {
      const res = await apiFetch("/billing/cancel", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reason: reason.trim() })
      });
      if (res.status === 401) {
        setError("Your session has expired. Please sign in again to cancel your subscription.");
        return;
      }
      if (!res.ok) {
        const data = (await res.json().catch(() => null)) as { detail?: string } | null;
        setError(
          typeof data?.detail === "string"
            ? data.detail
            : "We couldn't process the cancellation. Please try again."
        );
        return;
      }
      const data = (await res.json()) as CancelResponse;
      setResult(data);
      setStep("done");
    } catch {
      setError("A network error occurred. Please check your connection and try again.");
    } finally {
      setSubmitting(false);
    }
  }

  if (step === "done" && result) {
    return (
      <section className="cancel-flow" aria-live="polite">
        <div className="cancel-card cancel-card--confirmed">
          <p className="eyebrow">Account canceled successfully</p>
          <h2>Your membership has been canceled.</h2>
          <p className="cancel-confirm__lead">
            Your access will remain active until it automatically deactivates on{" "}
            <strong>{formatDate(result.effective_date)}</strong>. You will not be billed again.
          </p>
          <div className="cancel-confirm__reason">
            <span>Reason recorded</span>
            <p>{result.reason}</p>
          </div>
          <div className="cancel-actions">
            <Link className="button button--primary" href="/account">
              Back to account
            </Link>
          </div>
        </div>
      </section>
    );
  }

  if (step === "intent") {
    return (
      <section className="cancel-flow">
        <div className="cancel-card">
          <p className="cancel-step">Step 1 of 2</p>
          <h2>Cancel your JHI subscription</h2>
          <p className="cancel-lead">
            Before you cancel, note what happens next. Your subscription remains active through the
            end of your current billing period, then automatically deactivates — no auto-renewal
            traps and no surprise fees. You can resubscribe at any time.
          </p>
          <ul className="cancel-list">
            <li>Access to research, records, and diligence tools continues until your period ends.</li>
            <li>Saved data on your organization is retained per our data-retention policy.</li>
            <li>We&apos;ll ask for one full sentence of feedback so we can improve.</li>
          </ul>
          <div className="cancel-actions">
            <button className="button button--danger" type="button" onClick={() => setStep("reason")}>
              Continue to cancel
            </button>
            <Link className="button button--ghost" href="/account">
              Never mind — keep my subscription
            </Link>
          </div>
        </div>
      </section>
    );
  }

  // step === "reason"
  return (
    <section className="cancel-flow">
      <div className="cancel-card">
        <p className="cancel-step">Step 2 of 2</p>
        <h2>Tell us why you&apos;re leaving</h2>
        <p className="cancel-lead">
          We&apos;re sorry to see you go. In a full sentence, what problem were you hoping to solve
          but couldn&apos;t? Your reason is required and recorded with your cancellation.
        </p>

        <label className="cancel-field" htmlFor="cancel-reason">
          <span className="cancel-field__label">Cancellation reason</span>
          <textarea
            id="cancel-reason"
            className={`cancel-reason${touched ? (valid ? " cancel-reason--valid" : " cancel-reason--invalid") : ""}`}
            rows={5}
            value={reason}
            placeholder="For example: The platform was excellent, but our team paused all new subscriptions this quarter."
            onChange={(e) => setReason(e.target.value)}
            onBlur={() => setTouched(true)}
            aria-invalid={showInvalid}
            aria-describedby="cancel-reason-help"
          />
          <span
            id="cancel-reason-help"
            className={`cancel-help${touched ? (valid ? " cancel-help--valid" : " cancel-help--invalid") : ""}`}
          >
            {valid
              ? "Thank you — your reason reads as a complete sentence."
              : "Your reason must be a complete sentence (at least four words, ending with a period)."}
          </span>
        </label>

        {error ? <p className="cancel-error">{error}</p> : null}

        <div className="cancel-actions">
          <button
            className="button button--danger"
            type="button"
            onClick={completeCancellation}
            disabled={!valid || submitting}
          >
            {submitting ? "Canceling…" : "Complete cancellation"}
          </button>
          <Link className="button button--ghost" href="/account">
            Never mind — we&apos;re staying!
          </Link>
        </div>
      </div>
    </section>
  );
}
