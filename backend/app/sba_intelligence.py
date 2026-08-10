# JHI-SIG: 69M2705M | SBA Lending Intelligence engine | JHI Research & Analytics Firm, Inc. (proprietary)
"""SBA Lending Intelligence — derived analytics from the SBA's *public* 7(a)/504
loan-level FOIA datasets (https://data.sba.gov/dataset/7-a-504-foia).

These datasets are U.S. government public-domain records the SBA itself publishes for
open download — this engine downloads/parses them (NO scraping of marketplaces such as
BizBuySell). From the loan-level rows we derive, per NAICS/industry:

    • funding volume (count + gross approval $)
    • typical deal sizes (median / average gross approval)
    • the most active lenders (banks by count + volume)
    • approval/volume trends by fiscal year
    • the change-of-ownership share (a direct read on acquisition financing)

Governance: only DERIVED aggregates are surfaced — never a raw borrower row. Even so,
the loader caches raw pulls to a **gitignored** directory (``backend/.sba_cache/``) so
licensed/large source files never enter version control.

Resilience / always-deliver: the loader tries the live dataset first, then a warm cache,
then falls back to a small **shipped sample** (``app/data/sba_sample_7a.csv``) so the
engine and the newsletter always render. ``fetch_sba_dataset`` is a module-level hook so
tests stay fully network-free (monkeypatch it).

TODO(live-data): wire ``SBA_7A_DATASET_URL`` to the current SBA FOIA CSV export and enable
the scheduled refresh. Until then the shipped sample drives the derived figures and every
surface is labelled "illustrative sample" so nothing is misrepresented.
"""

from __future__ import annotations

import csv
import io
import json
import os
import threading
import time
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# Public SBA FOIA export (7(a), FY2020-present). Overridable via env for the live refresh.
# Left unset by default so the engine is deterministic/offline unless explicitly enabled.
SBA_7A_DATASET_URL = os.getenv("SBA_7A_DATASET_URL", "").strip()

USER_AGENT = "John Henry Investments Research (research@johnhenrycapital.com)"
HTTP_TIMEOUT = 30.0
CACHE_TTL_SECONDS = 24 * 3600

_CACHE_DIR = Path(__file__).resolve().parent.parent / ".sba_cache"
_SAMPLE_PATH = Path(__file__).resolve().parent / "data" / "sba_sample_7a.csv"

_MEM_LOCK = threading.Lock()
_MEM_CACHE: dict[str, tuple[float, list["SbaLoan"]]] = {}


class ProviderError(RuntimeError):
    """An SBA dataset fetch failed."""


@dataclass
class SbaLoan:
    """A single derived-safe loan record (aggregation input only)."""

    program: str
    state: str
    naics_code: str
    naics_description: str
    fiscal_year: int
    gross_approval: float
    sba_guaranteed: float
    term_months: int
    bank_name: str
    jobs_supported: int
    business_type: str

    @property
    def is_change_of_ownership(self) -> bool:
        return "change of ownership" in self.business_type.strip().lower()


@dataclass
class IndustryFunding:
    naics_code: str
    naics_description: str
    loan_count: int
    total_gross_approval: float
    avg_gross_approval: float
    median_gross_approval: float
    change_of_ownership_pct: float
    avg_term_months: float


@dataclass
class LenderActivity:
    bank_name: str
    loan_count: int
    total_gross_approval: float


@dataclass
class YearTrend:
    fiscal_year: int
    loan_count: int
    total_gross_approval: float
    avg_gross_approval: float


@dataclass
class SbaIntelligence:
    source: str
    data_mode: str  # "live" | "cache" | "sample"
    as_of: datetime
    loan_count: int
    fiscal_years: list[int]
    total_gross_approval: float
    by_industry: list[IndustryFunding]
    active_lenders: list[LenderActivity]
    yearly_trends: list[YearTrend]
    notes: list[str] = field(default_factory=list)


# --------------------------------------------------------------------------- #
# Fetch / cache / parse
# --------------------------------------------------------------------------- #
def fetch_sba_dataset(url: str) -> str:
    """Download the raw SBA FOIA CSV text. Module-level so tests monkeypatch it.

    Kept intentionally thin (pure stdlib) — parsing/derivation happens downstream.
    """
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT) as response:
            return response.read().decode("utf-8-sig", errors="replace")
    except Exception as exc:  # noqa: BLE001 - normalized to ProviderError
        raise ProviderError(f"SBA dataset fetch failed: {exc}") from exc


def _disk_cache_path() -> Path:
    return _CACHE_DIR / "sba_7a_rows.json"


def _write_disk_cache(loans: list[SbaLoan]) -> None:
    try:
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        payload = {"ts": time.time(), "rows": [loan.__dict__ for loan in loans]}
        _disk_cache_path().write_text(json.dumps(payload), encoding="utf-8")
    except OSError:
        pass  # cache is best-effort; never break generation


