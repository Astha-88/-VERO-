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


def test_create_service_record() -> None:
    vehicle_id = create_test_vehicle()

    response = client.post(
        f"/vehicles/{vehicle_id}/service-records",
        json={
            "service_date": "2026-08-30",
            "service_type": "Regular Service",
            "description": "Engine oil and filter replaced",
            "odometer_reading": 45000,
            "service_center": "ABC Motors",
            "cost": "5500.00",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["vehicle_id"] == vehicle_id
    assert data["service_type"] == "Regular Service"
    assert data["description"] == "Engine oil and filter replaced"
    assert data["odometer_reading"] == 45000
    assert data["service_center"] == "ABC Motors"
    assert data["cost"] == "5500.00"
    assert "id" in data
    assert "created_at" in data


def test_create_service_record_vehicle_not_found() -> None:
    response = client.post(
        "/vehicles/999999999/service-records",
        json={
            "service_date": "2026-08-30",
            "service_type": "Regular Service",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle not found"


def test_get_service_records() -> None:
    vehicle_id = create_test_vehicle()

    client.post(
        f"/vehicles/{vehicle_id}/service-records",
        json={
            "service_date": "2026-08-20",
            "service_type": "Repair",
            "description": "Brake pads replaced",
            "cost": "3000.00",
        },
    )

    client.post(
        f"/vehicles/{vehicle_id}/service-records",
        json={
            "service_date": "2026-08-25",
            "service_type": "Regular Service",
            "description": "Oil change",
            "cost": "1500.00",
        },
    )

    response = client.get(
        f"/vehicles/{vehicle_id}/service-records"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["service_date"] == "2026-08-25"
    assert data[1]["service_date"] == "2026-08-20"


def test_get_service_records_empty() -> None:
    vehicle_id = create_test_vehicle()

    response = client.get(
        f"/vehicles/{vehicle_id}/service-records"
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_service_records_vehicle_not_found() -> None:
    response = client.get(
        "/vehicles/999999999/service-records"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle not found"


def test_delete_service_record() -> None:
    vehicle_id = create_test_vehicle()

    create_response = client.post(
        f"/vehicles/{vehicle_id}/service-records",
        json={
            "service_date": "2026-08-30",
            "service_type": "Repair",
            "description": "Tyre replacement",
        },
    )

    assert create_response.status_code == 201

    service_record_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/vehicles/{vehicle_id}/service-records/{service_record_id}"
    )

    assert delete_response.status_code == 204

    response = client.get(
        f"/vehicles/{vehicle_id}/service-records"
    )

    assert response.status_code == 200
    assert response.json() == []


def test_delete_service_record_not_found() -> None:
    vehicle_id = create_test_vehicle()

    response = client.delete(
        f"/vehicles/{vehicle_id}/service-records/999999999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Service record not found"


def test_delete_service_record_wrong_vehicle() -> None:
    vehicle_id = create_test_vehicle()
    other_vehicle_id = create_test_vehicle()

    create_response = client.post(
        f"/vehicles/{vehicle_id}/service-records",
        json={
            "service_date": "2026-08-30",
            "service_type": "Repair",
        },
    )

    assert create_response.status_code == 201

    service_record_id = create_response.json()["id"]

    response = client.delete(
        f"/vehicles/{other_vehicle_id}/service-records/{service_record_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Service record not found"
