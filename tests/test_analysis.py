import pytest

from src import analysis
from src.data_loader import clean
from src.generate_sample_data import generate_sample_dataframe


@pytest.fixture
def df():
    return clean(generate_sample_dataframe(n_rows=200, seed=42))


def test_content_type_counts(df):
    result = analysis.content_type_counts(df)
    assert result["count"].sum() == len(df)
    assert set(result["type"]) <= {"Movie", "TV Show"}


def test_titles_added_per_year(df):
    result = analysis.titles_added_per_year(df)
    assert (result["count"] > 0).all()
    assert result["year_added"].is_monotonic_increasing
    assert result[["year_added", "type"]].duplicated().sum() == 0


def test_top_countries_excludes_unknown(df):
    result = analysis.top_countries(df, n=5)
    assert "Unknown" not in result["country"].values
    assert len(result) <= 5


def test_top_genres_shape(df):
    result = analysis.top_genres(df, n=5)
    assert len(result) <= 5
    assert (result["count"] > 0).all()


def test_rating_distribution_sums_to_total(df):
    result = analysis.rating_distribution(df)
    assert result["count"].sum() == len(df)


def test_duration_summary_has_both_types(df):
    result = analysis.duration_summary(df)
    assert set(result["type"]) == {"Movie (minutes)", "TV Show (seasons)"}


def test_kpi_summary_matches_counts(df):
    kpis = analysis.kpi_summary(df)
    assert kpis["total_titles"] == len(df)
    assert kpis["movies"] + kpis["tv_shows"] == kpis["total_titles"]
    assert kpis["years_covered"] == (
        df["release_year"].max() - df["release_year"].min() + 1
    )


def test_release_year_trend(df):
    result = analysis.release_year_trend(df)

    assert set(result["type"]) <= {"Movie", "TV Show"}
    assert (result["count"] > 0).all()
    assert result["release_year"].is_monotonic_increasing


def test_top_directors_excludes_unknown(df):
    result = analysis.top_directors(df, n=5)

    assert "Unknown" not in result["director"].values
    assert len(result) <= 5
    assert (result["count"] > 0).all()
