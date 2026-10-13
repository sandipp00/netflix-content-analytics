
-- Business question: Which listed genre categories are most common?
-- Each title can have multiple genres.

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
)
SELECT
    genre,
    COUNT(DISTINCT show_id) AS title_count
FROM genre_split
WHERE genre <> ''
GROUP BY genre
ORDER BY title_count DESC
LIMIT 10;
