import re
from decimal import Decimal, InvalidOperation

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crypto_models import (
    CryptoHoldingCreate,
    CryptoHoldingRead,
    CryptoHoldingsSummary,
    NetworksResponse,
    SupportedNetwork,
    WATCH_ONLY_NOTICE,
)
from app.db_models import CryptoHoldingDB
from app.foundation_models import Principal

CUSTODY_MODEL = "non_custodial_watch_only"

# Supported networks with a light public-address format check and common assets.
SUPPORTED_NETWORKS: dict[str, dict] = {
    "bitcoin": {
        "label": "Bitcoin",
        "assets": ["BTC"],
        "address": re.compile(r"^(bc1[0-9a-z]{11,87}|[13][a-km-zA-HJ-NP-Z1-9]{25,39})$"),
    },
    "ethereum": {
        "label": "Ethereum / EVM",
        "assets": ["ETH", "USDC", "USDT", "DAI", "WBTC"],
        "address": re.compile(r"^0x[0-9a-fA-F]{40}$"),
    },
    "xrpl": {
        "label": "XRP Ledger",
        "assets": ["XRP"],
        "address": re.compile(r"^r[1-9A-HJ-NP-Za-km-z]{24,34}$"),
    },
    "stellar": {
        "label": "Stellar",
        "assets": ["XLM"],
        "address": re.compile(r"^G[A-Z2-7]{55}$"),
    },
    "solana": {
        "label": "Solana",
        "assets": ["SOL"],
        "address": re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$"),
    },
    "other": {
        "label": "Other / manual",
        "assets": [],
        "address": None,
    },
}

# Patterns that indicate a SECRET was submitted. These are rejected outright so a
# private key or seed phrase can never be persisted.
_SECRET_PATTERNS = [
    re.compile(r"^(0x)?[0-9a-fA-F]{64}$"),          # 32-byte hex private key / raw seed
    re.compile(r"^[5KL][1-9A-HJ-NP-Za-km-z]{50,51}$"),  # Bitcoin WIF private key
    re.compile(r"^S[A-Z2-7]{55}$"),                 # Stellar secret key (starts with S)
    re.compile(r"^s[1-9A-HJ-NP-Za-km-z]{25,35}$"),  # XRP family secret seed (starts with s)
    re.compile(r"^(xprv|yprv|zprv)[1-9A-HJ-NP-Za-km-z]{50,}$"),  # extended PRIVATE key
]
_MNEMONIC_WORD_COUNTS = {12, 15, 18, 21, 24}


class CryptoSecretRejected(ValueError):
    """Raised when a submitted value looks like a private key or seed phrase."""


def looks_like_secret(value: str) -> bool:
    candidate = value.strip()
    if not candidate:
        return False
    if any(pattern.match(candidate) for pattern in _SECRET_PATTERNS):
        return True
    words = candidate.split()
    if len(words) in _MNEMONIC_WORD_COUNTS and all(
        re.fullmatch(r"[a-zA-Z]{3,8}", word) for word in words
    ):
        return True
    return False


class CryptoService:
    """Watch-only crypto holdings. Stores public data only — never secrets."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def networks(self) -> NetworksResponse:
        return NetworksResponse(
            custody_model=CUSTODY_MODEL,
            notice=WATCH_ONLY_NOTICE,
            networks=[
                SupportedNetwork(key=key, label=meta["label"], assets=meta["assets"])
                for key, meta in SUPPORTED_NETWORKS.items()
            ],
        )

    def add_holding(self, principal: Principal, payload: CryptoHoldingCreate) -> CryptoHoldingRead:
        network = payload.network.strip().lower()
        if network not in SUPPORTED_NETWORKS:
            raise ValueError(f"Unsupported network '{payload.network}'.")

        asset_symbol = payload.asset_symbol.strip().upper()
        if not re.fullmatch(r"[A-Z0-9]{2,12}", asset_symbol):
            raise ValueError("asset_symbol must be 2-12 uppercase letters/digits (for example BTC).")

        # Reject anything that resembles a secret in ANY user-supplied field.
        for field_value in (payload.address, payload.label, payload.notes):
            if field_value and looks_like_secret(field_value):
                raise CryptoSecretRejected(
                    "It looks like you submitted a private key or seed phrase. For your "
                    "security this platform is non-custodial and only stores public, "
                    "watch-only data — never private keys or seed phrases."
                )

        address = payload.address.strip() if payload.address else None
        if address:
            pattern = SUPPORTED_NETWORKS[network]["address"]
            if pattern is not None and not pattern.match(address):
                raise ValueError(
                    f"'{address}' is not a valid public {SUPPORTED_NETWORKS[network]['label']} "
                    "address."
                )

        quantity = self._normalize_quantity(payload.quantity)

        holding = CryptoHoldingDB(
            user_id=principal.user_id,
            organization_id=principal.organization_id,
            network=network,
            asset_symbol=asset_symbol,
            address=address,
            quantity=quantity,
            label=payload.label.strip()[:120],
            notes=(payload.notes.strip() if payload.notes else None),
            custody_model=CUSTODY_MODEL,
        )
        self.db.add(holding)
        self.db.commit()
        self.db.refresh(holding)
        return self._read(holding)

    def list_holdings(self, principal: Principal) -> list[CryptoHoldingRead]:
        holdings = self.db.scalars(
            select(CryptoHoldingDB)
            .where(CryptoHoldingDB.user_id == principal.user_id)
            .order_by(CryptoHoldingDB.created_at.desc())
        ).all()
        return [self._read(holding) for holding in holdings]

    def delete_holding(self, principal: Principal, holding_id: str) -> None:
        holding = self.db.scalar(
            select(CryptoHoldingDB).where(
                CryptoHoldingDB.id == holding_id,
                CryptoHoldingDB.user_id == principal.user_id,
            )
        )
        if holding is None:
            raise LookupError("Holding not found.")
        self.db.delete(holding)
        self.db.commit()

    def summary(self, principal: Principal) -> CryptoHoldingsSummary:
        holdings = self.db.scalars(
            select(CryptoHoldingDB).where(CryptoHoldingDB.user_id == principal.user_id)
        ).all()
        by_asset: dict[str, Decimal] = {}
        networks: set[str] = set()
        for holding in holdings:
            networks.add(holding.network)
            by_asset[holding.asset_symbol] = by_asset.get(holding.asset_symbol, Decimal("0")) + (
                Decimal(holding.quantity or "0")
            )
        return CryptoHoldingsSummary(
            custody_model=CUSTODY_MODEL,
            total_holdings=len(holdings),
            networks=len(networks),
            by_asset={asset: format(value.normalize(), "f") for asset, value in by_asset.items()},
        )

    @staticmethod
    def _normalize_quantity(raw: str) -> str:
        try:
            value = Decimal(str(raw).strip() or "0")
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("quantity must be a number.") from exc
        if value < 0:
            raise ValueError("quantity cannot be negative.")
        return format(value.normalize(), "f")

    @staticmethod
    def _read(holding: CryptoHoldingDB) -> CryptoHoldingRead:
        return CryptoHoldingRead(
            id=holding.id,
            network=holding.network,
            asset_symbol=holding.asset_symbol,
            address=holding.address,
            quantity=holding.quantity,
            label=holding.label,
            notes=holding.notes,
            custody_model=holding.custody_model,
            created_at=holding.created_at,
            updated_at=holding.updated_at,
        )
