# Newsletter Distribution — Step B (Email)

> JHI-SIG: 69M2705M · JHI Research & Analytics Firm, Inc. (proprietary)
> Plan of record for emailing the editorial editions. Companion: `EDITORIAL_CHARTER.md`.

## Where Step A left off
On-platform generation is **live** — the VP of Editorial (AI) auto-generates **The
Economic Brief**, **Red Alerts**, and the **Cross-Asset Opportunity Scan** from the
public data we poll, rendered at `/newsletters` and exportable to PDF.

## Step B — what ships next
| Piece | Status | Notes |
| --- | --- | --- |
| **Subscriber capture** | ✅ Built | Opt-in on the Newsletters desk → `POST /api/v1/leads` (source `newsletter-subscribe`). Durable in Postgres via the existing leads store. |
| **Email-ready render** | ⏳ To build | Server-side render of each edition to inline-styled, email-safe HTML (email clients ignore external CSS). Reuse the deterministic builders. |
| **Send service (SES)** | ⛔ Blocked on credentials | AWS SES (or equivalent) client + verified sender domain. **Founder action:** add `AWS_SES_*` (or provider) keys to Secrets. Without them the pipeline cannot send. |
| **Scheduling** | ⏳ To build | Cadence per edition (e.g., weekly Brief; Red Alerts on trigger). Cron/worker or scheduled task. |
| **Compliance** | ⏳ To build | One-click **unsubscribe**, physical address, and CAN-SPAM/GDPR footer on every send; suppression list. |

## Gating / founder action
Live sending is **blocked until email-provider credentials are added to Secrets**
(e.g., `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` + a verified SES sender, or a
provider key). Once present, Cy wires the send service + scheduler behind an
`ENABLE_NEWSLETTER_EMAIL` flag and we test on a seed list before general send.

## Governance
- Editions remain **public-data sourced** today (no licensed-vendor footprint).
- When licensed data (Nasdaq/Sharadar) is folded in, emailed editions carry **derived-only**
  content per `docs/legal/nasdaq/FOUNDER_RESOLUTION_2026-07-20.md` (no spillage), and honor
  any mandatory-attribution + external-distribution/end-user-cap terms.
- Every send includes the standard research/education disclaimer + unsubscribe.
