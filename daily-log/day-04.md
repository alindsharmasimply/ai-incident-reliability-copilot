## Alert Ingestion

The backend supports alert ingestion through:

POST /api/v1/alerts

An alert represents a raw signal from a monitoring source such as Prometheus, CloudWatch, Datadog, or another observability tool.

Current behavior:
- accepts alert payload
- generates or accepts an idempotency key
- creates a new incident for a new alert
- creates a CREATED timeline event
- returns the existing alert and incident if the same idempotency key is received again

Why idempotency matters:
Monitoring tools and queues may retry delivery. Without idempotency, duplicate alerts can create duplicate incidents and increase operational noise.