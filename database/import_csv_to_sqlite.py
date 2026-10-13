
from pathlib import Path
import sqlite3

import pandas as pd

# Resolve paths from the repository root.
ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "netflix_titles.csv"
DB_PATH = ROOT / "database" / "netflix.db"


def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {CSV_PATH}\n"
            "Place netflix_titles.csv inside the data folder."
        )

    df = pd.read_csv(CSV_PATH)

    if df.empty:
        raise ValueError("The Netflix CSV contains no records.")

    required_columns = {
        "show_id",
        "type",
        "title",
        "release_year",
        "country",
        "listed_in",
    }
    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    # Keep the source dataset unchanged; SQLite receives its own copy.
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(
            "netflix_titles",
            conn,
            if_exists="replace",
            index=False,
        )

        total = pd.read_sql_query(
            "SELECT COUNT(*) AS total FROM netflix_titles",
            conn,
        ).iloc[0]["total"]

        print(f"Database created: {DB_PATH}")
        print(f"Rows imported: {total}")
        print("Columns:")
        print(", ".join(df.columns))

    print("Import completed successfully.")


if __name__ == "__main__":
    main()
