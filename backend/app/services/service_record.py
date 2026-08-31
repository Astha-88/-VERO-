from sqlalchemy.orm import Session

from app.models.service_record import ServiceRecord
from app.models.vehicle import Vehicle
from app.schemas.service_record import ServiceRecordCreate


def create_service_record(
    db: Session,
    vehicle_id: int,
    service_data: ServiceRecordCreate,
) -> ServiceRecord:
    vehicle = db.get(Vehicle, vehicle_id)

    if vehicle is None:
        raise ValueError("Vehicle not found")

    service_record = ServiceRecord(
        vehicle_id=vehicle_id,
        **service_data.model_dump(),
    )

    db.add(service_record)
    db.commit()
    db.refresh(service_record)

    return service_record


def get_service_records(
    db: Session,
    vehicle_id: int,
) -> list[ServiceRecord]:
    vehicle = db.get(Vehicle, vehicle_id)

    if vehicle is None:
        raise ValueError("Vehicle not found")

    return (
        db.query(ServiceRecord)
        .filter(ServiceRecord.vehicle_id == vehicle_id)
        .order_by(ServiceRecord.service_date.desc())
        .all()
    )


def delete_service_record(
    db: Session,
    vehicle_id: int,
    service_record_id: int,
) -> None:
    service_record = db.get(ServiceRecord, service_record_id)

    if (
        service_record is None
        or service_record.vehicle_id != vehicle_id
    ):
        raise ValueError("Service record not found")

    db.delete(service_record)
    db.commit()
