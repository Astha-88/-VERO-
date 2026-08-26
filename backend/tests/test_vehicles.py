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
