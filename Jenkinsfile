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
                        export DEBIAN_FRONTEND=noninteractive
                        if ! command -v python3 >/dev/null 2>&1; then
                            apt-get update -qq
                            apt-get install -y -qq python3 python3-pip python3-venv
                        fi
                        rm -rf .jenkins-venv
                        python3 -m venv .jenkins-venv
                        .jenkins-venv/bin/pip install -q pylint
                        .jenkins-venv/bin/python -m pylint --fail-under=5.0 --rcfile=.pylintrc src/etl_loader.py app/main.py version_check.py
                    '''
                }
            }
        }

        // В образе jenkins/jenkins без кастомного Dockerfile часто нет docker CLI — ставим при необходимости (нужны права root в контейнере).
        stage('Docker CLI') {
            steps {
                sh '''
                    export DEBIAN_FRONTEND=noninteractive
                    if ! [ -x /usr/bin/docker ]; then
                        apt-get update -qq
                        apt-get install -y -qq docker.io
                    fi
                    if [ -S /var/run/docker.sock ]; then
                        chmod 666 /var/run/docker.sock 2>/dev/null || true
                    fi
                '''
            }
        }

        stage('Build Image') {
            steps {
                dir('Lab2') {
                    sh "/usr/bin/docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                }
            }
        }

        stage('Test Run') {
            steps {
                sh "/usr/bin/docker run --rm ${IMAGE_NAME}:${BUILD_NUMBER} python version_check.py --version"
            }
        }

        stage('Deploy') {
            steps {
                echo 'CD: локально помечаем последний успешный образ тегом latest'
                sh "/usr/bin/docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
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
