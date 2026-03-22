#!/bin/bash
set -e
# Сокет Docker с хоста: GID группы docker в контейнере часто не совпадает с хостом — даём доступ для lint/build job (учебный контур).
if [ -S /var/run/docker.sock ]; then
  chmod 666 /var/run/docker.sock 2>/dev/null || true
fi
exec /usr/local/bin/jenkins.sh "$@"
