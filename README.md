# 🎬 Netflix Content Analytics

Exploratory data analysis and an interactive dashboard for the Netflix
content catalog — content type mix, release/add trends, top countries and
genres, ratings, duration, and directors.

Built as a data science portfolio project: a reusable analysis layer
(`src/`), a full EDA notebook, and a Streamlit dashboard on top of the same
code, so nothing is written twice.

## Features

- **Reusable analysis module** (`src/analysis.py`) — pandas functions for
  every chart, unit-tested and shared between the notebook and the dashboard.
- **EDA notebook** (`notebooks/01_eda.ipynb`) — cleaning, missing-value
  audit, and a full walkthrough with commentary.
- **Interactive dashboard** (`app.py`) — Streamlit + Plotly, with filters for
  content type, release year range, and country, plus KPI tiles and 8 charts.
- **Works without a Kaggle account** — if the real dataset isn't present, a
  synthetic sample with the same schema is generated automatically
  (`src/generate_sample_data.py`), so `git clone && run` works immediately.
- **Tested** — `pytest` suite covering data cleaning and every analysis
  function; GitHub Actions CI runs it on every push/PR.

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

```bash
git clone <your-fork-url>
cd netflix-content-analytics
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
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

This project is built around the Kaggle
[**Netflix Movies and TV Shows**](https://www.kaggle.com/datasets/shivamb/netflix-shows)
dataset (`netflix_titles.csv`: title, type, director, cast, country,
date added, release year, rating, duration, genres, description).

See [`data/README.md`](data/README.md) for how to download it. Without it,
every entry point falls back to a generated sample dataset with identical
structure — convenient for development, but not a substitute for the real
data when drawing conclusions.

## Tech stack

Python · pandas · Streamlit · Plotly · Matplotlib/Seaborn · pytest · GitHub Actions

## License

[MIT](LICENSE)
