from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.alert import AlertCreate, AlertResponse
from app.services.alert_service import AlertService

router = APIRouter(prefix="/alerts", tags=["Alerts"])

service = AlertService()


@router.post("", response_model=AlertResponse)
def ingest_alert(payload: AlertCreate, db: Session = Depends(get_db)):
    alert, duplicate = service.ingest_alert(db, payload)

    response = AlertResponse.model_validate(alert)
    response.duplicate = duplicate

    return response
