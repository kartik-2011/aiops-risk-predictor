from app.risk_engine import calculate_risk
from app.schemas import TelemetryInput


def test_low_risk_service_gets_healthy_recommendation():
    prediction = calculate_risk(
        TelemetryInput(
            service_name="catalog-api",
            cpu_percent=25,
            memory_percent=35,
            latency_ms=120,
            error_rate_percent=0.1,
            requests_per_minute=300,
        )
    )

    assert prediction.risk_level == "low"
    assert prediction.risk_score == 0
    assert prediction.recommendations == ["Service is healthy. Continue normal monitoring."]


def test_critical_risk_caps_score_at_100():
    prediction = calculate_risk(
        TelemetryInput(
            service_name="payment-api",
            cpu_percent=98,
            memory_percent=92,
            latency_ms=2200,
            error_rate_percent=12,
            requests_per_minute=9000,
        )
    )

    assert prediction.risk_level == "critical"
    assert prediction.risk_score == 100
    assert len(prediction.recommendations) >= 4

