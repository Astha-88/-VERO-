from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.vehicle import VehicleCreate, VehicleResponse
from app.services.vehicle import create_vehicle, get_vehicle

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.post("", response_model=VehicleResponse, status_code=201)
def create_vehicle_endpoint(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db),  # noqa: B008
) -> VehicleResponse:
    try:
        return create_vehicle(db, vehicle_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc


@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle_endpoint(
    vehicle_id: int,
    db: Session = Depends(get_db),  # noqa: B008
) -> VehicleResponse:
    try:
        return get_vehicle(db, vehicle_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
