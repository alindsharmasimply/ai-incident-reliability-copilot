from datetime import datetime

from pydantic import BaseModel, Field

from app.models.alert import AlertStatus
from app.models.incident import IncidentSeverity


class AlertCreate(BaseModel):
    source: str = Field(min_length=2, max_length=100)
    service_name: str = Field(min_length=2, max_length=100)
    alert_type: str = Field(min_length=2, max_length=100)
    title: str = Field(min_length=3, max_length=255)
    description: str | None = None
    severity: IncidentSeverity
    idempotency_key: str | None = Field(default=None, max_length=255)
    payload: dict | None = None


class AlertResponse(BaseModel):
    id: str
    idempotency_key: str
    source: str
    service_name: str
    alert_type: str
    title: str
    description: str | None
    severity: IncidentSeverity
    status: AlertStatus
    incident_id: str | None
    received_at: datetime
    duplicate: bool = False

    model_config = {"from_attributes": True}
