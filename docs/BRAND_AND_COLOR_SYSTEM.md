# John Henry Investments — Brand & Color System

A conversion-oriented visual identity for the John Henry Investments intelligence
platform. Every color choice is grounded in color psychology and behavioral
economics, and is tuned to move both **B2C** (individual investors / wealth
builders) and **B2B** (advisors, family offices, firms) prospects from *visit*
to *sign-up*.

## Logo

The mark is a **trust-navy badge** with a refined **gold** border holding four
**ascending bars** that grow from **emerald** at the base to **gold** at the top,
crowned by a gold upward arrow.

Why it works:

- **Ascending bars + upward arrow** = an instantly readable "economic growth /
  returns up-and-to-the-right" schema. Familiar schemas are processed faster
  (processing fluency), which raises trust and likability.
- **Emerald → gold transition** literally encodes the brand promise: *growth*
  (emerald) compounding into *wealth* (gold).
- **Navy badge + gold border** signals premium financial credibility, the
  category cue users expect from a serious investment brand.

Assets:

- In-app vector emblem: `src/components/logo.tsx` (and favicon `src/app/icon.svg`)
- Full logo lockup and standalone emblem renders are attached to the PR.

## Core palette

| Token | Hex | Meaning (behavioral science) | Primary use |
| --- | --- | --- | --- |
| Trust (deep blue) | `#2f74ff` | Blue is the most universally trusted hue and the dominant color in finance/banking. It signals security, competence, and stability, which **lowers perceived risk** — the single biggest barrier to a financial sign-up. | Links, info, B2B credibility cues, Enterprise tier accent, chat/user bubble |
| Growth (emerald) | `#1fc585` | Green carries strong "gain / money / go" associations. Used sparingly as the **only** primary-action color so the decisive CTA pops (Von Restorff / isolation effect), maximizing click-through. | Primary CTA buttons, "Generate report", positive metrics |
| Premium (gold) | `#e3b765` | Gold conveys prestige, achievement, and aspiration. It frames the wealth identity and justifies premium pricing. | Eyebrows/labels, list bullets, Consumer tier accent, logo border |
| Ink (navy base) | `#06121f` | Dark, low-glare canvas that makes data and accents read as confident and high-end; reduces cognitive load for long analytical sessions. | Page background, cards |
| Text / Muted | `#eef5fb` / `#9db0c0` | High-contrast neutral type for legibility and effortless scanning. | Body copy |

CSS source of truth: the `:root` custom properties in `src/app/globals.css`.

## The conversion logic (why this beats an all-gold scheme)

1. **Trust first, then action.** Visitors must feel *safe* before they act. A
   blue-anchored, navy canvas establishes credibility; the emerald CTA then
   gives a single, unambiguous "grow your money" action to click.
2. **One job per color.** Gold = aspiration/labels, blue = trust/links, emerald
   = *act now*. Restricting the action color to one hue increases CTA salience
   and measured click-through versus a palette where the accent is everywhere.
3. **Loss-aversion friendly.** Green = "gain/safe to proceed"; we avoid using
   red/alarm colors on the path to sign-up so the journey never signals danger.

## B2C vs B2B tuning

The same core palette is re-weighted per audience because the two segments
respond to different motivators.

| | B2C (retail investors, wealth builders) | B2B (advisors, family offices, firms) |
| --- | --- | --- |
| Dominant emotion | Aspiration, optimism, self-improvement | Trust, competence, risk reduction, ROI |
| Lead accent | **Gold** (wealth aspiration) + energetic **emerald** CTAs | **Trust-blue** (credibility) with restrained **emerald** CTAs |
| CTA copy intent | "Start growing" / "Open dashboard" (instant value) | "Book a demo" / "Talk to sales" (consultative) |
| Proof emphasis | Returns, opportunity score, momentum | Security, controls, role permissions, audit |

This is implemented today on the pricing tiers, where each plan leads with the
color that converts its audience:

- **Consumer (B2C)** → gold top accent (aspiration)
- **Professional** → emerald top accent (growth / ROI)
- **Enterprise / Family Office (B2B)** → trust-blue top accent (credibility)

See `.pricing-grid .pricing-card:nth-child(n)` in `src/app/globals.css`.
