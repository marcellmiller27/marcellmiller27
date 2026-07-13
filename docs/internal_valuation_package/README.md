# John Henry Investments — Internal Valuation & Financial-Planning Package

> JHI-SIG: 69M2705M · **INTERNAL by default.** JHI Research & Analytics Firm, Inc. is a **software
> publisher** that builds desktop and mobile research platforms; this package values and plans around
> **our own internally-developed software IP**. It is used for **internal planning, software-asset /
> IP valuation (ASC 350-40 support), estate/insurance, and lending/debt underwriting** — **not** a
> current offer to sell securities or a solicitation of investment.
>
> **Optionality retained:** JHI is presently **private and bootstrapped (no outside investors)**. The
> deck/model materials below are **kept intact** so leadership retains the *choice* to present them for
> an outside opportunity **if and only if** the Board ever elects to — nothing here commits JHI to, or
> forecloses, that path.

## Purpose

This folder contains the financial model, DCF, chart data, an internal company & platform overview,
and supporting materials for the John Henry Investments platform.

## Files

| File | Purpose |
| --- | --- |
| `PITCH_DECK.md` | Slide-by-slide company & platform overview (internal; retained for optional external use) |
| `JOHN_HENRY_INVESTMENTS_PITCH_DECK.pptx` | Generated PowerPoint overview |
| `FINANCIAL_MODEL_DCF.md` | Narrative financial model with DCF, charts, and assumptions |
| `JOHN_HENRY_INVESTMENTS_FINANCIAL_MODEL.xlsx` | Generated Excel workbook (operating model, DCF, marketing, personnel) |
| `../FIVE_STAGE_VALUATION_MODEL.md` | Five-stage market-cap/equity-value scenarios and probability-weighted valuation ranges |
| `financial_model_base_case.csv` | Full five-year base-case model |
| `dcf_model.csv` | Discounted cash flow schedule |
| `revenue_projection.csv` | Revenue projection chart data |
| `expenditure_projection.csv` | Expenditure projection chart data |
| `marketing_projection.csv` | Marketing projection chart data |
| `staffing_projection.csv` | Personnel projection chart data |
| `model_assumptions.csv` | Pricing, mix, payment, discount rate, and terminal growth assumptions |
| `generate_pitch_deck.py` | Regenerates the PowerPoint overview |
| `generate_financial_model_xlsx.py` | Regenerates the Excel workbook |
| `requirements.txt` | Python dependencies for deck/workbook generation |

## Financial model contents

- Five-year base-case projections · revenue · expenditure · marketing · staffing/professional-services
- EBITDA · capex · working capital · cash-tax estimate · free cash flow
- DCF valuation · terminal value · estimated enterprise value

## Regenerate files

```bash
python3 -m pip install -r docs/internal_valuation_package/requirements.txt
python3 docs/internal_valuation_package/generate_pitch_deck.py
python3 docs/internal_valuation_package/generate_financial_model_xlsx.py
```

## Disclaimer

All figures are estimates for **internal planning and discussion**. This package is **not** an offer to
sell securities, a solicitation of investment, or investment/accounting/valuation/tax/legal advice, and
is **not** a guarantee of future performance.
