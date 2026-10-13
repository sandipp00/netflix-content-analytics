
-- Business question:
-- Which directors have the most titles in the Netflix catalog?

WITH director_counts AS (
    SELECT
        TRIM(director) AS director,
        COUNT(*) AS title_count
    FROM netflix_titles
    WHERE director IS NOT NULL
      AND TRIM(director) <> ''
    GROUP BY TRIM(director)
),

director_rankings AS (
    SELECT
        director,
        title_count,

        ROW_NUMBER() OVER (
            ORDER BY title_count DESC, director ASC
        ) AS row_num,

        RANK() OVER (
            ORDER BY title_count DESC
        ) AS director_rank,

        DENSE_RANK() OVER (
            ORDER BY title_count DESC
        ) AS dense_rank
    FROM director_counts
)

SELECT
    row_num,
    director,
    title_count,
    director_rank,
    dense_rank
FROM director_rankings
ORDER BY row_num
LIMIT 10;
