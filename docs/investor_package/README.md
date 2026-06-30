# John Henry Investments Investor Package

> **Posture note:** JHI is a **research & analytics firm** that **never manages outside
> funds / client money**, but **is open to outside equity (VC/seed)** to fund the company
> (`docs/COMPANY_POSTURE_AND_COMPLIANCE.md`). These materials support **fundraising** (and
> internal/IP/estate/lending use). To raise VC, plan for a fundable structure (Delaware
> C-corp, clean cap table, IP assignment) — confirm with counsel. Be honest in diligence:
> the Opportunity Score's predictive validity is still unproven (position as research/insight).

## Purpose

This folder contains a pitch deck, PowerPoint presentation, financial model, DCF model, chart data, and diligence materials for the John Henry Investments platform — for **fundraising** (VC/seed) as well as internal planning, IP valuation, estate/insurance, and lender/banking use.

## Files

| File | Purpose |
| --- | --- |
| `PITCH_DECK.md` | Slide-by-slide pitch deck source content |
| `JOHN_HENRY_INVESTMENTS_PITCH_DECK.pptx` | Generated PowerPoint presentation |
| `FINANCIAL_MODEL_DCF.md` | Narrative financial model with DCF, charts, assumptions, and investor interpretation |
| `JOHN_HENRY_INVESTMENTS_FINANCIAL_MODEL.xlsx` | Generated Excel workbook with operating model, DCF, marketing, and personnel sheets |
| `../FIVE_STAGE_VALUATION_MODEL.md` | Five-stage market-cap/equity-value scenarios and probability-weighted valuation ranges |
| `financial_model_base_case.csv` | Full five-year base-case model |
| `dcf_model.csv` | Discounted cash flow schedule |
| `revenue_projection.csv` | Revenue projection chart data |
| `expenditure_projection.csv` | Expenditure projection chart data |
| `marketing_projection.csv` | Marketing projection chart data |
| `staffing_projection.csv` | Personnel projection chart data |
| `model_assumptions.csv` | Pricing, mix, payment, discount rate, and terminal growth assumptions |
| `generate_pitch_deck.py` | Regenerates the PowerPoint deck |
| `generate_financial_model_xlsx.py` | Regenerates the Excel workbook |
| `requirements.txt` | Python dependencies for deck/workbook generation |

## Generated PowerPoint slides

The PowerPoint includes:

1. Title
2. Problem
3. Solution
4. Product modules
5. Revenue model
6. Revenue projection chart
7. Expenditure projection chart
8. Marketing projection chart
9. EBITDA projection
10. Discounted cash flow
11. Personnel hierarchy
12. Competitive moat
13. Go-to-market
14. Risk controls
15. Use of funds
16. Investor ask
17. Additional recommendations
18. Closing

## Financial model contents

The model includes:

- Five-year base-case projections
- Revenue projections
- Expenditure projections
- Marketing projections
- Staffing/professional-services projections
- EBITDA
- Capex
- Working capital
- Cash tax estimate
- Free cash flow
- DCF valuation
- Terminal value
- Estimated enterprise value

## Additional recommended investor materials

The following should be added before investor meetings:

- Live spreadsheet with editable assumptions
- Product screenshots
- Product demo video
- Founder biography
- Pilot customer list or target customer pipeline
- Legal/compliance memo
- Churn and retention assumptions
- Customer acquisition channel strategy
- Competitive landscape
- Data moat and Opportunity Score methodology
- Use-of-funds allocation by milestone
- Risk disclosure appendix
- Cap table and fundraising terms

## Regenerate files

Install dependencies:

```bash
python3 -m pip install -r docs/investor_package/requirements.txt
```

Regenerate PowerPoint:

```bash
python3 docs/investor_package/generate_pitch_deck.py
```

Regenerate Excel model:

```bash
python3 docs/investor_package/generate_financial_model_xlsx.py
```

## Planning disclaimer

All financial projections are estimates for planning and discussion. They are not investment advice, accounting advice, valuation advice, tax advice, legal advice, or a guarantee of future performance.
