from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config import get_settings
from app.database import engine, init_db
from app.rate_limit import RateLimitMiddleware
from app.routers import (
    accounting,
    agents,
    auth,
    bea,
    billing,
    crm,
    dashboards,
    deal_xray,
    financial_diligence,
    integrations,
    leads,
    market,
    mobile_auth,
    pipeline,
    reports,
    research,
    support,
    valuations,
)

get_settings().validate()
init_db()

app = FastAPI(
    title="John Henry Investments Backend",
    version="0.1.0",
    description=(
        "Backend API for general journal accounting entries, audit reports, "
        "financial reports, executive dashboards, CRM workflows, and external integrations."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware)

app.include_router(accounting.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(mobile_auth.router, prefix="/api/v1")
app.include_router(billing.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")
app.include_router(dashboards.router, prefix="/api/v1")
app.include_router(crm.router, prefix="/api/v1")
app.include_router(market.router, prefix="/api/v1")
app.include_router(bea.router, prefix="/api/v1")
app.include_router(research.router, prefix="/api/v1")
app.include_router(valuations.router, prefix="/api/v1")
app.include_router(deal_xray.router, prefix="/api/v1")
app.include_router(financial_diligence.router, prefix="/api/v1")
app.include_router(pipeline.router, prefix="/api/v1")
app.include_router(support.router, prefix="/api/v1")
app.include_router(agents.router, prefix="/api/v1")
app.include_router(leads.router, prefix="/api/v1")
app.include_router(integrations.router, prefix="/api/v1")


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "John Henry Investments Backend",
        "status": "online",
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/ready")
def ready() -> dict[str, str]:
    """Readiness probe: verifies the database is reachable."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001 - report not-ready on any DB failure
        raise HTTPException(status_code=503, detail="Database not ready.") from exc
    return {"status": "ready"}
