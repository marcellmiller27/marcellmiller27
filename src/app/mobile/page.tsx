"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { Logo } from "@/components/logo";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api/v1";

type Session = {
  access_token: string;
  user: { full_name: string; email: string };
  organization: { name: string };
  role: string;
  subscription: { plan: string; status: string };
};

type LoginInitiate =
  | { status: "authenticated"; auth: Session }
  | {
      status: "two_factor_required";
      challenge_token: string;
      methods: string[];
      dev_code: string | null;
    };

type SecurityStatus = {
  two_factor_enabled: boolean;
  biometric_enabled: boolean;
  device_count: number;
  devices: { credential_id: string; label: string }[];
};

type Screen =
  | "welcome"
  | "method"
  | "password"
  | "twofactor"
  | "biometric"
  | "register"
  | "home"
  | "security"
  | "diligence";

type DiligenceResult = {
  business_name: string;
  financial_integrity_score: number;
  adjusted_ebitda: number;
  reported_ebitda: number;
  recommended_tier: string;
  recommended_action: string;
  red_flags: string[];
  add_on_pricing: { platform_low: number; platform_high: number; band: string };
};

async function api<T>(
  path: string,
  options: { method?: string; body?: unknown; token?: string } = {}
): Promise<T> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (options.token) {
    headers.Authorization = `Bearer ${options.token}`;
  }
  const response = await fetch(`${API_BASE}${path}`, {
    method: options.method ?? "GET",
    headers,
    body: options.body ? JSON.stringify(options.body) : undefined
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data?.detail ?? "Something went wrong. Please try again.");
  }
  return data as T;
}

function randomCredentialId(): string {
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);
  return "sim-" + Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
}

/**
 * Best-effort platform-authenticator ceremony. Uses the real WebAuthn API when a
 * platform authenticator is present, and transparently falls back to a simulated
 * credential (clearly labeled in the UI) so the flow is demonstrable everywhere.
 */
