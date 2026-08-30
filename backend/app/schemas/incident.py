from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class IncidentCreate(BaseModel):
    incident_type: str
    incident_date: date
    severity: str
    description: str | None = None
    reported_by: str | None = None
    repair_cost: Decimal | None = None


class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vehicle_id: int
    incident_type: str
    incident_date: date
    severity: str
    description: str | None
    reported_by: str | None
    repair_cost: Decimal | None
    created_at: datetime
