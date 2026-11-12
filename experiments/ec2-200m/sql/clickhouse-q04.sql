WITH work_country AS (
            SELECT DISTINCT wi.work_id, i.country_code
            FROM work_institution wi JOIN institutions i
            ON wi.institution_id=i.institution_id
            WHERE i.country_code IS NOT NULL AND i.country_code != '')
            SELECT w.publication_year, a.country_code AS country_a,
            b.country_code AS country_b,
            count(DISTINCT a.work_id) AS collaborative_works
            FROM work_country a JOIN work_country b ON a.work_id=b.work_id
            AND a.country_code < b.country_code
            JOIN works w ON a.work_id=w.work_id
            GROUP BY w.publication_year, a.country_code, b.country_code;
