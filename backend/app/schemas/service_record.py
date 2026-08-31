from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ServiceRecordCreate(BaseModel):
    service_date: date
    service_type: str
    odometer_reading: int | None = None
    description: str | None = None
    service_center: str | None = None
    cost: Decimal | None = None


class ServiceRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vehicle_id: int
    service_date: date
    service_type: str
    odometer_reading: int | None
    description: str | None
    service_center: str | None
    cost: Decimal | None
    created_at: datetime
