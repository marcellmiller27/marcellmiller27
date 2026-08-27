# JHI-SIG: 69M2705M | SectorProfile registry | JHI Research & Analytics Firm, Inc. (proprietary)
"""Aegira SectorProfile registry — the sector-aware baseline that grounds every
ratio-dashboard status flag and driver note.

A universal threshold (e.g. "current ratio > 2 is healthy") is misleading across
sectors: banks intentionally carry high leverage, energy companies intentionally
carry high CapEx, tech companies intentionally carry high SG&A / low tangible
assets. This module encodes the sector-specific thresholds, relevant-KPI list,
and non-applicable ratios so the unified dashboard sheet (see
`backend/app/ratio_dashboard.py`) reports status honestly instead of mechanically.

Doctrine (BOARD_MINUTES_2026-08-26.md §9.4 + §11.2):
  - "Universal thresholds" are non-negotiable-ly wrong.  Compare to peers +
    prior periods.
  - Every ratio row on the dashboard carries a `sector_relevant` bit; ratios
    marked non-relevant render as `N/M — sector` (not applicable to sector),
    not as green/red or 0.

Coverage in this baseline registry:
  - technology
  - bank / depository
  - industrial (capital goods)
  - consumer_discretionary
  - consumer_staples
  - energy
  - reit  (real estate investment trust)
  - default  (used as a fallback when the target's sector is unknown)

Governance: this is a metric registry only. Values are conservative starting
points grounded in NYU Stern (Damodaran) industry-margin references and
practitioner convention. They are quarterly-reviewed alongside the ratio
library (§11.5) and every deliverable stamps its sector-profile version.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Sector(str, Enum):
    TECHNOLOGY = "technology"
    BANK = "bank"
    INDUSTRIAL = "industrial"
    CONSUMER_DISCRETIONARY = "consumer_discretionary"
    CONSUMER_STAPLES = "consumer_staples"
    ENERGY = "energy"
    REIT = "reit"
    DEFAULT = "default"


class Direction(str, Enum):
    """Which direction improves the ratio's status ('higher is better' etc.)."""

    HIGHER = "higher"      # e.g. gross margin, ROE, interest coverage
    LOWER = "lower"        # e.g. debt / equity, DSO, payout ratio
    RANGE = "range"        # e.g. current ratio (too low OR too high both flag)


@dataclass(frozen=True)
class RatioThreshold:
    """Sector threshold band for one ratio.

    Semantics:
      - direction=HIGHER: green ≥ good_ceiling, amber good_floor..good_ceiling,
        red < good_floor.
      - direction=LOWER: green ≤ good_floor, amber good_floor..good_ceiling,
        red > good_ceiling.
      - direction=RANGE: green good_floor..good_ceiling, amber ±0.5× outside,
        red beyond ±0.5× outside.
    """

    ratio_id: str
    direction: Direction
    good_floor: float
    good_ceiling: float
    unit: str = "ratio"
    note: str = ""


@dataclass(frozen=True)
class SectorProfile:
    sector: Sector
    name: str
    relevant_ratios: frozenset[str]
    non_relevant_ratios: frozenset[str]
    thresholds: tuple[RatioThreshold, ...]
    # Ordered list of sector-specific KPIs that appear on the dashboard on top of
    # the standard six sections (e.g. NIM for banks, ARR for tech, FFO for REITs).
    sector_kpis: tuple[str, ...] = field(default_factory=tuple)

    def threshold_for(self, ratio_id: str) -> RatioThreshold | None:
        for t in self.thresholds:
            if t.ratio_id == ratio_id:
                return t
        return None

    def is_relevant(self, ratio_id: str) -> bool:
        if ratio_id in self.non_relevant_ratios:
            return False
        if not self.relevant_ratios:
            return True
        return ratio_id in self.relevant_ratios


# --------------------------------------------------------------------------- #
# Canonical ratio ids used across the dashboard (mirrors §11.2 / §9.4)
# --------------------------------------------------------------------------- #
# Profitability
GROSS_MARGIN = "gross_margin"
OPERATING_MARGIN = "operating_margin"
NET_MARGIN = "net_margin"
EBITDA_MARGIN = "ebitda_margin"
ROA = "roa"
ROE = "roe"
ROCE = "roce"

