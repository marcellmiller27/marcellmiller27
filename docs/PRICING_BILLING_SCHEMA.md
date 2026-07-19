# Pricing & Billing Schema — "Mirror the NASDAQ Mechanism"

**Strategic principle (founder, 2026-07-15):** *Best defense is a strong offense.*
We attack the market confidently because the **economics defend themselves** — we
**denominate JHI billing in the same unit NASDAQ licenses in (the external end
user / paid seat)**, so cost and revenue move in **lockstep** and margin is locked
in structurally. Think backwards from the heavy-lifting expenditures (data + cloud),
price the unit well above cost, then leapfrog forward on revenue drivers.

> Companion: `docs/MARKET_DATA_VENDOR_COMPARISON.md` (data licensing), and the model
> script `scripts/pricing_margin_model.py` (reproduces every number below).
> Estimates for internal planning — not a forecast. NASDAQ overage rate is a
> placeholder pending the signed Service Description.

## 0. Tier numbering convention (founder, 2026-07-15) — AUTHORITATIVE
To avoid ambiguity, JHI numbers tiers **top-down** (T1 = highest/premium):

| Tier | Package | Price | Premium? | Premium-feature access (e.g. Company→Excel workbook) |
|---|---|---|---|---|
| **T1** | **Enterprise** | $1,500/mo | ✅ Premium | ✅ Yes (richest: branded / portfolio / batch) |
| **T2** | **Professional** | $299/mo | ✅ Premium | ✅ Yes (company/comps workbook) |
| **T3** | **Consumer / Individual** | $50/mo | — Individual | ❌ No access |

**Premium features are gated to T1 (Enterprise) + T2 (Professional). T3 (the $50
individual package) does not receive them** — which also makes them an upgrade
lever (T3 → T2/T1). Backend gate: `dependencies.require_premium` (allows plans
`ENTERPRISE`/`PROFESSIONAL`).

## 1. The mirrored mechanism
| NASDAQ (our cost) | JHI (our revenue) — mirrored |
|---|---|
| Unit = **external end user** | Unit = **paid seat** (= one end user) |
| Up to **1,000** users included (flat) | Each tier **includes a base # of seats** |
| **Overage** above 1,000 at a higher rate | **Per-additional-seat** above the base |

Every seat we sell maps to exactly one NASDAQ user; our per-additional-seat charge
mirrors their overage. Grow past the base → the client pays **us** more and we pay
**NASDAQ** more, in lockstep. **No free-seat leakage, by construction.**

## 2. Seat schema (the anchor)
| Tier | Price | Seats | Additional seats |
|---|---|---|---|
| **Consumer** | $50/mo | 1 | — (single seat) |
| **Professional** | $299/mo | 1 | — (single seat) |
| **Enterprise** | $1,500/mo | **5 included** | **$99 / seat / mo** |

Consumer & Professional stay single-seat (clean, mass-market). Enterprise's
per-additional-seat line **is our mirror of NASDAQ's overage.** The platform already
supports this (Enterprise "team accounts & role permissions" + the Gatekeeper RBAC),
and Stripe bills per-seat natively via subscription `quantity`.

## 3. Why risk is low — unit economics (verified by the model)
Fully-loaded marginal cost per seat ≈ **NASDAQ ~$1.50 + cloud ~$1.50 + 3% processing**.

| Unit | Seat price | Cost/seat | Gross margin |
|---|---|---|---|
| Consumer seat | $50 | $4.50 | **91%** |
| Professional seat | $299 | $11.97 | **96%** |
| Enterprise (per-seat-equiv) | $300 | $12.00 | **96%** |
| Enterprise add'l seat | $99 | $5.97 | **94%** |

**Overage stress (Consumer seat) — margin holds even if NASDAQ's per-user rate rises:**
| NASDAQ $/user/mo | Consumer gross margin |
|---|---|
| $1.50 (at cap) | 91% |
| $3.00 (2×, placeholder) | 88% |
| $6.00 (4×) | 82% |
| $10.00 | 74% |
| $15.00 (10×) | 64% |

Even a **10× punitive overage** leaves a 64% margin on the *cheapest* tier. The
surcharge is a rounding error against the revenue it rides on.

## 4. Scale scenarios (illustrative mix; margins are robust to mix)
| Scenario | End users | Revenue/yr | NASDAQ/mo | Gross margin |
|---|---|---|---|---|
| Near-term | ~1,200 | ~$1.87M | $2,100 | **94.5%** |
| Mid | ~5,000 | ~$7.27M | $13,560 | **93.5%** |
| Full-scale target | ~59,500 | ~$59.3M | $177,000 | **91.6%** |

*(Gross margin = revenue − data − cloud − processing. "EBITDA" in the model adds only
lean fixed opex; it **excludes sales & marketing / 1099 commissions**, which are a
customer-acquisition investment layered on top — see the sales-commission model.)*

## 5. NASDAQ alignment — this *simplifies* the negotiation
Because we bill per seat, **we can accept NASDAQ's per-user counting** — every counted
user is a *paying* seat, so there is no free-seat leakage to fear. The one item still
worth nailing in the Service Description is the **overage rate** (so the per-seat
margin above the cap is a known number). Cleaner ask, less to negotiate. See
`docs/legal/nasdaq/ORDER_FORM_REVIEW.md`.

## 6. Copy reconciliation
The homepage currently says *"no per-seat surprises"* (`src/app/page.tsx`). Mirroring
NASDAQ introduces transparent per-seat pricing on **Enterprise**, so reframe the
promise as **"transparent — no *surprise* seat fees."** Consumer/Professional remain
single-seat, so the simple feel holds for the mass tiers. (Copy change tracked
separately; not yet applied.)

## 7. Proposed board resolution
> *Resolved,* that JHI adopts a **per-external-end-user (per-seat) billing schema that
> mirrors the NASDAQ licensing mechanism** — Consumer and Professional single-seat at
> $50 and $299/mo; Enterprise at $1,500/mo including 5 seats with additional seats at
> $99/seat/mo — so that data cost and subscription revenue are denominated in the same
> unit and move in lockstep; and that JHI accept NASDAQ's per-user counting provided the
> overage rate is fixed in the signed Service Description.

## 8. Open items
- [ ] Founder to confirm/adjust the **$99 additional-seat** price and **5-seat** base.
- [ ] Fix the **NASDAQ overage rate** in the Service Description (Monday call).
- [ ] Validate the **AWS/GCP per-user cost estimate** against an actual infra audit.
- [ ] Apply the pricing-page + Stripe (`quantity`) changes once numbers are locked.
- [ ] Reconcile the homepage "no per-seat surprises" copy.
