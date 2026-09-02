import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_test_vehicle() -> tuple[int, str]:
    
    registration_number = f"TR-{uuid.uuid4().hex[:10].upper()}"

    response = client.post(
        "/vehicles",
        json={"registration_number": registration_number},
    )

    assert response.status_code == 201

    data = response.json()

    return data["id"], data["registration_number"]


def test_risk_assessment_low_risk() -> None:
    vehicle_id, _ = create_test_vehicle()

    client.post(
        f"/vehicles/{vehicle_id}/details",
        json={
            "make": "Toyota",
            "model": "Fortuner",
            "manufacturing_year": 2023,
            "fuel_type": "Diesel",
        },
    )

    client.post(
        f"/vehicles/{vehicle_id}/ownership",
        json={
            "owner_sequence": 1,
            "owner_name": "First Owner",
        },
    )

    response = client.get(
        f"/vehicles/{vehicle_id}/risk-assessment"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["risk_score"] == 0
    assert data["risk_level"] == "Low"
    assert data["red_flags"] == []
    assert any(
    "No incident records" in signal
    for signal in data["positive_signals"]
)


def test_risk_assessment_incident_increases_risk() -> None:
    vehicle_id, _ = create_test_vehicle()

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
        f"/vehicles/{vehicle_id}/risk-assessment"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["risk_score"] == 5
    assert data["risk_level"] == "Low"
    assert len(data["red_flags"]) >= 1


def test_risk_assessment_severe_incident_and_high_repair_cost() -> None:
    vehicle_id, _ = create_test_vehicle()

    client.post(
        f"/vehicles/{vehicle_id}/incidents",
        json={
            "incident_type": "Accident",
            "incident_date": "2024-08-15",
            "severity": "Severe",
            "description": "Major accident",
            "reported_by": "Owner",
            "repair_cost": "150000.00",
        },
    )

    response = client.get(
        f"/vehicles/{vehicle_id}/risk-assessment"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["risk_score"] == 45
    assert data["risk_level"] == "Moderate"


def test_risk_assessment_multiple_owners() -> None:
    vehicle_id, _ = create_test_vehicle()

    for sequence in range(1, 4):
        response = client.post(
            f"/vehicles/{vehicle_id}/ownership",
            json={
                "owner_sequence": sequence,
                "owner_name": f"Owner {sequence}",
            },
        )

        assert response.status_code == 201

    response = client.get(
        f"/vehicles/{vehicle_id}/risk-assessment"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["risk_score"] == 10
    assert data["risk_level"] == "Low"


def test_risk_assessment_vehicle_not_found() -> None:
    response = client.get(
        "/vehicles/999999999/risk-assessment"
    )

    assert response.status_code == 404


def test_risk_assessment_score_capped_at_100() -> None:
    vehicle_id, _ = create_test_vehicle()

    for index in range(5):
        response = client.post(
            f"/vehicles/{vehicle_id}/incidents",
            json={
                "incident_type": "Accident",
                "incident_date": "2024-08-15",
                "severity": "Severe",
                "description": f"Severe incident {index}",
                "reported_by": "Owner",
                "repair_cost": "150000.00",
            },
        )

        assert response.status_code == 201

    response = client.get(
        f"/vehicles/{vehicle_id}/risk-assessment"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["risk_score"] == 100
    assert data["risk_level"] == "Very High"
