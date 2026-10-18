pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        STUDENT_NAME = 'Danil'
        STUDENT_SURNAME = 'Marchenko'
        STUDENT_GROUP = 'IT2-2303'
        STUDENT_ID = '41587'
        DOCKER_IMAGE = 'marchenko-danil-devops'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'python3 -m compileall -q app tests'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m unittest discover -s tests -v'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t "$DOCKER_IMAGE:$BUILD_NUMBER" .'
            }
        }

        stage('Docker Run') {
            steps {
                sh '''
                    set -eu
                    CONTAINER_NAME="marchenko-ci-${BUILD_NUMBER}"
                    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
                    docker run -d --name "$CONTAINER_NAME" -p 127.0.0.1::8000 -e STUDENT_NAME="$STUDENT_NAME" -e STUDENT_SURNAME="$STUDENT_SURNAME" -e STUDENT_GROUP="$STUDENT_GROUP" -e STUDENT_ID="$STUDENT_ID" "$DOCKER_IMAGE:$BUILD_NUMBER"
                    PORT="$(docker port "$CONTAINER_NAME" 8000/tcp | awk -F: '{print $NF}')"
                    export PORT
                    python3 - <<'PY'
import os
from urllib.request import urlopen

with urlopen(f"http://127.0.0.1:{os.environ['PORT']}/student", timeout=10) as response:
    body = response.read().decode()
    assert response.status == 200
    assert "Danil" in body and "Marchenko" in body
    assert "IT2-2303" in body and "41587" in body
    print(body)
PY
                    docker logs "$CONTAINER_NAME"
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f "marchenko-ci-${BUILD_NUMBER}" >/dev/null 2>&1 || true'
        }
    }
}
