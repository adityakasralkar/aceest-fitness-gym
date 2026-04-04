pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Pulling code from GitHub...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                dir('backend') {
                    sh 'python3 -m pip install --upgrade pip'
                    sh 'python3 -m pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    cd backend
                    python -m pytest tests/ -v
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t aceest-backend ./backend'
            }
        }
    }

    post {
        always {
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