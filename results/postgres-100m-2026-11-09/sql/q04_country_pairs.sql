-- Keep one country set per Work and retain only internationally affiliated Works.
-- Distinct country pairs occur once per Work, so COUNT(*) preserves the original COUNT(DISTINCT work_id).
WITH international AS MATERIALIZED
(
    SELECT wi.work_id, array_agg(DISTINCT i.country_code) AS countries
    FROM public.work_institution AS wi
    JOIN public.institutions AS i ON wi.institution_id = i.institution_id
    WHERE i.country_code IS NOT NULL AND i.country_code != ''
    GROUP BY wi.work_id
    HAVING count(DISTINCT i.country_code) > 1
)
SELECT w.publication_year,
       a.country_code AS country_a,
       b.country_code AS country_b,
       count(*) AS collaborative_works
FROM international AS c
JOIN public.works AS w ON c.work_id = w.work_id
CROSS JOIN LATERAL unnest(c.countries) AS a(country_code)
CROSS JOIN LATERAL unnest(c.countries) AS b(country_code)
WHERE a.country_code < b.country_code
GROUP BY w.publication_year, a.country_code, b.country_code
ORDER BY w.publication_year, collaborative_works DESC;
