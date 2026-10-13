
-- Business question: How has the content release mix changed over time?

SELECT
    release_year,
    type AS content_type,
    COUNT(*) AS title_count
FROM netflix_titles
WHERE release_year IS NOT NULL
GROUP BY release_year, type
ORDER BY release_year, content_type;
