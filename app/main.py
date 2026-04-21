import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.logging_config import configure_logging
from app.risk_engine import calculate_risk
from app.schemas import RiskPrediction, TelemetryInput

configure_logging()
logger = logging.getLogger("aiops-risk-predictor")

app = FastAPI(
    title="AIOps Incident Risk Predictor",
    description="Predicts incident risk from service telemetry for DevOps monitoring demos.",
    version="1.0.0",
)


@app.get("/", response_class=HTMLResponse)
def dashboard() -> str:
    return Path("app/static/index.html").read_text(encoding="utf-8")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy", "service": "aiops-risk-predictor"}


@app.post("/predict", response_model=RiskPrediction)
def predict(telemetry: TelemetryInput) -> RiskPrediction:
    prediction = calculate_risk(telemetry)
    logger.info(
        "risk prediction generated",
        extra={
            "app_event": "risk_prediction",
            "service_name": prediction.service_name,
            "risk_score": prediction.risk_score,
            "risk_level": prediction.risk_level,
        },
    )
    return prediction


@app.get("/sample")
def sample_payload() -> TelemetryInput:
    return TelemetryInput(
        service_name="payment-api",
        cpu_percent=86,
        memory_percent=78,
        latency_ms=930,
        error_rate_percent=7.5,
        requests_per_minute=2400,
    )
