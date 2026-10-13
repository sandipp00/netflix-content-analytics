# 🎬 Netflix Content Analytics

Exploratory data analysis and an interactive dashboard for the Netflix content catalog. The project analyzes content type, catalog growth, release years, countries, genres, ratings, duration, and directors using the Netflix Movies and TV Shows dataset.

Built as a data analyst portfolio project with a reusable analysis layer (`src/`), a full EDA notebook, SQL analysis with SQLite, and a Streamlit dashboard sharing the same analysis functions.

## Features

- **Reusable analysis module** (`src/analysis.py`) — pandas functions for every chart, unit-tested and shared between the notebook and the dashboard.
- **EDA notebook** (`notebooks/01_eda.ipynb`) — cleaning, missing-value audit, and a full walkthrough with commentary.
- **Interactive dashboard** (`app.py`) — Streamlit + Plotly, with filters for content type, release year range, and country, plus KPI tiles, 7 interactive charts, and a duration summary table.
- **SQL analysis** (`sql/`) — five SQLite queries answering business questions about content type, country entries, genres, release trends, and directors.
- **Works without a Kaggle account** — if the real dataset isn't present, a synthetic sample with the same schema is generated automatically (`src/generate_sample_data.py`), so `git clone && run` works immediately. The SQLite import step requires the real CSV.
- **Tested** — `pytest` suite covering data cleaning, analysis functions, and execution of SQL queries; GitHub Actions CI runs the repository's configured tests on every push/PR.

## Project structure

```
netflix-content-analytics/
├── app.py                     # Streamlit dashboard
├── data/
│   ├── README.md              # How to get the real Kaggle dataset
│   └── netflix_titles.csv     # (not committed — see data/README.md)
├── database/
│   └── import_csv_to_sqlite.py # Import the CSV into a local SQLite database
├── sql/
│   ├── 01_content_overview.sql
│   ├── 02_country_analysis.sql
│   ├── 03_genre_analysis.sql
│   ├── 04_release_trends.sql
│   └── 05_advanced_analysis.sql
├── notebooks/
│   └── 01_eda.ipynb           # Full exploratory analysis
├── src/
│   ├── data_loader.py         # Load + clean the dataset
│   ├── generate_sample_data.py # Synthetic fallback dataset
│   └── analysis.py            # Chart-ready aggregation functions
├── tests/
│   ├── test_data_loader.py
│   ├── test_analysis.py
│   └── test_sql_queries.py    # SQL execution tests
├── .github/workflows/ci.yml   # CI: install deps + run pytest
├── requirements.txt
└── LICENSE
```

## Getting started

### Windows PowerShell

```powershell
git clone https://github.com/sandipp00/netflix-content-analytics.git
cd netflix-content-analytics
python -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
```

### macOS / Linux

