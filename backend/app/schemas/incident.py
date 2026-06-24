from datetime import datetime
from pydantic import BaseModel, Field

from app.models.incident import IncidentSeverity, IncidentStatus
from app.models.incident_event import IncidentEventType


class IncidentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    description: str | None = None
    service_name: str = Field(min_length=2, max_length=100)
    severity: IncidentSeverity


class IncidentResponse(BaseModel):
    id: str
    title: str
    description: str | None
    service_name: str
    severity: IncidentSeverity
    status: IncidentStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class IncidentEventResponse(BaseModel):
    id: str
    incident_id: str
    event_type: IncidentEventType
    message: str
    created_by: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class IncidentDetailResponse(IncidentResponse):
    events: list[IncidentEventResponse] = []
