from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ingest_alert_creates_incident():
    payload = {
        "source": "prometheus",
        "service_name": "checkout-service",
        "alert_type": "5xx_error_rate",
        "title": "Checkout service 5xx error rate is high",
        "description": "5xx error rate crossed threshold",
        "severity": "SEV2",
        "idempotency_key": "test-alert-create-incident-001",
        "payload": {
            "threshold": "5%",
            "window": "5m",
        },
    }

    response = client.post("/api/v1/alerts", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["source"] == payload["source"]
    assert data["service_name"] == payload["service_name"]
    assert data["alert_type"] == payload["alert_type"]
    assert data["severity"] == payload["severity"]
    assert data["duplicate"] is False
    assert data["incident_id"] is not None


def test_duplicate_alert_returns_existing_incident():
    payload = {
        "source": "prometheus",
        "service_name": "payment-service",
        "alert_type": "latency_spike",
        "title": "Payment service latency spike",
        "description": "p95 latency crossed threshold",
        "severity": "SEV2",
        "idempotency_key": "test-duplicate-alert-001",
        "payload": {
            "threshold": "800ms",
            "window": "10m",
        },
    }

    first_response = client.post("/api/v1/alerts", json=payload)
    assert first_response.status_code == 200

    first_data = first_response.json()
    assert first_data["duplicate"] is False

    second_response = client.post("/api/v1/alerts", json=payload)
    assert second_response.status_code == 200

    second_data = second_response.json()
    assert second_data["duplicate"] is True
    assert second_data["incident_id"] == first_data["incident_id"]
    assert second_data["id"] == first_data["id"]


def test_alert_rejects_invalid_payload():
    payload = {
        "source": "x",
        "service_name": "checkout-service",
        "alert_type": "5xx",
        "title": "ok",
        "severity": "SEV2",
    }

    response = client.post("/api/v1/alerts", json=payload)

    assert response.status_code == 422
