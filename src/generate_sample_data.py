"""Generate a synthetic Netflix titles dataset with the same schema as the
Kaggle "Netflix Movies and TV Shows" dataset (netflix_titles.csv), so the repo
runs end-to-end without requiring a Kaggle download.
"""

import random
from datetime import date

import pandas as pd

TITLES_MOVIE = [
    "Silent Horizon", "The Last Signal", "Beneath the Ash", "Midnight Ledger",
    "Glass Kingdom", "Paper Moonlight", "Echoes of Tomorrow", "Crimson Harbor",
    "The Ivory Line", "Static Bloom", "Winter's Debt", "Neon Requiem",
    "The Salt Road", "Hollow Verdict", "Lanterns for the Lost", "Iron Orchard",
    "The Quiet Defector", "Ashfall", "Velvet Circuit", "Borrowed Light",
]
TITLES_SHOW = [
    "Fractured City", "The Cartel Files", "Nightshift Dispatch", "House of Ledgers",
    "Coastal Static", "The Recruit Diaries", "Whistleblower", "The Understudy",
    "Signal Lost", "Cold Harbor", "The Last Precinct", "Ember & Ash",
    "The Boardroom", "Undertow", "The Archivists", "Blackout District",
    "The Substitute", "Paper Trail", "Ghost Protocol Diaries", "The Firm Below",
]
DIRECTORS = [
    "Maria Alden", "Kenji Watanabe", "Priya Nair", "Diego Ferreira",
    "Amara Okafor", "Lukas Berg", "Chiara Rossi", "Hassan El-Amin",
    "Sofia Reyes", "Tomas Novak", None, None,
]
ACTORS = [
    "Elena Cross", "Marcus Webb", "Ines Duarte", "Ravi Malhotra", "Noor Haddad",
    "Liam O'Connor", "Yuki Tanaka", "Grace Mwangi", "Pablo Ibarra", "Anya Kowalski",
    "Ben Okonkwo", "Sana Iqbal", "Theo Marchetti", "Freya Lindqvist", "Jonas Kim",
]
COUNTRIES = [
    "United States", "India", "United Kingdom", "Canada", "France", "Japan",
    "South Korea", "Germany", "Spain", "Brazil", "Nigeria", "Mexico",
    "Australia", "Egypt", "Italy",
]
GENRES = [
    "Dramas", "Comedies", "Documentaries", "Action & Adventure", "Thrillers",
    "International TV Shows", "Crime TV Shows", "Romantic Movies",
    "Children & Family Movies", "Sci-Fi & Fantasy", "Horror Movies",
    "Stand-Up Comedy", "Reality TV", "Anime Series", "Sports Movies",
]
RATINGS_MOVIE = ["G", "PG", "PG-13", "R", "NC-17", "TV-MA", "TV-14"]
RATINGS_SHOW = ["TV-Y", "TV-Y7", "TV-G", "TV-PG", "TV-14", "TV-MA"]


def _random_duration(content_type, rng):
    if content_type == "Movie":
        return f"{rng.randint(70, 180)} min"

    seasons = rng.randint(1, 9)
    return f"{seasons} Season{'s' if seasons > 1 else ''}"


def _random_date_added(release_year, rng):
    year = rng.randint(release_year, 2021)
    month = rng.randint(1, 12)
    day = rng.randint(1, 28)
    d = date(year, month, day)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def generate_sample_dataframe(n_rows: int = 600, seed: int = 42) -> pd.DataFrame:
    """Return a synthetic dataframe matching the netflix_titles.csv schema."""
    rng = random.Random(seed)
    rows = []
    for i in range(n_rows):
        content_type = rng.choice(["Movie", "TV Show"])
        pool = TITLES_MOVIE if content_type == "Movie" else TITLES_SHOW
        title = f"{rng.choice(pool)} {rng.choice(['', 'II', 'III', ': Origins', ': Rebirth', ''])}".strip()
        release_year = rng.randint(1998, 2021)
        n_countries = rng.randint(1, 3)
        n_genres = rng.randint(1, 3)
        n_cast = rng.randint(2, 6)
        rows.append(
            {
                "show_id": f"s{i + 1}",
                "type": content_type,
                "title": title,
                "director": rng.choice(DIRECTORS),
                "cast": ", ".join(rng.sample(ACTORS, n_cast)),
                "country": ", ".join(rng.sample(COUNTRIES, n_countries)),
                "date_added": _random_date_added(release_year, rng),
                "release_year": release_year,
                "rating": rng.choice(RATINGS_MOVIE if content_type == "Movie" else RATINGS_SHOW),
                "duration": _random_duration(content_type, rng),
                "listed_in": ", ".join(rng.sample(GENRES, n_genres)),
                "description": "A synthetic placeholder description generated for demo purposes.",
            }
        )
    return pd.DataFrame(rows)


def write_sample_csv(path: str = "data/netflix_titles.csv", n_rows: int = 600, seed: int = 42) -> None:
    df = generate_sample_dataframe(n_rows=n_rows, seed=seed)
    df.to_csv(path, index=False)


if __name__ == "__main__":
    write_sample_csv()
    print("Sample dataset written to data/netflix_titles.csv")
