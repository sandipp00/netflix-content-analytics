
-- Business question: Which countries are most represented?
-- Country values can contain multiple countries.
-- This query counts the full country field as stored.

SELECT
    COALESCE(NULLIF(TRIM(country), ''), 'Unknown') AS country,
    COUNT(*) AS title_count
FROM netflix_titles
GROUP BY COALESCE(NULLIF(TRIM(country), ''), 'Unknown')
ORDER BY title_count DESC
LIMIT 10;
