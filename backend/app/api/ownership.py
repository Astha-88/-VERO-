
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.ownership import OwnershipCreate, OwnershipResponse
from app.services.ownership import (
    create_ownership,
    delete_ownership,
    get_ownership,
)

router = APIRouter(
    prefix="/vehicles/{vehicle_id}/ownership",
    tags=["ownership"],
)


@router.post(
    "",
    response_model=OwnershipResponse,
    status_code=201,
)
def create_ownership_endpoint(
    vehicle_id: int,
    ownership_data: OwnershipCreate,
    db: Session = Depends(get_db),
) -> OwnershipResponse:
    try:
        return create_ownership(
            db,
            vehicle_id,
            ownership_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[OwnershipResponse],
)
def get_ownership_endpoint(
    vehicle_id: int,
    db: Session = Depends(get_db),
) -> list[OwnershipResponse]:
    try:
        return get_ownership(db, vehicle_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{ownership_id}",
    status_code=204,
)
def delete_ownership_endpoint(
    vehicle_id: int,
    ownership_id: int,
    db: Session = Depends(get_db),
) -> None:
    try:
        ownership_records = get_ownership(db, vehicle_id)

        if not any(
            record.id == ownership_id
            for record in ownership_records
        ):
            raise ValueError("Ownership record not found")

        delete_ownership(db, ownership_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
