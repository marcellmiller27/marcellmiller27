# E2 — Qualified Third-Party Shortlist (Grounded-LLM Editorial Layer)

**Owner:** Cy Henry (VP Software Engineering — AI) · **Signature:** `69M2705M`
**Purpose:** A vetted shortlist of third parties to **review and engage under contract** for **E2** —
the grounded, fact-locked LLM drafting layer that elevates the editorial voice (Ellery Vance) while
the deterministic engine remains the fact backbone. Pairs with `docs/EDITORIAL_PROGRAM_ASSESSMENT.md`
and `docs/EDITORIAL_STYLE_GUIDE.md`.

> Founder decision needed to start E2: pick a provider, set a **monthly token budget**, add the
> **API key** to Secrets. Everything below is capability-level guidance for procurement — confirm
> current terms/pricing directly with each vendor at contract time.

## 1. Non-negotiable selection criteria (our bar)
1. **No training on our data** — contractual guarantee the provider won't train on our prompts/outputs (protects our methodology + NASDAQ-licensed-derived content).
2. **Enterprise data protection** — signed **DPA**, **SOC 2 Type II** (and ideally ISO 27001), data-residency options, encryption in transit/at rest.
3. **Data isolation** — no licensed-data spillage; ability to keep inference within our cloud account/VPC where possible.
4. **Groundable** — supports retrieval/tool use so the model writes **only** from our engine's figures (fact-lock), with low hallucination on flagship models.
5. **Reliability & scale** — SLA/uptime, rate limits that fit a scheduled newsletter cadence.
6. **Commercial fit** — usage-based pricing, no lock-in, portability (so we can switch models).

## 2. Primary shortlist — foundation-model / LLM API providers
| # | Vendor | What we'd use | Why qualified | Contract / compliance notes |
|---|---|---|---|---|
| 1 | **Microsoft Azure OpenAI Service** | GPT-family (flagship + mini) via Azure | Enterprise wrapper around OpenAI models; **data not used to train**; DPA/SOC2; VNet/private endpoints; content filters | Strong default for regulated use; keep inference in our Azure tenant |
| 2 | **Anthropic (Claude)** — direct or via **AWS Bedrock** / **GCP Vertex** | Claude flagship for institutional long-form drafting | Strong instruction-following + low hallucination; **no-train** commercial terms; available inside Bedrock/Vertex (data stays in our cloud account) | Bedrock/Vertex path gives cloud-native DPA + isolation |
| 3 | **AWS Bedrock** (multi-model) | Anthropic/Meta/Mistral/Amazon models behind one API, **in our AWS account** | Model-portability + data stays in-account; IAM/VPC controls; single procurement | Best if we standardize on AWS; avoids per-vendor contracts |
| 4 | **Google Cloud Vertex AI (Gemini)** | Gemini flagship + grounding tools | Enterprise DPA/SOC2; native grounding/retrieval; data-governance controls | Good if we lean GCP; strong grounding tooling |
| 5 | **OpenAI (direct, Enterprise/API)** | GPT-family | Frontier quality; **Business/Enterprise terms = no training on data**; DPA available | Viable direct; Azure path preferred for stricter isolation |

## 3. Alternatives / specialists (evaluate if the above don't fit)
| Vendor | Niche | When to consider |
|---|---|---|
| **Cohere** | Enterprise RAG + private/VPC deployment | Data-sovereignty priority; retrieval-first product |
| **Mistral AI** | Strong open/enterprise models; EU-based, deployable | EU data-residency; self-host/portability |
| **Meta Llama (self-hosted)** | Open-weight, run in our own infra | Maximum control / zero data egress; we own the ops burden |
| **Databricks (Mosaic AI)** | Governed model serving on our data platform | If our data stack consolidates on Databricks |

## 4. Supporting tooling (usually contracted alongside the model)
- **Guardrails / safety:** Guardrails AI or NVIDIA NeMo Guardrails — enforce fact-lock, "not advice" filter, PII/spillage checks.
- **Orchestration / RAG:** LangChain/LlamaIndex (libraries) for retrieval over our engine's outputs.
- **Observability / eval:** LangSmith, Arize Phoenix, or Weights & Biases — track hallucination, latency, cost, and drift (feeds E4 learning).
- **E-sign / procurement:** standard MSA + DPA execution (legal).

