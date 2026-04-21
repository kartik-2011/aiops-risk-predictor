from pydantic import BaseModel, Field


class TelemetryInput(BaseModel):
    service_name: str = Field(..., min_length=2, examples=["payment-api"])
    cpu_percent: float = Field(..., ge=0, le=100, examples=[86])
    memory_percent: float = Field(..., ge=0, le=100, examples=[78])
    latency_ms: float = Field(..., ge=0, examples=[930])
    error_rate_percent: float = Field(..., ge=0, le=100, examples=[7.5])
    requests_per_minute: int = Field(..., ge=0, examples=[2400])


class RiskPrediction(BaseModel):
    service_name: str
    risk_score: int
    risk_level: str
    recommendations: list[str]

