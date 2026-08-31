from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.models.ownership import Ownership
from app.models.service_record import ServiceRecord
from app.models.vehicle import Vehicle
from app.models.vehicle_details import VehicleDetails
from app.schemas.vehicle_profile import VehicleProfileResponse


def get_vehicle_profile(
    db: Session,
    vehicle_id: int,
) -> VehicleProfileResponse:
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
        .order_by(ServiceRecord.service_date.desc())
        .all()
    )

    incidents = (
        db.query(Incident)
        .filter(Incident.vehicle_id == vehicle_id)
        .order_by(Incident.incident_date.desc())
        .all()
    )

    return VehicleProfileResponse(
        id=vehicle.id,
        registration_number=vehicle.registration_number,
        created_at=vehicle.created_at,
        details=details,
        ownership=ownership,
        service_records=service_records,
        incidents=incidents,
    )
