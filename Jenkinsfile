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

        // Один bash-скрипт: apt + при необходимости статический docker CLI в WORKSPACE (доступно и для jenkins, и для root).
        stage('Build Image') {
            steps {
                dir('Lab2') {
                    sh """#!/bin/bash
set -e
export DEBIAN_FRONTEND=noninteractive
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:\$PATH"
JDOCKER="${env.WORKSPACE}/.jenkins-docker-cli"
mkdir -p "\$JDOCKER"

ensure_docker() {
  if command -v docker >/dev/null 2>&1; then return 0; fi
  if [ -x /usr/bin/docker ]; then return 0; fi
  if [ -x "\$JDOCKER/docker" ]; then export PATH="\$JDOCKER:\$PATH"; return 0; fi
  return 1
}

if ! ensure_docker; then
  apt-get update -qq
  apt-get install -y -qq docker.io || true
  hash -r
fi

if ! ensure_docker; then
  apt-get install -y -qq curl ca-certificates
  curl -fsSL "https://download.docker.com/linux/static/stable/x86_64/docker-26.1.4.tgz" -o /tmp/dock.tgz
  tar -xzf /tmp/dock.tgz -C /tmp
  install -m 755 /tmp/docker/docker "\$JDOCKER/docker" || true
  if install -m 755 /tmp/docker/docker /usr/local/bin/docker 2>/dev/null; then hash -r; fi
  export PATH="\$JDOCKER:\$PATH"
  hash -r
fi

ensure_docker || { echo "ERROR: docker CLI not available"; exit 127; }
command -v docker
docker version --format '{{.Client.Version}}' || docker --version

if [ -S /var/run/docker.sock ]; then
  chmod 666 /var/run/docker.sock 2>/dev/null || true
fi

docker build -t ${env.IMAGE_NAME}:${env.BUILD_NUMBER} .
"""
                }
            }
        }

        stage('Test Run') {
            steps {
                sh """#!/bin/bash
set -e
export PATH="${env.WORKSPACE}/.jenkins-docker-cli:/usr/local/bin:/usr/bin:/sbin:/bin:\$PATH"
if [ -S /var/run/docker.sock ]; then chmod 666 /var/run/docker.sock 2>/dev/null || true; fi
command -v docker
docker run --rm ${env.IMAGE_NAME}:${env.BUILD_NUMBER} python version_check.py --version
"""
            }
        }

        stage('Deploy') {
            steps {
                echo 'CD: локально помечаем последний успешный образ тегом latest'
                sh """#!/bin/bash
set -e
export PATH="${env.WORKSPACE}/.jenkins-docker-cli:/usr/local/bin:/usr/bin:/sbin:/bin:\$PATH"
if [ -S /var/run/docker.sock ]; then chmod 666 /var/run/docker.sock 2>/dev/null || true; fi
docker tag ${env.IMAGE_NAME}:${env.BUILD_NUMBER} ${env.IMAGE_NAME}:latest
"""
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
