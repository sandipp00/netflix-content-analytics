
import sqlite3
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = ROOT / "sql"


@pytest.fixture
def connection(tmp_path):
    """Create a temporary SQLite database for SQL query tests."""
    db_path = tmp_path / "netflix_test.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    conn.execute(
        """
        CREATE TABLE netflix_titles (
            show_id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            director TEXT,
            country TEXT,
            release_year INTEGER,
            listed_in TEXT,
            date_added TEXT
        )
        """
    )

    sample_rows = [
        (
            "s1", "Movie", "Film A", "Director A",
            "United States", 2020,
            "Dramas, International Movies", "January 10, 2020"
        ),
        (
            "s2", "Movie", "Film B", "Director A",
            "United States", 2019,
            "Comedies, International Movies", "March 15, 2021"
        ),
        (
            "s3", "TV Show", "Series A", "Director B",
            "India, United States", 2021,
            "TV Dramas, International TV Shows", "June 20, 2021"
        ),
        (
            "s4", "Movie", "Film C", "Director C",
            "Canada", 2018,
            "Documentaries", "July 5, 2022"
        ),
        (
            "s5", "TV Show", "Series B", "Director B",
            "Canada", 2022,
            "Comedies, TV Dramas", "August 1, 2022"
        ),
        (
            "s6", "Movie", "Film D", "Director D",
            None, 2023,
            "Action & Adventure", None
        ),
    ]

    conn.executemany(
        """
        INSERT INTO netflix_titles (
            show_id, type, title, director, country,
            release_year, listed_in, date_added
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        sample_rows,
    )
    conn.commit()

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
        "06_genre_ranking.sql",
        "07_year_over_year_growth.sql",
        "08_director_rankings.sql",
    ],
)
def test_sql_query_executes(connection, sql_file):
    query_path = SQL_DIR / sql_file
    assert query_path.exists(), f"SQL file not found: {query_path}"

    query = query_path.read_text(encoding="utf-8")
    cursor = connection.execute(query)
    rows = cursor.fetchall()

    assert cursor.description is not None
    assert rows, f"{sql_file} returned no rows"
