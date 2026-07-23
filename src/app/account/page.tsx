import Link from "next/link";
import { AppShell } from "@/components/app-shell";
import { LogoutButton } from "@/components/logout-button";

const accountFoundation = [
  {
    label: "Organization",
    value: "Persistent workspace",
    note: "Each account belongs to an organization for team, subscription, and audit isolation."
  },
  {
    label: "Role",
    value: "Admin foundation",
    note: "The first registered user becomes admin; future roles include investor, advisor, CPA, attorney, banker, and family office."
  },
  {
    label: "Subscription",
    value: "Plan entitlement",
    note: "Consumer, Professional, and Enterprise plans can control access to platform features."
  },
  {
    label: "Audit",
    value: "Event trail",
    note: "Registration, login, checkout, and webhook events are recorded in persistent audit logs."
  }
];

export default function AccountPage() {
  return (
    <AppShell
      eyebrow="Account"
      title="Your account & organization"
      description="The backend now provides the account structure needed for protected dashboards, plan-based entitlements, billing status, and operational audit review."
    >
      <section className="app-grid app-grid--four">
        {accountFoundation.map((item) => (
          <article className="app-card" key={item.label}>
            <span>{item.label}</span>
            <strong>{item.value}</strong>
            <p>{item.note}</p>
          </article>
        ))}
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Session</p>
        </div>
        <LogoutButton />
      </section>

      <section className="app-section app-section--split">
        <div>
          <p className="eyebrow">Subscription</p>
          <h2>Manage or cancel your plan</h2>
          <p>
            Change is always in your control. You can cancel your subscription in two steps — access
            continues through the end of your billing period, then deactivates automatically with no
            auto-renewal traps.
          </p>
          <div className="cancel-actions">
            <Link className="button button--ghost button--danger-ghost" href="/account/cancel">
              Cancel subscription
            </Link>
          </div>
        </div>
        <div className="table-card">
          <article className="table-row">
            <div>
              <span>Retention policy</span>
              <strong>Access until period end</strong>
            </div>
            <p>No mid-period clawback; you keep access through the paid period.</p>
            <div className="risk risk--low">Fair</div>
          </article>
          <article className="table-row">
            <div>
              <span>Reason on record</span>
              <strong>Full-sentence explanation</strong>
            </div>
            <p>Cancellations require a complete-sentence reason, recorded in the audit trail.</p>
            <div className="risk risk--low">Logged</div>
          </article>
        </div>
      </section>

      <section className="app-section app-section--split">
        <div>
          <p className="eyebrow">Protected APIs</p>
          <h2>Bearer-token access is available for platform routes</h2>
          <p>
            Front-end integration can now store the access token in a secure session strategy and
            pass it to protected backend endpoints.
          </p>
        </div>
        <div className="table-card">
          {["/api/v1/auth/me", "/api/v1/billing/subscription", "/api/v1/billing/audit-logs"].map(
            (route) => (
              <article className="table-row" key={route}>
                <div>
                  <span>Protected route</span>
                  <strong>{route}</strong>
                </div>
                <p>Requires Authorization: Bearer token.</p>
                <div className="risk risk--low">Ready</div>
              </article>
            )
          )}
        </div>
      </section>
    </AppShell>
  );
}
