from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_test_vehicle() -> int:
    registration_number = f"DL{uuid4().hex[:8].upper()}"

    response = client.post(
        "/vehicles",
        json={"registration_number": registration_number},
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_create_vehicle_details() -> None:
    vehicle_id = create_test_vehicle()

    response = client.post(
        f"/vehicles/{vehicle_id}/details",
        json={
            "make": "Maruti Suzuki",
            "model": "Swift",
            "variant": "ZXI",
            "manufacturing_year": 2022,
            "fuel_type": "Petrol",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["vehicle_id"] == vehicle_id
    assert data["make"] == "Maruti Suzuki"
    assert data["model"] == "Swift"
    assert data["variant"] == "ZXI"
    assert data["manufacturing_year"] == 2022
    assert data["fuel_type"] == "Petrol"
    assert "id" in data
    assert "created_at" in data


def test_create_vehicle_details_vehicle_not_found() -> None:
    response = client.post(
        "/vehicles/999999/details",
        json={
            "make": "Maruti Suzuki",
            "model": "Swift",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle not found"


def test_create_duplicate_vehicle_details() -> None:
    vehicle_id = create_test_vehicle()

    payload = {
        "make": "Hyundai",
        "model": "i20",
        "variant": "Sportz",
        "manufacturing_year": 2021,
        "fuel_type": "Petrol",
    }

    first_response = client.post(
        f"/vehicles/{vehicle_id}/details",
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        f"/vehicles/{vehicle_id}/details",
        json=payload,
    )

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Vehicle details already exist"


def test_get_vehicle_details() -> None:
    vehicle_id = create_test_vehicle()

    client.post(
        f"/vehicles/{vehicle_id}/details",
        json={
            "make": "Honda",
            "model": "City",
            "variant": "VX",
            "manufacturing_year": 2020,
            "fuel_type": "Petrol",
        },
    )

    response = client.get(
        f"/vehicles/{vehicle_id}/details",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["vehicle_id"] == vehicle_id
    assert data["make"] == "Honda"
    assert data["model"] == "City"


def test_get_vehicle_details_not_found() -> None:
    response = client.get(
        "/vehicles/999999/details",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle details not found"


def test_update_vehicle_details() -> None:
    vehicle_id = create_test_vehicle()

    client.post(
        f"/vehicles/{vehicle_id}/details",
        json={
            "make": "Toyota",
            "model": "Innova",
            "variant": "GX",
            "manufacturing_year": 2019,
            "fuel_type": "Diesel",
        },
    )

    response = client.put(
        f"/vehicles/{vehicle_id}/details",
        json={
            "make": "Toyota",
            "model": "Innova Crysta",
            "variant": "ZX",
            "manufacturing_year": 2021,
            "fuel_type": "Diesel",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["vehicle_id"] == vehicle_id
    assert data["make"] == "Toyota"
    assert data["model"] == "Innova Crysta"
    assert data["variant"] == "ZX"
    assert data["manufacturing_year"] == 2021
    assert data["fuel_type"] == "Diesel"


def test_update_vehicle_details_not_found() -> None:
    response = client.put(
        "/vehicles/999999/details",
        json={
            "make": "Toyota",
            "model": "Fortuner",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle details not found"
