from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DueDiligenceStepResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vehicle_id: int
    step_type: str
    status: str
    source: str | None = None
    cost: float | None = None
    notes: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