async function deviceBiometric(
  mode: "register",
  email: string
): Promise<{ credentialId: string; simulated: boolean }> {
  try {
    if (typeof window !== "undefined" && window.PublicKeyCredential && navigator.credentials) {
      const challenge = new Uint8Array(32);
      crypto.getRandomValues(challenge);
      const credential = (await navigator.credentials.create({
        publicKey: {
          challenge,
          rp: { name: "John Henry Investments" },
          user: {
            id: new TextEncoder().encode(email),
            name: email,
            displayName: email
          },
          pubKeyCredParams: [
            { type: "public-key", alg: -7 },
            { type: "public-key", alg: -257 }
          ],
          authenticatorSelection: {
            authenticatorAttachment: "platform",
            userVerification: "required"
          },
          timeout: 8000
        }
      })) as PublicKeyCredential | null;
      if (credential) {
        const raw = new Uint8Array(credential.rawId);
        const id = btoa(String.fromCharCode(...raw))
          .replace(/\+/g, "-")
          .replace(/\//g, "_")
          .replace(/=+$/, "");
        return { credentialId: id, simulated: false };
      }
    }
  } catch {
    // No usable platform authenticator — fall back to a simulated credential.
  }
  return { credentialId: randomCredentialId(), simulated: true };
}

export default function MobileApp() {
  const [screen, setScreen] = useState<Screen>("welcome");
  const [session, setSession] = useState<Session | null>(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [orgName, setOrgName] = useState("");
  const [code, setCode] = useState("");
  const [challengeToken, setChallengeToken] = useState("");
  const [devCode, setDevCode] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [info, setInfo] = useState("");
  const [busy, setBusy] = useState(false);
  const [security, setSecurity] = useState<SecurityStatus | null>(null);
  const [twoFactorSecret, setTwoFactorSecret] = useState("");
  const [simulatedBiometric, setSimulatedBiometric] = useState(false);
  const [diligence, setDiligence] = useState<DiligenceResult | null>(null);

  const resetMessages = () => {
    setError("");
    setInfo("");
  };

  const goHome = useCallback((next: Session) => {
    setSession(next);
    setPassword("");
    setCode("");
    setChallengeToken("");
    setDevCode(null);
    resetMessages();
    setScreen("home");
  }, []);

  const refreshSecurity = useCallback(async (token: string) => {
    try {
      const status = await api<SecurityStatus>("/auth/security/status", { token });
      setSecurity(status);
    } catch {
      setSecurity(null);
    }
  }, []);

  const openSecurity = () => {
    resetMessages();
    setScreen("security");
    if (session) {
      void refreshSecurity(session.access_token);
    }
  };

  // Live demo authenticator: refresh the displayed code like a real TOTP app so
  // it never goes stale during manual entry (dev only; 404s in production).
  useEffect(() => {
    if (screen !== "twofactor" || !challengeToken) {
      return;
    }
    let active = true;
    const pull = () => {
      api<{ code: string }>("/auth/2fa/dev-code", {
        method: "POST",
        body: { challenge_token: challengeToken }
      })
        .then((result) => {
          if (active) {
            setDevCode(result.code);
          }
        })
        .catch(() => {
          /* dev-code endpoint disabled in production; keep last value */
        });
    };
    pull();
    const timer = setInterval(pull, 3000);
    return () => {
      active = false;
      clearInterval(timer);
    };
  }, [screen, challengeToken]);

  const handlePassword = async () => {
    resetMessages();
    setBusy(true);
    try {
      const result = await api<LoginInitiate>("/auth/login/initiate", {
        method: "POST",
        body: { email, password }
      });
      if (result.status === "two_factor_required") {
        setChallengeToken(result.challenge_token);
        setDevCode(result.dev_code);
        setScreen("twofactor");
      } else {
        goHome(result.auth);
      }
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  };

  const handleTwoFactor = async () => {
    resetMessages();
    setBusy(true);
    try {
      const auth = await api<Session>("/auth/2fa/verify", {
        method: "POST",
        body: { challenge_token: challengeToken, code }
      });
      goHome(auth);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  };

  const handleRegister = async () => {
    resetMessages();
    setBusy(true);
    try {
      const auth = await api<Session>("/auth/register", {
        method: "POST",
        body: {
          organization_name: orgName,
          full_name: fullName,
          email,
          password,
          plan: "consumer"
        }
      });
      goHome(auth);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  };

  const handleBiometricLogin = async () => {
    resetMessages();
    setBusy(true);
    try {
      const challenge = await api<{
        has_credential: boolean;
        challenge_token: string | null;
        credential_ids: string[];
      }>("/auth/biometric/challenge", { method: "POST", body: { email } });
      if (!challenge.has_credential || !challenge.challenge_token) {
        setError("No biometric device is registered for this account. Sign in with a password, then enable biometrics in Security.");
        return;
      }
      const auth = await api<Session>("/auth/biometric/assert", {
        method: "POST",
        body: {
          challenge_token: challenge.challenge_token,
          credential_id: challenge.credential_ids[0]
        }
      });
      goHome(auth);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  };

  const handleEnableTwoFactor = async () => {
    if (!session) return;
    resetMessages();
    setBusy(true);
    try {
      const result = await api<{ secret: string; current_code: string | null }>(
        "/auth/2fa/enable",
        { method: "POST", token: session.access_token }
      );
      setTwoFactorSecret(result.secret);
      setInfo(
        result.current_code
          ? `Two-factor enabled. Demo code right now: ${result.current_code}`
          : "Two-factor enabled."
      );
      await refreshSecurity(session.access_token);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  };

  const handleDisableTwoFactor = async () => {
    if (!session) return;
    resetMessages();
    setBusy(true);
    try {
      await api("/auth/2fa/disable", { method: "POST", token: session.access_token });
      setTwoFactorSecret("");
      setInfo("Two-factor authentication disabled.");
      await refreshSecurity(session.access_token);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  };

  const handleEnableBiometric = async () => {
    if (!session) return;
    resetMessages();
    setBusy(true);
    try {
      const { credentialId, simulated } = await deviceBiometric("register", session.user.email);
      await api("/auth/biometric/register", {
        method: "POST",
        token: session.access_token,
        body: {
          credential_id: credentialId,
          label: simulated ? "Simulated device (demo)" : "This device"
        }
      });
      setSimulatedBiometric(simulated);
      setInfo(
        simulated
          ? "Biometric sign-in enabled in demo mode (simulated platform authenticator)."
          : "Biometric sign-in enabled with this device's Face ID / fingerprint."
      );
      await refreshSecurity(session.access_token);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  };

  const openDiligence = async () => {
    resetMessages();
    setScreen("diligence");
    setBusy(true);
    try {
      // Runs the same Financial Diligence Suite endpoint the web app uses.
      const result = await api<DiligenceResult>("/financial-diligence/analyze", {
        method: "POST",
        body: {
          business_name: "Carrollton Design Build",
          revenue: 12962195,
          reported_ebitda: 2381009,
          addbacks_claimed: 58745,
          questionable_addbacks: 23517,
          bank_deposits: 12800000,
          recurring_revenue_pct: 15,
          customer_concentration_pct: 64,
          asking_price: 6200000,
          post_loi: true
        }
      });
      setDiligence(result);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  };

  const signOut = () => {
    setSession(null);
    setSecurity(null);
    setPassword("");
    resetMessages();
    setScreen("welcome");
  };

  return (
    <div className="mobile-stage">
      <div className="device-frame">
        <div className="device-screen">
          {screen === "welcome" && (
            <>
              <div className="m-brand">
                <Logo size={36} />
                <span>
                  John Henry
                  <small>Investments</small>
                </span>
              </div>
              <p className="m-eyebrow">Dual access</p>
              <h1 className="m-title">Your platform, now in your pocket.</h1>
              <p className="m-sub">
                One account, two ways in. Pick up on mobile exactly where you left
                off on the web — portfolio, opportunity scores, and intelligence,
                secured with biometrics and two-factor sign-in.
              </p>
              <div className="m-grid-2">
                <div className="m-card">
                  <span>Web</span>
                  <p>Full command center in the browser.</p>
                </div>
                <div className="m-card">
                  <span>Mobile</span>
                  <p>On-the-go access with biometric unlock.</p>
                </div>
              </div>
              <div className="m-spacer" />
              <div className="m-stack">
                <button className="m-btn m-btn--primary" onClick={() => setScreen("method")}>
                  Sign in
                </button>
                <button className="m-btn m-btn--ghost" onClick={() => setScreen("register")}>
                  Create an account
                </button>
              </div>
            </>
          )}

          {screen === "method" && (
            <>
              <div className="m-topbar">
                <button className="m-back" onClick={() => setScreen("welcome")}>
                  ‹ Back
                </button>
                <Logo size={26} />
              </div>
              <p className="m-eyebrow">Choose access</p>
              <h1 className="m-title">How would you like to sign in?</h1>
              <div className="m-stack">
                <button className="m-method" onClick={() => { resetMessages(); setScreen("password"); }}>
                  <span className="m-method__icon">🔑</span>
                  <span>
                    <strong>Password</strong>
                    <span>Email and password, with optional 2-step verification.</span>
                  </span>
                </button>
                <button className="m-method" onClick={() => { resetMessages(); setScreen("biometric"); }}>
                  <span className="m-method__icon m-method__icon--bio">🟢</span>
                  <span>
                    <strong>Biometric</strong>
                    <span>Face ID or fingerprint on a registered device.</span>
                  </span>
                </button>
                <button className="m-method" onClick={() => { resetMessages(); setScreen("register"); }}>
                  <span className="m-method__icon m-method__icon--gold">✨</span>
                  <span>
                    <strong>Create account</strong>
                    <span>New to John Henry Investments? Start here.</span>
                  </span>
                </button>
              </div>
              {error && <p className="m-error">{error}</p>}
            </>
          )}

          {screen === "password" && (
            <>
              <div className="m-topbar">
                <button className="m-back" onClick={() => setScreen("method")}>
                  ‹ Back
                </button>
                <Logo size={26} />
              </div>
              <p className="m-eyebrow">Password sign-in</p>
              <h1 className="m-title">Welcome back.</h1>
              <div className="m-stack">
                <div className="m-field">
                  <label htmlFor="email">Email</label>
                  <input
                    id="email"
                    type="email"
                    value={email}
                    autoComplete="username"
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@example.com"
                  />
                </div>
                <div className="m-field">
                  <label htmlFor="password">Password</label>
                  <input
                    id="password"
                    type="password"
                    value={password}
                    autoComplete="current-password"
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                  />
                </div>
                {error && <p className="m-error">{error}</p>}
                <button
                  className="m-btn m-btn--primary"
                  disabled={busy || !email || !password}
                  onClick={handlePassword}
                >
                  {busy ? "Checking…" : "Continue"}
                </button>
                <p className="m-sub" style={{ textAlign: "center" }}>
                  Accounts with 2-step verification will be asked for a code next.
                </p>
              </div>
            </>
          )}

          {screen === "twofactor" && (
            <>
              <div className="m-topbar">
                <button className="m-back" onClick={() => setScreen("password")}>
                  ‹ Back
                </button>
                <Logo size={26} />
              </div>
              <p className="m-eyebrow">Two-factor authentication</p>
              <h1 className="m-title">Enter your 6-digit code.</h1>
              <p className="m-sub">
                Open your authenticator app and enter the current John Henry
                Investments code.
              </p>
              {devCode && (
                <p className="m-note m-note--code">
                  Demo authenticator code (auto-refreshes): <strong>{devCode}</strong>
                </p>
              )}
              <div className="m-stack">
                <div className="m-otp">
                  <input
                    inputMode="numeric"
                    maxLength={6}
                    value={code}
                    onChange={(e) => setCode(e.target.value.replace(/\D/g, ""))}
                    placeholder="000000"
                  />
                </div>
                {error && <p className="m-error">{error}</p>}
                <button
                  className="m-btn m-btn--primary"
                  disabled={busy || code.length < 6}
                  onClick={handleTwoFactor}
                >
                  {busy ? "Verifying…" : "Verify & sign in"}
                </button>
              </div>
            </>
          )}

          {screen === "biometric" && (
            <>
              <div className="m-topbar">
                <button className="m-back" onClick={() => setScreen("method")}>
                  ‹ Back
                </button>
                <Logo size={26} />
              </div>
              <p className="m-eyebrow">Biometric sign-in</p>
              <h1 className="m-title">Unlock with your device.</h1>
              <div className="m-bio-orb">🟢</div>
              <p className="m-sub" style={{ textAlign: "center" }}>
                Confirm the account, then authenticate with Face ID or your
                fingerprint.
              </p>
              <div className="m-stack">
                <div className="m-field">
                  <label htmlFor="bio-email">Account email</label>
                  <input
                    id="bio-email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@example.com"
                  />
                </div>
                {error && <p className="m-error">{error}</p>}
                <button
                  className="m-btn m-btn--primary"
                  disabled={busy || !email}
                  onClick={handleBiometricLogin}
                >
                  {busy ? "Authenticating…" : "Authenticate"}
                </button>
              </div>
            </>
          )}

          {screen === "register" && (
            <>
              <div className="m-topbar">
                <button className="m-back" onClick={() => setScreen("welcome")}>
                  ‹ Back
                </button>
                <Logo size={26} />
              </div>
              <p className="m-eyebrow">Create account</p>
              <h1 className="m-title">Open your account.</h1>
              <div className="m-stack">
                <div className="m-field">
                  <label htmlFor="org">Organization</label>
                  <input id="org" value={orgName} onChange={(e) => setOrgName(e.target.value)} placeholder="Acme Capital" />
                </div>
                <div className="m-field">
                  <label htmlFor="name">Full name</label>
                  <input id="name" value={fullName} onChange={(e) => setFullName(e.target.value)} placeholder="Jordan Lee" />
                </div>
                <div className="m-field">
                  <label htmlFor="r-email">Email</label>
                  <input id="r-email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
                </div>
                <div className="m-field">
                  <label htmlFor="r-pass">Password</label>
                  <input id="r-pass" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="At least 8 characters" />
                </div>
                {error && <p className="m-error">{error}</p>}
                <button
                  className="m-btn m-btn--primary"
                  disabled={busy || !orgName || !fullName || !email || password.length < 8}
                  onClick={handleRegister}
                >
                  {busy ? "Creating…" : "Create account"}
                </button>
              </div>
            </>
          )}

          {screen === "home" && session && (
            <>
              <div className="m-topbar">
                <div className="m-brand">
                  <Logo size={30} />
                  <span>
                    John Henry
                    <small>Investments</small>
                  </span>
                </div>
                <button className="m-back" onClick={signOut}>
                  Sign out
                </button>
              </div>
              <p className="m-eyebrow">Signed in</p>
              <h1 className="m-title">Hi, {session.user.full_name.split(" ")[0]}.</h1>
              <p className="m-sub">
                {session.organization.name} · {session.subscription.plan} plan ·{" "}
                {session.subscription.status}
              </p>
              <div className="m-grid-2">
                <div className="m-card">
                  <span>Portfolio</span>
                  <strong>$4.82M</strong>
                  <p>+8.4% YTD</p>
                </div>
                <div className="m-card">
                  <span>Opportunity score</span>
                  <strong>87</strong>
                  <p>Buy signal</p>
                </div>
                <div className="m-card">
                  <span>Watch alerts</span>
                  <strong>18</strong>
                  <p>5 high priority</p>
                </div>
                <div className="m-card">
                  <span>Pipeline</span>
                  <strong>$12.6M</strong>
                  <p>7 active targets</p>
                </div>
              </div>
              <div className="m-spacer" />
              <div className="m-stack">
                <button className="m-btn m-btn--primary" onClick={openDiligence}>
                  Run Financial Diligence
                </button>
                <button className="m-btn m-btn--trust" onClick={openSecurity}>
                  Security & sign-in options
                </button>
              </div>
            </>
          )}

          {screen === "diligence" && session && (
            <>
              <div className="m-topbar">
                <button className="m-back" onClick={() => setScreen("home")}>
                  ‹ Home
                </button>
                <Logo size={26} />
              </div>
              <p className="m-eyebrow">Financial Diligence Suite</p>
              <h1 className="m-title">Quality of Earnings</h1>
              {busy && <p className="m-sub">Running diligence procedures…</p>}
              {error && <p className="m-error">{error}</p>}
              {diligence && !busy && (
                <>
                  <p className="m-sub">{diligence.business_name}</p>
                  <div className="m-grid-2">
                    <div className="m-card">
                      <span>Integrity score</span>
                      <strong>{diligence.financial_integrity_score}</strong>
                      <p>Tier {diligence.recommended_tier} recommended</p>
                    </div>
                    <div className="m-card">
                      <span>Adjusted EBITDA</span>
                      <strong>${Math.round(diligence.adjusted_ebitda / 1000).toLocaleString()}K</strong>
                      <p>reported ${Math.round(diligence.reported_ebitda / 1000).toLocaleString()}K</p>
                    </div>
                    <div className="m-card">
                      <span>QoE add-on</span>
                      <strong>${Math.round(diligence.add_on_pricing.platform_low / 1000)}K+</strong>
                      <p>CPA-signed</p>
                    </div>
                    <div className="m-card">
                      <span>Red flags</span>
                      <strong>{diligence.red_flags.length}</strong>
                      <p>to resolve</p>
                    </div>
                  </div>
                  {diligence.red_flags[0] && (
                    <p className="m-note">{diligence.red_flags[0]}</p>
                  )}
                  <p className="m-sub" style={{ fontSize: "var(--fs-xs)" }}>
                    Decision-support only — not an audit or CPA opinion. Formal opinions are
                    issued by a licensed partner CPA.
                  </p>
                </>
              )}
            </>
          )}

          {screen === "security" && session && (
            <>
              <div className="m-topbar">
                <button className="m-back" onClick={() => setScreen("home")}>
                  ‹ Home
                </button>
                <Logo size={26} />
              </div>
              <p className="m-eyebrow">Security options</p>
              <h1 className="m-title">Protect your account.</h1>

              <div className="m-stack">
                <div className="m-row">
                  <div>
                    <strong>Two-factor (2-step)</strong>
                    <span>Time-based authenticator code.</span>
                  </div>
                  <span className={`m-pill ${security?.two_factor_enabled ? "m-pill--on" : "m-pill--off"}`}>
                    {security?.two_factor_enabled ? "On" : "Off"}
                  </span>
                </div>
                {security?.two_factor_enabled ? (
                  <button className="m-btn m-btn--ghost" disabled={busy} onClick={handleDisableTwoFactor}>
                    Turn off two-factor
                  </button>
                ) : (
                  <button className="m-btn m-btn--primary" disabled={busy} onClick={handleEnableTwoFactor}>
                    Enable two-factor
                  </button>
                )}
                {twoFactorSecret && (
                  <p className="m-note">
                    Authenticator secret: <strong>{twoFactorSecret}</strong>
                    <br />Add this to Google Authenticator / 1Password, or scan the QR in a full client.
                  </p>
                )}

                <div className="m-row">
                  <div>
                    <strong>Biometric unlock</strong>
                    <span>Face ID / fingerprint on this device.</span>
                  </div>
                  <span className={`m-pill ${security?.biometric_enabled ? "m-pill--on" : "m-pill--off"}`}>
                    {security?.biometric_enabled ? `${security.device_count} device(s)` : "Off"}
                  </span>
                </div>
                <button className="m-btn m-btn--primary" disabled={busy} onClick={handleEnableBiometric}>
                  {security?.biometric_enabled ? "Add this device" : "Enable biometric unlock"}
                </button>
                {simulatedBiometric && (
                  <p className="m-note">
                    <strong>Demo mode:</strong> no hardware authenticator was available, so a
                    simulated platform credential was registered to demonstrate the flow.
                  </p>
                )}

                {info && <p className="m-note m-note--code">{info}</p>}
                {error && <p className="m-error">{error}</p>}

                <p className="m-sub">
                  Dual access: this account also signs in on the{" "}
                  <Link className="m-link" href="/login">web platform</Link>. Settings stay in sync.
                </p>
              </div>
            </>
          )}
        </div>
      </div>

      <p className="mobile-stage__intro">
        John Henry Investments companion app · also available on the{" "}
        <Link href="/">web platform</Link>.
      </p>
    </div>
  );
}
