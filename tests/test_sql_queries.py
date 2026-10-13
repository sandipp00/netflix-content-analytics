import sqlite3
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "database" / "netflix.db"
SQL_DIR = ROOT / "sql"


@pytest.fixture
def connection():
    if not DB_PATH.exists():
        pytest.skip("Netflix SQLite database not found. Import the CSV first.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
    finally:
        conn.close()


@pytest.mark.parametrize(
    "sql_file",
    [
        "01_content_overview.sql",
        "02_country_analysis.sql",
        "03_genre_analysis.sql",
        "04_release_trends.sql",
        "05_advanced_analysis.sql",
    ],
)
def test_sql_query_executes(connection, sql_file):
    query_path = SQL_DIR / sql_file
    assert query_path.exists(), f"SQL file not found: {query_path}"

    query = query_path.read_text(encoding="utf-8")
    cursor = connection.execute(query)
    rows = cursor.fetchall()

    assert rows, f"{sql_file} returned no rows"
    assert cursor.description is not None