# Liquidity
CURRENT_RATIO = "current_ratio"
QUICK_RATIO = "quick_ratio"
CASH_RATIO = "cash_ratio"

# Efficiency
ASSET_TURNOVER = "asset_turnover"
INVENTORY_TURNOVER = "inventory_turnover"
RECEIVABLES_TURNOVER = "receivables_turnover"
DSO = "dso"

# Solvency
DEBT_TO_EQUITY = "debt_to_equity"
DEBT_TO_ASSETS = "debt_to_assets"
INTEREST_COVERAGE = "interest_coverage"
DSCR = "dscr"

# Cash flow
CFO_TO_CAPEX = "cfo_to_capex"
CFO_TO_NET_INCOME = "cfo_to_net_income"
FCF_MARGIN = "fcf_margin"

# Valuation
PE = "pe_ratio"
PB = "pb_ratio"
PS = "ps_ratio"
EV_EBITDA = "ev_ebitda"

# Sector-specific KPIs
NIM = "net_interest_margin"                # bank
EFFICIENCY_RATIO = "efficiency_ratio"      # bank (cost / income)
ARR_GROWTH = "arr_growth"                  # tech / SaaS
RD_INTENSITY = "rd_intensity"              # tech
FFO_MULTIPLE = "ffo_multiple"              # REIT
BOEPD = "boepd"                            # energy (barrels of oil eq. / day)
FINDING_DEV_COST = "finding_development_cost"  # energy


# --------------------------------------------------------------------------- #
# Profiles
# --------------------------------------------------------------------------- #
_TECH = SectorProfile(
    sector=Sector.TECHNOLOGY,
    name="Technology / Software",
    relevant_ratios=frozenset({
        GROSS_MARGIN, OPERATING_MARGIN, NET_MARGIN, EBITDA_MARGIN, ROE, ROA, ROCE,
        CURRENT_RATIO, QUICK_RATIO, CASH_RATIO,
        DEBT_TO_EQUITY, INTEREST_COVERAGE, ASSET_TURNOVER,
        CFO_TO_CAPEX, CFO_TO_NET_INCOME, FCF_MARGIN,
        PE, PS, EV_EBITDA, RD_INTENSITY, ARR_GROWTH,
    }),
    non_relevant_ratios=frozenset({INVENTORY_TURNOVER, DSCR, NIM, EFFICIENCY_RATIO,
                                    FFO_MULTIPLE, BOEPD, FINDING_DEV_COST}),
    thresholds=(
        RatioThreshold(GROSS_MARGIN, Direction.HIGHER, 0.55, 0.75, "pct",
                       "SaaS peer range typically 55–75%."),
        RatioThreshold(OPERATING_MARGIN, Direction.HIGHER, 0.10, 0.25, "pct"),
        RatioThreshold(NET_MARGIN, Direction.HIGHER, 0.10, 0.20, "pct"),
        RatioThreshold(EBITDA_MARGIN, Direction.HIGHER, 0.15, 0.35, "pct"),
        RatioThreshold(ROE, Direction.HIGHER, 0.12, 0.25, "pct"),
        RatioThreshold(ROA, Direction.HIGHER, 0.05, 0.15, "pct"),
        RatioThreshold(ROCE, Direction.HIGHER, 0.10, 0.20, "pct"),
        RatioThreshold(CURRENT_RATIO, Direction.RANGE, 1.5, 3.0, "ratio",
                       "Cash-rich SaaS often above range; not a red flag."),
        RatioThreshold(QUICK_RATIO, Direction.HIGHER, 1.0, 2.0, "ratio"),
        RatioThreshold(DEBT_TO_EQUITY, Direction.LOWER, 0.30, 1.00, "ratio"),
        RatioThreshold(INTEREST_COVERAGE, Direction.HIGHER, 5.0, 15.0, "mult"),
        RatioThreshold(CFO_TO_CAPEX, Direction.HIGHER, 3.0, 8.0, "mult",
                       "Low-CapEx models typically well above 3×."),
        RatioThreshold(CFO_TO_NET_INCOME, Direction.HIGHER, 0.9, 1.3, "ratio"),
        RatioThreshold(FCF_MARGIN, Direction.HIGHER, 0.10, 0.25, "pct"),
        RatioThreshold(PE, Direction.RANGE, 20.0, 40.0, "mult",
                       "SaaS multiples vary widely; interpret vs. peers + growth."),
        RatioThreshold(PS, Direction.RANGE, 4.0, 12.0, "mult"),
        RatioThreshold(EV_EBITDA, Direction.RANGE, 15.0, 30.0, "mult"),
        RatioThreshold(RD_INTENSITY, Direction.RANGE, 0.12, 0.25, "pct",
                       "Too low → under-investment; too high → burn."),
    ),
    sector_kpis=(ARR_GROWTH, RD_INTENSITY),
)

