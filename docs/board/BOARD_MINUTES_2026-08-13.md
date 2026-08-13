# Board Minutes — JHI Research & Analytics Firm, Inc.

**Meeting date:** 2026-08-13 · **Type:** Founder working session (thesis of record + platform ops) · **Recorder:** Cy Henry (VP, Software Engineering — Cloud Agent)
**Product:** Aegira · **Publisher:** JHI Research & Analytics Firm, Inc.
**Present:** Founder (Galen Marcellus Miller).

> NOT legal/tax/accounting advice. Prior session: `docs/board/BOARD_MINUTES_2026-08-10.md`.
> Signature of record — `JHI-SIG: 69M2705M`. Ethos: *How we do anything is how we do everything.*

---

## 1. Shipped / operational this session (✅)

- **Documents module locked to staff-only (security).** `#167` — internal firm files (5-yr projections, commission
  model, competitor audits, data-redistribution matrix) were subscriber-visible; now staff-only across menu, route
  (server-side staff redirect), and file serving (moved out of the public web root behind a `require_staff` endpoint).
- **Reports page fixed + two new editions.** `#170` / `#173`-adjacent — every Reports card was a dead button;
  all four now open live, generated editions with PDF export. New **Crypto Intelligence** and **Dividend
  Opportunities** editions built on the existing newsletter engine.
- **Global site footer + Aegira messaging.** `#172` — persistent About / Contact / Help / Support / Legal / Privacy /
  Terms footer on every page (created the five missing pages); Home/About hero set to **"See what Wall Street sees."**
- **Company deep-dive construct.** `#166` — People/Governance, Segments, Operations depth plan tied to Valuation 2.0.
- **Institutional per-ticker workbook.** `#173` — one branded Excel file: **daily + weekly technicals**, options
  context, full ratio breakdown (EPS, margins, revenue trend, D/E, ROE, FCF), and DCF valuation. Supersedes `#169`.
- **Top-20 competitive differentiation research.** `#171` — 23 firms torn down w/ 2026 pricing → pain-point matrix,
  Aegira differentiation thesis, Tier packaging, and a P1/P2/P3 "pain-points to own" backlog.

## 2. Secrets health-check (✅ / action)

Full live probe of API keys in-platform:

| Secret | Result |
| --- | --- |
| BEA, BLS, NASDAQ Data Link (Sharadar **SF1** — subscription live), Bedrock (`AWS_BEARER_TOKEN_BEDROCK`) | **PASS** |
| FRED | Was rejected (key saved with a leading space → 33 chars vs 32). **Fix `#175`** whitespace-strips all data keys so padded secrets never silently fail. |
| `DATA_GOV_API_KEY` | Uploaded to Secrets; injected into **new** agent VMs only, so not testable in the session it was added. To be wired (Treasury / EIA / FDIC / Census) and verified next session. |

## 3. THESIS OF RECORD — AI Sales Agent team (Tier 1 & Tier 2)

**Proposal (Founder):** build a sales team of AI agents that hold professional conversations with qualified leads —
via chat or virtual/voice — to understand needs and pain points and guide the prospect to select **Tier 1 or Tier 2**
and pay the **upfront subscription** for their organization.

**Key design decision (Founder, de-risking):** the AI agent **does not take payment or PII over the
call/chat**. It **walks the prospect through the platform's own checkout module**, where the customer **enters their
own data and payment** on Aegira's PCI-compliant, self-serve checkout. The agent is a **concierge to the door** —
the customer completes the transaction on-platform.

**Board assessment (VP Engineering):**

- **Realistic and provable end-to-end.** The self-serve-checkout mechanic removes PII/PCI handling by the agent,
  eliminates chargeback-by-proxy risk, and works identically for chat or AI voice.
- **Reuses existing infrastructure:** the fact-locked Bedrock/Anthropic layer (`editorial_llm`), the top-20
  pain-point/differentiation corpus (`#171`), and the pricing schema — so a **grounded (RAG), guardrailed** sales
  agent is largely assembly, not greenfield.
- **Permanent guardrail that remains = what the agent *says*:** strict grounding to our own corpus, an
  investment-advice / unsubstantiated-claim blocklist, and mandatory disclaimers (same discipline as the numeric
  fact-lock in editorial). Tier recommendation is a **deterministic rules engine**; the LLM *explains* the pick, it
  does not *invent* it.
- **Open compliance item (not a blocker):** **consent-to-contact (TCPA)** governs *unsolicited outbound* regardless
  of PII — so outbound is **opt-in / warm leads only**; inbound is clean. If AI voice is used, **disclose it is an AI
  assistant** (one line; builds trust).
- **Dependency:** live self-serve close needs **Stripe** (Purchase Flow Phase B — keys pending).

**Provability plan (thesis → proven):**

1. **Crawl** — inbound, grounded, guardrailed **chat qualifier**: discovery → pain points → Tier 1/2 recommendation
   → hand-off to on-platform checkout. Advance only if the **hallucination/compliance-flag rate is ~zero**.
2. **Walk** — add nurture sequences + lead scoring + CRM; let it complete **self-serve** checkouts (customer enters
   own data). Measure **conversion lift vs. control**.
3. **Run** — Tier 1 / org: agent does full qualification + proposal prep; expand outbound to **opt-in** only.

**Board action:** **Thesis adopted of record.** Detailed build (`docs/AI_SALES_AGENT_CONSTRUCT.md`) to be authored when
sequenced against current platform priorities. Not started this session by Founder direction ("update board of minutes
with this thesis for now").

## 4. Founder-side open items

- Merge **`#175`** → FRED fully live.
- Provide **Stripe** keys → unlocks Purchase Flow Phase B (and the AI Sales Agent self-serve close).
- Host + credentials decision → **permanent always-on deployment** (the durable fix for sandbox "changes not showing";
  local Docker requires `git pull` before rebuild — ZIP snapshots are stale by design).

## 5. Next

Founder signaled additional platform issues across several subject matters to be addressed in subsequent working
sessions. This thesis is parked as adopted-of-record pending sequencing.

---

*Recorded by Cy Henry, VP Software Engineering (AI). JHI-SIG: 69M2705M. TeamWork makes the DreamWork.*
