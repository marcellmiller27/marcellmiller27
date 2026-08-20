# JHI-SIG: 69M2705M | US government economic data adapter (api.data.gov) | JHI Research & Analytics Firm, Inc. (proprietary)
from datetime import datetime

from pydantic import BaseModel


class GovIndicator(BaseModel):
    """One normalized government-data value, threaded with its as-of provenance.

    The core fields (``key``/``label``/``value``/``unit``/``period``/``status``/``note``)
    are shape-compatible with the Economics module's ``MacroPoint`` so the same
    front-end panel renders these feeds unchanged. The Data-Foundation as-of doctrine
    (``cadence``/``as_of_label``/``freshness``) rides alongside for honest labeling.
    """

    key: str
    label: str
    value: float | None = None
    unit: str = ""
    period: str | None = None  # actual data date/period the value belongs to
    # "ok" | "unavailable" | "requires_credentials" | "pending"
    status: str = "ok"
    note: str | None = None
    # Data Foundation as-of doctrine (Phase 1).
    cadence: str | None = None            # daily/weekly/monthly/quarterly/annual/irregular
    as_of_label: str | None = None        # e.g. "Daily · as of Aug 18, 2026"
    freshness: str | None = None          # current / overdue / fetch-failed


class GovSeriesResponse(BaseModel):
    source: str
    provider: str  # provider key surfaced in /market/providers (e.g. "eia")
    as_of: datetime
    requires_key: bool = False
    # "live" (keyed + working / keyless) | "requires_credentials" (key missing)
    key_status: str = "live"
    indicators: list[GovIndicator]
