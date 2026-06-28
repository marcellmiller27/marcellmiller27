// JHI-SIG: 69M2705M | Identity, Auth & Security | John Henry Investments (proprietary)
import Link from "next/link";
import { PlatformShell } from "@/components/platform-shell";

export default function LoginPage() {
  return (
    <PlatformShell
      eyebrow="Secure access"
      title="Sign in to protected platform workflows"
      description="Login validates hashed credentials and returns a signed bearer token containing user, organization, role, and subscription context."
    >
      <section className="app-section--split">
        <article className="app-card">
          <span>Dual access</span>
          <strong>Mobile companion app</strong>
          <p>
            The same account signs in on mobile with password, two-factor, and
            biometric unlock.
          </p>
          <Link className="button button--primary" href="/mobile" style={{ marginTop: "1rem" }}>
            Open the mobile app
          </Link>
        </article>
        <article className="app-card">
          <span>Sign-in methods</span>
          <strong>Password · 2FA · Biometric</strong>
          <p>
            Multi-factor sign-in is backed by `/api/v1/auth/login/initiate`,
            `/auth/2fa/*`, and `/auth/biometric/*`.
          </p>
        </article>
      </section>

      <section className="app-grid app-grid--three">
        <article className="app-card">
          <span>Endpoint</span>
          <strong>/api/v1/auth/login</strong>
          <p>Accepts email and password, then returns a bearer token for protected API calls.</p>
        </article>
        <article className="app-card">
          <span>Protected identity</span>
          <strong>/api/v1/auth/me</strong>
          <p>Returns the current user, organization, role, and subscription for an authenticated session.</p>
        </article>
        <article className="app-card">
          <span>Security</span>
          <strong>PBKDF2 + HMAC token</strong>
          <p>Passwords are salted and hashed. Tokens are signed and expire based on backend settings.</p>
        </article>
      </section>
    </PlatformShell>
  );
}
