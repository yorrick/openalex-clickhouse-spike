-- One distinct country set per Work gives exactly one occurrence of each
-- unordered country pair. The successful PostgreSQL Works primary key proves
-- that joining the selected Work cohort does not multiply these occurrences.
WITH international AS (
    SELECT wi.work_id, groupUniqArray(i.country_code) AS countries
    FROM work_institution wi
    INNER JOIN institutions i ON wi.institution_id=i.institution_id
    WHERE i.country_code IS NOT NULL AND i.country_code != ''
    GROUP BY wi.work_id
    HAVING length(countries)>1
)
SELECT w.publication_year,
       pair.1 AS country_a,
       pair.2 AS country_b,
       count() AS collaborative_works
FROM works w
INNER JOIN international c ON w.work_id=c.work_id
ARRAY JOIN arrayFlatten(arrayMap(
    a -> arrayMap(b -> tuple(a,b), arrayFilter(b -> a<b,c.countries)),
    c.countries)) AS pair
GROUP BY w.publication_year,country_a,country_b;
