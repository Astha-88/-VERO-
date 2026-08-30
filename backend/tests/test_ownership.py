from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_test_vehicle() -> int:
    registration_number = f"DL01{uuid4().hex[:8].upper()}"
    response = client.post(
        "/vehicles",
        json={
            "registration_number": registration_number,
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_create_ownership() -> None:
    vehicle_id = create_test_vehicle()

    response = client.post(
        f"/vehicles/{vehicle_id}/ownership",
        json={
            "owner_sequence": 1,
            "owner_name": "Test Owner",
            "purchase_date": "2024-01-15",
            "transfer_date": None,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["vehicle_id"] == vehicle_id
    assert data["owner_sequence"] == 1
    assert data["owner_name"] == "Test Owner"
    assert data["purchase_date"] == "2024-01-15"
    assert data["transfer_date"] is None


def test_create_ownership_vehicle_not_found() -> None:
    response = client.post(
        "/vehicles/999999/ownership",
        json={
            "owner_sequence": 1,
            "owner_name": "Test Owner",
            "purchase_date": "2024-01-15",
        },
    )

    assert response.status_code == 404


def test_get_ownership() -> None:
    vehicle_id = create_test_vehicle()

    client.post(
        f"/vehicles/{vehicle_id}/ownership",
        json={
            "owner_sequence": 1,
            "owner_name": "First Owner",
            "purchase_date": "2022-01-01",
            "transfer_date": "2024-01-01",
        },
    )

    client.post(
        f"/vehicles/{vehicle_id}/ownership",
        json={
            "owner_sequence": 2,
            "owner_name": "Second Owner",
            "purchase_date": "2024-01-01",
        },
    )

    response = client.get(
        f"/vehicles/{vehicle_id}/ownership",
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["owner_sequence"] == 1
    assert data[1]["owner_sequence"] == 2


def test_get_ownership_vehicle_not_found() -> None:
    response = client.get(
        "/vehicles/999999/ownership",
    )

    assert response.status_code == 404


def test_delete_ownership() -> None:
    vehicle_id = create_test_vehicle()

    create_response = client.post(
        f"/vehicles/{vehicle_id}/ownership",
        json={
            "owner_sequence": 1,
            "owner_name": "Test Owner",
            "purchase_date": "2024-01-15",
        },
    )

    ownership_id = create_response.json()["id"]

    response = client.delete(
        f"/vehicles/{vehicle_id}/ownership/{ownership_id}",
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/vehicles/{vehicle_id}/ownership",
    )

    assert get_response.status_code == 200
    assert get_response.json() == []


def test_delete_ownership_not_found() -> None:
    vehicle_id = create_test_vehicle()

    response = client.delete(
        f"/vehicles/{vehicle_id}/ownership/999999",
    )

    assert response.status_code == 404


def test_delete_ownership_wrong_vehicle() -> None:
    vehicle_id = create_test_vehicle()
    other_vehicle_id = create_test_vehicle()

    create_response = client.post(
        f"/vehicles/{vehicle_id}/ownership",
        json={
            "owner_sequence": 1,
            "owner_name": "Test Owner",
            "purchase_date": "2024-01-15",
        },
    )

    ownership_id = create_response.json()["id"]

    response = client.delete(
        f"/vehicles/{other_vehicle_id}/ownership/{ownership_id}",
    )

    assert response.status_code == 404

    get_response = client.get(
        f"/vehicles/{vehicle_id}/ownership",
    )

    assert get_response.status_code == 200
    assert len(get_response.json()) == 1
