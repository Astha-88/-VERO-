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
