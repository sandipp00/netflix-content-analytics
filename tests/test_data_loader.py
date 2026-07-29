import pandas as pd

from src.data_loader import clean
from src.generate_sample_data import generate_sample_dataframe


def test_generate_sample_dataframe_schema():
    df = generate_sample_dataframe(n_rows=50, seed=1)
    expected_cols = {
        "show_id", "type", "title", "director", "cast", "country",
        "date_added", "release_year", "rating", "duration", "listed_in",
        "description",
    }
    assert expected_cols.issubset(df.columns)
    assert len(df) == 50
    assert set(df["type"].unique()) <= {"Movie", "TV Show"}


def test_generate_sample_dataframe_is_deterministic():
    df1 = generate_sample_dataframe(n_rows=20, seed=7)
    df2 = generate_sample_dataframe(n_rows=20, seed=7)
    pd.testing.assert_frame_equal(df1, df2)


def test_clean_fills_missing_values():
    raw = generate_sample_dataframe(n_rows=30, seed=3)
    raw.loc[0, "director"] = None
    raw.loc[0, "country"] = None
    df = clean(raw)
    assert df.loc[0, "director"] == "Unknown"
    assert df.loc[0, "country"] == "Unknown"
    assert not df["rating"].isna().any()


def test_clean_derives_expected_columns():
    df = clean(generate_sample_dataframe(n_rows=30, seed=4))
    for col in ["year_added", "country_list", "genre_list", "cast_list", "primary_country"]:
        assert col in df.columns

    movies = df[df["type"] == "Movie"]
    shows = df[df["type"] == "TV Show"]
    assert movies["duration_minutes"].notna().all()
    assert movies["duration_seasons"].isna().all()
    assert shows["duration_seasons"].notna().all()
    assert shows["duration_minutes"].isna().all()
