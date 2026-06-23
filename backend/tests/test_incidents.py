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
