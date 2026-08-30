from sqlalchemy.orm import Session

from app.models.ownership import Ownership
from app.models.vehicle import Vehicle
from app.schemas.ownership import OwnershipCreate


def create_ownership(
    db: Session,
    vehicle_id: int,
    ownership_data: OwnershipCreate,
) -> Ownership:
    vehicle = db.get(Vehicle, vehicle_id)

    if vehicle is None:
        raise ValueError("Vehicle not found")

    ownership = Ownership(
        vehicle_id=vehicle_id,
        **ownership_data.model_dump(),
    )

    db.add(ownership)
    db.commit()
    db.refresh(ownership)

    return ownership


def get_ownership(
    db: Session,
    vehicle_id: int,
) -> list[Ownership]:
    vehicle = db.get(Vehicle, vehicle_id)

    if vehicle is None:
        raise ValueError("Vehicle not found")

    return (
        db.query(Ownership)
        .filter(Ownership.vehicle_id == vehicle_id)
        .order_by(Ownership.owner_sequence)
        .all()
    )


def delete_ownership(
    db: Session,
    ownership_id: int,
) -> None:
    ownership = db.get(Ownership, ownership_id)

    if ownership is None:
        raise ValueError("Ownership record not found")

    db.delete(ownership)
    db.commit()
