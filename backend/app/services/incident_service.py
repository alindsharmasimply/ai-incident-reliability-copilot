from fastapi import HTTPException
from sqlalchemy.orm import Session, selectinload

from app.models.incident import Incident
from app.models.incident_event import IncidentEvent, IncidentEventType
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
        db.flush()  # Avoids committing the incident to the db so that the incident.id can be used within the same transaction

        event = IncidentEvent(
            incident_id=incident.id,
            event_type=IncidentEventType.created,
            message=f"Event created for service {payload.service_name}",
            created_by="system",
        )
        db.add(event)
        db.commit()
        db.refresh(
            incident
        )  # Pulls the absolute freshest data back from the database into the python object

        return self.get_incident_by_id(db, incident_id=incident.id)

    def list_incidents(self, db: Session) -> list[Incident]:
        return db.query(Incident).order_by(Incident.created_at.desc()).all()

    def get_incident_by_id(self, db: Session, incident_id: str) -> Incident:
        incident = (
            db.query(Incident)
            .options(selectinload(Incident.events))
            .filter(Incident.id == incident_id)
            .first()
        )
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        return incident

    def delete_incident(self, db: Session, id: str) -> None:
        db.query(Incident).filter(Incident.id == id).delete(synchronize_session="fetch")
        db.commit()

    def get_incident_timeline(
        self, db: Session, incident_id: str
    ) -> list[IncidentEvent]:
        incident = self.get_incident_by_id(db, incident_id=incident_id)
        return incident.events
