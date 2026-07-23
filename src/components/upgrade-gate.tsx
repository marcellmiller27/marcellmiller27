// JHI-SIG: 69M2705M | Upgrade gate (free → paid CTA) | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";

// Shown to free / public readers in place of the full edition body — the conversion CTA.
export function UpgradeGate() {
  return (
    <div className="upgrade-gate">
      <p className="eyebrow">Subscriber edition</p>
      <h3>Unlock the full edition</h3>
      <p>
        You&apos;re reading the free preview. The full edition — every section, all Red Alerts,
        and the complete Cross-Asset Opportunity Scan — is included with a JHI subscription
        (Tier 1–3), alongside the full platform: records, screening, and diligence tools.
      </p>
      <div className="upgrade-gate__actions">
        <Link className="button button--primary" href="/pricing">
          See plans &amp; upgrade
        </Link>
        <Link className="button button--secondary" href="/register">
          Create an account
        </Link>
      </div>
    </div>
  );
}
