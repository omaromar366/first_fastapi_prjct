from fastapi.testclient import TestClient

from app.main import app

from unittest.mock import patch


def test_create_parcel(client):
    payload = {
        "name": "Nike shoes",
        "weight": "1.5",
        "type_id": 1,
        "declared_value_usd": "120",
    }

    response = client.post("/parcels", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Nike shoes"
    assert data["weight"] == "1.50"
    assert data["parcel_type"]["id"] == 1
    assert data["declared_value_usd"] == "120.00"
    assert "session_id" in response.cookies

def test_get_parcels_returns_only_current_session_parcels(client):
    first_payload = {
        "name": "Jacket",
        "weight": "1.2",
        "type_id": 1,
        "declared_value_usd": "100",
    }

    second_payload = {
        "name": "Phone",
        "weight": "0.4",
        "type_id": 2,
        "declared_value_usd": "300",
    }

    client.post("/parcels", json=first_payload)
    client.post("/parcels", json=second_payload)

    response = client.get("/parcels")

    assert response.status_code == 200

    data = response.json()

    items = data["items"]

    assert len(items) == 2

    names = [item["name"] for item in items]
    assert "Jacket" in names
    assert "Phone" in names

    other_client = TestClient(app)
    other_response = other_client.get("/parcels")

    assert other_response.status_code == 200
    assert other_response.json() == {"items": []}

def test_get_parcel_by_id_only_for_owner(client):
    payload = {
        "name": "MacBook",
        "weight": "2.0",
        "type_id": 2,
        "declared_value_usd": "1500",
    }

    create_response = client.post("/parcels", json=payload)

    assert create_response.status_code == 200

    parcel_id = create_response.json()["id"]

    response = client.get(f"/parcels/{parcel_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "MacBook"

    other_client = TestClient(app)

    forbidden_response = other_client.get(f"/parcels/{parcel_id}")

    assert forbidden_response.status_code == 404

@patch("app.services.calculate_delivery.get_usd_to_rub_rate")
def test_calculate_delivery_cost(mock_rate, client):
    mock_rate.return_value = 100

    payload = {
        "name": "Laptop",
        "weight": "2.0",
        "type_id": 2,
        "declared_value_usd": "1000",
    }

    create_response = client.post("/parcels", json=payload)

    assert create_response.status_code == 200

    response = client.post("/parcels/calculate")

    assert response.status_code == 200

    data = response.json()

    items = data["items"]

    assert len(items) == 1

    parcel = items[0]

    expected_cost = ((2.0 * 0.5) + (1000 * 0.01)) * 100

    assert float(parcel["delivery_cost_rub"]) == expected_cost