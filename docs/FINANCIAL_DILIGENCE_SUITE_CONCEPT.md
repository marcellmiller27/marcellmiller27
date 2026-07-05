# Financial Diligence Suite — Product Concept

> JHI-SIG: 69M2705M · Decision-support product. **Not** an audit, review, or CPA
> opinion. Formal assurance opinions (Unqualified / Qualified / Adverse / Disclaimer)
> are issued only by a **licensed partner CPA firm** engaging the target entity.

## 1. The opportunity
Search-fund / SMB / lower-middle-market buyers ("silverback" acquisitions, EBITDA
$1M–$20M) need to know whether a seller's earnings are **real and durable** before
they buy. The industry-standard funnel is: **(1) analytics screening → (2) Quality of
Earnings (QoE) on the shortlist → (3) formal attest only after LOI.** Manual QoE runs
$20K–$80K and audits $30K–$175K. JHI attacks that cost/speed gap with software +
a partner-CPA network.

## 2. Decision: partner network, not an owned CPA firm
JHI **outsources the CPA function to a vetted partner network** rather than forming an
attest firm. Rationale: capital-light, no CPA-ownership/peer-review burden, no attest
E&O on JHI's books, and instant multi-state licensing coverage. JHI is the **software +
deal-flow layer**; partner CPAs carry the signature and liability.

**Compliance guardrails (design with counsel):**
- Economics are structured as a **SaaS / software + workpaper-prep fee** (and/or a
  disclosed marketplace fee) — never a prohibited commission on an attest client
  (AICPA 1.520 + state boards). For non-attest QoE, referral fees are permissible if
  disclosed.
- **Language discipline everywhere:** "analysis / decision-support / QoE / agreed-upon
  procedures," never "audit opinion" at the SaaS layer.
- Data security bar rises (ingesting bank statements / financials) — ties to
  `docs/SECURITY_POSTURE_AND_DATA_PROTECTION.md`.

## 3. The three tiers
| Tier | Name | Attest? | Delivered by | What it is |
| --- | --- | --- | --- | --- |
| **A** | Financial Integrity Screening | No | JHI platform (automated) | Included with subscription. Proof-of-cash flags, EBITDA normalization, working-capital & revenue-quality checks, Financial Integrity Score. |
| **B** | Quality of Earnings (buy-side FDD) | No | Partner CPA (advisory, signed) | **Flagship add-on.** Software-accelerated QoE workpapers reviewed & signed by a licensed partner CPA — faster, lower cost than manual. |
| **C** | Formal attest (AUP / review / audit) | Yes | Partner CPA firm (engages target) | Only when a lender/deal requires assurance. The four opinions live here only. |

## 4. Add-on pricing (illustrative benchmarks)
Keyed to target EBITDA/SDE; platform price undercuts the manual market while the partner
CPA signs. Final pricing pending partner quotes + willingness-to-pay testing.

| Target size | Manual QoE (market) | JHI platform QoE (all-in) | of which JHI software fee |
| --- | --- | --- | --- |
| SBA / search-fund (SDE < $1M) | $15K–$30K | **$3,900–$6,500** | ~$1,500–$2,500 |
| $1M–$3M EBITDA | $25K–$50K | **$8K–$16K** | ~$3K–$5K |
| $3M–$10M EBITDA | $40K–$80K | **$18K–$35K** | ~$6K–$10K |
| $10M–$20M EBITDA | $75K–$150K+ | **$40K–$70K** | ~$12K–$20K |

Marketing anchor for the core niche: **"Deal QoE Report — from $4,900, CPA-signed, ~2 weeks."**

## 5. As-built (this module)
- **Backend:** `app/financial_diligence.py` (engine), `app/financial_diligence_models.py`,
  `app/routers/financial_diligence.py`. Endpoints under `/api/v1/financial-diligence`:
  - `POST /analyze` → Financial Integrity Score, adjusted EBITDA, proof-of-cash,
    NWC peg, revenue quality, debt-like items, red flags, recommended tier, add-on price.
  - `GET /tiers` → the three tiers.
  - `GET /pricing` → price bands vs. the manual market.
  - `POST /engagement` → partner-CPA engagement quote + routing (`FDS-` reference).
- **Frontend:** `/diligence-suite` page + `components/financial-diligence.tsx`; nav link.
- **Mobile:** `/mobile` "Run Financial Diligence" screen hitting the same endpoint.
- **Tests:** `backend/tests/test_financial_diligence.py`.

Procedures the engine runs: EBITDA normalization & add-back scrutiny · proof-of-cash
(deposits vs. revenue) · net-working-capital peg · quality-of-revenue (recurring +
concentration) · debt-like items review.

## 6. Competitive position
- **vs SaaS** (Grata, SourceScrub, Axial, BizBuySell, deal-room tools): almost all do
  sourcing OR a data room OR analytics — few connect screening → CPA-signed QoE → close
  in one funnel, and essentially none for the underserved sub-$5M segment.
- **vs traditional** (QoE boutiques, CPA firms): faster + cheaper via automation, and JHI
  hands partners pre-worked, qualified deals (lead-gen for them) — a win-win.
- **Moat = execution**: partner-network quality, data, turnaround reliability, and trust,
  not features alone.

## 7. Open items
- Counsel: fee-structure + engagement-letter templates; multi-state partner agreements.
- Partner-network onboarding + SLAs + standardized workpaper templates.
- Data ingestion: extend the Integrations module (accounting connectors / uploads /
  bank statements) to feed the QoE workpapers.
- Willingness-to-pay validation on the pricing table.
