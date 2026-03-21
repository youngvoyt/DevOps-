# Лабораторная работа №2 — Docker и Docker Compose

**Вариант 10:** PostgreSQL + pgAdmin + ETL (loader) + Streamlit.

Материалы лабораторной лежат **в этой папке `Lab2/`**. Датасет `course_project_test.csv` ожидается в **корне репозитория** (как в ЛР1).

## Быстрый старт

Открой PowerShell и перейди в `Lab2`:

```powershell
cd Lab2
Copy-Item .env.example .env
# при необходимости отредактируй .env (порты, пароли)
```

Убедись, что файл **`..\course_project_test.csv`** существует (на уровень выше папки `Lab2`).

При ошибках сборки на Windows (BuildKit):

```powershell
$env:DOCKER_BUILDKIT="0"
$env:COMPOSE_DOCKER_CLI_BUILD="0"
docker compose up --build -d
```

Проверка:

```powershell
docker compose ps
```

- Streamlit: http://127.0.0.1:8501  
- pgAdmin: http://127.0.0.1:5050 (логин/пароль из `.env`, email — **не** `*.local`, например `admin@example.com`)

Подключение к БД из pgAdmin: **Host** `cdap-db`, **Port** `5432`, БД/пользователь из `.env`.

## Структура `Lab2/`

```text
Lab2/
├── app/main.py           # Streamlit
├── src/etl_loader.py    # ETL в PostgreSQL
├── data/data_dictionary.md
├── docs/                 # скриншоты отчёта
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── requirements.txt
└── README.md
```

## Скриншоты (пример имён)

Файлы клади в **`Lab2/docs/`**:

- `lab2_01_docker_compose_ps.png` — `docker compose ps`
- `lab2_01b_docker_ps.png` — `docker ps -a` (по требованию методички)
- `lab2_02_db_logs.png` — логи PostgreSQL
- `lab2_03_loader_success.png` — `docker compose logs loader`
- `lab2_04_analytics_app_logs.png` — логи Streamlit
- `lab2_05_streamlit_dashboard.png` — браузер
- `lab2_07_pgadmin_connected.png` — pgAdmin с таблицами

## Остановка

```powershell
docker compose down
docker compose down -v   # с удалением данных БД
```
