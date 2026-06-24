from urllib import response

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_incident_valid_payload():
    payload = {
        "title": "Search service error spike",
        "description": "5xx errors increased after latest deployment",
        "service_name": "search-service",
        "severity": "SEV2",
    }

    response = client.post("/api/v1/incidents", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == payload["title"]
    assert data["service_name"] == payload["service_name"]
    assert data["severity"] == payload["severity"]
    assert data["status"] == "OPEN"
    assert "id" in data
    assert "created_at" in data


def test_create_incident_rejects_short_title():
    payload = {
        "title": "x",
        "description": "Invalid incident title",
        "service_name": "search-service",
        "severity": "SEV2",
    }

    response = client.post("/api/v1/incidents", json=payload)

    assert response.status_code == 422


def test_get_incident_by_id_returns_details():
    payload = {
        "title": "Inventory service latency spike",
        "description": "p95 latency crossed threshold",
        "service_name": "inventory-service",
        "severity": "SEV3",
    }

    create_response = client.post("/api/v1/incidents", json=payload)
    assert create_response.status_code == 200

    incident_id = create_response.json()["id"]

    detail_response = client.get(f"/api/v1/incidents/{incident_id}")
    assert detail_response.status_code == 200

    data = detail_response.json()
    assert data["id"] == incident_id
    assert data["title"] == payload["title"]
    assert "events" in data
    assert len(data["events"]) >= 1
    assert data["events"][0]["event_type"] == "CREATED"


def test_get_incident_timeline_returns_events():
    payload = {
        "title": "Recommendation service failures",
        "description": "Error rate increased",
        "service_name": "recommendation-service",
        "severity": "SEV2",
    }

    create_response = client.post("/api/v1/incidents", json=payload)
    assert create_response.status_code == 200

    incident_id = create_response.json()["id"]

    timeline_response = client.get(f"/api/v1/incidents/{incident_id}/timeline")
    assert timeline_response.status_code == 200

    events = timeline_response.json()

    assert len(events) >= 1
    assert events[0]["incident_id"] == incident_id
    assert events[0]["event_type"] == "CREATED"


def test_get_unknown_incident_returns_404():
    incident_id = "Some-non-existent-id"
    response = client.get(f"/api/v1/incidents/{incident_id}")

    assert response.status_code == 404
