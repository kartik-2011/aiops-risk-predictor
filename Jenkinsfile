pipeline {
    agent any

    options {
        timestamps()
    }

    parameters {
        string(name: 'IMAGE_NAME', defaultValue: 'aiops-risk-predictor', description: 'Docker image name, including registry if needed')
        string(name: 'EMAIL_TO', defaultValue: 'student@example.com', description: 'Email address for pipeline notification demo')
        booleanParam(name: 'PUSH_IMAGE', defaultValue: false, description: 'Push image to Docker registry')
        booleanParam(name: 'DEPLOY_K8S', defaultValue: false, description: 'Deploy manifests to Kubernetes')
        booleanParam(name: 'SEND_EMAIL', defaultValue: true, description: 'Send build result email after pipeline finishes')
    }

    environment {
        IMAGE_NAME = "${params.IMAGE_NAME}"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Build Tools') {
            steps {
                sh 'git --version'
                sh 'python3 --version'
                sh 'docker version'
            }
        }

        stage('Create Python Environment') {
            steps {
                sh 'python3 -m venv .venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '. .venv/bin/activate && pip install --upgrade pip'
                sh '. .venv/bin/activate && pip install -r requirements-dev.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '. .venv/bin/activate && pytest -q'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Smoke Test Docker Image') {
            steps {
                sh "docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} python -c \"from app.risk_engine import _risk_level; assert _risk_level(80) == 'critical'\""
            }
        }

        stage('Push Docker Image') {
            when {
                expression { return params.PUSH_IMAGE }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'DOCKERHUB_CREDENTIALS', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                    sh 'docker push ${IMAGE_NAME}:${IMAGE_TAG}'
                    sh 'docker push ${IMAGE_NAME}:latest'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            when {
                expression { return params.DEPLOY_K8S }
            }
            steps {
                withCredentials([file(credentialsId: 'KUBE_CONFIG', variable: 'KUBECONFIG')]) {
                    sh 'kubectl apply -f k8s/'
                    sh 'kubectl rollout status deployment/aiops-risk-predictor'
                }
            }
        }
    }

    post {
        always {
            script {
                if (params.SEND_EMAIL) {
                    mail(
                        to: params.EMAIL_TO,
                        subject: "Jenkins ${currentBuild.currentResult}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body: """Pipeline result: ${currentBuild.currentResult}
Job: ${env.JOB_NAME}
Build number: ${env.BUILD_NUMBER}
Git branch: ${env.BRANCH_NAME ?: 'main'}
Build URL: ${env.BUILD_URL}

Stages demonstrated:
- Checkout from GitHub
- Verify build tools
- Create Python environment
- Install dependencies
- Run unit tests
- Build Docker image
- Smoke test Docker image
- Optional Docker push
- Optional Kubernetes deploy
"""
                    )
                }
            }
        }
    }
}
