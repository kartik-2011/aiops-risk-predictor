pipeline {
    agent any

    parameters {
        string(name: 'IMAGE_NAME', defaultValue: 'aiops-risk-predictor', description: 'Docker image name, including registry if needed')
        booleanParam(name: 'PUSH_IMAGE', defaultValue: false, description: 'Push image to Docker registry')
        booleanParam(name: 'DEPLOY_K8S', defaultValue: false, description: 'Deploy manifests to Kubernetes')
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

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && pip install -r requirements-dev.txt'
            }
        }

        stage('Test') {
            steps {
                sh '. .venv/bin/activate && pytest -q'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .'
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
}
