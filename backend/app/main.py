from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import accounting, crm, dashboards, reports

app = FastAPI(
    title="John Henry Investments Backend",
    version="0.1.0",
    description=(
        "Backend API for general journal accounting entries, audit reports, "
        "financial reports, executive dashboards, and CRM workflows."
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
app.include_router(reports.router, prefix="/api/v1")
app.include_router(dashboards.router, prefix="/api/v1")
app.include_router(crm.router, prefix="/api/v1")


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
