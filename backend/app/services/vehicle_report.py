from sqlalchemy.orm import Session

from app.models.external_evidence import ExternalEvidence
from app.schemas.vehicle_report import VehicleReportResponse
from app.services.risk_assessment import get_risk_assessment
from app.services.vehicle_profile import get_vehicle_profile


def get_vehicle_report(
    db: Session,
    vehicle_id: int,
) -> VehicleReportResponse:
    profile = get_vehicle_profile(db, vehicle_id)
    risk_assessment = get_risk_assessment(db, vehicle_id)

    external_evidence = (
        db.query(ExternalEvidence)
        .filter(ExternalEvidence.vehicle_id == vehicle_id)
        .order_by(ExternalEvidence.retrieved_at.desc())
        .all()
    )

    return VehicleReportResponse(
        vehicle=profile,
        external_evidence=external_evidence,        
        risk_assessment=risk_assessment,
    )
