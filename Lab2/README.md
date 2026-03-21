# Лабораторная работа №2 — Docker и Docker Compose

## Студент

| | |
|---|---|
| **ФИО** | Войт Иван Иванович |
| **Группа** | БД-251м |
| **Вариант** | **10** |

**Предметная область (как в ЛР1):** предсказание дефолта заемщиков (финансы).

---

## О работе

В рамках задания я **самостоятельно** подготовил переносимый стек: описал сервисы в **Docker Compose**, собрал образ приложения по **Dockerfile**, настроил переменные окружения через **`.env`**, проверил запуск на **Windows (Docker Desktop)** и зафиксировал результат скриншотами в папке `docs/`.  
Код ETL и дашборда писал и отлаживал локально; при необходимости правил порты (например, если `5432` был занят на ПК) и параметры в `.env`.

---

## Что сделано по варианту 10

| Компонент | Назначение |
|-----------|------------|
| **PostgreSQL** (`db`) | Хранение таблиц после загрузки и расчёта метрик |
| **Loader** (init) | Одноразовый контейнер: читает CSV, пишет данные в БД, завершается |
| **Streamlit** (`analytics_app`) | Веб-интерфейс: метрики и выборка из БД |
| **pgAdmin** | Веб-GUI для PostgreSQL (требование варианта) |

Сеть: **`backend-network`**. Пароли и порты — из **`.env`**, не зашиты в `docker-compose.yml`. Данные БД — в **именованном volume**.

---

## Откуда берётся датасет

Файл **`course_project_test.csv`** должен лежать в **корне репозитория** (как в лабораторной №1), **рядом с папкой `Lab2/`**.  
В `docker-compose.yml` он подключается в loader **только на чтение** (`:ro`).

---

## Запуск (PowerShell)

Перейди в каталог лабораторной:

```powershell
cd Lab2
```

Создай локальный конфиг (в Git не коммитится):

```powershell
Copy-Item .env.example .env
```

При необходимости отредактируй `.env` (пароли, `POSTGRES_PORT`, `PGADMIN_PORT`).

Подними контейнеры:

```powershell
docker compose up --build -d
```

Если на Windows сборка падает с ошибкой BuildKit, перед запуском:

```powershell
$env:DOCKER_BUILDKIT="0"
$env:COMPOSE_DOCKER_CLI_BUILD="0"
docker compose up --build -d
```

Проверка:

```powershell
docker compose ps
```

| Сервис | Адрес в браузере |
|--------|------------------|
| Дашборд (Streamlit) | http://127.0.0.1:8501 |
| pgAdmin | http://127.0.0.1:5050 |

**Вход в pgAdmin:** email и пароль из `.env` (`PGADMIN_DEFAULT_EMAIL`, `PGADMIN_DEFAULT_PASSWORD`).  
Важно: в поле email **не использовать** адреса вида `*@something.local` — образ pgAdmin может их отклонить; лучше `admin@example.com` или обычная почта.

**Подключение сервера в pgAdmin:**

| Параметр | Значение |
|----------|-----------|
| Host | `cdap-db` |
| Port | `5432` *(внутри Docker; не путать с портом хоста из `.env`)* |
| Database / User / Password | как в `.env` (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`) |

---

## Структура папки `Lab2/`

```
Lab2/
├── app/
│   └── main.py              # Streamlit-приложение
├── src/
│   └── etl_loader.py        # ETL: CSV → PostgreSQL
├── data/
│   └── data_dictionary.md   # краткое описание полей (связь с ЛР1)
├── docs/                    # скриншоты для отчёта
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example             # шаблон переменных (без секретов)
├── requirements.txt
└── README.md
```

---

## Скриншоты для защиты

Файлы размещаются в **`Lab2/docs/`**:

| Файл | Что показать |
|------|----------------|
| `lab2_01_docker_compose_ps.png` | вывод `docker compose ps` |
| `lab2_01b_docker_ps.png` | вывод `docker ps -a` (если требует методичка) |
| `lab2_02_db_logs.png` | логи PostgreSQL: `docker compose logs db` |
| `lab2_03_loader_success.png` | успешный ETL: `docker compose logs loader` |
| `lab2_04_analytics_app_logs.png` | логи приложения: `docker compose logs analytics_app` |
| `lab2_05_streamlit_dashboard.png` | открытый в браузере Streamlit |
| `lab2_07_pgadmin_connected.png` | pgAdmin с подключением к БД и таблицами |

---

## Остановка

```powershell
docker compose down
```

Полный сброс данных БД и pgAdmin (тома):

```powershell
docker compose down -v
```

---

*Репозиторий на GitHub: [youngvoyt/DevOps-](https://github.com/youngvoyt/DevOps-). Материалы ЛР2 — в каталоге [`Lab2`](https://github.com/youngvoyt/DevOps-/tree/main/Lab2).*
