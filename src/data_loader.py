
"""Load and clean the Netflix titles dataset.

Loads data/netflix_titles.csv when available. Otherwise, generates
synthetic sample data and emits a warning so the fallback is visible.
See data/README.md for instructions on obtaining the real dataset.
"""

from pathlib import Path
import warnings

import pandas as pd

from src.generate_sample_data import generate_sample_dataframe

DEFAULT_DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "netflix_titles.csv"
)

REQUIRED_COLUMNS = {
    "type",
    "title",
    "date_added",
    "country",
    "listed_in",
    "cast",
    "director",
    "rating",
    "duration",
}


def load_raw(path=DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load the CSV or generate sample data if the file is absent."""
    path = Path(path)

    if path.is_file():
        try:
            return pd.read_csv(path)
        except (OSError, pd.errors.ParserError, UnicodeDecodeError) as exc:
            raise ValueError(
                f"Could not read the Netflix dataset at {path}: {exc}"
            ) from exc

    warnings.warn(
        f"Dataset not found at {path}. Using synthetic sample data; "
        "results will not represent the real Netflix catalog.",
        UserWarning,
        stacklevel=2,
    )
    return generate_sample_dataframe()


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich the raw Netflix titles dataframe."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")

    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    df = df.copy()

    # Normalize text columns and handle missing values.
    for column in ["director", "country", "cast"]:
        df[column] = (
            df[column].astype("string").fillna("Unknown").str.strip()
        )

    df["rating"] = (
        df["rating"].astype("string").fillna("Not Rated").str.strip()
    )

    # Parse dates safely; invalid or missing dates become NaT.
    df["date_added"] = pd.to_datetime(
        df["date_added"].astype("string").str.strip(),
        format="mixed",
        errors="coerce",
    )
    df["year_added"] = df["date_added"].dt.year
    df["month_added"] = df["date_added"].dt.month_name()

    # Normalize multi-value columns.
    for column in ["country", "listed_in"]:
        df[column] = (
            df[column].astype("string").fillna("Unknown").str.strip()
        )

    df["country_list"] = df["country"].apply(
        lambda value: [
            item.strip() for item in value.split(",") if item.strip()
        ]
        if value != "Unknown"
        else ["Unknown"]
    )

    df["genre_list"] = df["listed_in"].apply(
        lambda value: [
            item.strip() for item in value.split(",") if item.strip()
        ]
        if value != "Unknown"
        else []
    )

    df["cast_list"] = df["cast"].apply(
        lambda value: [
            item.strip() for item in value.split(",") if item.strip()
        ]
        if value != "Unknown"
        else []
    )

    df["primary_country"] = df["country_list"].apply(
        lambda countries: countries[0] if countries else "Unknown"
    )

    # Extract numeric duration without assuming every value is valid.
    duration_num = pd.to_numeric(
        df["duration"]
        .astype("string")
        .str.extract(r"(\d+)", expand=False),
        errors="coerce",
    )

    df["duration_minutes"] = duration_num.where(
        df["type"] == "Movie"
    )
    df["duration_seasons"] = duration_num.where(
        df["type"] == "TV Show"
    )

    return df


def load_clean(path=DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load the dataset and return its cleaned version."""
    return clean(load_raw(path))
