# AIOps Incident Risk Predictor

An easy, deployable domain-specific DevOps project for monitoring service health and predicting incident risk from runtime metrics.

The project is intentionally compact so you can demonstrate Git, Jenkins, Docker, Ansible, Kubernetes, and ELK monitoring without fighting a huge codebase.

## Domain

**AIOps / DevOps Monitoring**

The app accepts service telemetry such as CPU usage, memory usage, latency, error rate, and request rate. It calculates an incident risk level and returns operational recommendations. It also writes structured JSON logs that can be collected by Filebeat and visualized in ELK.

## Features

- FastAPI backend with Swagger UI
- Browser dashboard at `/`
- Incident risk prediction API
- JSON structured logs for ELK
- Unit tests with pytest
- Dockerfile and Docker Compose
- Kubernetes deployment, service, configmap, and HPA
- Jenkins CI/CD pipeline
- Ansible deployment playbook
- Filebeat example config for ELK ingestion

## Quick Start

Use Python 3.12 for local development. The Docker image also uses Python 3.12.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- Dashboard: http://localhost:8000
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Example Prediction Request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "service_name": "payment-api",
    "cpu_percent": 86,
    "memory_percent": 78,
    "latency_ms": 930,
    "error_rate_percent": 7.5,
    "requests_per_minute": 2400
  }'
```

## Docker

```bash
docker build -t aiops-risk-predictor:latest .
docker run -p 8000:8000 aiops-risk-predictor:latest
```

Or:

```bash
docker compose up --build
```

## Kubernetes

```bash
kubectl apply -f k8s/
kubectl port-forward svc/aiops-risk-predictor 8000:80
```

## Jenkins

The included `Jenkinsfile` runs:

1. Dependency install
2. Unit tests
3. Docker image build
4. Optional image push
5. Optional Kubernetes deployment

Set these Jenkins credentials/parameters as needed:

- `DOCKERHUB_CREDENTIALS`
- `IMAGE_NAME`
- `KUBE_CONFIG`

## Ansible

Install the Docker collection once, update `ansible/inventory.ini`, then run:

```bash
ansible-galaxy collection install -r ansible/requirements.yml
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml
```

## ELK Monitoring

The app logs JSON to stdout. In Docker/Kubernetes, collect container logs with Filebeat or Elastic Agent. A sample Filebeat config is included in `elk/filebeat.yml`.

For a full local ELK demo, use:

```bash
docker compose up -d --build
docker compose -f docker-compose.elk.yml up -d
```

Then open Kibana at http://127.0.0.1:5601 and follow `ELK_MONITORING.md`.

Useful Kibana fields:

- `app_event`
- `service_name`
- `risk_level`
- `risk_score`
- `recommendations`

## Project Structure

```text
app/
  main.py
  risk_engine.py
  schemas.py
  logging_config.py
  static/
tests/
k8s/
ansible/
elk/
Dockerfile
docker-compose.yml
Jenkinsfile
```