def _read_disk_cache() -> list[SbaLoan] | None:
    path = _disk_cache_path()
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if time.time() - float(payload.get("ts", 0)) > CACHE_TTL_SECONDS:
            return None
        return [SbaLoan(**row) for row in payload.get("rows", [])]
    except (OSError, ValueError, TypeError):
        return None


def _to_float(value: str | None) -> float:
    if not value:
        return 0.0
    cleaned = value.replace("$", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _to_int(value: str | None) -> int:
    return int(round(_to_float(value)))


# Real SBA FOIA exports use a stable-ish header vocabulary; map the columns we need
# with a few common aliases so the same parser handles the live file and the sample.
_ALIASES: dict[str, tuple[str, ...]] = {
    "program": ("Program",),
    "state": ("BorrState", "ProjectState"),
    "naics_code": ("NaicsCode",),
    "naics_description": ("NaicsDescription",),
    "fiscal_year": ("ApprovalFiscalYear",),
    "gross_approval": ("GrossApproval",),
    "sba_guaranteed": ("SBAGuaranteedApproval", "SBAGuarantee"),
    "term_months": ("TermInMonths",),
    "bank_name": ("BankName", "ThirdPartyLender_Name", "CDC_Name"),
    "jobs_supported": ("JobsSupported",),
    "business_type": ("BusinessType", "NewBusiness"),
}


def _pick(row: dict[str, str], field_name: str) -> str:
    for alias in _ALIASES[field_name]:
        if alias in row and row[alias] not in (None, ""):
            return row[alias]
    return ""


def parse_sba_csv(text: str) -> list[SbaLoan]:
    """Parse SBA FOIA CSV text → derived-safe loan records (skips unusable rows)."""
    reader = csv.DictReader(io.StringIO(text))
    loans: list[SbaLoan] = []
    for row in reader:
        naics = _pick(row, "naics_code").strip()
        fy = _to_int(_pick(row, "fiscal_year"))
        gross = _to_float(_pick(row, "gross_approval"))
        if not naics or fy <= 0 or gross <= 0:
            continue
        loans.append(
            SbaLoan(
                program=(_pick(row, "program").strip() or "7a"),
                state=_pick(row, "state").strip(),
                naics_code=naics,
                naics_description=_pick(row, "naics_description").strip() or f"NAICS {naics}",
                fiscal_year=fy,
                gross_approval=gross,
                sba_guaranteed=_to_float(_pick(row, "sba_guaranteed")),
                term_months=_to_int(_pick(row, "term_months")),
                bank_name=_pick(row, "bank_name").strip() or "Undisclosed lender",
                jobs_supported=_to_int(_pick(row, "jobs_supported")),
                business_type=_pick(row, "business_type").strip(),
            )
        )
    return loans


def _load_sample() -> list[SbaLoan]:
    return parse_sba_csv(_SAMPLE_PATH.read_text(encoding="utf-8"))


def load_loans(refresh: bool = False) -> tuple[list[SbaLoan], str]:
    """Return (loans, data_mode) with graceful degradation: live → cache → sample.

    ``data_mode`` is one of ``live`` / ``cache`` / ``sample`` so callers can label the
    provenance honestly on-screen.
    """
    if not refresh:
        cached = _read_disk_cache()
        if cached:
            return cached, "cache"

    if SBA_7A_DATASET_URL:
        try:
            text = fetch_sba_dataset(SBA_7A_DATASET_URL)
            loans = parse_sba_csv(text)
            if loans:
                _write_disk_cache(loans)
                return loans, "live"
        except ProviderError:
            pass  # fall through to sample — always deliver

    return _load_sample(), "sample"


# --------------------------------------------------------------------------- #
# Derivation
# --------------------------------------------------------------------------- #
def _median(values: list[float]) -> float:
    vals = sorted(values)
    if not vals:
        return 0.0
    n = len(vals)
    mid = n // 2
    return vals[mid] if n % 2 else (vals[mid - 1] + vals[mid]) / 2.0


def summarize(loans: list[SbaLoan], data_mode: str = "sample", top_n: int = 10) -> SbaIntelligence:
    """Pure aggregation of loan records into the derived intelligence surface."""
    total = sum(loan.gross_approval for loan in loans)
    years = sorted({loan.fiscal_year for loan in loans})

    # Funding by NAICS/industry.
    by_naics: dict[str, list[SbaLoan]] = {}
    for loan in loans:
        by_naics.setdefault(loan.naics_code, []).append(loan)
    industries: list[IndustryFunding] = []
    for naics, group in by_naics.items():
        grosses = [g.gross_approval for g in group]
        coo = sum(1 for g in group if g.is_change_of_ownership)
        industries.append(
            IndustryFunding(
                naics_code=naics,
                naics_description=group[0].naics_description,
                loan_count=len(group),
                total_gross_approval=sum(grosses),
                avg_gross_approval=sum(grosses) / len(grosses),
                median_gross_approval=_median(grosses),
                change_of_ownership_pct=100.0 * coo / len(group),
                avg_term_months=sum(g.term_months for g in group) / len(group),
            )
        )
    industries.sort(key=lambda i: i.total_gross_approval, reverse=True)

    # Active lenders.
    by_bank: dict[str, list[SbaLoan]] = {}
    for loan in loans:
        by_bank.setdefault(loan.bank_name, []).append(loan)
    lenders = [
        LenderActivity(
            bank_name=bank,
            loan_count=len(group),
            total_gross_approval=sum(g.gross_approval for g in group),
        )
        for bank, group in by_bank.items()
    ]
    lenders.sort(key=lambda le: (le.loan_count, le.total_gross_approval), reverse=True)

    # Yearly trends.
    by_year: dict[int, list[SbaLoan]] = {}
    for loan in loans:
        by_year.setdefault(loan.fiscal_year, []).append(loan)
    trends = [
        YearTrend(
            fiscal_year=year,
            loan_count=len(group),
            total_gross_approval=sum(g.gross_approval for g in group),
            avg_gross_approval=sum(g.gross_approval for g in group) / len(group),
        )
        for year, group in sorted(by_year.items())
    ]

    notes: list[str] = []
    if data_mode == "sample":
        notes.append(
            "Illustrative sample dataset (shipped) — connect the live SBA 7(a) FOIA export "
            "to refresh with the full public loan-level records."
        )
    sources = {
        "live": "U.S. Small Business Administration — 7(a) FOIA loan-level data (public).",
        "cache": "U.S. Small Business Administration — 7(a) FOIA loan-level data (cached).",
        "sample": "U.S. Small Business Administration — 7(a) FOIA schema (illustrative sample).",
    }
    return SbaIntelligence(
        source=sources.get(data_mode, sources["sample"]),
        data_mode=data_mode,
        as_of=datetime.now(timezone.utc),
        loan_count=len(loans),
        fiscal_years=years,
        total_gross_approval=total,
        by_industry=industries[:top_n],
        active_lenders=lenders[:top_n],
        yearly_trends=trends,
        notes=notes,
    )


def intelligence(refresh: bool = False, top_n: int = 10) -> SbaIntelligence:
    """Convenience: load (resilient) + summarize, with a short in-memory memo."""
    key = f"intel:{top_n}"
    if not refresh:
        with _MEM_LOCK:
            hit = _MEM_CACHE.get(key)
            if hit and hit[0] > time.time():
                return summarize(hit[1], _mode_for(hit[1]), top_n=top_n)
    loans, mode = load_loans(refresh=refresh)
    with _MEM_LOCK:
        _MEM_CACHE[key] = (time.time() + 300, loans)
        _MEM_MODE[id(loans)] = mode
    return summarize(loans, mode, top_n=top_n)


# Track the provenance of a memoized list so a memo hit reports the same data_mode.
_MEM_MODE: dict[int, str] = {}


def _mode_for(loans: list[SbaLoan]) -> str:
    return _MEM_MODE.get(id(loans), "sample")


def reset_cache() -> None:
    """Clear the in-memory memo (used by tests)."""
    with _MEM_LOCK:
        _MEM_CACHE.clear()
        _MEM_MODE.clear()


def industry_snapshot(intel: SbaIntelligence, naics_prefixes: list[str]) -> IndustryFunding | None:
    """Aggregate the matching NAICS groups into one snapshot for a target industry.

    ``naics_prefixes`` are matched as string prefixes (e.g. ``["2382"]`` catches both
    plumbing/HVAC 238220 and electrical 238210 when a broader trade view is wanted).
    """
    matched = [
        i for i in intel.by_industry
        if any(i.naics_code.startswith(p) for p in naics_prefixes)
    ]
    if not matched:
        return None
    total = sum(i.total_gross_approval for i in matched)
    count = sum(i.loan_count for i in matched)
    if count == 0:
        return None
    # Weight the averages by loan count so the blended snapshot is representative.
    avg = total / count
    med = _median([i.median_gross_approval for i in matched])
    coo = sum(i.change_of_ownership_pct * i.loan_count for i in matched) / count
    term = sum(i.avg_term_months * i.loan_count for i in matched) / count
    label = matched[0].naics_description if len(matched) == 1 else "Selected trades"
    return IndustryFunding(
        naics_code="+".join(i.naics_code for i in matched),
        naics_description=label,
        loan_count=count,
        total_gross_approval=total,
        avg_gross_approval=avg,
        median_gross_approval=med,
        change_of_ownership_pct=coo,
        avg_term_months=term,
    )
