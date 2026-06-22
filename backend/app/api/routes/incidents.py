from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.incident import IncidentCreate, IncidentResponse
from app.services.incident_service import IncidentService

router = APIRouter(prefix="/incidents", tags=["Incidents"])

service = IncidentService()


@router.post("", response_model=IncidentResponse)
def create_incident(
    payload: IncidentCreate,
    db: Session = Depends(get_db),
):
    return service.create_incident(db, payload)


@router.get("", response_model=list[IncidentResponse])
def list_incidents(db: Session = Depends(get_db)):
    return service.list_incidents(db)
