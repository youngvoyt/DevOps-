"""Тесты ETL (quality gate / отчётность ЛР4)."""

import pandas as pd

from src.etl_loader import normalize_columns


def test_normalize_columns_renames() -> None:
    df = pd.DataFrame({"Col Name": [1], "X": [2]})
    out = normalize_columns(df)
    assert list(out.columns) == ["col_name", "x"]
