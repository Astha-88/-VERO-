from pydantic import Field

from app.schemas.incident import IncidentResponse
from app.schemas.ownership import OwnershipResponse
from app.schemas.service_record import ServiceRecordResponse
from app.schemas.vehicle import VehicleResponse
from app.schemas.vehicle_details import VehicleDetailsResponse


class VehicleProfileResponse(VehicleResponse):
    details: VehicleDetailsResponse | None = None
    ownership: list[OwnershipResponse] = Field(default_factory=list)
    service_records: list[ServiceRecordResponse] = Field(default_factory=list)
    incidents: list[IncidentResponse] = Field(default_factory=list)
