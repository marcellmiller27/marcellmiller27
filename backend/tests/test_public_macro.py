import pytest
from fastapi.testclient import TestClient

from app import public_macro_services as pms
from app.main import app
from app.public_macro_services import PublicMacroService

client = TestClient(app)


@pytest.fixture(autouse=True)
def _clear_cache():
    pms.reset_cache()
    yield
    pms.reset_cache()


def test_treasury_parses_debt(monkeypatch):
    monkeypatch.setattr(pms, "fetch_treasury_debt", lambda: {
        "record_date": "2026-07-14",
        "tot_pub_debt_out_amt": "39470152218599.01",
        "debt_held_public_amt": "31751114853068.90",
    })
    r = PublicMacroService().treasury()
    by = {i.key: i for i in r.indicators}
    assert by["total_public_debt"].value == pytest.approx(39470152218599.01)
    assert by["total_public_debt"].period == "2026-07-14"
    assert by["debt_held_by_public"].value == pytest.approx(31751114853068.90)


def test_world_bank_parses_indicators(monkeypatch):
    monkeypatch.setattr(pms, "fetch_world_bank",
                        lambda country, ind: [{"page": 1}, [{"value": 123.0, "date": "2024"}]])
    r = PublicMacroService().world_bank("US")
    assert len(r.indicators) == 5
    assert all(i.value == 123.0 and i.period == "2024" for i in r.indicators)


def test_imf_prefers_latest_actual_over_projection(monkeypatch):
    # 2030 is a future projection; latest actual (<= current year) should win.
    monkeypatch.setattr(pms, "fetch_imf", lambda code, country: {
        "values": {code: {country: {"2023": 2.9, "2024": 2.8, "2030": 1.8}}}
    })
    r = PublicMacroService().imf("USA")
    growth = next(i for i in r.indicators if i.key == "NGDP_RPCH")
    assert growth.value == pytest.approx(2.8)
    assert growth.period == "2024"


def test_oecd_parses_cli(monkeypatch):
    monkeypatch.setattr(pms, "fetch_oecd_cli", lambda country: {
        "data": {"dataSets": [{"observations": {"0:0:0:0:0:0:0:0:0:0": [99.84, 0, 0, 0, None]}}]}
    })
    r = PublicMacroService().oecd("USA")
    cli = r.indicators[0]
    assert cli.key == "cli"
    assert cli.value == pytest.approx(99.84)


def test_endpoints(monkeypatch):
    monkeypatch.setattr(pms, "fetch_treasury_debt", lambda: {
        "record_date": "2026-07-14", "tot_pub_debt_out_amt": "39470152218599.01",
        "debt_held_public_amt": "31751114853068.90",
    })
    monkeypatch.setattr(pms, "fetch_world_bank",
                        lambda country, ind: [{}, [{"value": 1.0, "date": "2024"}]])
    monkeypatch.setattr(pms, "fetch_imf", lambda code, country: {
        "values": {code: {country: {"2024": 2.0}}}})
    monkeypatch.setattr(pms, "fetch_oecd_cli", lambda country: {
        "data": {"dataSets": [{"observations": {"0": [100.0]}}]}})
    for path in ("/api/v1/macro/treasury", "/api/v1/macro/world-bank",
                 "/api/v1/macro/imf", "/api/v1/macro/oecd"):
        resp = client.get(path)
        assert resp.status_code == 200, path
        assert resp.json()["indicators"]


def test_unavailable_on_fetch_error(monkeypatch):
    def _boom(*a, **k):
        raise pms.ProviderError("network down")

    monkeypatch.setattr(pms, "fetch_treasury_debt", _boom)
    r = PublicMacroService().treasury()
    assert r.indicators[0].status == "unavailable"
