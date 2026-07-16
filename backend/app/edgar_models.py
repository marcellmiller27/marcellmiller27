from datetime import datetime

from pydantic import BaseModel


class EdgarFinancials(BaseModel):
    """Normalized headline annual financials from SEC EDGAR (public, no key).

    Values are the most recent annual (10-K/20-F/40-F) figures reported via XBRL.
    SEC data is US public domain — display and redistribution permitted with a
    declared User-Agent and fair-access compliance.
    """

    ticker: str
    cik: str
    entity_name: str
    fiscal_year: int | None = None
    period_end: str | None = None
    currency: str = "USD"

    revenue: float | None = None
    cost_of_revenue: float | None = None
    gross_profit: float | None = None
    operating_income: float | None = None
    net_income: float | None = None
    total_assets: float | None = None
    total_liabilities: float | None = None
    stockholders_equity: float | None = None
    cash_and_equivalents: float | None = None

    gross_margin: float | None = None
    operating_margin: float | None = None
    net_margin: float | None = None

    source: str = "SEC EDGAR (data.sec.gov)"
    as_of: datetime
    disclaimer: str = (
        "Public SEC XBRL data (most recent annual filing). For research/analysis; "
        "verify against the original filing before relying on it."
    )


class EdgarYear(BaseModel):
    fiscal_year: int
    revenue: float | None = None
    cost_of_revenue: float | None = None
    gross_profit: float | None = None
    operating_income: float | None = None
    net_income: float | None = None
    total_assets: float | None = None
    total_liabilities: float | None = None
    stockholders_equity: float | None = None
    cash_and_equivalents: float | None = None
    gross_margin: float | None = None
    operating_margin: float | None = None
    net_margin: float | None = None


class EdgarHistory(BaseModel):
    ticker: str
    cik: str
    entity_name: str
    currency: str = "USD"
    years: list[EdgarYear]
    source: str = "SEC EDGAR (data.sec.gov)"
    as_of: datetime
    disclaimer: str = (
        "Public SEC XBRL annual data. For research/analysis; verify against the filings."
    )
