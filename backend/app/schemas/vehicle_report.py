from pydantic import BaseModel

from app.schemas.external_evidence import ExternalEvidenceResponse
from app.schemas.risk_assessment import RiskAssessmentResponse
from app.schemas.vehicle_profile import VehicleProfileResponse


class VehicleReportResponse(BaseModel):
    vehicle: VehicleProfileResponse
    external_evidence: list[ExternalEvidenceResponse]
    risk_assessment: RiskAssessmentResponse
