from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.vehicle_report import VehicleReportResponse
from app.services.vehicle_report import get_vehicle_report

router = APIRouter(
    prefix="/vehicles/{vehicle_id}/report",
    tags=["vehicle-report"],
)


@router.get(
    "",
    response_model=VehicleReportResponse,
    status_code=status.HTTP_200_OK,
)
def get_report(
    vehicle_id: int,
    db: Session = Depends(get_db),
) -> VehicleReportResponse:
    try:
        return get_vehicle_report(db, vehicle_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
