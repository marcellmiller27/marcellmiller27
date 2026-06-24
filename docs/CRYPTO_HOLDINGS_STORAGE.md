# Crypto Holdings Storage — Design & Security Advice

## Short answer to "store users' crypto wallet keys?"

**Do not store users' private keys or seed phrases in the application database.**
Holding private keys makes John Henry Investments a *custodial* service, which is
one of the highest‑risk things a fintech can do:

- **Catastrophic, irreversible breach impact.** A single database compromise (or a
  malicious insider, leaked backup, or logging mistake) means attackers can drain
  every user's funds. There is no chargeback or reversal on-chain.
- **Regulatory / licensing exposure.** Custody of customer crypto typically triggers
  money‑transmitter and custody regimes (e.g., US state MTLs / NYDFS BitLicense,
  EU MiCA CASP authorization) plus AML/KYC, audits, and capital requirements.
- **Operational burden.** Real custody requires HSMs or MPC, cold storage, key
  ceremonies, withdrawal controls, SOC 2, insurance, and 24/7 security operations —
  not an app table.

This platform's purpose is **investment intelligence and portfolio tracking**, which
does not require custody at all. So the implemented design is **non‑custodial,
watch‑only**.

## What we built instead (recommended design)

Store only **public, watch‑only** data: networks, asset symbols, optional public
addresses, quantities, and labels. The schema has **no column for a private key or
seed phrase**, and the API actively **rejects** anything that looks like a secret.

### Data model — `crypto_holdings` (`backend/app/db_models.py`)

| Column | Notes |
| --- | --- |
| `user_id` / `organization_id` | Owner scope; queries are filtered per authenticated user. |
| `network` | `bitcoin`, `ethereum`, `xrpl`, `stellar`, `solana`, `other`. |
| `asset_symbol` | `BTC`, `ETH`, `XRP`, `XLM`, tokens, … |
| `address` | **Public** receive address (optional). Never a private key. |
| `quantity` | Decimal stored as string (no float drift). |
| `label`, `notes` | User annotations. |
| `custody_model` | Always `non_custodial_watch_only`. |

### API (`/api/v1/crypto`, `backend/app/routers/crypto.py`)

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/crypto/networks` | Supported networks/assets + non‑custodial notice (public). |
| `POST` | `/crypto/holdings` | Add a watch‑only holding (validates address, rejects secrets). |
| `GET` | `/crypto/holdings` | List the authenticated user's holdings. |
| `GET` | `/crypto/holdings/summary` | Totals by asset + network/holding counts. |
| `DELETE` | `/crypto/holdings/{id}` | Remove a holding. |

### Guardrails (`backend/app/crypto_services.py`)

- **Secret detection** rejects (HTTP 422) inputs in any field that match a private
  key or seed: 32‑byte hex, Bitcoin WIF, Stellar `S…` secret keys, XRP `s…` seeds,
  extended private keys (`xprv`/`yprv`/`zprv`), and 12–24‑word BIP‑39 mnemonics.
- **Public address format validation** per network (HTTP 400 on mismatch).
- **Per‑user scoping** so one user can never read another's holdings.

## If true custody is ever required

Only pursue this with explicit product/legal intent, and even then **never** store
raw keys in the app database. Use one of:

- A regulated **custody provider** (Fireblocks, BitGo, Coinbase Custody, Anchorage).
- **MPC / threshold signatures** so no single system ever holds a complete key.
- **HSM‑backed** keys with envelope encryption via a managed KMS, strict withdrawal
  policies, and independent security audits — plus the relevant licenses, AML/KYC,
  and insurance.

To enrich the watch‑only experience without custody, balances/prices can be read
from public blockchain explorers / market data APIs keyed off the stored public
addresses (read‑only), keeping the platform free of any fund‑moving credentials.
