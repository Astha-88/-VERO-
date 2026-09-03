from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.services.external_vehicle_data import get_external_vehicle_data

router = APIRouter(
    prefix="/external-lookup",
    tags=["external-lookup"],
)


class ExternalVehicleLookupRequest(BaseModel):
    registration_number: str


@router.post("")
def external_vehicle_lookup(
    request: ExternalVehicleLookupRequest,
):
    try:
        return get_external_vehicle_data(
            request.registration_number
        )

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"External vehicle data provider failed: {exc}",
	)from exc
