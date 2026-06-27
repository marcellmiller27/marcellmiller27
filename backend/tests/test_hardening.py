import pytest
from fastapi.testclient import TestClient

from app import rate_limit
from app.config import Settings
from app.main import app

client = TestClient(app)


def test_health_and_ready() -> None:
    assert client.get("/health").json()["status"] == "healthy"
    assert client.get("/ready").json()["status"] == "ready"


def test_config_validation_blocks_unsafe_production(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("AUTH_JWT_SECRET", "development-only-change-me")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./x.db")
    with pytest.raises(RuntimeError):
        Settings().validate()


def test_config_validation_ok_in_dev(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "development")
    Settings().validate()  # no raise


def test_config_validation_ok_with_real_prod_secret(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("AUTH_JWT_SECRET", "x" * 40)  # >= 32 bytes
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://u:p@db:5432/jhi")
    Settings().validate()  # no raise


def test_config_validation_rejects_short_prod_secret(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("AUTH_JWT_SECRET", "too-short-secret")  # < 32 bytes
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://u:p@db:5432/jhi")
    with pytest.raises(RuntimeError):
        Settings().validate()


def test_rate_limit_is_env_gated(monkeypatch) -> None:
    rate_limit.reset()
    monkeypatch.setenv("RATE_LIMIT_PER_MINUTE", "3")
    statuses = [client.get("/api/v1/leads/count").status_code for _ in range(5)]
    assert 429 in statuses  # throttled after the limit
    rate_limit.reset()


def test_rate_limit_off_by_default() -> None:
    rate_limit.reset()
    # No RATE_LIMIT_PER_MINUTE env -> never throttles.
    assert all(client.get("/api/v1/leads/count").status_code == 200 for _ in range(6))


def test_fundamentals_status_gated_by_key(monkeypatch) -> None:
    monkeypatch.delenv("NASDAQ_DATA_LINK_API_KEY", raising=False)
    monkeypatch.delenv("FUNDAMENTALS_API_KEY", raising=False)
    assert client.get("/api/v1/research/fundamentals-status").json()["available"] is False

    monkeypatch.setenv("NASDAQ_DATA_LINK_API_KEY", "test-key")
    body = client.get("/api/v1/research/fundamentals-status").json()
    assert body["available"] is True
    assert body["provider"] == "sharadar_sf1"


def test_providers_include_sharadar() -> None:
    providers = {p["key"] for p in client.get("/api/v1/market/providers").json()["providers"]}
    assert "sharadar_sf1" in providers
