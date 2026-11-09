"""Explicit loader revision: SELECT-list UNNEST, no correlated wide-list join."""
import sys
import load_data as original

BASE_PROJECTION = original.projection


def projection(table, tier, source_override=None):
    if table not in ('work_author', 'work_institution', 'work_topic', 'citation_edge'):
        return BASE_PROJECTION(table, tier)
    source = source_override or original.source('works', tier)
    work = original.NUM('id')
    valid = f'{work} IS NOT NULL'
    if table == 'work_author':
        author = original.NUM('a.author.id')
        return (f'SELECT {work},{author},a.author_position,coalesce(a.is_corresponding,false) '
                f'FROM (SELECT id,unnest(authorships) AS a FROM {source}) '
                f'WHERE {valid} AND {author} IS NOT NULL')
    if table == 'work_institution':
        author = original.NUM('author_raw')
        institution = original.NUM('institution.id')
        return (f'SELECT DISTINCT {work},{author},{institution} '
                f'FROM (SELECT id,a.author.id AS author_raw,unnest(a.institutions) AS institution '
                f'FROM (SELECT id,unnest(authorships) AS a FROM {source})) '
                f'WHERE {valid} AND {author} IS NOT NULL AND {institution} IS NOT NULL')
    if table == 'work_topic':
        topic = original.NUM('topic.id')
        primary = original.NUM('primary_raw')
        return (f'SELECT {work},{topic},CAST(topic.score AS FLOAT),coalesce({topic}={primary},false) '
                f'FROM (SELECT id,primary_topic.id AS primary_raw,unnest(topics) AS topic FROM {source}) '
                f'WHERE {valid} AND {topic} IS NOT NULL AND topic.score IS NOT NULL')
    cited = original.NUM('ref')
    year = ('CASE WHEN publication_year BETWEEN 0 AND 65535 '
            'THEN CAST(publication_year AS INTEGER) ELSE NULL END')
    return (f'SELECT {work},{cited},min({year}) '
            f'FROM (SELECT id,publication_year,unnest(referenced_works) AS ref FROM {source}) '
            f'WHERE {valid} AND {cited} IS NOT NULL GROUP BY 1,2')


if __name__ == '__main__':
    original.projection = projection
    original.main()
