from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_vehicle() -> None:
    registration_number = f"MH{uuid4().hex[:8].upper()}"

    response = client.post(
        "/vehicles",
        json={"registration_number": registration_number},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["registration_number"] == registration_number
    assert "id" in data
    assert "created_at" in data


def test_create_duplicate_vehicle() -> None:
    registration_number = f"KA{uuid4().hex[:8].upper()}"

    first_response = client.post(
        "/vehicles",
        json={"registration_number": registration_number},
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/vehicles",
        json={"registration_number": registration_number},
    )

    assert second_response.status_code == 409

    assert (
        second_response.json()["detail"]
        == f"Vehicle with registration number {registration_number} already exists"
    )
def test_get_vehicle() -> None:
    registration_number = f"DL{uuid4().hex[:8].upper()}"

    create_response = client.post(
        "/vehicles",
        json={"registration_number": registration_number},
    )

    assert create_response.status_code == 201

    vehicle_id = create_response.json()["id"]

    response = client.get(f"/vehicles/{vehicle_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == vehicle_id
    assert data["registration_number"] == registration_number


def test_get_vehicle_not_found() -> None:
    response = client.get("/vehicles/999999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle with id 999999999 not found"


def test_list_vehicles() -> None:
    registration_number = f"DL{uuid4().hex[:8].upper()}"

    create_response = client.post(
        "/vehicles",
        json={"registration_number": registration_number},
    )

    assert create_response.status_code == 201

    response = client.get("/vehicles?limit=1000&offset=0")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "limit" in data
    assert "offset" in data
    assert "total" in data

    assert data["limit"] == 1000
    assert data["offset"] == 0
    assert data["total"] >= 1

    registrations = [
        vehicle["registration_number"]
        for vehicle in data["items"]
    ]

    assert registration_number in registrations


def test_list_vehicles_pagination() -> None:
    registration_numbers = [
        f"UP{uuid4().hex[:8].upper()}"
        for _ in range(3)
    ]

    for registration_number in registration_numbers:
        response = client.post(
            "/vehicles",
            json={"registration_number": registration_number},
        )
        assert response.status_code == 201

    response = client.get("/vehicles?limit=2&offset=0")

    assert response.status_code == 200

    data = response.json()

    assert data["limit"] == 2
    assert data["offset"] == 0
    assert len(data["items"]) == 2
    assert data["total"] >= 3
