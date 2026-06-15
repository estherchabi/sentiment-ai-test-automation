pipeline {
    agent any

    environment {
        SONAR_TOKEN    = credentials('sonar-token')
        SONAR_HOST_URL = 'http://sonarqube:9000'
        IMAGE_NAME     = "sentiment-ai"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    pylint src/ --fail-under=7.0 \
                           --output-format=parseable \
                           > pylint-report.txt || true
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'pylint-report.txt',
                                     allowEmptyArchive: true
                }
            }
        }

        stage('Tests Unitaires') {
            steps {
                sh '''
                    pytest tests/test_model.py \
                           --cov=src \
                           --cov-report=xml:coverage.xml \
                           --junit-xml=junit-unit.xml \
                           -v
                '''
            }
            post {
                always {
                    junit 'junit-unit.xml'
                }
            }
        }

        stage('Tests Integration') {
            steps {
                sh '''
                    pytest tests/test_api.py \
                           --junit-xml=junit-integration.xml \
                           -v
                '''
            }
            post {
                always {
                    junit 'junit-integration.xml'
                }
            }
        }

        stage('Build Docker') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('SonarQube') {
            steps {
                script {
                    docker.image('sonarsource/sonar-scanner-cli:5').inside(
                        "--network sentiment-network"
                    ) {
                        sh """
                            sonar-scanner \
                              -Dsonar.projectKey=sentiment-ai \
                              -Dsonar.sources=src \
                              -Dsonar.tests=tests \
                              -Dsonar.python.coverage.reportPaths=coverage.xml \
                              -Dsonar.host.url=${SONAR_HOST_URL} \
                              -Dsonar.token=${SONAR_TOKEN}
                        """
                    }
                }
            }
        }

        stage('Security Scan') {
            steps {
                sh 'bandit -r src/ -f json -o bandit-report.json || true'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit-report.json',
                                     allowEmptyArchive: true
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        failure {
            echo 'Pipeline echoue. Verifiez les rapports.'
        }
        success {
            echo 'Pipeline reussi. Quality Gate passe.'
        }
    }
}