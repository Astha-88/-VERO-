from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate


def create_vehicle(db: Session, vehicle_data: VehicleCreate) -> Vehicle:
    vehicle = Vehicle(
        registration_number=vehicle_data.registration_number,
    )

    db.add(vehicle)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError(
            f"Vehicle with registration number "
            f"{vehicle_data.registration_number} already exists"
        )

    db.refresh(vehicle)
    return vehicle
