from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def auth_headers() -> dict:
    unique = uuid4().hex[:10]
    registered = client.post(
        "/api/v1/auth/register",
        json={
            "organization_name": f"Crypto Org {unique}",
            "full_name": "Crypto Holder",
            "email": f"crypto-{unique}@example.com",
            "password": "SecurePass123",
            "plan": "consumer",
        },
    ).json()
    return {"Authorization": f"Bearer {registered['access_token']}"}


def test_networks_are_public_and_non_custodial() -> None:
    response = client.get("/api/v1/crypto/networks")
    assert response.status_code == 200
    body = response.json()
    assert body["custody_model"] == "non_custodial_watch_only"
    keys = {network["key"] for network in body["networks"]}
    assert {"bitcoin", "ethereum", "xrpl", "stellar"}.issubset(keys)


def test_add_watch_only_holdings_for_each_asset() -> None:
    headers = auth_headers()
    samples = [
        ("bitcoin", "BTC", "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq"),
        ("ethereum", "ETH", "0x52908400098527886E0F7030069857D2E4169EE7"),
        ("xrpl", "XRP", "rPEPPER7kfTD9w2To4CQk6UCfuHM9c6GDY"),
        ("stellar", "XLM", "G" + "A" * 55),
    ]
    for network, asset, address in samples:
        response = client.post(
            "/api/v1/crypto/holdings",
            headers=headers,
            json={
                "network": network,
                "asset_symbol": asset,
                "address": address,
                "quantity": "1.5",
                "label": f"My {asset} wallet",
            },
        )
        assert response.status_code == 201, (network, response.json())
        body = response.json()
        assert body["custody_model"] == "non_custodial_watch_only"
        assert body["asset_symbol"] == asset


def test_quantity_only_holding_without_address_is_allowed() -> None:
    headers = auth_headers()
    response = client.post(
        "/api/v1/crypto/holdings",
        headers=headers,
        json={"network": "ethereum", "asset_symbol": "USDC", "quantity": "250"},
    )
    assert response.status_code == 201
    assert response.json()["address"] is None


def test_private_key_hex_is_rejected() -> None:
    headers = auth_headers()
    private_key = "0x" + "a" * 64
    response = client.post(
        "/api/v1/crypto/holdings",
        headers=headers,
        json={"network": "ethereum", "asset_symbol": "ETH", "address": private_key},
    )
    assert response.status_code == 422
    assert "private key" in response.json()["detail"].lower()


def test_seed_phrase_is_rejected() -> None:
    headers = auth_headers()
    mnemonic = "legal winner thank year wave sausage worth useful legal winner thank yellow"
    response = client.post(
        "/api/v1/crypto/holdings",
        headers=headers,
        json={"network": "bitcoin", "asset_symbol": "BTC", "notes": mnemonic},
    )
    assert response.status_code == 422
    assert "seed phrase" in response.json()["detail"].lower()


def test_wif_private_key_is_rejected() -> None:
    headers = auth_headers()
    wif = "5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ"
    response = client.post(
        "/api/v1/crypto/holdings",
        headers=headers,
        json={"network": "bitcoin", "asset_symbol": "BTC", "address": wif},
    )
    assert response.status_code == 422


def test_invalid_address_for_network_is_rejected() -> None:
    headers = auth_headers()
    response = client.post(
        "/api/v1/crypto/holdings",
        headers=headers,
        json={"network": "bitcoin", "asset_symbol": "BTC", "address": "not-a-btc-address"},
    )
    assert response.status_code == 400


def test_list_summary_and_delete_flow() -> None:
    headers = auth_headers()
    client.post(
        "/api/v1/crypto/holdings",
        headers=headers,
        json={"network": "bitcoin", "asset_symbol": "BTC", "quantity": "0.5"},
    )
    created = client.post(
        "/api/v1/crypto/holdings",
        headers=headers,
        json={"network": "bitcoin", "asset_symbol": "BTC", "quantity": "0.25"},
    ).json()

    listing = client.get("/api/v1/crypto/holdings", headers=headers)
    assert listing.status_code == 200
    assert len(listing.json()) == 2

    summary = client.get("/api/v1/crypto/holdings/summary", headers=headers)
    assert summary.status_code == 200
    assert summary.json()["by_asset"]["BTC"] == "0.75"

    deleted = client.delete(f"/api/v1/crypto/holdings/{created['id']}", headers=headers)
    assert deleted.status_code == 204
    assert len(client.get("/api/v1/crypto/holdings", headers=headers).json()) == 1


def test_holdings_are_scoped_per_user() -> None:
    headers_a = auth_headers()
    headers_b = auth_headers()
    client.post(
        "/api/v1/crypto/holdings",
        headers=headers_a,
        json={"network": "xrpl", "asset_symbol": "XRP", "quantity": "100"},
    )
    assert len(client.get("/api/v1/crypto/holdings", headers=headers_b).json()) == 0


def test_holdings_require_authentication() -> None:
    response = client.get("/api/v1/crypto/holdings")
    assert response.status_code == 401
