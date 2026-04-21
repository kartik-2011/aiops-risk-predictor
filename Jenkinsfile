pipeline {
    agent any

    options {
        timestamps()
    }

    parameters {
        string(name: 'IMAGE_NAME', defaultValue: 'aiops-risk-predictor', description: 'Docker image name, including registry if needed')
        string(name: 'EMAIL_TO', defaultValue: 'kartikahluwalia2011@gmail.com', description: 'Email address for pipeline notification demo')
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
            steps {
                script {
                    if (params.PUSH_IMAGE) {
                        withCredentials([usernamePassword(credentialsId: 'DOCKERHUB_CREDENTIALS', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                            sh 'docker push ${IMAGE_NAME}:${IMAGE_TAG}'
                            sh 'docker push ${IMAGE_NAME}:latest'
                        }
                    } else {
                        sh '''
                            echo "Docker push demo stage"
                            echo "Image is ready locally: ${IMAGE_NAME}:${IMAGE_TAG}"
                            echo "Real registry push is disabled because PUSH_IMAGE=false."
                            docker image inspect ${IMAGE_NAME}:${IMAGE_TAG} >/dev/null
                        '''
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    if (params.DEPLOY_K8S) {
                        withCredentials([file(credentialsId: 'KUBE_CONFIG', variable: 'KUBECONFIG')]) {
                            sh 'kubectl apply -f k8s/'
                            sh 'kubectl rollout status deployment/aiops-risk-predictor'
                        }
                    } else {
                        sh '''
                            echo "Kubernetes deployment demo stage"
                            echo "Real cluster deployment is disabled because DEPLOY_K8S=false."
                            test -f k8s/deployment.yaml
                            test -f k8s/service.yaml
                            test -f k8s/hpa.yaml
                            test -f k8s/configmap.yaml
                            echo "Kubernetes manifests are present and ready."
                        '''
                    }
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
- Docker push or push-readiness demo
- Kubernetes deploy or manifest-readiness demo
"""
                    )
                }
            }
        }
    }
}
