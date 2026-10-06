# 🎬 Netflix Content Analytics

Exploratory data analysis and an interactive dashboard for the Netflix content catalog. The project analyzes content type, catalog growth, release years, countries, genres, ratings, duration, and directors using the Netflix Movies and TV Shows dataset.

Built as a data analyst portfolio project with a reusable analysis layer (`src/`), a full EDA notebook, and a Streamlit dashboard sharing the same analysis functions.

## Features

- **Reusable analysis module** (`src/analysis.py`) — pandas functions for every chart, unit-tested and shared between the notebook and the dashboard.
- **EDA notebook** (`notebooks/01_eda.ipynb`) — cleaning, missing-value audit, and a full walkthrough with commentary.
- **Interactive dashboard** (`app.py`) — Streamlit + Plotly, with filters for content type, release year range, and country, plus KPI tiles and 8 charts.
- **Works without a Kaggle account** — if the real dataset isn't present, a synthetic sample with the same schema is generated automatically (`src/generate_sample_data.py`), so `git clone && run` works immediately.
- **Tested** — `pytest` suite covering data cleaning and every analysis function; GitHub Actions CI runs it on every push/PR.

## Project structure

```
netflix-content-analytics/
├── app.py                     # Streamlit dashboard
├── data/
│   ├── README.md              # How to get the real Kaggle dataset
│   └── netflix_titles.csv     # (not committed — see data/README.md)
├── notebooks/
│   └── 01_eda.ipynb           # Full exploratory analysis
├── src/
│   ├── data_loader.py         # Load + clean the dataset
│   ├── generate_sample_data.py# Synthetic fallback dataset
│   └── analysis.py            # Chart-ready aggregation functions
├── tests/
│   ├── test_data_loader.py
│   └── test_analysis.py
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
pytest -v
```

## Dataset

This project is built around the Kaggle [**Netflix Movies and TV Shows**](https://www.kaggle.com/datasets/shivamb/netflix-shows) dataset (`netflix_titles.csv`: title, type, director, cast, country, date added, release year, rating, duration, genres, description).

See [`data/README.md`](data/README.md) for how to download it. Without it, every entry point falls back to a generated sample dataset with identical structure — convenient for development, but not a substitute for the real data when drawing conclusions.

## What this project demonstrates

- **Data cleaning:** missing-value handling, date parsing, multi-value field normalization, and duration feature extraction.
- **Exploratory analysis:** content mix, catalog growth, release trends, ratings, countries, genres, and directors.
- **Dashboarding:** interactive filtering with Streamlit and Plotly.
- **Software quality:** reusable analysis functions, deterministic test data, pytest coverage, and GitHub Actions CI.
- **Reproducibility:** the project runs without committing the Kaggle dataset and clearly separates synthetic fallback data from real-data analysis.

## Portfolio notes

For portfolio screenshots and interview discussions, use the **real Netflix dataset** rather than the synthetic fallback. The synthetic dataset exists only to make the repository runnable and testable without external data access.

## Tech stack

Python · pandas · Streamlit · Plotly · Matplotlib/Seaborn · pytest · GitHub Actions

## License

[MIT](LICENSE)