_BANK = SectorProfile(
    sector=Sector.BANK,
    name="Bank / Depository",
    relevant_ratios=frozenset({
        ROA, ROE, NIM, EFFICIENCY_RATIO, DEBT_TO_ASSETS,
        # deliberately DE-emphasized: current ratio, quick ratio (banks
        # intentionally have low liquid-asset ratios by these definitions).
    }),
    non_relevant_ratios=frozenset({
        GROSS_MARGIN, OPERATING_MARGIN, EBITDA_MARGIN, ROCE,
        CURRENT_RATIO, QUICK_RATIO, CASH_RATIO,
        INVENTORY_TURNOVER, ASSET_TURNOVER, RECEIVABLES_TURNOVER, DSO,
        DEBT_TO_EQUITY, INTEREST_COVERAGE, DSCR,
        CFO_TO_CAPEX, FCF_MARGIN, EV_EBITDA,
        RD_INTENSITY, ARR_GROWTH, FFO_MULTIPLE, BOEPD, FINDING_DEV_COST,
    }),
    thresholds=(
        RatioThreshold(ROA, Direction.HIGHER, 0.008, 0.015, "pct",
                       "1% ROA benchmark for peer-median community banks."),
        RatioThreshold(ROE, Direction.HIGHER, 0.08, 0.15, "pct"),
        RatioThreshold(NIM, Direction.HIGHER, 0.025, 0.040, "pct"),
        RatioThreshold(EFFICIENCY_RATIO, Direction.LOWER, 0.55, 0.70, "pct",
                       "Cost / revenue: lower is better."),
        RatioThreshold(NET_MARGIN, Direction.HIGHER, 0.15, 0.30, "pct"),
        RatioThreshold(PE, Direction.RANGE, 8.0, 15.0, "mult"),
        RatioThreshold(PB, Direction.RANGE, 0.8, 1.8, "mult",
                       "Below 1× book often signals capital / credit stress."),
    ),
    sector_kpis=(NIM, EFFICIENCY_RATIO),
)

