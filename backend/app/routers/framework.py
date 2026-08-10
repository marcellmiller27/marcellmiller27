# JHI-SIG: 69M2705M | Acquisition Intelligence Framework | JHI Research & Analytics Firm, Inc. (proprietary)
"""Router for the Aegira Acquisition Intelligence Framework.

Serves the educational framework elements, the key-financial-ratios engine, the
due-diligence checklist, derived industry benchmarks, the market-analysis template,
and an email-gated lead-gen toolkit that reuses the newsletter/lead capture.
"""

import re
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.db_models import LeadDB
from app.framework_content import (
    DUE_DILIGENCE_CHECKLIST,
    FRAMEWORK_ELEMENTS,
    INDUSTRY_BENCHMARKS,
    MARKET_ANALYSIS_TEMPLATE,
    RATIO_CATALOG,
    RESEARCH_DISCLAIMER,
    TOOLKIT_CTA_HREF,
    TOOLKIT_CTA_LABEL,
    TOOLKIT_RESOURCES,
)
from app.framework_models import (
    DueDiligenceChecklist,
    FrameworkElementList,
    IndustryBenchmarks,
    MarketAnalysisTemplate,
    RatioCatalog,
    RatioInputs,
    RatioReport,
    ToolkitRequest,
    ToolkitResponse,
)
from app.framework_ratios import compute_ratios

router = APIRouter(prefix="/framework", tags=["framework"])

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@router.get("/elements", response_model=FrameworkElementList)
def elements() -> FrameworkElementList:
    """The ten framework elements: explainer + Aegira tool link + checklist."""
    return FRAMEWORK_ELEMENTS


@router.get("/ratios/catalog", response_model=RatioCatalog)
def ratios_catalog() -> RatioCatalog:
    """Definitions, formulas, plain-English meaning, and benchmark bands for each ratio."""
    return RATIO_CATALOG


@router.post("/ratios/compute", response_model=RatioReport)
def ratios_compute(payload: RatioInputs) -> RatioReport:
    """Compute + interpret key financial ratios from supplied figures (derived-only)."""
    return compute_ratios(payload)


@router.get("/due-diligence", response_model=DueDiligenceChecklist)
def due_diligence() -> DueDiligenceChecklist:
    """Comprehensive, categorized due-diligence checklist (exportable client-side)."""
    return DUE_DILIGENCE_CHECKLIST


@router.get("/industry-benchmarks", response_model=IndustryBenchmarks)
def industry_benchmarks() -> IndustryBenchmarks:
    """Derived sector benchmarks (margins / growth / multiples) from EDGAR/SF1 aggregates."""
    return INDUSTRY_BENCHMARKS


@router.get("/market-analysis", response_model=MarketAnalysisTemplate)
def market_analysis() -> MarketAnalysisTemplate:
    """TAM/SAM/SOM worksheet + five-forces + competitive-landscape template."""
    return MARKET_ANALYSIS_TEMPLATE


@router.post("/toolkit", response_model=ToolkitResponse, status_code=status.HTTP_201_CREATED)
def toolkit(payload: ToolkitRequest, db: Annotated[Session, Depends(get_db)]) -> ToolkitResponse:
    """Email-gated free entry: capture a lead, then return the acquisition toolkit + CTA."""
    email = payload.email.strip().lower()
    if not _EMAIL_RE.match(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Enter a valid email.")

    existing = db.scalar(select(LeadDB).where(LeadDB.email == email))
    if existing is not None:
        outcome = "already_on_list"
        message = "Welcome back — your Acquisition Intelligence toolkit is unlocked below."
    else:
        db.add(
            LeadDB(
                email=email,
                full_name=(payload.full_name.strip() if payload.full_name else None),
                interest="Acquisition Intelligence",
                source="acquisition-intelligence-toolkit",
            )
        )
        db.commit()
        outcome = "captured"
        message = "You're in — your Acquisition Intelligence toolkit is unlocked below."

    return ToolkitResponse(
        status=outcome,
        message=message,
        resources=TOOLKIT_RESOURCES,
        cta_label=TOOLKIT_CTA_LABEL,
        cta_href=TOOLKIT_CTA_HREF,
        disclaimer=RESEARCH_DISCLAIMER,
    )


@router.get("/lead-count")
def lead_count(db: Annotated[Session, Depends(get_db)]) -> dict[str, int]:
    """Count of toolkit leads captured (funnel telemetry)."""
    count = db.scalar(
        select(func.count())
        .select_from(LeadDB)
        .where(LeadDB.source == "acquisition-intelligence-toolkit")
    )
    return {"count": count or 0}
