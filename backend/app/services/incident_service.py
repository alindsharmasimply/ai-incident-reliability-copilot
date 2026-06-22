from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.schemas.incident import IncidentCreate


class IncidentService:
    def create_incident(self, db: Session, payload: IncidentCreate) -> Incident:
        incident = Incident(
            title=payload.title,
            description=payload.description,
            service_name=payload.service_name,
            severity=payload.severity,
        )

        db.add(incident)
        db.commit()
        db.refresh(incident)

        return incident

    def list_incidents(self, db: Session) -> list[Incident]:
        return db.query(Incident).order_by(Incident.created_at.desc()).all()
