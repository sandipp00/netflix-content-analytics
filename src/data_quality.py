
"""Data quality validation for Netflix titles."""

import pandas as pd

VALID_TYPES = {"Movie", "TV Show"}
REQUIRED_COLUMNS = {"show_id", "type", "title", "release_year"}


def validate_titles(df: pd.DataFrame) -> dict:
    """Return data quality metrics without modifying the DataFrame."""
    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    duplicate_ids = int(
        df["show_id"].duplicated(keep=False).sum()
    )

    missing_required = {}

    for column in ["show_id", "type", "title"]:
        values = df[column].astype("string")
        missing_required[column] = int(
            (values.isna() | values.str.strip().eq("")).sum()
        )

    invalid_types = int(
        (~df["type"].isin(VALID_TYPES)).sum()
    )

    years = pd.to_numeric(df["release_year"], errors="coerce")
    nonblank_years = (
        df["release_year"].notna()
        & df["release_year"].astype("string").str.strip().ne("")
    )

    invalid_years = (
        nonblank_years
        & (
            years.isna()
            | (years < 1900)
            | (years > pd.Timestamp.now().year)
            | (years % 1 != 0)
        )
    )

    return {
        "row_count": len(df),
        "duplicate_show_id_rows": duplicate_ids,
        "missing_required_fields": missing_required,
        "invalid_content_types": invalid_types,
        "invalid_release_years": int(invalid_years.sum()),
    }
