from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class OwnershipCreate(BaseModel):
    owner_sequence: int
    owner_name: str | None = None
    purchase_date: date | None = None
    transfer_date: date | None = None


class OwnershipResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vehicle_id: int
    owner_sequence: int
    owner_name: str | None
    purchase_date: date | None
    transfer_date: date | None
    created_at: datetime
