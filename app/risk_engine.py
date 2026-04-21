from app.schemas import RiskPrediction, TelemetryInput


def calculate_risk(telemetry: TelemetryInput) -> RiskPrediction:
    score = 0
    recommendations: list[str] = []

    if telemetry.cpu_percent >= 85:
        score += 25
        recommendations.append("Scale pods or inspect CPU-heavy processes.")
    elif telemetry.cpu_percent >= 70:
        score += 15
        recommendations.append("Watch CPU trend and prepare horizontal scaling.")

    if telemetry.memory_percent >= 85:
        score += 25
        recommendations.append("Check memory leaks and increase memory limits.")
    elif telemetry.memory_percent >= 70:
        score += 15
        recommendations.append("Review memory growth and cache usage.")

    if telemetry.latency_ms >= 1000:
        score += 25
        recommendations.append("Investigate slow dependencies and database queries.")
    elif telemetry.latency_ms >= 500:
        score += 15
        recommendations.append("Review latency dashboards and recent deployments.")

    if telemetry.error_rate_percent >= 5:
        score += 25
        recommendations.append("Trigger incident workflow and inspect application errors.")
    elif telemetry.error_rate_percent >= 2:
        score += 15
        recommendations.append("Check logs for rising 4xx/5xx error patterns.")

    if telemetry.requests_per_minute >= 3000:
        score += 10
        recommendations.append("Traffic spike detected; verify autoscaling capacity.")

    score = min(score, 100)
    risk_level = _risk_level(score)

    if not recommendations:
        recommendations.append("Service is healthy. Continue normal monitoring.")

    return RiskPrediction(
        service_name=telemetry.service_name,
        risk_score=score,
        risk_level=risk_level,
        recommendations=recommendations,
    )


def _risk_level(score: int) -> str:
    if score >= 75:
        return "critical"
    if score >= 45:
        return "high"
    if score >= 20:
        return "medium"
    return "low"

