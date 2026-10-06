"""Reusable analysis functions over the cleaned Netflix titles dataframe.

Each function takes the cleaned dataframe (see src.data_loader.load_clean)
and returns a small, chart-ready dataframe or scalar. Kept dependency-free
of any plotting library so the same functions serve the notebook, the
Streamlit app, and the tests.
"""

import pandas as pd


def content_type_counts(df: pd.DataFrame) -> pd.DataFrame:
    return df["type"].value_counts().rename_axis("type").reset_index(name="count")


def titles_added_per_year(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.dropna(subset=["year_added"])
        .groupby(["year_added", "type"])
        .size()
        .reset_index(name="count")
    )
    out["year_added"] = out["year_added"].astype(int)
    return out.sort_values("year_added")


def top_countries(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    exploded = df.explode("country_list")
    exploded = exploded[exploded["country_list"] != "Unknown"]
    counts = exploded["country_list"].value_counts().head(n)
    return counts.rename_axis("country").reset_index(name="count")


def top_genres(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    exploded = df.explode("genre_list")
    counts = exploded["genre_list"].value_counts().head(n)
    return counts.rename_axis("genre").reset_index(name="count")


def rating_distribution(df: pd.DataFrame) -> pd.DataFrame:
    return df["rating"].value_counts().rename_axis("rating").reset_index(name="count")


def duration_summary(df: pd.DataFrame) -> pd.DataFrame:
    movies = df.loc[df["type"] == "Movie", "duration_minutes"].dropna()
    shows = df.loc[df["type"] == "TV Show", "duration_seasons"].dropna()
    return pd.DataFrame(
        {
            "type": ["Movie (minutes)", "TV Show (seasons)"],
            "mean": [movies.mean(), shows.mean()],
            "median": [movies.median(), shows.median()],
            "min": [movies.min(), shows.min()],
            "max": [movies.max(), shows.max()],
        }
    )


def release_year_trend(df: pd.DataFrame) -> pd.DataFrame:
    out = df.groupby(["release_year", "type"]).size().reset_index(name="count")
    return out.sort_values("release_year")


def top_directors(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    counts = df.loc[df["director"] != "Unknown", "director"].value_counts().head(n)
    return counts.rename_axis("director").reset_index(name="count")


def kpi_summary(df: pd.DataFrame) -> dict:
    if df.empty:
        years_covered = 0
    else:
        years_covered = int(df["release_year"].max() - df["release_year"].min() + 1)

    return {
        "total_titles": int(len(df)),
        "movies": int((df["type"] == "Movie").sum()),
        "tv_shows": int((df["type"] == "TV Show").sum()),
        "countries": int(df.explode("country_list")["country_list"].nunique()),
        "genres": int(df.explode("genre_list")["genre_list"].nunique()),
        "years_covered": years_covered,
    }
