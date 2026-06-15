pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                sh 'pip3 install -r requirements.txt --break-system-packages'
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
    }

    post {
        failure {
            echo 'Pipeline echoue. Verifiez les rapports.'
        }
        success {
            echo 'Pipeline reussi. Tous les stages sont verts.'
        }
    }
}