import hashlib
import json

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.alert import Alert, AlertStatus
from app.models.incident import Incident
from app.models.incident_event import IncidentEvent, IncidentEventType
from app.schemas.alert import AlertCreate


class AlertService:
    def generate_idempotency_key(self, payload: AlertCreate):
        if payload.idempotency_key:
            return payload.idempotency_key

        fingerprint_source = {
            "source": payload.source,
            "service_name": payload.service_name,
            "alert_type": payload.alert_type,
            "title": payload.title,
            "severity": payload.severity,
        }

        raw = json.dumps(fingerprint_source, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    # The boolean response signifies whether the alert is a duplicate
    def ingest_alert(self, db: Session, payload: AlertCreate) -> tuple[Alert, bool]:
        idempotency_key = self.generate_idempotency_key(payload)

        existing_alert = (
            db.query(Alert).filter(Alert.idempotency_key == idempotency_key).first()
        )

        if existing_alert:
            return existing_alert, True  # a duplicate, hence true

        incident = Incident(
            title=payload.title,
            description=payload.description,
            service_name=payload.service_name,
            severity=payload.severity,
        )

        db.add(incident)
        db.flush()

        alert = Alert(
            idempotency_key=idempotency_key,
            source=payload.source,
            service_name=payload.service_name,
            alert_type=payload.alert_type,
            title=payload.title,
            description=payload.description,
            severity=payload.severity,
            status=AlertStatus.processed,
            payload=payload.payload,
            incident_id=incident.id,
        )

        event = IncidentEvent(
            incident_id=incident.id,
            event_type=IncidentEventType.created,
            message=f"Incident created from alert type {payload.alert_type}",
            created_by=payload.source,
        )

        db.add(alert)
        db.add(event)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()

            existing_alert = (
                db.query(Alert).filter(Alert.idempotency_key == idempotency_key).first()
            )

            if existing_alert:
                return existing_alert, True  # a duplicate, hence true

            raise

        db.refresh(alert)

        return alert, False  # not a duplicate, hence false
