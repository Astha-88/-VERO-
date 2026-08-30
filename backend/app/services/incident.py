from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.models.vehicle import Vehicle
from app.schemas.incident import IncidentCreate


def create_incident(
    db: Session,
    vehicle_id: int,
    incident_data: IncidentCreate,
) -> Incident:
    vehicle = db.get(Vehicle, vehicle_id)

    if vehicle is None:
        raise ValueError("Vehicle not found")

    incident = Incident(
        vehicle_id=vehicle_id,
        **incident_data.model_dump(),
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


def get_incidents(
    db: Session,
    vehicle_id: int,
) -> list[Incident]:
    vehicle = db.get(Vehicle, vehicle_id)

    if vehicle is None:
        raise ValueError("Vehicle not found")

    return (
        db.query(Incident)
        .filter(Incident.vehicle_id == vehicle_id)
        .order_by(Incident.incident_date.desc())
        .all()
    )


def delete_incident(
    db: Session,
    vehicle_id: int,
    incident_id: int,
) -> None:
    incident = (
        db.query(Incident)
        .filter(
            Incident.id == incident_id,
            Incident.vehicle_id == vehicle_id,
        )
        .first()
    )

    if incident is None:
        raise ValueError("Incident record not found")

    db.delete(incident)
    db.commit()