## 5. Recommendation (ranked — and a clarification)
**Important:** these are **not three like-for-like competitors.** **Claude is a model; Bedrock and
Azure are platforms that host models.** Claude runs *on* AWS Bedrock (and GCP Vertex); Azure hosts
OpenAI's **GPT** (not Claude). So the recommendation is a **model + platform pairing**, ranked:

1. **AWS Bedrock hosting Anthropic Claude** *(platform + model together)* — **top pick.** Claude's institutional long-form quality and low hallucination, delivered inside **our AWS account** (data-in-account, no-train, IAM/VPC isolation) under **one contract**, with model portability (swap models without re-integrating).
2. **Anthropic Claude — direct** *(or via GCP Vertex)* — same model, direct enterprise contract. Choose if we're **not** standardizing on AWS.
3. **Azure OpenAI (GPT family)** — the **alternative**, best if we're a Microsoft/Azure shop. Note: Azure = GPT, **not** Claude.

*(So to answer directly: it's not "1) Bedrock 2) Claude 3) Azure" as separate items — #1 is **Bedrock + Claude paired**; #2 is Claude direct; #3 is Azure/GPT as the alternative.)*

- **Guardrails from day one:** the LLM only rephrases figures our deterministic engine produces (fact-lock). Never let it source numbers.
- **Run a 2–3 vendor bake-off** on the same editions before signing: score on voice quality, factual fidelity (zero invented figures), latency, cost/edition, and contract terms.

## 6. Procurement checklist (to execute a contract)
- [ ] Confirm **no-training** clause + **DPA** + **SOC 2 Type II** (request report).
- [ ] Confirm data-residency / in-account inference option.
- [ ] Pilot key + **monthly budget cap**; measure cost per edition.
- [ ] Bake-off scoring (voice, fidelity, latency, cost) → select.
- [ ] Legal: MSA + DPA; add API key to Secrets; wire behind our guardrails + editor approval (E3).

## 7. Model evaluation (OPEN — 2026-07-23) — decision NOT closed
The Founder created an **AWS account**, so all candidates are available on **AWS Bedrock** under one
account — ideal for a head-to-head bake-off before committing. **This decision is open; still under
discussion.** Candidates on the table:

| Candidate (on Bedrock) | Profile | Fit for institutional editorial |
|---|---|---|
| **Anthropic Claude Sonnet 5** | Balanced flagship; strong long-form, low hallucination | **Top** for nuanced institutional prose |
| **Amazon Nova Premier** | Amazon's flagship; strong price/performance, native to Bedrock | Cost-efficient; solid general drafting |
| **Meta Llama 3.1 70B Instruct** | Open-weight; lowest cost; self-hostable later | Cost/control; may need more prompt tuning for voice |

**Which Claude on Bedrock:** the **Sonnet** tier (Sonnet 5) is the right balance of quality/cost;
**Opus** if we want maximum quality on flagship editions; **Haiku** for cheap, high-volume runs.

**Recommendation:** don't pick blind — run the **bake-off across all three on Bedrock** (same editions;
score voice, factual fidelity [zero invented figures], latency, cost/edition), then lock the model. All
paths keep the **fact-lock guardrail** (the model only rephrases engine-produced figures) and the E1 house style.

### To run the bake-off (Founder actions — when the discussion closes)
1. Enable **Bedrock model access** for the candidates in the AWS console (Claude Sonnet 5, Nova Premier, Llama 3.1 70B).
2. Add AWS credentials to Secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` (a Bedrock-enabled region).
3. Confirm a monthly budget cap.

### What Cy builds once unblocked
- A backend drafting service (behind `ENABLE_LLM_EDITORIAL`, **off by default**): engine facts → chosen Bedrock model in the E1 house style → output **validated to contain no new/changed numbers** → deterministic fallback on any guardrail failure.
- A **bake-off harness** comparing the candidates (+ the deterministic baseline) on the same editions.

---
*Next step:* Founder closes the model discussion (or authorizes the bake-off) → enable Bedrock access + add AWS creds → Cy runs the bake-off and wires the fact-locked E2 layer.
