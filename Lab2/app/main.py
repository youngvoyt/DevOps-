import os

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine


def get_db_url() -> str:
    db_host = os.getenv("DB_HOST", "db")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "credit_risk")
    db_user = os.getenv("DB_USER", "cdap_user")
    db_password = os.getenv("DB_PASSWORD", "cdap_password")
    return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


st.set_page_config(page_title="CDAP - Credit Default Analytics", layout="centered")
st.title("CDAP: Credit Default Analytics")
st.caption("ЛР2: Docker + Compose + PostgreSQL + pgAdmin")

engine = create_engine(get_db_url())

metrics_df = pd.read_sql("SELECT * FROM analytics_metrics", engine)
sample_df = pd.read_sql("SELECT * FROM analytics_raw LIMIT 10", engine)

st.subheader("Метрики")
st.metric("Total records", int(metrics_df.loc[0, "total_records"]))
st.metric("Default rate", float(metrics_df.loc[0, "default_rate"]))

st.subheader("Первые 10 строк данных")
st.dataframe(sample_df, use_container_width=True)
