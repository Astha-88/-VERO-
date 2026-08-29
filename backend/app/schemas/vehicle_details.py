from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VehicleDetailsCreate(BaseModel):
    make: str | None = None
    model: str | None = None
    variant: str | None = None
    manufacturing_year: int | None = None
    fuel_type: str | None = None


class VehicleDetailsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vehicle_id: int
    make: str | None
    model: str | None
    variant: str | None
    manufacturing_year: int | None
    fuel_type: str | None
    created_at: datetime
