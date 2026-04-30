pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    parameters {
        booleanParam(
            name: 'PUSH_TO_DOCKERHUB',
            defaultValue: false,
            description: 'Enable after the dockerhub-credentials Jenkins credential is configured.'
        )
        booleanParam(
            name: 'RUN_SONARQUBE',
            defaultValue: false,
            description: 'Enable after local SonarQube and Jenkins SonarScanner are configured.'
        )
    }

    environment {
        DOCKER_IMAGE = 'adityakasralkar/aceest-fitness-gym'
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
        SONARQUBE_INSTALLATION = 'ACEest SonarQube'
        SMOKE_CONTAINER = "aceest-smoke-${BUILD_NUMBER}"
        SMOKE_PORT = '5050'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Pulling code from GitHub...'
                checkout scm
            }
        }

        stage('Prepare Build Metadata') {
            steps {
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short=8 HEAD',
                        returnStdout: true
                    ).trim()
                    env.SAFE_BRANCH = sh(
                        script: "git rev-parse --abbrev-ref HEAD | sed 's#[^A-Za-z0-9_.-]#-#g'",
                        returnStdout: true
                    ).trim()
                    env.IMAGE_TAG = "${env.SAFE_BRANCH}-${env.BUILD_NUMBER}-${env.GIT_COMMIT_SHORT}"
                    env.APP_VERSION = env.IMAGE_TAG
                }
                echo "Building ${DOCKER_IMAGE}:${IMAGE_TAG}"
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    docker run --rm \
                        -v "${WORKSPACE}/backend:/app" \
                        -w /app \
                        python:3.11-slim \
                        sh -c "
                            pip install --no-cache-dir --upgrade pip &&
                            pip install --no-cache-dir -r requirements.txt
                        "
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    docker run --rm \
                        -v "${WORKSPACE}/backend:/app" \
                        -w /app \
                        python:3.11-slim \
                        sh -c "
                            pip install --no-cache-dir -r requirements.txt &&
                            python -m black --check . &&
                            python -m flake8 .
                        "
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    docker run --rm \
                        -v "${WORKSPACE}/backend:/app" \
                        -w /app \
                        python:3.11-slim \
                        sh -c "
                            pip install --no-cache-dir -r requirements.txt &&
                            mkdir -p reports &&
                            python -m pytest tests/ -v \
                                --junitxml=reports/pytest.xml \
                                --cov=app \
                                --cov-report=xml:reports/coverage.xml
                        "
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'backend/reports/pytest.xml'
                    archiveArtifacts allowEmptyArchive: true, artifacts: 'backend/reports/*.xml'
                }
            }
        }

        stage('SonarQube Analysis') {
            when {
                expression { return params.RUN_SONARQUBE }
            }
            steps {
                withSonarQubeEnv("${SONARQUBE_INSTALLATION}") {
                    sh 'sonar-scanner'
                }
            }
        }

        stage('SonarQube Quality Gate') {
            when {
                expression { return params.RUN_SONARQUBE }
            }
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build \
                        --build-arg APP_VERSION="${APP_VERSION}" \
                        --build-arg DEPLOYMENT_VARIANT="jenkins" \
                        -t "${DOCKER_IMAGE}:${IMAGE_TAG}" \
                        -t "${DOCKER_IMAGE}:latest" \
                        ./backend
                '''
            }
        }

        stage('Test Inside Docker') {
            steps {
                sh '''
                    docker run --rm \
                        -e FLASK_ENV=testing \
                        -e APP_VERSION="${APP_VERSION}" \
                        -e DEPLOYMENT_VARIANT="docker-test" \
                        "${DOCKER_IMAGE}:${IMAGE_TAG}" \
                        python -m pytest tests/ -v
                '''
            }
        }

        stage('Docker Smoke Test') {
            steps {
                sh '''
                    docker rm -f "${SMOKE_CONTAINER}" >/dev/null 2>&1 || true
                    docker run -d \
                        --name "${SMOKE_CONTAINER}" \
                        -p "${SMOKE_PORT}:5000" \
                        -e FLASK_ENV=testing \
                        -e APP_VERSION="${APP_VERSION}" \
                        -e DEPLOYMENT_VARIANT="docker-smoke" \
                        "${DOCKER_IMAGE}:${IMAGE_TAG}"

                    for attempt in $(seq 1 30); do
                        python3 -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:${SMOKE_PORT}/health', timeout=2).read().decode())" \
                            && exit 0
                        sleep 1
                    done

                    docker logs "${SMOKE_CONTAINER}" || true
                    exit 1
                '''
            }
        }

        stage('Push Docker Image') {
            when {
                expression { return params.PUSH_TO_DOCKERHUB }
            }
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: "${DOCKER_CREDENTIALS_ID}",
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        echo "${DOCKERHUB_TOKEN}" \
                            | docker login --username "${DOCKERHUB_USERNAME}" --password-stdin
                        docker push "${DOCKER_IMAGE}:${IMAGE_TAG}"
                        docker push "${DOCKER_IMAGE}:latest"
                    '''
                }
            }
        }

    }

    post {
        always {
            sh 'docker rm -f "${SMOKE_CONTAINER}" >/dev/null 2>&1 || true'
            sh 'docker logout >/dev/null 2>&1 || true'
            echo 'Pipeline finished (Success or Failure)'
            cleanWs()  // cleans workspace after build
        }

        success {
            echo 'BUILD SUCCESSFUL - All stages passed!'
        }

        failure {
            echo 'BUILD FAILED - Check logs above'
        }

        unstable {
            echo 'BUILD UNSTABLE - Some tests may have failed'
        }

        aborted {
            echo 'BUILD ABORTED - Manually stopped or interrupted'
        }
    }
}
