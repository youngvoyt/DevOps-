// ЛР4: CI/CD для образа ЛР2 (ETL + Streamlit). Вариант 10 — уведомления о статусе сборки.
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'my-analytics-app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Linting') {
            steps {
                dir('Lab2') {
                    sh '''
                        python3 -m pip install --user -q -r requirements.txt pylint
                        python3 -m pylint --fail-under=5.0 --rcfile=.pylintrc src/etl_loader.py app/main.py version_check.py
                    '''
                }
            }
        }

        stage('Build Image') {
            steps {
                dir('Lab2') {
                    sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                }
            }
        }

        stage('Test Run') {
            steps {
                sh "docker run --rm ${IMAGE_NAME}:${BUILD_NUMBER} python version_check.py --version"
            }
        }

        stage('Deploy') {
            steps {
                echo 'CD: локально помечаем последний успешный образ тегом latest'
                sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
            }
        }
    }

    post {
        success {
            echo "[NOTIFY] Build Success — ${JOB_NAME} #${BUILD_NUMBER}"
            sh "echo \"[NOTIFY] Build Success (заглушка под Telegram/e-mail) — ${JOB_NAME} #${BUILD_NUMBER}\""
        }
        failure {
            echo "[NOTIFY] Build Fail — ${JOB_NAME} #${BUILD_NUMBER}"
            sh "echo \"[NOTIFY] Build Fail (заглушка под Telegram/e-mail) — ${JOB_NAME} #${BUILD_NUMBER}\""
        }
    }
}
