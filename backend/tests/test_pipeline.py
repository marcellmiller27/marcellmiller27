# JHI-SIG: 69M2705M | Deal Pipeline | John Henry Investments (proprietary)
"""Tests for the Deal Pipeline (save & revisit acquisition analyses)."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
BASE = "/api/v1/pipeline"


def _create(**overrides) -> dict:
    payload = {
        "business_name": "Carrollton Design Build",
        "deal_type": "deal_xray",
        "stage": "analysis",
        "score": 51,
        "recommendation": "Watch",
        "headline": "Construction mgmt · fairly priced",
        "inputs": {"revenue": 12_962_195, "asking_price": 6_200_000},
        "notes": "64% concentration to diligence.",
    }
    payload.update(overrides)
    resp = client.post(f"{BASE}/deals", json=payload)
    assert resp.status_code == 200, resp.text
    return resp.json()


def test_stages_are_ordered() -> None:
    resp = client.get(f"{BASE}/stages")
    assert resp.status_code == 200
    assert resp.json()[:3] == ["screen", "analysis", "qoe"]


def test_create_and_get_roundtrip() -> None:
    created = _create()
    assert created["id"]
    assert created["inputs"]["asking_price"] == 6_200_000
    got = client.get(f"{BASE}/deals/{created['id']}")
    assert got.status_code == 200
    assert got.json()["business_name"] == "Carrollton Design Build"


def test_list_includes_created_deal() -> None:
    created = _create(business_name="List Test Co")
    resp = client.get(f"{BASE}/deals")
    assert resp.status_code == 200
    assert any(d["id"] == created["id"] for d in resp.json())


def test_advance_stage() -> None:
    created = _create()
    resp = client.patch(f"{BASE}/deals/{created['id']}", json={"stage": "qoe"})
    assert resp.status_code == 200
    assert resp.json()["stage"] == "qoe"


def test_invalid_stage_rejected() -> None:
    created = _create()
    resp = client.patch(f"{BASE}/deals/{created['id']}", json={"stage": "not_a_stage"})
    assert resp.status_code == 400


def test_unknown_deal_type_rejected() -> None:
    resp = client.post(f"{BASE}/deals", json={"business_name": "X", "deal_type": "bogus"})
    assert resp.status_code == 400


def test_delete_removes_deal() -> None:
    created = _create()
    d = client.delete(f"{BASE}/deals/{created['id']}")
    assert d.status_code == 200 and d.json()["deleted"] is True
    assert client.get(f"{BASE}/deals/{created['id']}").status_code == 404


def test_get_missing_is_404() -> None:
    assert client.get(f"{BASE}/deals/does-not-exist").status_code == 404
