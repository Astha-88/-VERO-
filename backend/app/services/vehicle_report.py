from sqlalchemy.orm import Session

from app.schemas.vehicle_report import VehicleReportResponse
from app.services.risk_assessment import get_risk_assessment
from app.services.vehicle_profile import get_vehicle_profile


def get_vehicle_report(
    db: Session,
    vehicle_id: int,
) -> VehicleReportResponse:
    profile = get_vehicle_profile(db, vehicle_id)
    risk_assessment = get_risk_assessment(db, vehicle_id)

    return VehicleReportResponse(
        vehicle=profile,
        risk_assessment=risk_assessment,
    )
