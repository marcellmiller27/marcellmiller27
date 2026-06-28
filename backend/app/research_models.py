# JHI-SIG: 69M2705M | Research & Opportunity Score | John Henry Investments (proprietary)
from datetime import datetime

from pydantic import BaseModel, Field


# --- §8.2 Score back-test ------------------------------------------------- #
class BacktestResult(BaseModel):
    methodology: str
    score_definition: str
    universe: list[str]
    n_assets: int
    n_periods: int
    mean_information_coefficient: float | None
    ic_t_stat: float | None
    ic_hit_rate: float | None
    mean_top_minus_bottom_monthly_return: float | None
    annualized_long_short_return: float | None = None
    pass_criteria: str = ""
    h5_pass: bool = False
    interpretation: str
    caveats: list[str]
    status: str = "ok"
    as_of: datetime


class AssetScore(BaseModel):
    symbol: str
    opportunity_score: float


class OpportunityScoreSnapshot(BaseModel):
    as_of: datetime
    score_definition: str
    n_assets: int
    scores: list[AssetScore]
    status: str = "ok"


class EquityOOSBacktestResult(BaseModel):
    protocol: str
    universe: list[str]
    n_assets: int
    in_sample_periods: int
    oos_periods: int
    factor_weights: dict[str, float]
    oos_mean_information_coefficient: float | None
    oos_ic_t_stat: float | None
    oos_hit_rate: float | None
    gross_annualized_long_short: float | None
    net_annualized_long_short: float | None
    cost_bps_per_side: float
    avg_monthly_turnover: float | None
    pass_criteria: str
    oos_pass: bool
    interpretation: str
    solution_if_failed: list[str] = Field(default_factory=list)
    caveats: list[str] = Field(default_factory=list)
    status: str = "ok"
    as_of: datetime


class FundamentalsStatus(BaseModel):
    available: bool
    provider: str
    note: str
    required_solution: list[str]
    as_of: datetime


# --- §8.4 Segment adoption study ----------------------------------------- #
class AdoptionStudy(BaseModel):
    total_organizations: int
    total_users: int
    subscriptions_by_plan: dict[str, int]
    two_factor_adoption_rate: float
    biometric_adoption_rate: float
    activation_rate_login: float
    methodology: str
    dataset_quality: str
    deficiencies: list[str]
    as_of: datetime


# --- §8.5 Acquisition-engine validation ----------------------------------- #
class AcquisitionCaseResult(BaseModel):
    name: str
    normalized_ebitda: float
    dscr: float
    sba_eligible: bool
    recommendation: str
    expected: str
    agree: bool


class AcquisitionValidation(BaseModel):
    cases: list[AcquisitionCaseResult]
    n_cases: int
    agreement_rate: float
    methodology: str
    deficiencies: list[str]
    as_of: datetime


# --- Data coverage / deficiency matrix ------------------------------------ #
class CoverageRow(BaseModel):
    category: str
    realtime: bool
    provider: str | None
    status: str  # "live" | "partial" | "none"
    deficiency: str | None = None
    corrective_action: str | None = None


class DataCoverageReport(BaseModel):
    generated_at: datetime
    live_categories: int
    total_categories: int
    rows: list[CoverageRow]
    summary: str
    open_deficiencies: list[str] = Field(default_factory=list)
