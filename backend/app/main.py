from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers import (
    accounting,
    auth,
    billing,
    crm,
    dashboards,
    integrations,
    market,
    mobile_auth,
    reports,
    research,
    support,
    valuations,
)

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

app.include_router(accounting.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(mobile_auth.router, prefix="/api/v1")
app.include_router(billing.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")
app.include_router(dashboards.router, prefix="/api/v1")
app.include_router(crm.router, prefix="/api/v1")
app.include_router(market.router, prefix="/api/v1")
app.include_router(research.router, prefix="/api/v1")
app.include_router(valuations.router, prefix="/api/v1")
app.include_router(support.router, prefix="/api/v1")
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
