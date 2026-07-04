# John Henry Investments — AI Customer-Service Team Profiles

Five specialized AI agents support every onboarded member 24/7. An intelligent
router classifies each message and hands it to the right specialist; platform issues
(and anything unresolved) get an initial response and are **escalated to the founder**
as a tracked ticket. Live roster + photos: the `/team` page and `GET /api/v1/agents`.

| Photo | Agent | Role | Expertise | Escalates? |
| --- | --- | --- | --- | --- |
| `public/team/ava.png` | **Ava Bennett** | Onboarding Concierge | onboarding, account setup, walkthroughs, activation | no |
| `public/team/max.png` | **Max Carter** | Subscriptions & Billing Specialist | plans, pricing, upgrades, billing, Stripe | no |
| `public/team/sage.png` | **Sage Okafor** | Account & Security Agent | auth, 2FA, biometric, data protection, privacy | no |
| `public/team/quinn.png` | **Quinn Alvarez** | Product & Markets Guide | Opportunity Score, live market data, modules, how-to | no |
| `public/team/tess.png` | **Tess Nakamura** | Technical Support & Triage | incident triage, troubleshooting, bug intake, founder escalation | **yes** |

## Profiles

### Ava Bennett — Onboarding Concierge
Warm first point of contact for newly onboarded users. Trained on JHI's onboarding
playbooks and product docs; gets every new member from sign-up to first insight
(accounts, navigation, first actions).

### Max Carter — Subscriptions & Billing Specialist
Owns subscription and billing questions across Consumer, Professional, and Enterprise
plans — pricing, upgrades/downgrades, and the Stripe-based billing foundation. Trained
on the plan catalog and billing policies.

### Sage Okafor — Account & Security Agent
Account and security specialist: password, two-factor, and biometric sign-in, plus how
member data is protected. Calm and precise on access and privacy.

### Quinn Alvarez — Product & Markets Guide
Explains how the platform works — the John Henry Opportunity Score, live multi-asset
market data, and the modules — in plain language. Education and product guidance only,
never personalized financial advice.

### Tess Nakamura — Technical Support & Triage
First responder for platform issues. Acknowledges, triages severity, gives an initial
response, and forwards anything needing action to the **founder** as a tracked ticket
(`GET /api/v1/agents/tickets`) so nothing is missed.

## How routing & escalation work

- **Route:** the message is matched against the support knowledge base; its category
  maps to the owning agent (e.g., Billing → Max, Account & security → Sage).
- **Escalate:** if the message looks like a platform issue (bug/error/can't/broken/…)
  or the team can't answer confidently, **Tess** responds and opens a ticket assigned
  to the founder (priority `high` for issues).
- **Endpoints:** `GET /api/v1/agents` (roster), `POST /api/v1/agents/message`
  (route + answer + escalate), `GET /api/v1/agents/tickets` (founder view, auth).

*Note: these are AI personas (the names/photos are fictional brand identities for the
automated agents), not real individuals.*
