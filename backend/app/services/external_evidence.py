from sqlalchemy.orm import Session

from app.models.external_evidence import ExternalEvidence
from app.models.vehicle import Vehicle
from app.services.external_vehicle_data import get_external_vehicle_data


def refresh_external_evidence(
    db: Session,
    vehicle_id: int,
) -> list[ExternalEvidence]:
    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == vehicle_id)
        .first()
    )

    if vehicle is None:
        raise ValueError("Vehicle not found")

    external_data = get_external_vehicle_data(vehicle.registration_number)

    # Replace previous API Sathi snapshot for this vehicle.
    db.query(ExternalEvidence).filter(
        ExternalEvidence.vehicle_id == vehicle_id,
        ExternalEvidence.source == "api_sathi",
    ).delete(synchronize_session=False)

    rc_evidence = ExternalEvidence(
        vehicle_id=vehicle_id,
        source="api_sathi",
        evidence_type="rc_verification",
        source_record_id=external_data["registration_number"],
        data={
            "registration": external_data["registration"],
            "vehicle": external_data["vehicle"],
            "insurance": external_data["insurance"],
            "data_limitations": external_data["data_limitations"],
        },
    )

    db.add(rc_evidence)

    for challan in external_data["compliance"]["challans"]:
        db.add(
            ExternalEvidence(
                vehicle_id=vehicle_id,
                source="api_sathi",
                evidence_type="challan",
                source_record_id=challan["challan_no"],
                data=challan,
            )
        )

    db.commit()

    return (
        db.query(ExternalEvidence)
        .filter(
            ExternalEvidence.vehicle_id == vehicle_id,
            ExternalEvidence.source == "api_sathi",
        )
        .order_by(ExternalEvidence.retrieved_at.desc())
        .all()
    )
