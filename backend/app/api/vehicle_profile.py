from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.vehicle_profile import VehicleProfileResponse
from app.services.vehicle_profile import get_vehicle_profile

router = APIRouter(
    prefix="/vehicles/{vehicle_id}/profile",
    tags=["vehicle-profile"],
)


@router.get("", response_model=VehicleProfileResponse)
def get_vehicle_profile_endpoint(
    vehicle_id: int,
    db: Session = Depends(get_db),  # noqa: B008
) -> VehicleProfileResponse:
    try:
        return get_vehicle_profile(db, vehicle_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
