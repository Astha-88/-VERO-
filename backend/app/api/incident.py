from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.incident import IncidentCreate, IncidentResponse
from app.services.incident import (
    create_incident,
    delete_incident,
    get_incidents,
)

router = APIRouter(
    prefix="/vehicles/{vehicle_id}/incidents",
    tags=["incidents"],
)


@router.post(
    "",
    response_model=IncidentResponse,
    status_code=201,
)
def create_incident_endpoint(
    vehicle_id: int,
    incident_data: IncidentCreate,
    db: Session = Depends(get_db),  # noqa: B008
) -> IncidentResponse:
    try:
        return create_incident(
            db,
            vehicle_id,
            incident_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[IncidentResponse],
)
def get_incidents_endpoint(
    vehicle_id: int,
    db: Session = Depends(get_db),  # noqa: B008
) -> list[IncidentResponse]:
    try:
        return get_incidents(db, vehicle_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{incident_id}",
    status_code=204,
)
def delete_incident_endpoint(
    vehicle_id: int,
    incident_id: int,
    db: Session = Depends(get_db),  # noqa: B008
) -> None:
    try:
        delete_incident(
            db,
            vehicle_id,
            incident_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
