<!-- JHI-SIG: 69M2705M | Newsletter Editorial RAG activation runbook | JHI Research & Analytics Firm, Inc. (proprietary) -->

# Newsletter Editorial RAG — Activation Runbook

**Status: scaffolding merged, dormant.** The retrieval layer (`backend/app/editorial_rag.py`)
is flag-gated and a **graceful no-op** until the AWS resources below exist and the flags are
set. Merging it changes nothing in production: with the flags off, the newsletter behaves
exactly as before (deterministic build, optional E2 prose elevation).

This runbook explains how to stand up the corpus, the Amazon Bedrock Knowledge Base, IAM, and
the environment flags that switch it on.

---

## What it does when activated

When `ENABLE_EDITORIAL_RAG=1` **and** a `BEDROCK_KB_ID` is configured, `elevate_edition`
retrieves the most relevant historical/context passages from the Knowledge Base (semantic
search over a vector index) and injects them into Ellery's prompt as **read-only grounding
context**. The passages ground the *reasoning and narrative continuity* of the research-essay
and are surfaced to the reader **as citations** (via the `citations` field on the newsletter
content API response).

**Fact-lock is preserved end to end.** Retrieved passages are never a source of figures:
the deterministic engine remains the sole source of every number, and
`editorial_llm._apply` still reverts any rephrased field that introduces a number outside the
engine's whitelist. RAG can only make the prose better-reasoned; it cannot inject data.

Governance: the corpus is *our own* historical macro/markets research and public-domain
material — **never** raw licensed SF1 rows. Only derived/published research goes into S3.

---

## Prerequisites

- An AWS account with Amazon Bedrock enabled in your region (e.g. `us-east-1`), including
  model access for an embeddings model (e.g. Amazon Titan Text Embeddings v2) — request access
  in the Bedrock console under *Model access*.
- A vector store for the Knowledge Base. The lowest-friction option is **Amazon OpenSearch
  Serverless** (Bedrock can create the collection for you during KB setup). Alternatives:
  Aurora PostgreSQL + pgvector, Pinecone, Redis Enterprise.
- The `boto3` dependency (already declared in `backend/pyproject.toml`).

---

## Step 1 — Build the S3 corpus

1. Create a private bucket, e.g. `s3://aegira-editorial-research/`.
2. Upload our historical research as text-extractable documents (`.md`, `.txt`, `.pdf`,
   `.html`, `.docx`). Suggested structure:
   ```
   s3://aegira-editorial-research/
     macro/            # regime notes, rate-cycle history, inflation episodes
     markets/          # cross-asset context, factor-research write-ups (derived only)
     methodology/      # our published, pre-registered methodology notes
   ```
3. **Do not** upload licensed vendor rows (Sharadar/Nasdaq Data Link raw data) or anything
   under `backend/.sf1_cache/`. Only derived, publishable research belongs here.
4. Keep documents reasonably chunk-friendly (clear headings, self-contained paragraphs).

## Step 2 — Create the Bedrock Knowledge Base

Console path: **Bedrock → Knowledge bases → Create knowledge base**.

1. **Data source:** the S3 bucket/prefix from Step 1.
2. **Embeddings model:** Titan Text Embeddings v2 (or your approved model).
3. **Vector store:** *Quick create* an OpenSearch Serverless collection (or point at your own).
4. **Chunking:** default (or fixed-size ~300 tokens with 20% overlap) is a good start.
5. Create, then **Sync** the data source so documents are embedded and indexed.
6. Copy the **Knowledge base ID** (looks like `XXXXXXXXXX`) → this is `BEDROCK_KB_ID`.

CLI sketch (optional, once the vector store exists):
```bash
aws bedrock-agent create-knowledge-base --name aegira-editorial-kb ... --region us-east-1
aws bedrock-agent create-data-source --knowledge-base-id "$KB_ID" --name s3-corpus \
  --data-source-configuration '{"type":"S3","s3Configuration":{"bucketArn":"arn:aws:s3:::aegira-editorial-research"}}'
aws bedrock-agent start-ingestion-job --knowledge-base-id "$KB_ID" --data-source-id "$DS_ID"
```

## Step 3 — IAM

The **Knowledge Base service role** (created/used during KB setup) needs:
- `s3:GetObject`, `s3:ListBucket` on the corpus bucket.
- `bedrock:InvokeModel` on the embeddings model.
- The vector-store data-plane permissions (e.g. `aoss:APIAccessAll` for OpenSearch
  Serverless, scoped to the collection).

The **application principal** (the backend's role/user, or the credentials `boto3` resolves at
runtime) needs only retrieval:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["bedrock:Retrieve"],
      "Resource": "arn:aws:bedrock:us-east-1:<ACCOUNT_ID>:knowledge-base/<KB_ID>"
    }
  ]
}
```
Provide credentials the standard boto3 way (an IAM role on the compute, or
`AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` in the environment).

## Step 4 — Set the flags

Set these on the backend (Cursor Secrets / container env):

| Variable | Purpose | Example |
| --- | --- | --- |
| `ENABLE_EDITORIAL_RAG` | Master switch for RAG grounding | `1` |
| `BEDROCK_KB_ID` | The Knowledge Base ID from Step 2 | `XXXXXXXXXX` |
| `BEDROCK_KB_REGION` | KB region (falls back to `AWS_REGION`) | `us-east-1` |
| `EDITORIAL_RAG_TOP_K` | Passages to retrieve (default 4) | `4` |
| `ENABLE_LLM_EDITORIAL` | E2 must also be on for grounding to reach the LLM | `1` |

> RAG grounding only affects the LLM path. If `ENABLE_LLM_EDITORIAL` is off, the deterministic
> edition is returned unchanged (RAG is skipped).

## Step 5 — Verify

1. `docker exec <backend> printenv BEDROCK_KB_ID` → non-empty.
2. Call the content API for an edition and inspect the response `citations` array:
   ```bash
   curl -s localhost:8000/api/v1/newsletters/insider-briefs -H "Authorization: Bearer <token>" \
     | python -c "import sys,json;d=json.load(sys.stdin);print(len(d['citations']),'citations')"
   ```
   A non-empty `citations` list (with `source` S3 URIs) confirms retrieval is live.
3. Confirm fact-lock still holds: numbers on screen match the deterministic engine; no figure
   originates from a retrieved passage.

---

## Rollback

Set `ENABLE_EDITORIAL_RAG=0` (or unset `BEDROCK_KB_ID`). Retrieval returns `[]`, `citations`
is empty, and the editorial path reverts to E2/deterministic — no redeploy required.

## Cost & operational notes

- Retrieval cost = embeddings query + vector-store reads per edition build; editions are built
  on request and (for the heavy screen) cached, so volume is modest. Re-sync the data source
  when the corpus changes.
- A retrieval failure (throttling, permissions, outage) is swallowed: the edition still renders
  via E2/deterministic. Watch backend logs for `editorial_rag: retrieval unavailable`.
- Frontend rendering of the `citations` array (a "Sources & context" block under the edition)
  is a small, additive follow-up; the API already returns the data.
