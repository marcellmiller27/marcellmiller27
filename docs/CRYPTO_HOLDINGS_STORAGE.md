# Decision Record — Crypto wallets / holdings storage

**Status:** Decided — **the platform does not hold crypto wallets and does not
store wallet data.** Prior watch-only holdings code was removed.

## Question

Should John Henry Investments hold users' crypto wallets (private keys), or store
crypto wallet data (e.g., public addresses) for holdings tracking?

## Decision

1. **Custodial wallets (private keys / seed phrases): NO — never.** Holding keys
   makes the platform custodial, with catastrophic, irreversible breach impact and
   heavy licensing/AML obligations (MTL / BitLicense / MiCA), HSM/MPC, cold
   storage, SOC 2, and insurance requirements. This is out of scope for an
   investment-intelligence product and was never implemented.

2. **Non-custodial, watch-only address storage: removed.** A watch-only store
   (public addresses + quantities, with guardrails rejecting private keys/seed
   phrases) was prototyped, but is **not retained**. Rationale:
   - It is **not core** to the platform's intelligence/scoring thesis.
   - Persisting users' public wallet addresses is an unnecessary
     privacy/clustering and data-protection surface (addresses are linkable and
     de-anonymizable on-chain).
   - It blurs positioning — the platform is decision intelligence, **not a wallet**.
   - The same user value can be delivered later without storing any wallet data.

## Consequence

- No `crypto_holdings` table, no `/api/v1/crypto/*` endpoints, no wallet/key/address
  persistence anywhere in the codebase.
- The platform remains strictly **non-custodial**: it never holds, stores, or can
  move funds or fund-moving credentials.

## If crypto exposure is wanted later (safe path)

Represent crypto as **read-only portfolio analytics** without persisting wallet
data: let a user enter a quantity/allocation, or pull balances on demand from a
public block explorer the user points at, and price them via a market-data API.
Store positions/quantities — never private keys, and avoid persisting addresses
unless there is a clear, consented product reason and a privacy review. If true
custody is ever required, integrate a regulated custody/MPC provider (Fireblocks,
BitGo, Coinbase Custody, Anchorage) rather than a database of keys.

> The previously prototyped watch-only implementation is preserved in version
> control history and can be restored if a future decision reverses this one.
