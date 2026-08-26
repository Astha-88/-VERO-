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


def get_vehicle(db: Session, vehicle_id: int) -> Vehicle:
    vehicle = db.get(Vehicle, vehicle_id)

    if vehicle is None:
        raise ValueError(f"Vehicle with id {vehicle_id} not found")

    return vehicle