_INDUSTRIAL = SectorProfile(
    sector=Sector.INDUSTRIAL,
    name="Industrial / Capital Goods",
    relevant_ratios=frozenset({
        GROSS_MARGIN, OPERATING_MARGIN, NET_MARGIN, EBITDA_MARGIN, ROA, ROE, ROCE,
        CURRENT_RATIO, QUICK_RATIO,
        ASSET_TURNOVER, INVENTORY_TURNOVER, RECEIVABLES_TURNOVER, DSO,
        DEBT_TO_EQUITY, INTEREST_COVERAGE, DSCR,
        CFO_TO_CAPEX, CFO_TO_NET_INCOME, FCF_MARGIN,
        PE, PB, PS, EV_EBITDA,
    }),
    non_relevant_ratios=frozenset({
        NIM, EFFICIENCY_RATIO, ARR_GROWTH, RD_INTENSITY, FFO_MULTIPLE,
        BOEPD, FINDING_DEV_COST,
    }),
    thresholds=(
        RatioThreshold(GROSS_MARGIN, Direction.HIGHER, 0.20, 0.35, "pct"),
        RatioThreshold(OPERATING_MARGIN, Direction.HIGHER, 0.08, 0.16, "pct"),
        RatioThreshold(NET_MARGIN, Direction.HIGHER, 0.05, 0.12, "pct"),
        RatioThreshold(EBITDA_MARGIN, Direction.HIGHER, 0.12, 0.22, "pct"),
        RatioThreshold(ROA, Direction.HIGHER, 0.04, 0.10, "pct"),
        RatioThreshold(ROE, Direction.HIGHER, 0.10, 0.20, "pct"),
        RatioThreshold(ROCE, Direction.HIGHER, 0.10, 0.20, "pct"),
        RatioThreshold(CURRENT_RATIO, Direction.RANGE, 1.5, 2.5, "ratio"),
        RatioThreshold(INVENTORY_TURNOVER, Direction.HIGHER, 4.0, 8.0, "mult"),
        RatioThreshold(RECEIVABLES_TURNOVER, Direction.HIGHER, 5.0, 12.0, "mult"),
        RatioThreshold(DSO, Direction.LOWER, 30.0, 60.0, "days"),
        RatioThreshold(DEBT_TO_EQUITY, Direction.LOWER, 0.50, 1.50, "ratio"),
        RatioThreshold(INTEREST_COVERAGE, Direction.HIGHER, 3.0, 8.0, "mult"),
        RatioThreshold(DSCR, Direction.HIGHER, 1.25, 2.00, "mult"),
        RatioThreshold(CFO_TO_CAPEX, Direction.HIGHER, 1.2, 2.5, "mult",
                       "CapEx-heavy — below 1× flags stretched cash."),
        RatioThreshold(CFO_TO_NET_INCOME, Direction.HIGHER, 0.9, 1.3, "ratio"),
        RatioThreshold(PE, Direction.RANGE, 12.0, 20.0, "mult"),
        RatioThreshold(EV_EBITDA, Direction.RANGE, 8.0, 14.0, "mult"),
    ),
)

_CONSUMER_DISC = SectorProfile(
    sector=Sector.CONSUMER_DISCRETIONARY,
    name="Consumer Discretionary",
    relevant_ratios=frozenset({
        GROSS_MARGIN, OPERATING_MARGIN, NET_MARGIN, EBITDA_MARGIN, ROA, ROE,
        CURRENT_RATIO, QUICK_RATIO,
        ASSET_TURNOVER, INVENTORY_TURNOVER, RECEIVABLES_TURNOVER, DSO,
        DEBT_TO_EQUITY, INTEREST_COVERAGE, DSCR,
        CFO_TO_CAPEX, CFO_TO_NET_INCOME, FCF_MARGIN,
        PE, PS, EV_EBITDA,
    }),
    non_relevant_ratios=frozenset({
        NIM, EFFICIENCY_RATIO, ARR_GROWTH, RD_INTENSITY, FFO_MULTIPLE,
        BOEPD, FINDING_DEV_COST,
    }),
    thresholds=(
        RatioThreshold(GROSS_MARGIN, Direction.HIGHER, 0.30, 0.50, "pct"),
        RatioThreshold(OPERATING_MARGIN, Direction.HIGHER, 0.06, 0.15, "pct"),
        RatioThreshold(NET_MARGIN, Direction.HIGHER, 0.04, 0.10, "pct"),
        RatioThreshold(EBITDA_MARGIN, Direction.HIGHER, 0.10, 0.20, "pct"),
        RatioThreshold(INVENTORY_TURNOVER, Direction.HIGHER, 5.0, 10.0, "mult"),
        RatioThreshold(DSO, Direction.LOWER, 20.0, 45.0, "days"),
        RatioThreshold(DEBT_TO_EQUITY, Direction.LOWER, 0.50, 1.50, "ratio"),
        RatioThreshold(CFO_TO_CAPEX, Direction.HIGHER, 1.5, 3.0, "mult"),
        RatioThreshold(FCF_MARGIN, Direction.HIGHER, 0.05, 0.12, "pct"),
    ),
)

