# Jenkins + Docker CLI внутри образа (не монтируем /usr/bin/docker с хоста — на Windows это часто ломается).
FROM jenkins/jenkins:lts

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends docker.io \
    && rm -rf /var/lib/apt/lists/*

COPY jenkins-entrypoint.sh /usr/local/bin/jenkins-entrypoint.sh
# Убираем CR (Windows CRLF), иначе контейнер падает сразу после старта
RUN sed -i 's/\r$//' /usr/local/bin/jenkins-entrypoint.sh \
    && chmod +x /usr/local/bin/jenkins-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/jenkins-entrypoint.sh"]
