# JHI-SIG: 69M2705M | SectorProfile registry tests | JHI Research & Analytics Firm, Inc. (proprietary)
"""Tests for the SectorProfile registry and status_for computation."""

from __future__ import annotations

import pytest

from app.sector_profiles import (
    ARR_GROWTH,
    CURRENT_RATIO,
    DEBT_TO_EQUITY,
    EFFICIENCY_RATIO,
    FFO_MULTIPLE,
    GROSS_MARGIN,
    INTEREST_COVERAGE,
    INVENTORY_TURNOVER,
    NIM,
    OPERATING_MARGIN,
    PE,
    ROA,
    ROCE,
    Direction,
    RatioThreshold,
    Sector,
    Status,
    all_profiles,
    get_profile,
    status_for,
)


def test_all_seven_profiles_registered():
    """Baseline coverage: tech, bank, industrial, cons-disc, cons-staples, energy, reit, + default."""
    names = {p.sector for p in all_profiles()}
    assert Sector.TECHNOLOGY in names
    assert Sector.BANK in names
    assert Sector.INDUSTRIAL in names
    assert Sector.CONSUMER_DISCRETIONARY in names
    assert Sector.CONSUMER_STAPLES in names
    assert Sector.ENERGY in names
    assert Sector.REIT in names
    assert Sector.DEFAULT in names
    assert len(names) == 8


def test_get_profile_by_enum():
    p = get_profile(Sector.TECHNOLOGY)
    assert p.sector == Sector.TECHNOLOGY


def test_get_profile_by_string():
    p = get_profile("technology")
    assert p.sector == Sector.TECHNOLOGY


def test_get_profile_unknown_falls_back_to_default():
    p = get_profile("healthcare")
    assert p.sector == Sector.DEFAULT


def test_get_profile_none_is_default():
    p = get_profile(None)
    assert p.sector == Sector.DEFAULT


# --------------------------------------------------------------------------- #
# Relevance discipline — sector-specific ratios
# --------------------------------------------------------------------------- #
def test_bank_marks_inventory_turnover_non_relevant():
    p = get_profile(Sector.BANK)
    assert not p.is_relevant(INVENTORY_TURNOVER)
    assert not p.is_relevant(GROSS_MARGIN)
    assert p.is_relevant(NIM)
    assert p.is_relevant(EFFICIENCY_RATIO)


def test_tech_marks_inventory_turnover_non_relevant():
    p = get_profile(Sector.TECHNOLOGY)
    assert not p.is_relevant(INVENTORY_TURNOVER)
    assert p.is_relevant(ARR_GROWTH)


def test_reit_marks_pe_non_relevant():
    p = get_profile(Sector.REIT)
    assert not p.is_relevant(PE)
    assert p.is_relevant(FFO_MULTIPLE)


def test_energy_marks_gross_margin_non_relevant():
    p = get_profile(Sector.ENERGY)
    assert not p.is_relevant(GROSS_MARGIN)
    assert p.is_relevant(ROCE)


def test_industrial_relevant_set_covers_full_dashboard():
    """Industrial is the reference profile — should span all 6 sections."""
    p = get_profile(Sector.INDUSTRIAL)
    for rid in (GROSS_MARGIN, CURRENT_RATIO, DEBT_TO_EQUITY,
                INVENTORY_TURNOVER, OPERATING_MARGIN, PE):
        assert p.is_relevant(rid), f"{rid} should be relevant to industrial"


# --------------------------------------------------------------------------- #
# Status computation
# --------------------------------------------------------------------------- #
def test_status_higher_direction():
    t = RatioThreshold("x", Direction.HIGHER, 0.10, 0.20)
    assert status_for(0.05, t) == Status.RED
    assert status_for(0.15, t) == Status.AMBER
    assert status_for(0.25, t) == Status.GREEN


def test_status_lower_direction():
    t = RatioThreshold("x", Direction.LOWER, 0.30, 1.00)
    assert status_for(0.20, t) == Status.GREEN
    assert status_for(0.60, t) == Status.AMBER
    assert status_for(1.50, t) == Status.RED


def test_status_range_direction():
    # width = 1.5; amber band is (0.75..1.5) and (3.0..3.75); outside → red
    t = RatioThreshold("x", Direction.RANGE, 1.5, 3.0)
    assert status_for(2.0, t) == Status.GREEN
    assert status_for(1.0, t) == Status.AMBER   # borderline low
    assert status_for(3.5, t) == Status.AMBER   # borderline high (within +0.5×width)
    assert status_for(0.1, t) == Status.RED
    assert status_for(10.0, t) == Status.RED


def test_status_returns_nm_sector_when_threshold_missing():
    assert status_for(0.5, None) == Status.NM_SECTOR


def test_status_returns_nm_data_when_value_missing():
    t = RatioThreshold("x", Direction.HIGHER, 0.10, 0.20)
    assert status_for(None, t) == Status.NM_DATA


def test_status_handles_nan_and_inf():
    t = RatioThreshold("x", Direction.HIGHER, 0.10, 0.20)
    assert status_for(float("nan"), t) == Status.NM_DATA
    assert status_for(float("inf"), t) == Status.NM_DATA


# --------------------------------------------------------------------------- #
# Bank ROA threshold — anchored to the ~1% peer-median benchmark
# --------------------------------------------------------------------------- #
def test_bank_roa_threshold_reflects_1pct_benchmark():
    p = get_profile(Sector.BANK)
    t = p.threshold_for(ROA)
    assert t is not None
    assert t.direction == Direction.HIGHER
    # 1% is inside the amber-green band (green ≥ 1.5%, amber 0.8-1.5%)
    assert t.good_floor <= 0.01 <= t.good_ceiling
    assert status_for(0.012, t) == Status.AMBER   # 1.2% ROA is peer-median-ish
    assert status_for(0.020, t) == Status.GREEN


# --------------------------------------------------------------------------- #
# Interest-coverage bands — should require reasonable coverage everywhere
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("sector", [Sector.TECHNOLOGY, Sector.INDUSTRIAL, Sector.ENERGY,
                                    Sector.CONSUMER_STAPLES])
def test_interest_coverage_requires_at_least_3x_amber(sector):
    p = get_profile(sector)
    t = p.threshold_for(INTEREST_COVERAGE)
    if t is None:
        pytest.skip(f"no interest-coverage band for {sector}")
    # 2.0x should NOT be green in any of these sectors
    assert status_for(2.0, t) != Status.GREEN
