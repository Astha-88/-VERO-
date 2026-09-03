from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.risk_assessment import RiskAssessmentResponse
from app.services.risk_assessment import get_risk_assessment

router = APIRouter(
    prefix="/vehicles/{vehicle_id}/risk-assessment",
    tags=["risk-assessment"],
)


@router.get("", response_model=RiskAssessmentResponse)
def get_risk_assessment_endpoint(
    vehicle_id: int,
    db: Session = Depends(get_db),
) -> RiskAssessmentResponse:
    try:
        return get_risk_assessment(db, vehicle_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
