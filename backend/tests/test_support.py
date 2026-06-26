from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_faq_list_and_category_filter() -> None:
    response = client.get("/api/v1/support/faq")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 10
    assert "Billing" in body["categories"]

    filtered = client.get("/api/v1/support/faq", params={"category": "Billing"})
    assert filtered.status_code == 200
    assert all(item["category"] == "Billing" for item in filtered.json()["items"])
    assert filtered.json()["count"] >= 1


def test_ask_pricing_question() -> None:
    response = client.post("/api/v1/support/ask", json={"question": "how much does it cost?"})
    assert response.status_code == 200
    body = response.json()
    assert body["escalate"] is False
    assert body["category"] == "Billing"
    assert "$50" in body["answer"]


def test_ask_crypto_keys_question() -> None:
    body = client.post(
        "/api/v1/support/ask",
        json={"question": "do you store my crypto wallet private keys?"},
    ).json()
    assert body["escalate"] is False
    assert "non-custodial" in body["answer"].lower()


def test_ask_market_data_realtime_question() -> None:
    body = client.post(
        "/api/v1/support/ask",
        json={"question": "is the market data real time and where is it from"},
    ).json()
    assert body["escalate"] is False
    assert body["category"] == "Market data"


def test_ask_returns_followup_suggestions() -> None:
    body = client.post(
        "/api/v1/support/ask", json={"question": "how do I enable two factor authentication"}
    ).json()
    assert body["escalate"] is False
    assert isinstance(body["suggestions"], list)


def test_ask_low_confidence_escalates() -> None:
    body = client.post(
        "/api/v1/support/ask", json={"question": "zxcvbnm qwerty asdfgh"}
    ).json()
    assert body["escalate"] is True
    assert body["confidence"] == 0.0
    assert body["suggestions"]


def test_ask_validates_empty_question() -> None:
    assert client.post("/api/v1/support/ask", json={"question": ""}).status_code == 422
