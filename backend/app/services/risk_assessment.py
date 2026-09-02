from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.models.ownership import Ownership
from app.models.service_record import ServiceRecord
from app.models.vehicle import Vehicle
from app.models.vehicle_details import VehicleDetails
from app.schemas.risk_assessment import RiskAssessmentResponse


def get_risk_assessment(
    db: Session,
    vehicle_id: int,
) -> RiskAssessmentResponse:
    vehicle = db.get(Vehicle, vehicle_id)

    if vehicle is None:
        raise ValueError("Vehicle not found")

    details = (
        db.query(VehicleDetails)
        .filter(VehicleDetails.vehicle_id == vehicle_id)
        .first()
    )

    ownership = (
        db.query(Ownership)
        .filter(Ownership.vehicle_id == vehicle_id)
        .order_by(Ownership.owner_sequence)
        .all()
    )

    service_records = (
        db.query(ServiceRecord)
        .filter(ServiceRecord.vehicle_id == vehicle_id)
        .all()
    )

    incidents = (
        db.query(Incident)
        .filter(Incident.vehicle_id == vehicle_id)
        .all()
    )

    score = 0
    red_flags: list[str] = []
    positive_signals: list[str] = []

    # Incident risk
    for incident in incidents:
        severity = incident.severity.lower()

        if severity == "severe":
            score += 25
            red_flags.append("Severe accident or incident reported.")
        elif severity == "moderate":
            score += 15
            red_flags.append("Moderate accident or incident reported.")
        elif severity == "minor":
            score += 5
            red_flags.append("Minor accident or incident reported.")
        else:
            score += 10
            red_flags.append(
                f"Incident reported with {incident.severity} severity."
            )

        if incident.repair_cost is not None:
            repair_cost = float(incident.repair_cost)

            if repair_cost >= 100000:
                score += 20
                red_flags.append(
                    "Incident has reported repair costs of ₹1,00,000 or more."
                )
            elif repair_cost >= 50000:
                score += 10
                red_flags.append(
                    "Incident has reported repair costs between ₹50,000 and ₹1,00,000."
                )

    if not incidents:
    	positive_signals.append(
        	"No incident records are present in the supplied data."
    	)
    # Ownership risk
    owner_count = len(ownership)

    if owner_count == 0:
        pass
    elif owner_count == 1:
        positive_signals.append("Vehicle has a single recorded owner.")
    elif owner_count == 2:
        score += 5
        red_flags.append("Vehicle has had 2 recorded owners.")
    elif owner_count == 3:
        score += 10
        red_flags.append("Vehicle has had 3 recorded owners.")
    else:
        score += 15
        red_flags.append(
            f"Vehicle has had {owner_count} recorded owners."
        )

    # Vehicle age
    if details is not None and details.manufacturing_year is not None:
        current_year = datetime.now(UTC).year
        age = current_year - details.manufacturing_year

        if age >= 11:
            score += 10
            red_flags.append(
                f"Vehicle is approximately {age} years old."
            )
        elif age >= 6:
            score += 5
            red_flags.append(
                f"Vehicle is approximately {age} years old."
            )
        else:
            positive_signals.append(
                f"Vehicle is approximately {age} years old."
            )

    # Service history
    if service_records:
        positive_signals.append(
            f"{len(service_records)} service record(s) are available."
        )

    score = min(score, 100)

    if score >= 75:
        risk_level = "Very High"
    elif score >= 50:
        risk_level = "High"
    elif score >= 25:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    return RiskAssessmentResponse(
        risk_score=score,
        risk_level=risk_level,
        red_flags=red_flags,
        positive_signals=positive_signals,
    )
