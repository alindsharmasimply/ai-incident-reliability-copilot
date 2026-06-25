from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.incidents import router as incidents_router
from app.api.routes.alerts import router as alerts_router
from app.db.base import Base
from app.db.session import engine
from app.models import incident, incident_event, alert  # noqa: F401

# TODO: Migrations need to be done using Alembic. create_all is only good for prototype not for production


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Incident Reliability Copilot",
        version="0.1.0",
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(health_router)
    app.include_router(incidents_router, prefix="/api/v1")
    app.include_router(alerts_router, prefix="/api/v1")

    return app


app = create_app()
