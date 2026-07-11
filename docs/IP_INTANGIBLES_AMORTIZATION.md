# Intellectual Property & Intangible Assets — Capitalization & Amortization

How to account for the John Henry Investments platform's IP and proprietary
properties on the books, including capitalization policy and amortization schedules.
Ties into the durable accounting module (chart of accounts + journal entries +
trial balance).

> Not accounting/tax advice. This is a working framework — confirm policy, useful
> lives, and especially **tax treatment (IRC §174)** with a licensed CPA.

## 1. IP & proprietary property inventory

| Asset | Nature | Typical treatment |
| --- | --- | --- |
| Platform software (Next.js + FastAPI app, APIs, infra-as-code) | Internally‑developed software | **Capitalize** dev‑stage costs; amortize |
| John Henry Opportunity Score methodology + research/valuation engines | Proprietary models/algorithms | Capitalize as part of software / R&D (see notes) |
| AI agent system & support automation | Internally‑developed software | Capitalize dev‑stage costs |
| Brand: name, logo, mission, color system, content/docs | Trademark / brand | **Indefinite‑lived** intangible (not amortized; impairment‑tested) |
| Domain name(s) | Intangible | Capitalize; usually indefinite‑lived |
| Data/licenses (e.g., Sharadar, market feeds) | Licensed rights | Prepaid/expense over term (not owned IP) |

## 2. Capitalization policy (book / US GAAP)

For SaaS/internal‑use software, **ASC 350‑40** (IAS 38 internationally):

- **Preliminary (planning) stage** → **expense** as incurred.
- **Application development stage** → **capitalize** direct costs (developer time,
  AI/cloud build costs directly attributable, third‑party dev) to an intangible asset
  (account **1500 – Platform Development Asset (capitalized IP)**).
- **Post‑implementation / operation stage** (maintenance, ops) → **expense**.
- *(If the software were sold/licensed externally as a product, ASC 985‑20 applies —
  capitalize after technological feasibility. For a hosted SaaS, 350‑40 is typical.)*

**Internally‑generated brand** (name/logo): under IAS 38 / US GAAP, internally‑created
brands are generally **not capitalized** (expense); capitalize only acquired brands or
direct legal/registration costs of trademarks → account **1600**.

## 3. Useful lives & method

- **Software/IP (1500):** straight‑line over **3 years (36 months)** is a common,
  defensible useful life for fast‑moving software (range 3–5y). Begin amortizing when
  placed in service.
- **Trademarks/brand (1600):** **indefinite‑lived** → no amortization; annual
  impairment test.

## 4. Chart-of-accounts hooks (now in the platform)

The accounting module's chart of accounts now includes:
- `1500` Platform Development Asset (capitalized IP) — the intangible.
- `1510` Accumulated Amortization – Platform IP — contra‑asset.
- `1600` Trademarks & Brand (indefinite‑lived).
- `5300` Amortization Expense — P&L.

## 5. Journal entries

**Capitalize development cost** (e.g., $180,000 of qualifying dev‑stage cost):
```
Dr 1500 Platform Development Asset   180,000.00
   Cr 1000 Cash (or 2000 Accounts Payable)   180,000.00
```

**Monthly amortization** (straight‑line, $180,000 / 36 = $5,000/mo):
```
Dr 5300 Amortization Expense          5,000.00
   Cr 1510 Accumulated Amortization        5,000.00
```
Both post cleanly through `POST /api/v1/accounting/journal-entries` (balanced,
valid account codes), and flow into the trial balance.

## 6. Amortization schedule

A worked, straight‑line schedule (illustrative $180,000 / 36 months, in service
2026‑07) is generated to `docs/ip/amortization_schedule.csv`:

| Period | Opening NBV | Amortization | Accum. amort. | Closing NBV |
| --- | ---: | ---: | ---: | ---: |
| 2026‑07 | 180,000.00 | 5,000.00 | 5,000.00 | 175,000.00 |
| 2026‑08 | 175,000.00 | 5,000.00 | 10,000.00 | 170,000.00 |
| … | … | … | … | … |
| 2029‑06 | 5,000.00 | 5,000.00 | 180,000.00 | 0.00 |

Regenerate with your real numbers:
`python3 docs/ip/generate_amortization.py` (edit `CAPITALIZED_AMOUNT`,
`USEFUL_LIFE_MONTHS`, in‑service date).

## 7. Important tax note (don't miss this)

**Book ≠ tax.** Under **IRC §174** (post‑2022), **R&E/software development costs must be
capitalized and amortized for tax** — **5 years** (US) / **15 years** (foreign),
half‑year convention — even if expensed for book. This materially affects taxable
income. Track a separate §174 schedule and confirm with your CPA.

## 8. Recommended actions

1. Track qualifying **development‑stage** costs (incl. attributable AI/cloud build
   spend) to capitalize to `1500`; expense planning/maintenance.
2. Set the capitalization policy (threshold, useful life 3y) and document it.
3. Post the capitalization entry; record monthly amortization (entries above).
4. Maintain the amortization schedule (CSV/generator) and a **separate §174 tax
   schedule**.
5. Register trademarks; capitalize only legal/registration costs to `1600`.
6. Review intangibles annually for impairment.
