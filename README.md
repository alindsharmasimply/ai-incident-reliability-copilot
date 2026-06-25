#### A production-grade platform where engineering teams connect service logs, traces, alerts, runbooks, and deployment history.

#### The system uses RAG and tool-calling agents to diagnose incidents, suggest fixes, generate postmortems, create Jira/GitHub issues, and simulate rollback decisions.

## Build image on docker container
```
docker compose up --build
```
## Run tests
```
docker exec -it incident_copilot_backend env PYTHONPATH=. pytest
```
## To monitor logs
```
docker compose logs -f backend
```
## To install dependencies
```
pip install -e .
```
## To create alembic migration
```
docker-compose exec backend alembic revision --autogenerate -m "xoxoxoxoxoxoxo"
```
## To run the migrations and bring the db in sync
```
docker compose exec backend alembic upgrade head
```