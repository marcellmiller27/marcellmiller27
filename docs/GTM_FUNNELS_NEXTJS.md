# Funnels on Our Next.js Site + Is It the Preferred Launch Platform?

Answers two things: (1) what marketing funnels a Next.js site can deliver, and (2)
whether our own Next.js app is the preferred platform to take John Henry Investments
to market. Companion to `docs/HIGHLEVEL_EVALUATION.md`.

## Key distinction

Next.js builds **any funnel page/flow** you can imagine with full ownership, SEO, and
speed. What it does **not** include out of the box is the *automation/CRM/email‑SMS*
services behind funnels — you integrate those (mostly free/cheap tools). GHL bundles
those services but trades away ownership and adds lock‑in.

## Funnels Next.js can deliver (all of them)

| Funnel | What it is | Next.js delivers | Integrate for automation |
| --- | --- | --- | --- |
| **Landing / squeeze** | Lead magnet → email capture | Pages/components, fast + SEO | Email tool (Resend/SES/Loops) |
| **Long‑form sales / VSL** | Sales page with video + CTA | Full control, A/B, analytics | Video host, analytics |
| **Waitlist** | Pre‑launch demand capture | Form + serverless route + DB | Email confirmations |
| **Free trial / freemium** | Signup → activate → paid | Already built (auth/2FA) | Lifecycle email |
| **Checkout / paywall** | Plan selection → pay | Stripe (billing foundation built) | Stripe + webhooks (built) |
| **Application / qualification** | Gated B2B/enterprise intake | Multi‑step forms | CRM routing |
| **Booking / demo** | Schedule a call | Embed Cal.com/Calendly | Calendar tool |
| **Webinar / event** | Register → attend → offer | Reg pages + reminders | Email/SMS, webinar host |
| **Onboarding** | First‑value activation | In‑app flows (we own the app) | Product analytics |
| **Upsell / cross‑sell / downsell** | Tier moves, add‑ons | Pricing + in‑app prompts | Stripe |
| **Referral** | Invite → reward | Referral codes + routes | Email |
| **Re‑engagement / win‑back** | Email/SMS nudges | Triggers from app events | Email/SMS + automation |
| **Content / SEO** | Blog/MDX → capture | Native MDX, great SEO | CMS optional |

Cross‑cutting (all native or simple integrations): A/B testing (PostHog/Vercel flags),
analytics (GA4/PostHog/Plausible), retargeting pixels (Meta/Google), consent/compliance.

## The lean GTM stack on Next.js (the part GHL bundles)

- **Email/lifecycle:** Resend or AWS SES (cheap) / Loops / Customer.io.
- **CRM:** HubSpot Free or Attio (free/low tiers).
- **SMS (optional):** Twilio.
- **Analytics + A/B:** PostHog (generous free tier) or GA4 + Plausible.
- **Scheduling:** Cal.com (open‑source) / Calendly.
- **Payments:** Stripe — already integrated.

This stack typically runs **$0–$150/mo at MVP scale** and stays inside the lean budget
(`docs/OPERATING_COST_LEAN_VS_STAFFED.md`).

## Next.js site vs GHL — for our launch

| Factor | Our Next.js site | GoHighLevel |
| --- | --- | --- |
| Hosts the actual product | ✅ (it *is* the product) | ❌ marketing only |
| Funnel pages | ✅ unlimited, full control | ✅ builder, less control |
| Built‑in CRM/email/SMS/automation | ➖ integrate (cheap tools) | ✅ bundled |
| SEO / performance / branding | ✅ best‑in‑class | ➖ adequate |
| Data ownership | ✅ all in your DB/repo | ➖ in GHL |
| Lock‑in | ✅ none | ❌ funnels/contacts in GHL |
| Speed to stand up | ➖ you build it (you + AI) | ✅ fastest |
| Cost | infra + ~$0–150/mo tools | $97–$497/mo |

## Recommendation — is Next.js the preferred platform to launch?

**Yes — for John Henry Investments, our own Next.js site is the preferred launch
platform**, because:

1. **We already own it** — the product *is* a Next.js app; marketing pages are just
   more routes, so the funnel and the product share one codebase, brand, and login.
2. **Ownership & SEO** — content, data, and contacts stay in our systems; no lock‑in;
   best‑in‑class performance/SEO (critical for a markets/economics authority play).
3. **One source of truth** — leads and users live in the same DB; no GHL↔app sync.
4. **Cost & integration** — Stripe is already wired; add a free/cheap CRM + email +
   analytics for ~$0–150/mo.

**Trade‑off to accept:** you assemble the automation layer yourself (you + AI) instead
of GHL's all‑in‑one — slightly more setup, far more control and lower lock‑in.

**Choose GHL instead only if** speed‑to‑funnel without building outweighs ownership and
you don't mind a parallel system — and even then at the **$97** tier, not $497.

**Practical path:** launch GTM on the Next.js site (landing + waitlist/trial + checkout,
which mostly exist) and bolt on PostHog (analytics/A‑B), a free CRM, and Resend/SES for
lifecycle email. Revisit GHL only if a specific automation need isn't met.
