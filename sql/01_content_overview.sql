
-- Business question:
-- What is the distribution of movies and TV shows?

SELECT
    type AS content_type,
    COUNT(*) AS total_titles,
    ROUND(
        100.0 * COUNT(*) / (SELECT COUNT(*) FROM netflix_titles),
        2
    ) AS percentage
FROM netflix_titles
GROUP BY type
ORDER BY total_titles DESC;
