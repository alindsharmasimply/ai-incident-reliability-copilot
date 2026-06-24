import enum
import uuid
from datetime import datetime, UTC

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class IncidentEventType(str, enum.Enum):
    created = "CREATED"
    acknowledged = "ACKNOWLEDGED"
    status_changed = "STATUS_CHANGED"
    severity_changed = "SEVERITY_CHANGED"
    note_added = "NOTE_ADDED"
    diagnosis_started = "DIAGNOSIS_STARTED"
    diagnosis_completed = "DIAGNOSIS_COMPLETED"


class IncidentEvent(Base):
    __tablename__ = "incident_events"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    incident_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("incidents.id"),
        nullable=False,
        index=True,
    )

    event_type: Mapped[IncidentEventType] = mapped_column(
        Enum(IncidentEventType),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(Text, nullable=False)

    created_by: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
        index=True,
    )

    incident = relationship("Incident", back_populates="events")