_CONSUMER_STAPLES = SectorProfile(
    sector=Sector.CONSUMER_STAPLES,
    name="Consumer Staples",
    relevant_ratios=frozenset({
        GROSS_MARGIN, OPERATING_MARGIN, NET_MARGIN, EBITDA_MARGIN, ROA, ROE, ROCE,
        CURRENT_RATIO, QUICK_RATIO,
        ASSET_TURNOVER, INVENTORY_TURNOVER, RECEIVABLES_TURNOVER, DSO,
        DEBT_TO_EQUITY, INTEREST_COVERAGE, DSCR,
        CFO_TO_CAPEX, CFO_TO_NET_INCOME, FCF_MARGIN,
        PE, PB, PS, EV_EBITDA,
    }),
    non_relevant_ratios=frozenset({
        NIM, EFFICIENCY_RATIO, ARR_GROWTH, RD_INTENSITY, FFO_MULTIPLE,
        BOEPD, FINDING_DEV_COST,
    }),
    thresholds=(
        RatioThreshold(GROSS_MARGIN, Direction.HIGHER, 0.25, 0.45, "pct"),
        RatioThreshold(OPERATING_MARGIN, Direction.HIGHER, 0.10, 0.20, "pct"),
        RatioThreshold(NET_MARGIN, Direction.HIGHER, 0.07, 0.15, "pct"),
        RatioThreshold(EBITDA_MARGIN, Direction.HIGHER, 0.13, 0.22, "pct"),
        RatioThreshold(INVENTORY_TURNOVER, Direction.HIGHER, 6.0, 12.0, "mult"),
        RatioThreshold(DEBT_TO_EQUITY, Direction.LOWER, 0.60, 1.80, "ratio",
                       "Staples often carry higher, stable leverage."),
        RatioThreshold(INTEREST_COVERAGE, Direction.HIGHER, 4.0, 10.0, "mult"),
        RatioThreshold(CFO_TO_CAPEX, Direction.HIGHER, 2.0, 4.0, "mult"),
        RatioThreshold(FCF_MARGIN, Direction.HIGHER, 0.08, 0.15, "pct"),
        RatioThreshold(PE, Direction.RANGE, 15.0, 25.0, "mult"),
    ),
)

_ENERGY = SectorProfile(
    sector=Sector.ENERGY,
    name="Energy (E&P / Integrated)",
    relevant_ratios=frozenset({
        OPERATING_MARGIN, NET_MARGIN, EBITDA_MARGIN, ROA, ROE, ROCE,
        DEBT_TO_EQUITY, INTEREST_COVERAGE, DSCR,
        CFO_TO_CAPEX, CFO_TO_NET_INCOME, FCF_MARGIN,
        EV_EBITDA, BOEPD, FINDING_DEV_COST,
    }),
    non_relevant_ratios=frozenset({
        GROSS_MARGIN, INVENTORY_TURNOVER, RECEIVABLES_TURNOVER, DSO,
        NIM, EFFICIENCY_RATIO, ARR_GROWTH, RD_INTENSITY, FFO_MULTIPLE,
    }),
    thresholds=(
        RatioThreshold(OPERATING_MARGIN, Direction.HIGHER, 0.08, 0.25, "pct",
                       "Highly commodity-linked — normalize across the cycle."),
        RatioThreshold(NET_MARGIN, Direction.HIGHER, 0.05, 0.15, "pct"),
        RatioThreshold(EBITDA_MARGIN, Direction.HIGHER, 0.25, 0.45, "pct"),
        RatioThreshold(ROCE, Direction.HIGHER, 0.08, 0.15, "pct"),
        RatioThreshold(DEBT_TO_EQUITY, Direction.LOWER, 0.40, 1.20, "ratio"),
        RatioThreshold(INTEREST_COVERAGE, Direction.HIGHER, 4.0, 10.0, "mult"),
        RatioThreshold(CFO_TO_CAPEX, Direction.HIGHER, 1.0, 2.0, "mult",
                       "Below 1× → funding CapEx with debt."),
        RatioThreshold(EV_EBITDA, Direction.RANGE, 4.0, 8.0, "mult"),
    ),
    sector_kpis=(BOEPD, FINDING_DEV_COST),
)

