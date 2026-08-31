from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.service_record import (
    ServiceRecordCreate,
    ServiceRecordResponse,
)
from app.services.service_record import (
    create_service_record,
    delete_service_record,
    get_service_records,
)

router = APIRouter(
    prefix="/vehicles/{vehicle_id}/service-records",
    tags=["service-records"],
)


@router.post(
    "",
    response_model=ServiceRecordResponse,
    status_code=201,
)
def create_service_record_endpoint(
    vehicle_id: int,
    service_data: ServiceRecordCreate,
    db: Session = Depends(get_db),  # noqa: B008
) -> ServiceRecordResponse:
    try:
        return create_service_record(
            db,
            vehicle_id,
            service_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[ServiceRecordResponse],
)
def get_service_records_endpoint(
    vehicle_id: int,
    db: Session = Depends(get_db),  # noqa: B008
) -> list[ServiceRecordResponse]:
    try:
        return get_service_records(
            db,
            vehicle_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{service_record_id}",
    status_code=204,
)
def delete_service_record_endpoint(
    vehicle_id: int,
    service_record_id: int,
    db: Session = Depends(get_db),  # noqa: B008
) -> None:
    try:
        delete_service_record(
            db,
            vehicle_id,
            service_record_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
