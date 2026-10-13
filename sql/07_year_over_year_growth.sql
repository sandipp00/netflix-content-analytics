
-- Business question:
-- How did Netflix catalog additions change year over year?

WITH yearly_additions AS (
    SELECT
        CAST(SUBSTR(TRIM(date_added), -4) AS INTEGER) AS added_year,
        COUNT(*) AS titles_added
    FROM netflix_titles
    WHERE date_added IS NOT NULL
      AND TRIM(date_added) <> ''
      AND SUBSTR(TRIM(date_added), -4) GLOB '[0-9][0-9][0-9][0-9]'
    GROUP BY CAST(SUBSTR(TRIM(date_added), -4) AS INTEGER)
),

year_comparison AS (
    SELECT
        added_year,
        titles_added,
        LAG(titles_added) OVER (
            ORDER BY added_year
        ) AS previous_year_titles
    FROM yearly_additions
)

SELECT
    added_year,
    titles_added,
    previous_year_titles,
    titles_added - previous_year_titles AS absolute_change,
    ROUND(
        100.0 * (titles_added - previous_year_titles)
        / NULLIF(previous_year_titles, 0),
        2
    ) AS percentage_change
FROM year_comparison
ORDER BY added_year;

