from app import market_services


def _fake_payload():
    return {"Results": {"series": [{"data": [{"year": "2024", "period": "M01", "value": "300.0"}]}]}}


def test_bls_uses_registered_v2_when_key_present(monkeypatch):
    captured: dict[str, str] = {}

    def fake_get(url, data=None):
        captured["url"] = url
        return _fake_payload()

    monkeypatch.setattr(market_services, "_http_get_json", fake_get)
    monkeypatch.setenv("BLS_API_KEY", "abc123")
    market_services.bls_cpi_series()
    assert "publicAPI/v2" in captured["url"]
    assert "registrationkey=abc123" in captured["url"]


def test_bls_falls_back_to_v1_when_no_key(monkeypatch):
    captured: dict[str, str] = {}

    def fake_get(url, data=None):
        captured["url"] = url
        return _fake_payload()

    monkeypatch.setattr(market_services, "_http_get_json", fake_get)
    monkeypatch.delenv("BLS_API_KEY", raising=False)
    monkeypatch.delenv("BLS_REGISTRATION_KEY", raising=False)
    market_services.bls_cpi_series()
    assert "publicAPI/v1" in captured["url"]
    assert "registrationkey" not in captured["url"]


def test_bls_registration_key_alias(monkeypatch):
    monkeypatch.delenv("BLS_API_KEY", raising=False)
    monkeypatch.setenv("BLS_REGISTRATION_KEY", "xyz")
    assert market_services.bls_api_key() == "xyz"
