import enum
import uuid
from datetime import datetime, UTC

from sqlalchemy import DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class IncidentSeverity(str, enum.Enum):
    sev1 = "SEV1"
    sev2 = "SEV2"
    sev3 = "SEV3"
    sev4 = "SEV4"


class IncidentStatus(str, enum.Enum):
    open = "OPEN"
    investigating = "INVESTIGATING"
    mitigated = "MITIGATED"  # often a temporary safeguard
    resolved = "RESOLVED"


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    service_name: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[IncidentSeverity] = mapped_column(
        Enum(IncidentSeverity), nullable=False
    )
    status: Mapped[IncidentStatus] = mapped_column(
        Enum(IncidentStatus), nullable=False, default=IncidentStatus.open
    )

    events = relationship(
        "IncidentEvent",
        back_populates="incident",
        cascade="all, delete-orphan",
        order_by="IncidentEvent.created_at",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