_REIT = SectorProfile(
    sector=Sector.REIT,
    name="Real Estate Investment Trust",
    relevant_ratios=frozenset({
        OPERATING_MARGIN, NET_MARGIN, ROA, ROE,
        DEBT_TO_EQUITY, INTEREST_COVERAGE, DSCR,
        CFO_TO_NET_INCOME, FCF_MARGIN,
        PB, PS, FFO_MULTIPLE,
    }),
    non_relevant_ratios=frozenset({
        GROSS_MARGIN, ROCE, CURRENT_RATIO, QUICK_RATIO, CASH_RATIO,
        INVENTORY_TURNOVER, RECEIVABLES_TURNOVER, DSO,
        NIM, EFFICIENCY_RATIO, ARR_GROWTH, RD_INTENSITY,
        BOEPD, FINDING_DEV_COST, PE,
    }),
    thresholds=(
        RatioThreshold(DEBT_TO_EQUITY, Direction.RANGE, 0.60, 1.50, "ratio",
                       "REITs run high, stable leverage by design."),
        RatioThreshold(INTEREST_COVERAGE, Direction.HIGHER, 2.5, 5.0, "mult"),
        RatioThreshold(DSCR, Direction.HIGHER, 1.25, 1.80, "mult"),
        RatioThreshold(FFO_MULTIPLE, Direction.RANGE, 12.0, 20.0, "mult",
                       "Price / FFO — the REIT valuation standard, not P/E."),
    ),
    sector_kpis=(FFO_MULTIPLE,),
)

_DEFAULT = SectorProfile(
    sector=Sector.DEFAULT,
    name="Cross-sector default (unknown sector)",
    relevant_ratios=frozenset(),
    non_relevant_ratios=frozenset(),
    thresholds=(
        RatioThreshold(GROSS_MARGIN, Direction.HIGHER, 0.25, 0.45, "pct"),
        RatioThreshold(OPERATING_MARGIN, Direction.HIGHER, 0.08, 0.18, "pct"),
        RatioThreshold(NET_MARGIN, Direction.HIGHER, 0.05, 0.12, "pct"),
        RatioThreshold(EBITDA_MARGIN, Direction.HIGHER, 0.12, 0.22, "pct"),
        RatioThreshold(ROA, Direction.HIGHER, 0.05, 0.12, "pct"),
        RatioThreshold(ROE, Direction.HIGHER, 0.10, 0.20, "pct"),
        RatioThreshold(ROCE, Direction.HIGHER, 0.10, 0.20, "pct"),
        RatioThreshold(CURRENT_RATIO, Direction.RANGE, 1.5, 3.0, "ratio"),
        RatioThreshold(QUICK_RATIO, Direction.HIGHER, 1.0, 2.0, "ratio"),
        RatioThreshold(DEBT_TO_EQUITY, Direction.LOWER, 0.50, 1.50, "ratio"),
        RatioThreshold(INTEREST_COVERAGE, Direction.HIGHER, 3.0, 8.0, "mult"),
        RatioThreshold(DSCR, Direction.HIGHER, 1.25, 2.00, "mult"),
        RatioThreshold(ASSET_TURNOVER, Direction.HIGHER, 0.5, 1.5, "ratio"),
        RatioThreshold(INVENTORY_TURNOVER, Direction.HIGHER, 4.0, 8.0, "mult"),
        RatioThreshold(RECEIVABLES_TURNOVER, Direction.HIGHER, 5.0, 12.0, "mult"),
        RatioThreshold(DSO, Direction.LOWER, 30.0, 60.0, "days"),
        RatioThreshold(CFO_TO_CAPEX, Direction.HIGHER, 1.5, 3.0, "mult"),
        RatioThreshold(CFO_TO_NET_INCOME, Direction.HIGHER, 0.9, 1.3, "ratio"),
        RatioThreshold(FCF_MARGIN, Direction.HIGHER, 0.05, 0.12, "pct"),
        RatioThreshold(PE, Direction.RANGE, 12.0, 22.0, "mult"),
        RatioThreshold(PB, Direction.RANGE, 1.0, 3.0, "mult"),
        RatioThreshold(PS, Direction.RANGE, 1.0, 4.0, "mult"),
        RatioThreshold(EV_EBITDA, Direction.RANGE, 8.0, 14.0, "mult"),
    ),
)


