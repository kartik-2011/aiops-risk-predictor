# DevOps Pipeline Demo Steps

Use this file as your viva/demo flow. The application is simple; the important part is showing how code moves through the DevOps pipeline.

## 1. Git Stage

Purpose: store source code and track changes.

```bash
git status
git log --oneline
```

Explain:

- Git keeps the project history.
- Jenkins normally pulls this code from GitHub or another Git remote.

## 2. Test Stage

Purpose: check whether the app works before packaging.

```bash
source .venv/bin/activate
pytest -q
```

Expected result:

```text
4 passed
```

Explain:

- If tests fail, Jenkins stops the pipeline.
- This prevents broken code from reaching Docker or Kubernetes.

## 3. Docker Build Stage

Purpose: package the app and dependencies into one container image.

```bash
docker build -t aiops-risk-predictor:latest .
```

Explain:

- `Dockerfile` defines the app environment.
- The same image can run on your laptop, server, or Kubernetes.

## 4. Docker Run Stage

Purpose: run the packaged app.

```bash
docker run -d --name aiops-risk-predictor-demo -p 8000:8000 aiops-risk-predictor:latest
curl http://127.0.0.1:8000/health
```

Open:

```text
http://127.0.0.1:8000
```

Stop when finished:

```bash
docker stop aiops-risk-predictor-demo
docker rm aiops-risk-predictor-demo
```

## 5. Jenkins Stage

Purpose: automate the same commands.

In Jenkins:

1. Create a Pipeline job.
2. Connect it to your Git repository.
3. Select `Pipeline script from SCM`.
4. Jenkins reads `Jenkinsfile`.

Pipeline flow:

```text
Checkout -> Install Dependencies -> Test -> Build Docker Image -> Push Image -> Deploy to Kubernetes
```

For a simple college demo, keep `PUSH_IMAGE` and `DEPLOY_K8S` unchecked first. This shows CI. Enable them later when Docker Hub and Kubernetes credentials are ready.

## 6. Kubernetes Stage

Purpose: run the container in a cluster with replicas, service discovery, health checks, and scaling.

Enable Kubernetes in Docker Desktop or use Minikube/kind, then run:

```bash
kubectl apply -f k8s/
kubectl get pods
kubectl get svc
kubectl port-forward svc/aiops-risk-predictor 8000:80
```

Explain:

- Deployment creates pods.
- Service exposes the pods.
- HPA can scale pods based on CPU.
- Readiness/liveness probes check app health.

## 7. Ansible Stage

Purpose: automate deployment on a server.

Update `ansible/inventory.ini` with your server IP, then run:

```bash
ansible-galaxy collection install -r ansible/requirements.yml
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml
```

Explain:

- Ansible installs Docker.
- Copies project files to the server.
- Builds and starts the container automatically.

## 8. ELK Monitoring Stage

Purpose: collect and view application logs.

The app writes JSON logs. Filebeat can collect Docker container logs using `elk/filebeat.yml`.

Explain:

- Elasticsearch stores logs.
- Logstash/Filebeat ships and processes logs.
- Kibana visualizes logs and searches fields like `risk_level` and `service_name`.

## One-Line Pipeline Explanation

Code is pushed to Git, Jenkins automatically tests it, Docker packages it, Kubernetes or Ansible deploys it, and ELK monitors the running application logs.

