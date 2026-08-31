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
    return response.json()["id"], registration_number


def test_get_vehicle_profile() -> None:
    vehicle_id, registration_number  = create_test_vehicle()

    client.post(
        f"/vehicles/{vehicle_id}/details",
        json={
            "make": "Toyota",
            "model": "Fortuner",
            "variant": "4x4",
            "manufacturing_year": 2022,
            "fuel_type": "Diesel",
        },
    )

    client.post(
        f"/vehicles/{vehicle_id}/ownership",
        json={
            "owner_sequence": 1,
            "owner_name": "First Owner",
            "purchase_date": "2022-01-15",
            "transfer_date": "2024-03-10",
        },
    )

    client.post(
        f"/vehicles/{vehicle_id}/service-records",
        json={
            "service_date": "2024-06-20",
            "service_type": "Regular Service",
            "description": "Oil change",
            "cost": "2500.00",
        },
    )

    client.post(
        f"/vehicles/{vehicle_id}/incidents",
        json={
            "incident_type": "Accident",
            "incident_date": "2024-08-15",
            "severity": "Minor",
            "description": "Minor bumper damage",
            "reported_by": "Owner",
            "repair_cost": "12000.00",
        },
    )

    response = client.get(
        f"/vehicles/{vehicle_id}/profile"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == vehicle_id
    assert data["registration_number"] == registration_number

    assert data["details"]["make"] == "Toyota"
    assert data["details"]["model"] == "Fortuner"

    assert len(data["ownership"]) == 1
    assert data["ownership"][0]["owner_name"] == "First Owner"

    assert len(data["service_records"]) == 1
    assert data["service_records"][0]["service_type"] == "Regular Service"

    assert len(data["incidents"]) == 1
    assert data["incidents"][0]["incident_type"] == "Accident"


def test_get_vehicle_profile_empty_related_data() -> None:
    vehicle_id,_ = create_test_vehicle()

    response = client.get(
        f"/vehicles/{vehicle_id}/profile"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == vehicle_id
    assert data["details"] is None
    assert data["ownership"] == []
    assert data["service_records"] == []
    assert data["incidents"] == []


def test_get_vehicle_profile_not_found() -> None:
    response = client.get(
        "/vehicles/999999999/profile"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle not found"
