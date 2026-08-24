from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VehicleCreate(BaseModel):
    registration_number: str


class VehicleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    registration_number: str
    created_at: datetime
