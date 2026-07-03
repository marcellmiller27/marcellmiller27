import { LiveAccount } from "@/components/live-account";
import { PlatformShell } from "@/components/platform-shell";

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
    <PlatformShell
      eyebrow="Account foundation"
      title="User, organization, subscription, and audit context"
      description="The backend now provides the account structure needed for protected dashboards, plan-based entitlements, billing status, and operational audit review."
    >
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Live account</p>
          <h2>Your user, organization, role &amp; subscription</h2>
        </div>
        <LiveAccount />
      </section>

      <section className="app-grid app-grid--four">
        {accountFoundation.map((item) => (
          <article className="app-card" key={item.label}>
            <span>{item.label}</span>
            <strong>{item.value}</strong>
            <p>{item.note}</p>
          </article>
        ))}
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
    </PlatformShell>
  );
}
