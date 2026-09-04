from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.due_diligence import DueDiligenceStepResponse
from app.services.due_diligence import get_vehicle_steps

router = APIRouter(
    prefix="/vehicles/{vehicle_id}/due-diligence",
    tags=["due-diligence"],
)


@router.get(
    "",
    response_model=list[DueDiligenceStepResponse],
)
def get_due_diligence_steps(
    vehicle_id: int,
    db: Session = Depends(get_db),
) -> list[DueDiligenceStepResponse]:
    steps = get_vehicle_steps(db, vehicle_id)

    if not steps:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No due-diligence steps found for this vehicle",
        )

    return steps
