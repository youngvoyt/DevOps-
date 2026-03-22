# Отчет по лабораторной работе №3

## Тема

Оркестрация контейнеризированного приложения в среде Kubernetes.

## Цель работы

Получить практические навыки развертывания многоконтейнерного приложения в Kubernetes, перенести архитектуру из Docker Compose в K8s-манифесты, вынести конфигурацию в `ConfigMap` и `Secret`, обеспечить персистентность данных через `PersistentVolumeClaim` и настроить устойчивый жизненный цикл сервисов.

## Исходная архитектура

В качестве основы использовано решение из ЛР2:

- `PostgreSQL` как основная база данных
- `ETL loader` для разовой загрузки файла `course_project_test.csv`
- `Streamlit`-приложение для отображения метрик и первых строк набора данных

## Архитектура Kubernetes

В Kubernetes архитектура перенесена следующим образом:

- База данных:
  `Deployment` [`k8s/db-deployment.yaml`](k8s/db-deployment.yaml) + `Service` [`k8s/db-service.yaml`](k8s/db-service.yaml) + `PersistentVolumeClaim` [`k8s/pvc.yaml`](k8s/pvc.yaml)
- Приложение:
  `Deployment` [`k8s/app-deployment.yaml`](k8s/app-deployment.yaml) + `Service` [`k8s/app-service.yaml`](k8s/app-service.yaml)
- Разовая загрузка данных:
  `Job` [`k8s/loader-job.yaml`](k8s/loader-job.yaml)
- Конфигурация:
  `ConfigMap` [`k8s/configmap.yaml`](k8s/configmap.yaml)
- Секретные значения:
  `Secret` [`k8s/secret.yaml`](k8s/secret.yaml)

## Особенности реализации

- Для БД задано `replicas: 1`
- Для приложения задано `replicas: 3`, что соответствует варианту 10
- В `app-deployment.yaml` настроен `initContainer`, который ожидает доступность БД
- Для приложения настроены `readinessProbe` и `livenessProbe`
- Для БД подключен `PersistentVolumeClaim` объемом `1Gi`
- `loader Job` завершается со статусом `Complete`
- Приложение получает имя pod через переменную `POD_NAME`, что позволяет показывать экземпляр приложения и демонстрировать балансировку

## Использованные команды

```powershell
minikube start --profile lab3-docker --driver=docker
docker build -t cdap-analytics:lab3 .\Lab2
minikube -p lab3-docker image load cdap-analytics:lab3
kubectl apply -k .\Lab3\k8s
kubectl get all -n cdap-lab3
kubectl get pvc -n cdap-lab3
kubectl describe deployment credit-risk-app -n cdap-lab3
kubectl logs job/credit-risk-loader -n cdap-lab3
kubectl delete pod -n cdap-lab3 -l app=credit-risk-db
```

## Результаты проверки

1. Все основные ресурсы Kubernetes успешно созданы:
   `Deployment`, `Service`, `PVC`, `Job`, `Secret`, `ConfigMap`.
2. `credit-risk-loader` завершился со статусом `Complete`.
3. `credit-risk-app` работает в 3 репликах.
4. `postgres-pvc` находится в статусе `Bound`.
5. После удаления pod базы данных записи сохранились:
   до удаления pod в таблице `analytics_raw` было `2500` строк, после пересоздания pod осталось `2500` строк.

## Скриншоты

### 1. Общее состояние ресурсов кластера

![kubectl get all](docs/lab3_01_kubectl_get_all.png)

### 2. Состояние PVC

![kubectl get pvc](docs/lab3_02_kubectl_get_pvc.png)

### 3. Описание deployment приложения

![kubectl describe deployment](docs/lab3_03_kubectl_describe_app.png)

### 4. Логи ETL Job

![kubectl logs job](docs/lab3_04_kubectl_logs_loader.png)

### 5. Проверка доступа к приложению

Доступ подтвержден через `kubectl port-forward` и HTTP-запросы к `http://127.0.0.1:8501`.

![app access](docs/lab3_05_app_access.png)

### 6. Проверка персистентности данных

![persistence check](docs/lab3_06_persistence_check.png)

### 7. Список pod'ов после пересоздания БД

![kubectl get pods](docs/lab3_07_kubectl_get_pods.png)

## Вывод

В ходе работы приложение из Docker Compose было успешно перенесено в Kubernetes. Реализованы конфигурация через `ConfigMap` и `Secret`, хранение данных через `PVC`, разовая загрузка данных через `Job`, а также контроль жизненного цикла приложения с помощью `initContainer`, `readinessProbe` и `livenessProbe`. Требование варианта 10 выполнено: приложение развернуто в 3 репликах, база данных в 1 реплике.
