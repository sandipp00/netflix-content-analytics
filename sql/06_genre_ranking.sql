
-- Business question:
-- Which genres have the highest number of Netflix titles?

WITH RECURSIVE genre_split(show_id, genre, remaining) AS (
    SELECT
        show_id,
        '',
        COALESCE(listed_in, '') || ','
    FROM netflix_titles

    UNION ALL

    SELECT
        show_id,
        TRIM(SUBSTR(remaining, 1, INSTR(remaining, ',') - 1)),
        SUBSTR(remaining, INSTR(remaining, ',') + 1)
    FROM genre_split
    WHERE remaining <> ''
),

genre_counts AS (
    SELECT
        genre,
        COUNT(DISTINCT show_id) AS title_count
    FROM genre_split
    WHERE genre <> ''
    GROUP BY genre
),

ranked_genres AS (
    SELECT
        genre,
        title_count,
        DENSE_RANK() OVER (
            ORDER BY title_count DESC
        ) AS genre_rank
    FROM genre_counts
)

SELECT
    genre_rank,
    genre,
    title_count
FROM ranked_genres
ORDER BY genre_rank, genre
LIMIT 10;
