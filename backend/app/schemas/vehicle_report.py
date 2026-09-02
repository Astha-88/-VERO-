from pydantic import BaseModel

from app.schemas.risk_assessment import RiskAssessmentResponse
from app.schemas.vehicle_profile import VehicleProfileResponse


class VehicleReportResponse(BaseModel):
    vehicle: VehicleProfileResponse
    risk_assessment: RiskAssessmentResponse
