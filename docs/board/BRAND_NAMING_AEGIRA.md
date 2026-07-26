# Board Decision Record — Platform Brand Naming: "Aegira"

**Date:** 2026-07-26 · **Type:** Founder brand decision (recorded) · **Recorder:** Cy Henry (VP, Software Engineering — AI)
**Present:** Founder (Galen Marcellus Miller). · **Signature of record:** `69M2705M`
> Companion to the board minutes series. NOT legal/tax advice.

---

## 0. Addendum — 2026-07-26 (evening): name LOCKED + domains purchased
- **Name locked.** Founder confirmed: **"Aegira is what we use on platform"** — the platform/product brand is **Aegira**; **JHI Research & Analytics Firm, Inc.** remains the corporate entity / publisher of record. Status moves from *proposed* → **DECIDED**.
- **Primary domain: `aegiraenterprise.com`** (canonical / OG / `metadataBase` base). *(Note: `aegira.com` was unavailable; the founder selected the `aegiraenterprise.*` family instead.)*
- **Domain portfolio purchased via AWS Route 53 — registration in progress (awaiting completion):**
  - `aegiraenterprise.com` — **primary** (storefront + platform, canonical)
  - `aegiraenterprise.ai` — Aegira AI / research-assistant surface
  - `aegiraenterprise.io` — developer-adjacent / redirect
  - `aegiraenterprise.dev` — reserved for **Aegira API** (developer platform); Google TLD, HSTS-preloaded (HTTPS-forced)
  - `aegiraenterprise.app` — reserved for **Aegira Mobile** (investor app); Google TLD, HSTS-preloaded (HTTPS-forced)
- **Canonical policy:** `.com` is canonical; all other TLDs **301-redirect to `aegiraenterprise.com`** (or a dedicated sub-path) to preserve SEO authority and avoid duplicate-content splits. Redirects are registrar/DNS-level — no app code change.
- **Code applied (PR — brand-aegira-sweep):** default `NEXT_PUBLIC_SITE_URL` / `metadataBase` / OG base → `https://aegiraenterprise.com` in `src/app/layout.tsx`, `Dockerfile`, `docker-compose.yml` (overridable for staging/preview).
- **Still open:** DNS records once Route 53 registration completes; **SES sender domain** (`aegiraenterprise.com`) for newsletter send; trademark clearance/filing for "Aegira" (Cl. 9/36/42) via counsel remains in-flight and independent of registration.

---

## 1. The proposal
Name the **product/platform "Aegira"**, while **JHI Research & Analytics Firm, Inc.** remains the
**corporate entity / publisher**. This creates a clean two-layer identity:

- **JHI Research & Analytics Firm, Inc.** — the company (legal entity, publisher of record).
- **Aegira** — the platform/product brand, with a coherent product family:
  - Aegira **Platform** · Aegira **AI** · Aegira **Markets** · Aegira **Macro** · Aegira **Terminal**
    (pro desktop) · Aegira **Intelligence** · Aegira **Research** · Aegira **Enterprise** · Aegira **API**
    (developers) · Aegira **Mobile** (investor app) · Aegira **Studio** (model building/analytics).
- **Taglines under consideration:** *"See Further."* · *"Institutional Intelligence for Global Markets."* ·
  *"Economic Intelligence Platform."*

## 2. Rationale (recorded)
1. **"Aegis" DNA without copying it** — subconsciously reads as protection, strength, authority, confidence, yet stands as its own identity.
2. **Institutional register** — belongs in the peer set (Bloomberg · FactSet · Morningstar · Palantir · **Aegira**); sounds established, not trendy-startup.
3. **Scales as a product family** — every "Aegira ___" extension reads naturally.
4. **Premium phonetics** — three syllables, elegant, memorable (AE-GEE-RA / AY-JEER-A).
5. **Global, not finance-confined** — fits macro, sovereign debt, central banks, M&A, commodities, AI, crypto, economic intelligence — an intelligence company whose products evolve over decades.
6. **Vision fit** — an "operating system for economic intelligence," with JHI as the corporate identity behind it.

