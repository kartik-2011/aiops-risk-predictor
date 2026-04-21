from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_predict_endpoint():
    response = client.post(
        "/predict",
        json={
            "service_name": "payment-api",
            "cpu_percent": 86,
            "memory_percent": 78,
            "latency_ms": 930,
            "error_rate_percent": 7.5,
            "requests_per_minute": 2400,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["service_name"] == "payment-api"
    assert body["risk_level"] in {"high", "critical"}
    assert body["risk_score"] >= 70

