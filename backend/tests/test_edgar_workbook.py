import io
from datetime import datetime, timezone
from uuid import uuid4

import openpyxl
import pytest
from fastapi.testclient import TestClient

from app import edgar_services
from app.edgar_models import EdgarFinancials
from app.edgar_workbook import company_workbook
from app.main import app

client = TestClient(app)


def _fin() -> EdgarFinancials:
    return EdgarFinancials(
        ticker="TEST", cik="0000320193", entity_name="Test Corp",
        fiscal_year=2024, period_end="2024-12-31",
        revenue=1200.0, cost_of_revenue=700.0, gross_profit=500.0,
        operating_income=250.0, net_income=200.0, total_assets=5000.0,
        total_liabilities=3000.0, stockholders_equity=2000.0,
        cash_and_equivalents=800.0, gross_margin=0.4167,
        operating_margin=0.2083, net_margin=0.1667, as_of=datetime.now(timezone.utc),
    )


def test_company_workbook_generates_valid_xlsx():
    data = company_workbook(_fin(), branded=True)
    assert data[:2] == b"PK"  # xlsx is a zip
    wb = openpyxl.load_workbook(io.BytesIO(data))
    ws = wb["Company Financials"]
    joined = " ".join(str(c.value) for row in ws.iter_rows() for c in row if c.value)
    assert "Test Corp" in joined
    assert "Revenue" in joined
    assert "John Henry Investments" in joined  # branded line present


def _register(plan: str) -> str:
    unique = uuid4().hex[:10]
    resp = client.post("/api/v1/auth/register", json={
        "organization_name": f"WB Test {unique}",
        "full_name": "Jordan Lee",
        "email": f"wb-{unique}@example.com",
        "password": "SecurePass123",
        "plan": plan,
    })
    assert resp.status_code == 201
    return resp.json()["access_token"]


@pytest.fixture
def _mock_edgar(monkeypatch):
    monkeypatch.setattr(edgar_services, "company_tickers",
                        lambda: {"0": {"cik_str": 320193, "ticker": "TEST", "title": "Test Corp"}})

    def _facts(_cik):
        def a(v):
            return {"end": "2024-12-31", "val": v, "fy": 2024, "fp": "FY", "form": "10-K"}
        return {"entityName": "Test Corp", "facts": {"us-gaap": {
            "Revenues": {"units": {"USD": [a(1200)]}},
            "NetIncomeLoss": {"units": {"USD": [a(200)]}},
        }}}

    monkeypatch.setattr(edgar_services, "company_facts", _facts)
    edgar_services.reset_cache()
    yield
    edgar_services.reset_cache()


def test_export_denied_for_consumer_t3(_mock_edgar):
    token = _register("consumer")
    resp = client.get("/api/v1/fundamentals/edgar/TEST/export.xlsx",
                      headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403


def test_export_allowed_for_professional_t2(_mock_edgar):
    token = _register("professional")
    resp = client.get("/api/v1/fundamentals/edgar/TEST/export.xlsx",
                      headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert "spreadsheetml" in resp.headers["content-type"]
    assert resp.content[:2] == b"PK"


def test_export_allowed_for_enterprise_t1(_mock_edgar):
    token = _register("enterprise")
    resp = client.get("/api/v1/fundamentals/edgar/TEST/export.xlsx",
                      headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200


def test_export_requires_auth():
    resp = client.get("/api/v1/fundamentals/edgar/TEST/export.xlsx")
    assert resp.status_code == 401
