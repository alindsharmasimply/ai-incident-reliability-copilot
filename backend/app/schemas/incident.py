from datetime import datetime
from pydantic import BaseModel, Field

from app.models.incident import IncidentSeverity, IncidentStatus


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