PROFILES: dict[Sector, SectorProfile] = {
    p.sector: p for p in [_TECH, _BANK, _INDUSTRIAL, _CONSUMER_DISC,
                          _CONSUMER_STAPLES, _ENERGY, _REIT, _DEFAULT]
}


def get_profile(sector: Sector | str | None) -> SectorProfile:
    """Return the SectorProfile for a given sector value or name.

    Accepts an enum, a canonical string (``"technology"``), a display name
    (``"Technology / Software"``), or None (→ DEFAULT).
    """
    if sector is None:
        return PROFILES[Sector.DEFAULT]
    if isinstance(sector, Sector):
        return PROFILES.get(sector, PROFILES[Sector.DEFAULT])
    key = str(sector).strip().lower().replace(" ", "_").replace("/", "").replace("__", "_")
    try:
        return PROFILES[Sector(key)]
    except ValueError:
        # Try display name match
        for prof in PROFILES.values():
            if prof.name.lower() == str(sector).strip().lower():
                return prof
        return PROFILES[Sector.DEFAULT]


def all_profiles() -> list[SectorProfile]:
    """All registered SectorProfiles in stable order."""
    return list(PROFILES.values())


# --------------------------------------------------------------------------- #
# Deterministic status flag (§9.4 status column + §11.3)
# --------------------------------------------------------------------------- #
class Status(str, Enum):
    GREEN = "green"                 # inside good band
    AMBER = "amber"                 # borderline
    RED = "red"                     # outside acceptable range
    NM_SECTOR = "n/m-sector"        # not applicable to this sector
    NM_DATA = "n/m-data"            # data missing / negative earnings etc.


def status_for(
    value: float | None,
    threshold: RatioThreshold | None,
) -> Status:
    """Compute a deterministic status from a value + threshold.

    Returns NM_DATA when the value is missing or non-finite; returns NM_SECTOR
    when the threshold is missing (caller should check `SectorProfile.is_relevant`
    first when it wants to distinguish the two states).
    """
    if threshold is None:
        return Status.NM_SECTOR
    if value is None:
        return Status.NM_DATA
    try:
        v = float(value)
    except (TypeError, ValueError):
        return Status.NM_DATA
    if not (v == v) or v in (float("inf"), float("-inf")):
        return Status.NM_DATA

    lo, hi = float(threshold.good_floor), float(threshold.good_ceiling)
    if threshold.direction == Direction.HIGHER:
        if v >= hi:
            return Status.GREEN
        if v >= lo:
            return Status.AMBER
        return Status.RED
    if threshold.direction == Direction.LOWER:
        if v <= lo:
            return Status.GREEN
        if v <= hi:
            return Status.AMBER
        return Status.RED
    # RANGE
    width = hi - lo
    if lo <= v <= hi:
        return Status.GREEN
    outside = v < lo - 0.5 * width or v > hi + 0.5 * width
    return Status.RED if outside else Status.AMBER


__all__ = [
    # ratio ids
    "ARR_GROWTH", "ASSET_TURNOVER", "BOEPD", "CASH_RATIO", "CFO_TO_CAPEX",
    "CFO_TO_NET_INCOME", "CURRENT_RATIO", "DEBT_TO_ASSETS", "DEBT_TO_EQUITY",
    "DSCR", "DSO", "EBITDA_MARGIN", "EFFICIENCY_RATIO", "EV_EBITDA",
    "FCF_MARGIN", "FFO_MULTIPLE", "FINDING_DEV_COST", "GROSS_MARGIN",
    "INTEREST_COVERAGE", "INVENTORY_TURNOVER", "NET_MARGIN", "NIM",
    "OPERATING_MARGIN", "PB", "PE", "PS", "QUICK_RATIO", "RD_INTENSITY",
    "RECEIVABLES_TURNOVER", "ROA", "ROCE", "ROE",
    # registry + types
    "Direction", "PROFILES", "RatioThreshold", "Sector", "SectorProfile",
    "Status", "all_profiles", "get_profile", "status_for",
]
