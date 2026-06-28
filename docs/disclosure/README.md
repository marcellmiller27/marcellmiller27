# Coding Disclosure (Excel)

**`JHI_Coding_Disclosure.xlsx`** — full disclosure of all coding performed on the John
Henry Investments platform, organized **by component (subsystem)**, mapped to the
**skillset / job title** that would perform each action, with a **realistic hourly value
per action** and the estimated equivalent professional value.

## Workbook tabs
1. **Disclosure** — every work item: subsystem · action · job title · level · hourly rate (mid) · est. hours · value · key files · status.
2. **Rate Card** — realistic hourly rates (low/mid/high) by job title.
3. **Subsystem Summary** — hours and value rolled up per subsystem (live `SUMIF` formulas).
4. **Notes & Disclosure** — methodology, rate anchors, and disclaimers.

## Headline (mid-market rates)
- **44** work items across **15** subsystems
- **≈ 664** equivalent professional hours
- **≈ $99,540** equivalent professional value (mid)

## Regenerate
```bash
/workspace/.venv/bin/python docs/disclosure/generate_disclosure.py   # needs openpyxl (tooling only)
```

> Estimates of equivalent professional effort for a founder-led, AI-assisted build —
> a planning/disclosure artifact, **not** an invoice or audited record. Confirm with a
> CPA/controller before using for capitalization, valuation, or tax. Signature: `69M2705M`.