## 3. VP assessment (Cy)
- **Endorse.** It clears our **institutional-grade nomenclature** bar (name + disclosed function; not elementary), and the JHI-corporate / Aegira-platform split is a **clean, standard structure** (legal entity ≠ product brand).
- **It resolves an open issue for free:** the flagged legacy **"John Henry Investments"** mark on the storefront → replaced cleanly by **Aegira** (platform) with **JHI** as the corporate footer/publisher. (Supersedes the "brand-mark reconciliation" carry-over.)
- **Pronunciation:** recommend we **standardize on one** — *AY-JEER-ah* — and use it consistently (a two-pronunciation name creates friction).

## 4. 🔒 Due diligence BEFORE we lock it (do not skip)
1. **Trademark clearance** — USPTO (and international) search for "Aegira" in the relevant classes: **Cl. 9** (software), **Cl. 36** (financial info services), **Cl. 42** (SaaS/technology). Engage counsel to clear + file **before** public use.
2. **Domain acquisition** — secure **aegira.com** (+ **.ai / .io**). *(Note: we currently own `johnhenrycapital.com`; a platform rename means acquiring the Aegira domain and re-pointing the app's `metadataBase`/OG/canonical + SES sender domain. Keep JHI/johnhenrycapital as corporate if desired.)*
3. **Conflict check** — search for existing companies/products named "Aegira" (it is a real word/name — e.g., a place and a biological genus) to avoid confusion or infringement in our space.
4. **Linguistic check** — confirm no negative meaning/connotation in major languages.
5. **Social/handles** — availability of @Aegira across relevant platforms.

## 5. Platform implications once cleared (Cy to execute)
> **Superseded by §0 addendum:** primary domain is **`aegiraenterprise.com`** (not `aegira.com`, which was unavailable), purchased via Route 53.
- Point **`aegiraenterprise.com`** → set `NEXT_PUBLIC_SITE_URL`/`metadataBase`/OG + SES sender domain (defaults already landed in code).
- **Brand sweep:** replace "John Henry Investments" / platform display name → **Aegira** (display layer), keeping **JHI Research & Analytics Firm, Inc.** in the corporate footer/publisher line and `JHI-SIG` provenance.
- Roll the product-family names into the IA/menu as modules mature (Terminal, API, Studio, etc.).

## 6. Decision
- **Status: DECIDED (2026-07-26).** Platform brand = **Aegira**; corporate entity/publisher = **JHI Research & Analytics Firm, Inc.** Primary domain = **`aegiraenterprise.com`** (see §0 addendum). Trademark clearance/filing continues in parallel with counsel.
- Corporate/product structure **agreed:** JHI (corporate publisher) + **Aegira** (platform brand).

## Action items
| # | Action | Owner | Priority | Status |
|---|---|---|---|---|
| 1 | Engage counsel: **trademark clearance + filing** for "Aegira" (Cl. 9/36/42) | Founder + attorney | 🔴 | In progress |
| 2 | Acquire the **`aegiraenterprise.*`** domain family (.com/.ai/.io/.dev/.app) | Founder | 🔴 | ✅ Purchased via AWS Route 53 — registration in progress |
| 3 | Conflict/linguistic/social-handle checks | Cy (research) + Founder | 🟡 | Open |
| 4 | Execute the **brand sweep** (display → Aegira; JHI as corporate) + domain wiring | Cy | 🟡 | ✅ Sweep + `NEXT_PUBLIC_SITE_URL` default landed (brand-aegira-sweep) |
| 5 | On registration completion: set **DNS** + choose **SES sender domain** (`aegiraenterprise.com`) for newsletter send; configure `.ai/.io/.dev/.app` → 301 to `.com` | Founder + Cy | 🟡 | Open |

**Recorded by:** Cy Henry · signature of record `69M2705M`.
