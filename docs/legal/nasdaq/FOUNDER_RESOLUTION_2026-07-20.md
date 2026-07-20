# NASDAQ Data License — Founder Resolution (2026-07-20)

> JHI-SIG: 69M2705M · JHI Research & Analytics Firm, Inc. (proprietary)
> Founder directive of record resolving the open items in the NASDAQ (Nasdaq Data Link)
> engagement. **Not legal advice.** Companions: `DATA_LICENSE_TERMS_REVIEW.md`,
> `ORDER_FORM_REVIEW.md`, `SERVICE_ORDER_00151172_REVIEW.md`, `COUNSEL_REVIEW_BRIEF.md`;
> pricing: `../../PRICING_BILLING_SCHEMA.md`.

## Status: CLOSED
The firm is **proceeding into agreement** with Nasdaq (Nasdaq Data Link). The items below are the Founder's directives; they govern how we execute the MSA/Order Form and how we build against the data.

### Closure (2026-07-20, Founder)
- The **Founder will upload a new Order Form**; it will **not carry the previously stated/drafted addendum terms**.
- **The subject matter is closed** — no further negotiation of terms on our side.
- The firm's **binding operational commitment going forward is data-set isolation — no spillage** (see §4). This is the controlling requirement regardless of paperwork.

## Decisions

### 1. Seat basis (to be stated in the MSA)
- **Tiers 1–3 subscriptions are sold on a 1 user-seat basis.**
- **Additional seats are billed at current published rates** (per `../../PRICING_BILLING_SCHEMA.md`).
- This one-seat-per-subscription basis is to be **stated in the legal agreement (MSA)**.

### 2. Volume threshold / rate revisit
- The current commercial terms hold **up to 1,000 subscriptions / user-seats**.
- At that threshold we **revisit and renegotiate the rate** ("cross that bridge when we get to it"). Not a present-day concern; flagged for when volume approaches the cap.

### 3. Third-party distribution legality — Founder position
- The Founder is **not concerned with third-party distribution legality issues** for this engagement; proceed on that basis.
- (The clause-level analysis of external/Derived-Data distribution remains on file in `DATA_LICENSE_TERMS_REVIEW.md` for counsel; this note records the Founder's directive to move forward.)

### 4. Primary focus — data-set isolation (NO spillage)
The Founder's main requirement once we move forward:
- **No data-set spillage.** The licensed Nasdaq / Sharadar data set must **not leak, commingle, or be repurposed into other (third-party) data sets.**
- Keep the **licensed source data isolated and server-side**; the product exposes only JHI-owned **derived analytics** (scores, normalized metrics, research narratives), never the raw licensed fields, and never in a form that reconstructs them (consistent with `DATA_LICENSE_TERMS_REVIEW.md`).
- **No cross-contamination**: pipelines, caches, exports, and any downstream/third-party data sets must be kept separate from the licensed set so licensed data cannot bleed into a repurposed third-party data set.

## Engineering implications (for the Nasdaq Data Link integration)
- Isolate the licensed data store; do not merge licensed rows into shared/general datasets that feed other vendors or exports.
- Serve derived-only outputs to subscribers; keep raw licensed data internal.
- Add provenance/tagging so licensed-origin data is traceable and can be prevented from flowing into repurposed third-party data sets.

**Recorded by:** Cy Henry (VP, Software Engineering — AI teammate) · signature of record `69M2705M`.
