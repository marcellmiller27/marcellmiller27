# JHI-SIG: 69M2705M | Valuations | John Henry Investments (proprietary)
"""Modeled real-time valuations for private / illiquid asset classes.

OBJECTIVE: close the "not-yet-real-time" gap for classes that have no live market
quote (direct real estate, private businesses/SMB, private equity) by computing a
**modeled estimate** at request time from LIVE public inputs. These are explicitly
labeled ``modeled_estimate`` (not market quotes) and update whenever the underlying
live inputs (rates, sector proxies) move.

Models (transparent, documented):
  - Real estate: income approach. value = NOI / cap_rate, where
    cap_rate = live 10Y Treasury yield + risk spread. Rises/falls in real time with
    rates, like real cap rates.
  - Private business / SMB: market approach. EV = EBITDA * multiple, where
    multiple = public small-cap base multiple * (1 - illiquidity discount), tilted by
    the live small-cap proxy's daily move (sentiment).
  - Private equity: proxy-NAV approach. mark = committed capital adjusted by the live
    listed-PE proxy's daily move.

Live inputs come from the same MarketDataService used everywhere else, so estimates
stay consistent with the rest of the platform.
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.market_services import MarketDataService
from app.valuation_models import ValuationEstimate, ValuationReport

DISCLAIMER = (
    "Modeled estimates only — derived from live public inputs, NOT market quotes or "
    "appraisals. For illiquid/private assets these are directional and must be "
    "confirmed by a professional valuation."
)

# Documented assumptions.
RE_RISK_SPREAD_PCT = 2.5      # cap-rate spread over the 10Y, in percentage points
SMB_BASE_MULTIPLE = 8.0       # public small-cap-style EV/EBITDA
SMB_ILLIQUIDITY_DISCOUNT = 0.30
SENTIMENT_SENSITIVITY = 0.5   # how much a live proxy's % move tilts the estimate


def _now() -> datetime:
    return datetime.now(timezone.utc)


class ValuationService:
    def __init__(self, market: MarketDataService | None = None) -> None:
        self.market = market or MarketDataService()

    def _live(self, symbols: list[str]) -> dict[str, dict[str, float | None]]:
        quotes = self.market.quotes(symbols).quotes
        return {
            q.symbol: {"price": q.price, "change_percent": q.change_percent}
            for q in quotes
            if q.status == "ok"
        }

    def estimate(
        self,
        noi: float = 100_000.0,
        ebitda: float = 1_000_000.0,
        pe_committed: float = 1_000_000.0,
    ) -> ValuationReport:
        live = self._live(["UST10Y", "SMB_PROXY", "PE_PROXY"])
        estimates: list[ValuationEstimate] = []

        # 1) Direct real estate — income approach, cap rate driven by live 10Y.
        ust10y = (live.get("UST10Y") or {}).get("price")
        if ust10y is not None:
            cap_rate = (ust10y + RE_RISK_SPREAD_PCT) / 100.0
            value = noi / cap_rate if cap_rate > 0 else None
            estimates.append(
                ValuationEstimate(
                    asset_class="Direct real estate (per-property)",
                    method="Income approach: value = NOI / cap_rate",
                    estimated_value=round(value, 2) if value is not None else None,
                    unit="USD",
                    live_inputs={"ust10y_pct": ust10y},
                    assumptions={"noi": noi, "risk_spread_pct": RE_RISK_SPREAD_PCT,
                                 "cap_rate": round(cap_rate, 4)},
                    note="Cap rate moves in real time with the 10Y Treasury yield.",
                )
            )
        else:
            estimates.append(self._unavailable("Direct real estate (per-property)", noi))

        # 2) Private business / SMB — market approach tilted by live small-cap proxy.
        smb_change = (live.get("SMB_PROXY") or {}).get("change_percent") or 0.0
        sentiment = 1.0 + (smb_change / 100.0) * SENTIMENT_SENSITIVITY
        multiple = SMB_BASE_MULTIPLE * (1 - SMB_ILLIQUIDITY_DISCOUNT) * sentiment
        estimates.append(
            ValuationEstimate(
                asset_class="Private business / SMB",
                method="Market approach: EV = EBITDA * private multiple",
                estimated_value=round(ebitda * multiple, 2),
                unit="USD",
                live_inputs={"smb_proxy_change_pct": smb_change},
                assumptions={"ebitda": ebitda, "base_multiple": SMB_BASE_MULTIPLE,
                             "illiquidity_discount": SMB_ILLIQUIDITY_DISCOUNT,
                             "applied_multiple": round(multiple, 2)},
                note="Multiple = public small-cap base, illiquidity-discounted, tilted by live SMB proxy.",
            )
        )

        # 3) Private equity — proxy-NAV mark from live listed-PE proxy move.
        pe_change = (live.get("PE_PROXY") or {}).get("change_percent") or 0.0
        mark = pe_committed * (1 + pe_change / 100.0)
        estimates.append(
            ValuationEstimate(
                asset_class="Private equity holdings",
                method="Proxy-NAV: mark = committed * (1 + listed-PE proxy move)",
                estimated_value=round(mark, 2),
                unit="USD",
                live_inputs={"pe_proxy_change_pct": pe_change},
                assumptions={"committed_capital": pe_committed},
                note="Interim mark proxy between true GP statement marks.",
            )
        )

        return ValuationReport(as_of=_now(), disclaimer=DISCLAIMER, estimates=estimates)

    @staticmethod
    def _unavailable(asset_class: str, noi: float) -> ValuationEstimate:
        return ValuationEstimate(
            asset_class=asset_class,
            method="Income approach: value = NOI / cap_rate",
            estimated_value=None,
            unit="USD",
            live_inputs={},
            assumptions={"noi": noi},
            status="unavailable",
            note="Live rate input unavailable; estimate cannot be computed right now.",
        )