```bash
git clone https://github.com/sandipp00/netflix-content-analytics.git
cd netflix-content-analytics
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Run the dashboard

```bash
streamlit run app.py
```

### Run the notebook

```bash
jupyter notebook notebooks/01_eda.ipynb
```

### Run the tests

```bash
python -m pytest -v
```

## SQL analysis with SQLite

The project includes a small SQL analysis layer alongside the Python EDA and dashboard. The queries use the local SQLite table `netflix_titles` to answer practical catalog questions.

### Business questions

- What is the distribution of Movies and TV Shows?
- Which country entries are most common in the dataset?
- Which genres are most frequently listed?
- How does the release-year mix differ between Movies and TV Shows?
- Which directors have the most titles?

### SQL concepts demonstrated

- Aggregation with `COUNT()` and `GROUP BY`
- Handling missing values with `COALESCE()` and `NULLIF()`
- Common Table Expressions (CTEs), including a recursive CTE to split genre values
- Filtering and sorting with `WHERE`, `ORDER BY`, and `LIMIT`
- Query execution tests with `pytest`

### Query files

| File | Purpose |
|---|---|
| `sql/01_content_overview.sql` | Movie vs. TV Show distribution |
| `sql/02_country_analysis.sql` | Most common country field values |
| `sql/03_genre_analysis.sql` | Most frequently listed genres |
| `sql/04_release_trends.sql` | Release-year trends by content type |
| `sql/05_advanced_analysis.sql` | Directors with the most titles |
| `sql/06_genre_ranking.sql` | Genre ranking analysis |
| `sql/07_year_over_year_growth.sql` | Year-over-year growth analysis |
| `sql/08_director_rankings.sql` | Director ranking analysis |


### Build the local database

Download the real `netflix_titles.csv` dataset and place it in the `data/` folder as described in [`data/README.md`](data/README.md). From the repository root, run:

```powershell
python database/import_csv_to_sqlite.py
```

This creates `database/netflix.db` locally. Database files and generated outputs are excluded from Git; the source CSV is also not committed. The SQL import requires the real CSV, and its results should not be interpreted as real-world insights if you substitute synthetic data.

Run the SQL query tests with:

```powershell
python -m pytest tests/test_sql_queries.py -v
```

The SQL tests create a temporary SQLite database populated with synthetic fixture records. They verify that all eight SQL files exist, execute successfully, and return results without requiring the real dataset or a local database.

## Dataset

This project is built around the Kaggle [**Netflix Movies and TV Shows**](https://www.kaggle.com/datasets/shivamb/netflix-shows) dataset (`netflix_titles.csv`: title, type, director, cast, country, date added, release year, rating, duration, genres, description).

See [`data/README.md`](data/README.md) for how to download it. Without it, the Python dashboard and EDA entry points can fall back to generated sample data with identical structure — convenient for development, but not a substitute for the real data when drawing conclusions. The SQLite import script expects the real CSV at `data/netflix_titles.csv`.

## What this project demonstrates

- **Data cleaning:** missing-value handling, date parsing, multi-value field normalization, and duration feature extraction.
- **Exploratory analysis:** content mix, catalog growth, release trends, ratings, countries, genres, and directors.
- **SQL analysis:** SQLite queries using aggregation, CTEs, recursive splitting, filtering, and sorting.
- **Dashboarding:** interactive filtering with Streamlit and Plotly.
- **Software quality:** reusable analysis functions, deterministic test data, pytest coverage, and GitHub Actions CI.
- **Reproducibility:** the project runs without committing the Kaggle dataset and clearly separates synthetic fallback data from real-data analysis.

## Portfolio notes

For portfolio screenshots and interview discussions, use the **real Netflix dataset** rather than the synthetic fallback. The synthetic dataset exists only to make the repository runnable and testable without external data access.

## Business insights from the real dataset

The EDA was run against the real Kaggle dataset containing **8,807 titles**. The main findings are:

- **Movies dominate the catalog:** 6,131 titles (69.6%) are movies versus 2,676 TV Shows (30.4%).
- **The U.S. is the largest represented market:** 3,690 title records are associated with the United States. Because titles can have multiple countries, this is an association count, not a unique-title total.
- **International Movies is the largest genre category:** 2,752 title records are classified under this category; titles can belong to multiple genre categories.
- **Movie runtimes cluster around feature length:** average runtime is 99.6 minutes and median runtime is 98 minutes.
- **TV series are generally short:** the average is 1.8 seasons and the median is 1 season, although the maximum reaches 17 seasons.
- **Metadata completeness is uneven:** director has the highest missing rate at 29.9%, followed by country and cast at 9.4% each.
- **Catalog additions accelerated in the late 2010s:** the EDA shows a substantial rise in titles added during the late 2010s, followed by fewer additions in the latest years represented. This measures catalog additions, not Netflix production volume.

> **Analytical caveat:** the dataset is a catalog snapshot, so these findings describe the dataset represented here rather than Netflix's current catalog or business performance.

## Dashboard

The Streamlit dashboard provides interactive filtering by content type, release year, and country, with KPI cards, seven charts, and a duration summary table.

**Live demo:** [Netflix Content Analytics on Streamlit](https://netflix-content-analytics-gvhhhww7ij8tx8tmzhhowc.streamlit.app/)

### Dashboard screenshots

**Dashboard overview**

<img src="https://github.com/sandipp00/netflix-content-analytics/blob/master/docs/dashboard-overview.webp?raw=true" alt="Netflix dashboard overview" width="100%">

**Interactive filters**

<img src="https://github.com/sandipp00/netflix-content-analytics/blob/master/docs/dashboard-filters.webp?raw=true" alt="Netflix dashboard interactive filters" width="100%">

The screenshots above were captured from the deployed Streamlit application and show both the default dashboard and an interactive filtered view.

## Deploy with Streamlit Community Cloud

1. Push/merge this repository to GitHub.
2. Open Streamlit Community Cloud and sign in with GitHub.
3. Create a new app and select this repository, branch `master`, and entrypoint `app.py`.
4. Deploy the app.
5. Add the resulting public URL to the **Live demo** line above.

The repository is already structured for deployment: dependencies are declared in `requirements.txt`, the app falls back to deterministic sample data when the real CSV is absent, and no secrets are required.

## Tech stack

Python · pandas · SQLite · Streamlit · Plotly · Matplotlib/Seaborn · pytest · GitHub Actions

## License

[MIT](LICENSE)
