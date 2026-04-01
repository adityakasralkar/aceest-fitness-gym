pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Pulling code from GitHub...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    cd backend
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running Pytest...'
                sh '''
                    cd backend
                    python -m pytest tests/ -v
                '''
            }
        }

        stage('Docker Build') {
            agent any
            steps {
                echo 'Building Docker image...'
                sh '''
                    docker build -t aceest-backend ./backend
                '''
            }
        }
    }

    post {
        success {
            echo 'BUILD SUCCESSFUL - All stages passed!'
        }
        failure {
            echo 'BUILD FAILED - Check logs above'
        }
    }
}
