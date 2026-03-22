"""
Точка входа для CI/CD (ЛР4): проверка, что образ собран и отдаёт версию без БД и Streamlit.
"""

import argparse

__version__ = "1.0.0"
APP_NAME = "cdap-analytics-lab2"


def main() -> None:
    parser = argparse.ArgumentParser(description="CDAP Analytics — версия образа (Lab2)")
    parser.add_argument(
        "--version",
        action="version",
        version=f"{APP_NAME} {__version__}",
    )
    parser.parse_args()


if __name__ == "__main__":
    main()
