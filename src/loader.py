"""
Data loader for credit default dataset (course_project_test.csv).
"""

from pathlib import Path


def load_data(path: str):
    """
    Заглушка: имитация загрузки данных из локального CSV.
    В реальном проекте здесь будет чтение CSV и базовая проверка.
    """
    csv_path = Path(path)
    if not csv_path.exists():
        print(f"[WARN] File {csv_path} not found. Please make sure it is placed in the project directory.")
        return None

    print(f"[INFO] Loading data from {csv_path} ...")
    # TODO: реализовать фактическую загрузку данных, например через pandas.read_csv
    return None


if __name__ == "__main__":
    # Вариант 10: используем датасет course_project_test.csv из подкаталога data
    load_data("data/course_project_test.csv")

