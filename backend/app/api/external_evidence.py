from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.external_evidence import ExternalEvidenceResponse
from app.services.external_evidence import refresh_external_evidence

router = APIRouter(
    prefix="/vehicles/{vehicle_id}/external-evidence",
    tags=["external-evidence"],
)


@router.post(
    "/refresh",
    response_model=list[ExternalEvidenceResponse],
)
def refresh_vehicle_external_evidence(
    vehicle_id: int,
    db: Session = Depends(get_db),
) -> list[ExternalEvidenceResponse]:
    try:
        return refresh_external_evidence(db, vehicle_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"External vehicle data provider failed: {exc}",
        ) from exc
