from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.ai_summary import AISummaryResponse
from app.services.ai_summary import generate_ai_summary
from app.services.vehicle_report import get_vehicle_report

router = APIRouter(
    prefix="/vehicles/{vehicle_id}/ai-summary",
    tags=["ai-summary"],
)


@router.get("", response_model=AISummaryResponse, status_code=status.HTTP_200_OK)
def get_ai_summary(
    vehicle_id: int,
    db: Session = Depends(get_db),
) -> AISummaryResponse:
    try:
        report = get_vehicle_report(db, vehicle_id)
        report_data = report.model_dump(mode="json")
        return generate_ai_summary(report_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
