def test_get_parcel_types(client):
    response = client.get("/parcel-types")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "items" in data
    assert len(data["items"]) == 3

    names = [item["name"] for item in data["items"]]

    assert "одежда" in names
    assert "электроника" in names
    assert "разное" in names

