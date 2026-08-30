from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.vehicle_details import (
    VehicleDetailsCreate,
    VehicleDetailsResponse,
)
from app.services.vehicle_details import (
    create_vehicle_details,
    get_vehicle_details,
    update_vehicle_details,
)

router = APIRouter(
    prefix="/vehicles/{vehicle_id}/details",
    tags=["vehicle-details"],
)


@router.post("", response_model=VehicleDetailsResponse, status_code=201)
def create_vehicle_details_endpoint(
    vehicle_id: int,
    details_data: VehicleDetailsCreate,
    db: Session = Depends(get_db),  # noqa: B008
) -> VehicleDetailsResponse:
    try:
        return create_vehicle_details(
            db,
            vehicle_id,
            details_data,
        )
    except ValueError as exc:
        message = str(exc)

        if message == "Vehicle not found":
            raise HTTPException(
                status_code=404,
                detail=message,
            ) from exc

        raise HTTPException(
            status_code=409,
            detail=message,
        ) from exc


@router.get("", response_model=VehicleDetailsResponse)
def get_vehicle_details_endpoint(
    vehicle_id: int,
    db: Session = Depends(get_db),  # noqa: B008
) -> VehicleDetailsResponse:
    try:
        return get_vehicle_details(db, vehicle_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.put("", response_model=VehicleDetailsResponse)
def update_vehicle_details_endpoint(
    vehicle_id: int,
    details_data: VehicleDetailsCreate,
    db: Session = Depends(get_db),  # noqa: B008
) -> VehicleDetailsResponse:
    try:
        return update_vehicle_details(
            db,
            vehicle_id,
            details_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
