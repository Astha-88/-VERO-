from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.models.vehicle_details import VehicleDetails
from app.schemas.vehicle_details import VehicleDetailsCreate


def create_vehicle_details(
    db: Session,
    vehicle_id: int,
    details_data: VehicleDetailsCreate,
) -> VehicleDetails:
    vehicle = db.get(Vehicle, vehicle_id)

    if vehicle is None:
        raise ValueError("Vehicle not found")

    existing_details = (
        db.query(VehicleDetails)
        .filter(VehicleDetails.vehicle_id == vehicle_id)
        .first()
    )

    if existing_details is not None:
        raise ValueError("Vehicle details already exist")

    details = VehicleDetails(
        vehicle_id=vehicle_id,
        **details_data.model_dump(),
    )

    db.add(details)
    db.commit()
    db.refresh(details)

    return details


def get_vehicle_details(
    db: Session,
    vehicle_id: int,
) -> VehicleDetails:
    details = (
        db.query(VehicleDetails)
        .filter(VehicleDetails.vehicle_id == vehicle_id)
        .first()
    )

    if details is None:
        raise ValueError("Vehicle details not found")

    return details


def update_vehicle_details(
    db: Session,
    vehicle_id: int,
    details_data: VehicleDetailsCreate,
) -> VehicleDetails:
    details = get_vehicle_details(db, vehicle_id)

    for field, value in details_data.model_dump().items():
        setattr(details, field, value)

    db.commit()
    db.refresh(details)

    return details
