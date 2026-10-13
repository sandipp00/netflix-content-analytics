"""Data-quality regression tests for the cleaned Netflix dataset.

These tests validate invariants that should hold for both the deterministic
synthetic fixture and the real Kaggle dataset when it is supplied locally.
"""

import pandas as pd

from src.data_loader import clean
from src.generate_sample_data import generate_sample_dataframe
from src.data_quality import validate_titles

def test_sample_ids_are_unique():
    raw = generate_sample_dataframe(n_rows=500, seed=42)
    assert raw["show_id"].is_unique
    assert raw["show_id"].notna().all()


def test_cleaned_core_schema_and_types():
    df = clean(generate_sample_dataframe(n_rows=500, seed=42))

    required = {
        "show_id", "type", "title", "release_year", "rating",
        "country_list", "genre_list", "duration_minutes", "duration_seasons",
    }
    assert required.issubset(df.columns)
    assert df["title"].notna().all()
    assert df["type"].isin(["Movie", "TV Show"]).all()
    assert pd.api.types.is_integer_dtype(df["release_year"])
    assert df["release_year"].between(1900, 2100).all()


def test_cleaned_multivalue_fields_are_lists():
    df = clean(generate_sample_dataframe(n_rows=200, seed=42))

    assert df["country_list"].map(lambda x: isinstance(x, list) and len(x) >= 1).all()
    assert df["genre_list"].map(lambda x: isinstance(x, list) and len(x) >= 1).all()
    assert df["cast_list"].map(lambda x: isinstance(x, list)).all()


def test_duration_features_match_content_type():
    df = clean(generate_sample_dataframe(n_rows=500, seed=42))

    movies = df["type"].eq("Movie")
    shows = df["type"].eq("TV Show")

    assert df.loc[movies, "duration_minutes"].notna().all()
    assert df.loc[movies, "duration_seasons"].isna().all()
    assert df.loc[shows, "duration_seasons"].notna().all()
    assert df.loc[shows, "duration_minutes"].isna().all()

    assert (df.loc[movies, "duration_minutes"] > 0).all()
    assert (df.loc[shows, "duration_seasons"] > 0).all()


def test_cleaning_is_deterministic():
    raw = generate_sample_dataframe(n_rows=100, seed=99)
    first = clean(raw)
    second = clean(raw)

    pd.testing.assert_frame_equal(first, second)



def test_duplicate_ids_are_reported():
    df = pd.DataFrame({
        "show_id": ["s1", "s1"],
        "type": ["Movie", "Movie"],
        "title": ["Film A", "Film B"],
        "release_year": [2020, 2021],
    })

    result = validate_titles(df)

    assert result["duplicate_show_id_rows"] == 2


def test_missing_required_fields_are_reported():
    df = pd.DataFrame({
        "show_id": ["s1", "s2"],
        "type": ["Movie", "TV Show"],
        "title": ["Film A", " "],
        "release_year": [2020, 2021],
    })

    result = validate_titles(df)

    assert result["missing_required_fields"]["title"] == 1


def test_invalid_content_types_are_reported():
    df = pd.DataFrame({
        "show_id": ["s1"],
        "type": ["Series"],
        "title": ["Example"],
        "release_year": [2020],
    })

    assert validate_titles(df)["invalid_content_types"] == 1


def test_invalid_release_years_are_reported():
    df = pd.DataFrame({
        "show_id": ["s1", "s2", "s3"],
        "type": ["Movie", "Movie", "Movie"],
        "title": ["Film A", "Film B", "Film C"],
        "release_year": [1800, "unknown", 2020],
    })

    assert validate_titles(df)["invalid_release_years"] == 2


def test_missing_required_column_raises_error():
    import pytest

    df = pd.DataFrame({
        "show_id": ["s1"],
        "type": ["Movie"],
        "title": ["Film A"],
    })

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_titles(df)
