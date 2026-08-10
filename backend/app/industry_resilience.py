# JHI-SIG: 69M2705M | Recession-resilience + boomer-succession industry model | JHI Research & Analytics Firm, Inc. (proprietary)
"""Score main-street industries by **recession resilience** and **boomer-succession
opportunity** for SMB / search-fund / ETA acquirers.

Grounding (public data only):
    • BLS — employment & wages by industry, and employment stability through downturns
      (Current Employment Statistics / QCEW). Public domain.
    • U.S. Census — Business Dynamics / Survival and Annual Business Survey owner
      demographics (share of owners age 55+ — the "silver tsunami" proxy). Public domain.
    • BEA — industry value-added / margin context. Public domain.

The model exposes transparent sub-factor INPUTS (0-1 reference readings derived from the
sources above) and computes the two composite scores from disclosed weights, so the read
is auditable rather than a black box. Every displayed multiple/margin is DERIVED and shown
as a reference range, not a quote or appraisal.

Network-free by construction: the scored table is curated from public-data-derived
reference readings. ``enrich_from_bls`` / ``enrich_from_census`` are optional module-level
hooks (monkeypatchable) for a future live refresh; the engine renders fully without them.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ResilienceInputs:
    """Sub-factor readings (0-1) derived from public sources. Higher = more resilient."""

    essential_service: float      # non-discretionary demand (needs vs. wants)
    demand_stability: float       # BLS employment stability through recessions
    recurring_contract: float     # recurring/contract/repeat-revenue tendency


@dataclass
class SuccessionInputs:
    """Sub-factor readings (0-1). Higher = larger succession/acquisition opportunity."""

    owner_age_55plus: float       # Census/ABS: share of owners age 55+ (silver tsunami)
    fragmentation: float          # many small independents → roll-up / ETA runway
    financeability: float         # SBA-friendly, bankable cash flow (7(a) fit)


@dataclass
class IndustryProfile:
    key: str
    name: str
    naics_prefixes: list[str]
    resilience_inputs: ResilienceInputs
    succession_inputs: SuccessionInputs
    typical_multiple_low: float
    typical_multiple_base: float
    typical_multiple_high: float
    typical_ebitda_margin: float  # derived reference midpoint
    pros: list[str]
    cons: list[str]
    red_flags: list[str]
    # Public-data reference readings (annual, illustrative until live refresh wired).
    employment_thousands: float | None = None
    avg_annual_wage: float | None = None

    # --- Derived composite scores (0-100), computed from disclosed weights ---
    @property
    def recession_resilience(self) -> float:
        r = self.resilience_inputs
        score = (
            0.45 * r.essential_service
            + 0.35 * r.demand_stability
            + 0.20 * r.recurring_contract
        )
        return round(score * 100, 1)

    @property
    def succession_opportunity(self) -> float:
        s = self.succession_inputs
        score = (
            0.45 * s.owner_age_55plus
            + 0.30 * s.fragmentation
            + 0.25 * s.financeability
        )
        return round(score * 100, 1)

    @property
    def combined_score(self) -> float:
        """A single acquirer-attractiveness read: resilient AND transferable."""
        return round(0.6 * self.recession_resilience + 0.4 * self.succession_opportunity, 1)


# Disclosed weights (surfaced in methodology copy so the score is auditable).
RESILIENCE_WEIGHTS = {"essential_service": 0.45, "demand_stability": 0.35, "recurring_contract": 0.20}
SUCCESSION_WEIGHTS = {"owner_age_55plus": 0.45, "fragmentation": 0.30, "financeability": 0.25}


# ── Curated, public-data-derived reference table ─────────────────────────────
# Readings are illustrative reference values derived from BLS/Census/BEA public series;
# they are anchors for the transparent scoring, not point estimates or advice.
INDUSTRIES: list[IndustryProfile] = [
    IndustryProfile(
        key="hvac",
        name="HVAC & Refrigeration Services",
        naics_prefixes=["2382"],
        resilience_inputs=ResilienceInputs(0.90, 0.82, 0.55),
        succession_inputs=SuccessionInputs(0.78, 0.85, 0.85),
        typical_multiple_low=2.5, typical_multiple_base=3.4, typical_multiple_high=4.5,
        typical_ebitda_margin=0.15,
        pros=[
            "Essential, weather- and code-driven demand that persists through downturns.",
            "Service/replacement and maintenance contracts add recurring, sticky revenue.",
            "Highly fragmented, owner-operator base — a deep, financeable acquisition pool.",
        ],
        cons=[
            "Skilled-technician shortage constrains organic growth and raises labor cost.",
            "New-construction exposure adds a cyclical sleeve on top of the service base.",
        ],
        red_flags=[
            "Owner is the top salesperson/estimator — key-person risk on transition.",
            "Revenue skewed to install (new construction) over recurring service.",
        ],
        employment_thousands=1450.0, avg_annual_wage=62000.0,
    ),
    IndustryProfile(
        key="electrical",
        name="Electrical Contractors",
        naics_prefixes=["2382"],
        resilience_inputs=ResilienceInputs(0.85, 0.78, 0.50),
        succession_inputs=SuccessionInputs(0.76, 0.82, 0.82),
        typical_multiple_low=2.5, typical_multiple_base=3.2, typical_multiple_high=4.2,
        typical_ebitda_margin=0.14,
        pros=[
            "Code-mandated, safety-critical work with steady service/repair demand.",
            "Electrification and EV/solar tailwinds broaden the service mix.",
            "Fragmented trade with an aging licensed-owner base.",
        ],
        cons=["Project/backlog volatility; licensing gates the operator bench."],
        red_flags=["Concentrated in one GC or a few large projects."],
        employment_thousands=1050.0, avg_annual_wage=66000.0,
    ),
    IndustryProfile(
        key="healthcare_services",
        name="Outpatient / Allied Health Services",
        naics_prefixes=["6213", "6214"],
        resilience_inputs=ResilienceInputs(0.95, 0.90, 0.60),
        succession_inputs=SuccessionInputs(0.70, 0.75, 0.80),
        typical_multiple_low=3.5, typical_multiple_base=4.5, typical_multiple_high=6.0,
        typical_ebitda_margin=0.18,
        pros=[
            "Demographically-driven, largely non-discretionary demand.",
            "Insurance/payer mix supports recurring, defensible cash flow.",
            "Aging clinician-owners create a steady succession pipeline.",
        ],
        cons=[
            "Reimbursement and regulatory risk; credentialing on transfer.",
            "Clinician recruiting/retention is the binding growth constraint.",
        ],
        red_flags=[
            "Revenue dependent on one payer or one referring physician.",
            "Owner-clinician generates most billable production.",
        ],
        employment_thousands=2600.0, avg_annual_wage=71000.0,
    ),
    IndustryProfile(
        key="professional_services",
        name="Professional Services (Accounting/IT/Engineering)",
        naics_prefixes=["5413", "5412", "5415"],
        resilience_inputs=ResilienceInputs(0.75, 0.72, 0.65),
        succession_inputs=SuccessionInputs(0.80, 0.70, 0.75),
        typical_multiple_low=2.5, typical_multiple_base=3.6, typical_multiple_high=4.8,
        typical_ebitda_margin=0.20,
        pros=[
            "Asset-light, high-margin, retainer/repeat client relationships.",
            "Aging partner base with limited internal succession.",
        ],
        cons=["Talent-dependent; client relationships can be personal to the owner."],
        red_flags=["Top clients follow the departing owner-partner."],
        employment_thousands=1900.0, avg_annual_wage=88000.0,
    ),
    IndustryProfile(
        key="logistics",
        name="Trucking & Local Logistics",
        naics_prefixes=["4841", "4842", "4931"],
        resilience_inputs=ResilienceInputs(0.70, 0.62, 0.55),
        succession_inputs=SuccessionInputs(0.72, 0.80, 0.68),
        typical_multiple_low=2.5, typical_multiple_base=3.2, typical_multiple_high=4.2,
        typical_ebitda_margin=0.12,
        pros=[
            "Essential freight movement; contracted lanes add recurring revenue.",
            "Fragmented owner-operator base with succession pressure.",
        ],
        cons=[
            "Cyclical freight rates and fuel-cost exposure.",
            "Capex-heavy fleet; driver shortage pressures cost.",
        ],
        red_flags=["Single-shipper concentration; deferred fleet maintenance."],
        employment_thousands=1600.0, avg_annual_wage=55000.0,
    ),
    IndustryProfile(
        key="landscaping",
        name="Landscaping & Grounds Maintenance",
        naics_prefixes=["5617"],
        resilience_inputs=ResilienceInputs(0.62, 0.60, 0.60),
        succession_inputs=SuccessionInputs(0.68, 0.88, 0.72),
        typical_multiple_low=2.0, typical_multiple_base=2.8, typical_multiple_high=3.6,
        typical_ebitda_margin=0.13,
        pros=[
            "Recurring commercial maintenance contracts smooth demand.",
            "Extremely fragmented — a classic roll-up runway.",
        ],
        cons=["Seasonal and weather-dependent; discretionary residential sleeve."],
        red_flags=["Revenue concentrated in one-off installs vs. contracts."],
        employment_thousands=1200.0, avg_annual_wage=42000.0,
    ),
    IndustryProfile(
        key="auto_repair",
        name="Automotive Repair & Maintenance",
        naics_prefixes=["8111"],
        resilience_inputs=ResilienceInputs(0.82, 0.80, 0.50),
        succession_inputs=SuccessionInputs(0.74, 0.86, 0.75),
        typical_multiple_low=2.2, typical_multiple_base=3.0, typical_multiple_high=4.0,
        typical_ebitda_margin=0.14,
        pros=[
            "Aging vehicle fleet sustains counter-cyclical repair demand.",
            "Local, repeat customer base; real estate often attached.",
        ],
        cons=["EV transition shifts the long-run service mix; tech recruiting."],
        red_flags=["Deferred equipment/bay capex; owner is the master tech."],
        employment_thousands=680.0, avg_annual_wage=50000.0,
    ),
    IndustryProfile(
        key="restaurant",
        name="Full-Service Restaurants",
        naics_prefixes=["7225"],
        resilience_inputs=ResilienceInputs(0.35, 0.40, 0.30),
        succession_inputs=SuccessionInputs(0.55, 0.90, 0.45),
        typical_multiple_low=1.5, typical_multiple_base=2.2, typical_multiple_high=3.0,
        typical_ebitda_margin=0.09,
        pros=["Cash-flowing and plentiful supply of independent sellers."],
        cons=[
            "Highly discretionary, thin margins, and labor/food-cost sensitivity.",
            "High failure rate; brand and location risk on transfer.",
        ],
        red_flags=[
            "Undocumented cash sales; deferred kitchen/equipment capex.",
            "Success tied to a specific chef/owner.",
        ],
        employment_thousands=5200.0, avg_annual_wage=32000.0,
    ),
]


_BY_KEY = {p.key: p for p in INDUSTRIES}


# ── Optional live-enrichment hooks (monkeypatchable; never required) ─────────
def enrich_from_bls(profile: IndustryProfile) -> None:  # pragma: no cover - live hook
    """Placeholder for a live BLS refresh of employment/wage readings. No-op by default."""
    return None


def enrich_from_census(profile: IndustryProfile) -> None:  # pragma: no cover - live hook
    """Placeholder for a live Census/ABS refresh of owner-age readings. No-op by default."""
    return None


# ── Public API ──────────────────────────────────────────────────────────────
def get(key: str) -> IndustryProfile | None:
    return _BY_KEY.get(key.strip().lower())


def all_industries() -> list[IndustryProfile]:
    return list(INDUSTRIES)


def rank_by(metric: str = "combined_score") -> list[IndustryProfile]:
    """Rank industries by ``combined_score`` | ``recession_resilience`` | ``succession_opportunity``."""
    valid = {"combined_score", "recession_resilience", "succession_opportunity"}
    key = metric if metric in valid else "combined_score"
    return sorted(INDUSTRIES, key=lambda p: getattr(p, key), reverse=True)


def spotlight_for(now: datetime) -> IndustryProfile:
    """Deterministically rotate the per-issue spotlight so each edition features one
    industry, cycling weekly through the ranked list (stable for a given week)."""
    ranked = rank_by("combined_score")
    week_index = int(now.strftime("%U")) + (now.year * 53)
    return ranked[week_index % len(ranked)]
