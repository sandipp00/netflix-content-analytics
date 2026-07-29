"""Netflix Content Analytics — Streamlit dashboard.

Run with: streamlit run app.py
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src import analysis
from src.data_loader import load_clean

# Categorical palette slots (validated for CVD-safe adjacent contrast, see
# dataviz skill references/palette.md). Fixed order, assigned by entity.
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = (
    "#2a78d6", "#eb6834", "#1baf7a", "#eda100",
    "#e87ba4", "#008300", "#4a3aa7", "#e34948",
)
TYPE_COLORS = {"Movie": BLUE, "TV Show": ORANGE}
SEQUENTIAL_BLUE = ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]

st.set_page_config(page_title="Netflix Content Analytics", page_icon="🎬", layout="wide")


@st.cache_data
def get_data() -> pd.DataFrame:
    return load_clean()


def apply_chart_theme(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        plot_bgcolor="#fcfcfb",
        paper_bgcolor="#fcfcfb",
        font_color="#0b0b0b",
        legend_title_text="",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    fig.update_xaxes(gridcolor="#e1e0d9", linecolor="#c3c2b7")
    fig.update_yaxes(gridcolor="#e1e0d9", linecolor="#c3c2b7")
    return fig


df = get_data()

st.title("🎬 Netflix Content Analytics")
st.caption(
    "Exploring the Netflix content catalog — release trends, genres, "
    "countries, and ratings. Dataset: Kaggle *Netflix Movies and TV Shows* "
    "(or a generated sample if the CSV isn't present)."
)

# ---- Sidebar filters ----
st.sidebar.header("Filters")
type_options = sorted(df["type"].unique())
selected_types = st.sidebar.multiselect("Content type", type_options, default=type_options)

year_min, year_max = int(df["release_year"].min()), int(df["release_year"].max())
selected_years = st.sidebar.slider("Release year", year_min, year_max, (year_min, year_max))

country_options = sorted(analysis.top_countries(df, n=30)["country"])
selected_countries = st.sidebar.multiselect("Country (top 30 by volume)", country_options)

filtered = df[
    df["type"].isin(selected_types)
    & df["release_year"].between(*selected_years)
]
if selected_countries:
    filtered = filtered[
        filtered["country_list"].apply(lambda cs: any(c in selected_countries for c in cs))
    ]

if filtered.empty:
    st.warning("No titles match the current filters.")
    st.stop()

# ---- KPI row ----
kpis = analysis.kpi_summary(filtered)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total titles", f"{kpis['total_titles']:,}")
c2.metric("Movies", f"{kpis['movies']:,}")
c3.metric("TV shows", f"{kpis['tv_shows']:,}")
c4.metric("Countries", kpis["countries"])
c5.metric("Genres", kpis["genres"])

st.divider()

# ---- Row 1: content type split + titles added per year ----
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Movies vs. TV Shows")
    type_counts = analysis.content_type_counts(filtered)
    fig = px.pie(
        type_counts, names="type", values="count", hole=0.55,
        color="type", color_discrete_map=TYPE_COLORS,
    )
    fig.update_traces(textinfo="percent+label")
    st.plotly_chart(apply_chart_theme(fig), use_container_width=True)

with col2:
    st.subheader("Titles Added to Netflix per Year")
    added = analysis.titles_added_per_year(filtered)
    fig = px.bar(
        added, x="year_added", y="count", color="type", barmode="stack",
        color_discrete_map=TYPE_COLORS,
        labels={"year_added": "Year added", "count": "Titles"},
    )
    st.plotly_chart(apply_chart_theme(fig), use_container_width=True)

# ---- Row 2: release year trend + ratings ----
col3, col4 = st.columns(2)

with col3:
    st.subheader("Release Year Trend")
    trend = analysis.release_year_trend(filtered)
    fig = px.line(
        trend, x="release_year", y="count", color="type",
        color_discrete_map=TYPE_COLORS, markers=True,
        labels={"release_year": "Release year", "count": "Titles"},
    )
    st.plotly_chart(apply_chart_theme(fig), use_container_width=True)

with col4:
    st.subheader("Content Ratings")
    ratings = analysis.rating_distribution(filtered).sort_values("count", ascending=True)
    fig = px.bar(
        ratings, x="count", y="rating", orientation="h",
        color_discrete_sequence=[BLUE],
        labels={"count": "Titles", "rating": "Rating"},
    )
    st.plotly_chart(apply_chart_theme(fig), use_container_width=True)

# ---- Row 3: top countries + top genres ----
col5, col6 = st.columns(2)

with col5:
    st.subheader("Top 10 Countries by Title Count")
    countries = analysis.top_countries(filtered, n=10).sort_values("count", ascending=True)
    fig = px.bar(
        countries, x="count", y="country", orientation="h",
        color_discrete_sequence=[AQUA],
        labels={"count": "Titles", "country": "Country"},
    )
    st.plotly_chart(apply_chart_theme(fig), use_container_width=True)

with col6:
    st.subheader("Top 10 Genres")
    genres = analysis.top_genres(filtered, n=10).sort_values("count", ascending=True)
    fig = px.bar(
        genres, x="count", y="genre", orientation="h",
        color_discrete_sequence=[VIOLET],
        labels={"count": "Titles", "genre": "Genre"},
    )
    st.plotly_chart(apply_chart_theme(fig), use_container_width=True)

# ---- Row 4: duration + top directors ----
col7, col8 = st.columns(2)

with col7:
    st.subheader("Duration Summary")
    st.dataframe(analysis.duration_summary(filtered).round(1), use_container_width=True, hide_index=True)

with col8:
    st.subheader("Top 10 Directors by Title Count")
    directors = analysis.top_directors(filtered, n=10).sort_values("count", ascending=True)
    fig = px.bar(
        directors, x="count", y="director", orientation="h",
        color_discrete_sequence=[MAGENTA],
        labels={"count": "Titles", "director": "Director"},
    )
    st.plotly_chart(apply_chart_theme(fig), use_container_width=True)

with st.expander("View filtered data table"):
    st.dataframe(
        filtered[
            ["title", "type", "director", "country", "release_year",
             "rating", "duration", "listed_in"]
        ],
        use_container_width=True,
        hide_index=True,
    )
