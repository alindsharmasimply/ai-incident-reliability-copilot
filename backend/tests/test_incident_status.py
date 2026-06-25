from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def create_test_incident():
    payload = {
        "title": "Checkout status transition test",
        "description": "Testing incident status transitions",
        "service_name": "checkout-service",
        "severity": "SEV2",
    }

    response = client.post("/api/v1/incidents", json=payload)
    assert response.status_code == 200

    return response.json()

def test_valid_status_transition_adds_timeline_event():
    incident = create_test_incident()
    incident_id = incident["id"]

    response = client.patch(
        f"/api/v1/incidents/{incident_id}/status",
        json={
            "status": "ACKNOWLEDGED",
            "updated_by": "alind",
            "note": "Acknowledged during test",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ACKNOWLEDGED"
    assert any(
        event["event_type"] == "STATUS_CHANGED"
        for event in data["events"]
    )


def test_invalid_status_transition_is_rejected():
    incident = create_test_incident()
    incident_id = incident["id"]

    response = client.patch(
        f"/api/v1/incidents/{incident_id}/status",
        json={
            "status": "RESOLVED",
            "updated_by": "alind",
            "note": "Invalid direct transition",
        },
    )

    assert response.status_code == 400
    assert "Invalid status transition" in response.json()["detail"]