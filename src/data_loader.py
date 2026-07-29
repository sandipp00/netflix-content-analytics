"""Load and clean the Netflix titles dataset.

Looks for data/netflix_titles.csv (the Kaggle "Netflix Movies and TV Shows"
dataset). If it isn't present, generates a synthetic sample so the project
still runs end-to-end. See data/README.md for how to fetch the real dataset.
"""

import os

import pandas as pd

from src.generate_sample_data import generate_sample_dataframe

DEFAULT_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "netflix_titles.csv")


def load_raw(path: str = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load netflix_titles.csv, falling back to a generated sample dataset."""
    if os.path.exists(path):
        return pd.read_csv(path)
    return generate_sample_dataframe()


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich the raw Netflix titles dataframe.

    - Parses date_added into a real datetime and derives year/month_added.
    - Splits multi-value columns (country, listed_in, cast) into lists.
    - Extracts numeric duration for movies (minutes) and shows (seasons).
    - Fills missing director/country/rating with "Unknown".
    """
    df = df.copy()

    df["director"] = df["director"].fillna("Unknown")
    df["country"] = df["country"].fillna("Unknown")
    df["rating"] = df["rating"].fillna("Not Rated")
    df["cast"] = df["cast"].fillna("Unknown")

    df["date_added"] = pd.to_datetime(df["date_added"].str.strip(), errors="coerce")
    df["year_added"] = df["date_added"].dt.year
    df["month_added"] = df["date_added"].dt.month_name()

    df["country_list"] = df["country"].apply(lambda x: [c.strip() for c in x.split(",")])
    df["genre_list"] = df["listed_in"].apply(lambda x: [g.strip() for g in x.split(",")])
    df["cast_list"] = df["cast"].apply(
        lambda x: [c.strip() for c in x.split(",")] if x != "Unknown" else []
    )
    df["primary_country"] = df["country_list"].apply(lambda lst: lst[0])

    duration_num = df["duration"].str.extract(r"(\d+)").astype(float)[0]
    df["duration_minutes"] = duration_num.where(df["type"] == "Movie")
    df["duration_seasons"] = duration_num.where(df["type"] == "TV Show")

    return df


def load_clean(path: str = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Convenience wrapper: load_raw + clean in one call."""
    return clean(load_raw(path))
