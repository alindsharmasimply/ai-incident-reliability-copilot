from datetime import UTC, datetime
import enum
import uuid

from sqlalchemy import (
    JSON,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.incident import IncidentSeverity


class AlertStatus(str, enum.Enum):
    received = "RECEIVED"
    deduplicated = "DEDUPLICATED"
    processed = "PROCESSED"
    failed = "FAILED"


class Alert(Base):
    __tablename__ = "alerts"

    __table_args__ = (
        UniqueConstraint("idempotency_key", name="uq_alerts_idempotency_key"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    idempotency_key: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )

    source: Mapped[str] = mapped_column(String(100), nullable=False)

    service_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    alert_type: Mapped[str] = mapped_column(String(100), nullable=False)

    description: Mapped[str] = mapped_column(Text, nullable=True)

    severity: Mapped[str] = mapped_column(Enum(IncidentSeverity), nullable=False)

    status: Mapped[AlertStatus] = mapped_column(
        Enum(AlertStatus), nullable=False, default=AlertStatus.received
    )

    payload: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    incident_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("incidents.id"),
        nullable=True,
        index=True,
    )

    received_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
        index=True,
    )

    incident = relationship("Incident")
