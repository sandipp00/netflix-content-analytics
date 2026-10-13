
-- Business question: Which directors have the most titles?
-- Director values containing multiple names are treated as one field.

SELECT
    TRIM(director) AS director,
    COUNT(*) AS title_count,
    COUNT(DISTINCT type) AS content_types
FROM netflix_titles
WHERE director IS NOT NULL
  AND TRIM(director) <> ''
GROUP BY TRIM(director)
ORDER BY title_count DESC, director
LIMIT 10;
