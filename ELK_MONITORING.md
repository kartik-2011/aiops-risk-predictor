# ELK Monitoring Demo

This project logs structured JSON events from the FastAPI app. Filebeat collects the Docker container logs, sends them to Logstash, and Logstash stores them in Elasticsearch. Kibana is used to search and visualize the logs.

## Start App and ELK

```bash
docker compose up -d --build
docker compose -f docker-compose.elk.yml up -d
```

Open:

```text
App: http://127.0.0.1:8000
Kibana: http://127.0.0.1:5601
Elasticsearch: http://127.0.0.1:9200
```

## Generate Logs

Run this a few times:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "service_name": "payment-api",
    "cpu_percent": 91,
    "memory_percent": 82,
    "latency_ms": 1200,
    "error_rate_percent": 8.5,
    "requests_per_minute": 3200
  }'
```

## Check Elasticsearch

```bash
curl http://127.0.0.1:9200/_cat/indices?v
```

Look for:

```text
aiops-risk-predictor-YYYY.MM.DD
```

## Kibana Data View

In Kibana:

```text
Stack Management -> Data Views -> Create data view
```

Use:

```text
Name: aiops-risk-predictor
Index pattern: aiops-risk-predictor-*
Timestamp field: @timestamp
```

Then open:

```text
Discover -> aiops-risk-predictor
```

Search examples:

```text
service : "aiops-risk-predictor"
app_event : "risk_prediction"
app.risk_level : "critical"
app.service_name : "payment-api"
```

## Viva Explanation

Say:

```text
The application writes structured JSON logs. Filebeat collects Docker container logs, Logstash parses and forwards them, Elasticsearch stores them, and Kibana visualizes them. This completes the monitoring part of the DevOps pipeline.
```
