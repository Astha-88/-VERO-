from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ExternalEvidenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vehicle_id: int
    source: str
    evidence_type: str
    source_record_id: str | None = None
    data: dict
    retrieved_at: datetime
