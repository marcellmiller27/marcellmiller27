# JHI-SIG: 69M2705M | Acquisition Intelligence Framework | JHI Research & Analytics Firm, Inc. (proprietary)
"""Pydantic models for the Aegira Acquisition Intelligence Framework.

Educational + interactive module for search-fund / ETA / SMB acquirers.
Governance: all outputs are derived-only, fact-locked, and research-not-advice.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

# --- Framework elements (explainer + tool link + checklist) -------------------


class ElementExplainer(BaseModel):
    how_to: str
    what_to_look_for: list[str]
    why_it_matters: str


class ElementTool(BaseModel):
    label: str
    href: str
    description: str


class FrameworkElement(BaseModel):
    id: str
    name: str
    summary: str
    explainer: ElementExplainer
    tool: ElementTool
    checklist: list[str]


class FrameworkElementList(BaseModel):
    elements: list[FrameworkElement]
    disclaimer: str


# --- Key financial ratios -----------------------------------------------------


class RatioDefinition(BaseModel):
    key: str
    name: str
    category: str
    formula: str
    unit: str  # "x" | "%" | "ratio" | "$"
    plain_english: str
    benchmark: str
    higher_is_better: bool | None = None


class RatioCatalog(BaseModel):
    ratios: list[RatioDefinition]
    disclaimer: str


class RatioInputs(BaseModel):
    revenue: float | None = None
    cogs: float | None = None
    operating_expenses: float | None = None
    operating_income: float | None = None
    net_income: float | None = None
    ebitda: float | None = None
    sde: float | None = None
    purchase_price: float | None = None
    total_debt: float | None = None
    total_equity: float | None = None
    current_assets: float | None = None
    current_liabilities: float | None = None
    inventory: float | None = None
    annual_debt_service: float | None = None


class RatioResult(BaseModel):
    key: str
    name: str
    category: str
    unit: str
    value: float | None
    display: str
    status: str  # strong | adequate | caution | weak | reference | n/a
    interpretation: str
    benchmark: str


class RatioReport(BaseModel):
    results: list[RatioResult]
    summary: str
    disclaimer: str


# --- Due-diligence framework / checklist --------------------------------------


class DDItem(BaseModel):
    id: str
    text: str
    priority: str  # critical | standard


class DDCategory(BaseModel):
    id: str
    name: str
    purpose: str
    items: list[DDItem]


class DueDiligenceChecklist(BaseModel):
    categories: list[DDCategory]
    total_items: int
    disclaimer: str


# --- Industry analysis (derived sector benchmarks) ----------------------------


class SectorBenchmark(BaseModel):
    sector: str
    gross_margin_pct: float
    operating_margin_pct: float
    net_margin_pct: float
    revenue_growth_pct: float
    ev_ebitda_multiple: float
    note: str


class IndustryBenchmarks(BaseModel):
    sectors: list[SectorBenchmark]
    basis: str
    disclaimer: str


# --- Market analysis (TAM / competitive landscape template) -------------------


class MarketWorksheetField(BaseModel):
    key: str
    label: str
    hint: str


class MarketSection(BaseModel):
    id: str
    name: str
    guidance: str
    prompts: list[str]


class MarketAnalysisTemplate(BaseModel):
    sections: list[MarketSection]
    tam_worksheet: list[MarketWorksheetField]
    five_forces: list[str]
    disclaimer: str


# --- Lead-gen funnel (email-gated free toolkit) -------------------------------


class ToolkitRequest(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    full_name: str | None = Field(default=None, max_length=255)


class ToolkitResource(BaseModel):
    title: str
    body: str
    href: str | None = None


class ToolkitResponse(BaseModel):
    status: str  # captured | already_on_list
    message: str
    resources: list[ToolkitResource]
    cta_label: str
    cta_href: str
    disclaimer: str
