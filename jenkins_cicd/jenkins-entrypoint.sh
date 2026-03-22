#!/bin/sh
# Запуск как в официальном образе Jenkins (tini + jenkins.sh), плюс права на docker.sock.
if [ -S /var/run/docker.sock ]; then
  chmod 666 /var/run/docker.sock 2>/dev/null || true
fi
if [ -x /usr/bin/tini ]; then
  exec /usr/bin/tini -- /usr/local/bin/jenkins.sh "$@"
fi
if [ -x /bin/tini ]; then
  exec /bin/tini -- /usr/local/bin/jenkins.sh "$@"
fi
exec /usr/local/bin/jenkins.sh "$@"
