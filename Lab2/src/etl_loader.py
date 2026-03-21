import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


def get_db_url() -> str:
    db_host = os.getenv("DB_HOST", "db")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "credit_risk")
    db_user = os.getenv("DB_USER", "cdap_user")
    db_password = os.getenv("DB_PASSWORD", "cdap_password")
    return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def run_etl() -> None:
    input_file = Path(os.getenv("ETL_INPUT_FILE", "/app/input/course_project_test.csv"))
    if not input_file.exists():
        raise FileNotFoundError(f"Input dataset not found: {input_file}")

    print(f"[ETL] Reading file: {input_file}")
    df = pd.read_csv(input_file)
    if df.empty:
        raise ValueError("Input dataset is empty")

    df = normalize_columns(df)

    target_candidates = ["target_default", "target", "default", "is_default"]
    target_col = next((c for c in target_candidates if c in df.columns), None)
    if target_col is None:
        df["target_default"] = 0
        target_col = "target_default"

    db_url = get_db_url()
    engine = create_engine(db_url)

    print("[ETL] Writing table analytics_raw")
    df.to_sql("analytics_raw", engine, if_exists="replace", index=False)

    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS analytics_metrics"))
        conn.execute(
            text(
                f"""
                CREATE TABLE analytics_metrics AS
                SELECT
                    COUNT(*)::INT AS total_records,
                    ROUND(AVG(CAST({target_col} AS NUMERIC)), 6) AS default_rate
                FROM analytics_raw
                """
            )
        )

    print("[ETL] Done: analytics_raw and analytics_metrics created successfully")


if __name__ == "__main__":
    run_etl()
