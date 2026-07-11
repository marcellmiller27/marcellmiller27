import { PlatformShell } from "@/components/platform-shell";

const registrationFields = [
  "Organization name",
  "Full name",
  "Business email",
  "Password",
  "Subscription plan"
];

export default function RegisterPage() {
  return (
    <PlatformShell
      eyebrow="Authentication foundation"
      title="Create a John Henry Investments workspace"
      description="The backend now supports organization registration, secure password hashing, bearer tokens, trial subscriptions, and audit logging for account creation."
    >
      <section className="app-section app-section--split">
        <div>
          <p className="eyebrow">Registration API</p>
          <h2>POST /api/v1/auth/register</h2>
          <p>
            Creates an organization, admin user, membership record, trial subscription, signed access
            token, and audit log entry.
          </p>
        </div>
        <div className="app-grid app-grid--two">
          {registrationFields.map((field) => (
            <article className="app-card" key={field}>
              <span>Required field</span>
              <strong>{field}</strong>
            </article>
          ))}
        </div>
      </section>
    </PlatformShell>
  );
}
