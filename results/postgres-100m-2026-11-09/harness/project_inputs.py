"""Materialize only retained fields from immutable historical S3 versions."""
from pathlib import Path
from urllib.parse import quote, urlencode
import hashlib
import json
import shutil
import time

import duckdb
import psutil

from pg_helpers import HERE, dump
import load_data as original
from load_streaming import projection

ROOT = Path('/Users/yorrickjansen/work/openalex')
OLD_STUDY = Path('/Users/yorrickjansen/work/data/openalex-tier-scaling-20261106')
COLUMNS = {
    'works': ['work_id', 'canonical_id', 'publication_year', 'work_type', 'source_id', 'is_oa', 'is_xpac', 'cited_by_count', 'primary_topic_id'],
    'work_author': ['work_id', 'author_id', 'author_position', 'is_corresponding'],
    'work_institution': ['work_id', 'author_id', 'institution_id'],
    'work_topic': ['work_id', 'topic_id', 'score', 'is_primary'],
    'citation_edge': ['citing_work_id', 'cited_work_id', 'citing_year'],
    'authors': ['author_id', 'canonical_id', 'display_name', 'orcid'],
    'institutions': ['institution_id', 'canonical_id', 'display_name', 'country_code', 'institution_type'],
    'sources': ['source_id', 'canonical_id', 'display_name', 'issn_l', 'source_type'],
    'topics': ['topic_id', 'display_name', 'subfield_id', 'field_id', 'domain_id'],
}


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        while block := f.read(8 << 20):
            h.update(block)
    return h.hexdigest()


def main():
    manifest = json.loads((HERE / 'works-input-manifest.json').read_text())
    known = json.loads((ROOT / 'results/aws-scaling-2026-11-06/input-files.json').read_text())['files']
    known_by_key = {f['source_key']: f for f in known}
    cached = json.loads((OLD_STUDY / 'source-manifest.json').read_text())['files']
    cached_by_url = {f['original_url']: f for f in cached}
    paths = []
    for f in manifest['files']:
        previous = known_by_key.get(f['source_key'])
        if previous:
            f['version_id'] = previous['version_id']
            f['known_full_sha256'] = previous['sha256']
        old = cached_by_url.get(f['url'])
        if old:
            path = Path(old['local_path'])
            assert path.stat().st_size == old['bytes']
            assert path.stat().st_mtime_ns == old['local_mtime_ns']
            f['read_uri'] = str(path)
        else:
            f['read_uri'] = 'https://openalex.s3.amazonaws.com/' + quote(f['source_key'], safe='/=') + '?' + urlencode({'versionId': f['version_id']})
        paths.append(f['read_uri'])
    dump(HERE / 'works-input-manifest.json', manifest)
    d = duckdb.connect()
    d.execute("SET memory_limit='4GB'")
    d.execute('SET threads=8')
    d.execute('SET temp_directory=?', [str(HERE / 'temp')])
    d.execute('LOAD httpfs')
    # Real public range reads were witnessed before constructing this pipeline.
    source = 'read_parquet([' + ','.join(original.lit(path) for path in paths) + '], union_by_name=true)'
    expected_by_uri = {f['read_uri']: f['record_count'] for f in manifest['files']}
    rows = d.execute('SELECT file_name,num_rows FROM parquet_file_metadata(?)', [paths]).fetchall()
    actual = dict(rows)
    assert actual == expected_by_uri, 'Historical object footer rows differ from the pinned manifest'
    dump(HERE / 'results/source-footer-verification.json', {'all480match': True, 'declared_rows': sum(actual.values()), 'files': rows})
    print('All historical source footer counts match:', sum(actual.values()), flush=True)

    for table, columns in COLUMNS.items():
        target = HERE / 'projected' / (table + '.parquet')
        proof = HERE / 'results' / ('project-' + table + '.json')
        if proof.exists() and json.loads(proof.read_text()).get('state') == 'complete':
            assert target.exists(), target
            print(table, 'already projected', flush=True)
            continue
        if shutil.disk_usage(HERE).free < 80 * (1 << 30):
            raise RuntimeError('Host free disk below80GiB guard')
        if table == 'works':
            # The retained base Works projector takes its source from the tier catalog.
            # Rebind that exact source expression; relationship projectors accept an override.
            old_source = original.source('works', 'stage2_large')
            body = original.projection(table, 'stage2_large')
            assert body.count(old_source) == 1
            body = body.replace(old_source, source)
        elif table in ('authors', 'institutions', 'sources', 'topics'):
            body = original.projection(table, 'stage2_large')
        else:
            body = projection(table, 'stage100', source)
        sql = 'COPY (SELECT * FROM (' + body + ') AS normalized(' + ','.join(columns) + ')) TO ' + original.lit(str(target)) + " (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 122880)"
        (HERE / 'sql' / ('project-' + table + '.sql')).write_text(sql + ';\n')
        dump(proof, {'state': 'running', 'table': table, 'at': time.time(), 'sql_sha256': hashlib.sha256(sql.encode()).hexdigest()})
        print('Projecting', table, flush=True)
        start = time.monotonic()
        disk_before = psutil.disk_io_counters()._asdict()
        d.execute(sql)
        elapsed = time.monotonic() - start
        n = d.execute('SELECT count(*) FROM read_parquet(?)', [str(target)]).fetchone()[0]
        result = {'state': 'complete', 'table': table, 'rows': n, 'seconds': elapsed, 'bytes': target.stat().st_size,
                  'sha256': sha(target), 'columns': columns, 'host_free_after': shutil.disk_usage(HERE).free,
                  'host_io_before': disk_before, 'host_io_after': psutil.disk_io_counters()._asdict(),
                  'scope': 'DuckDB projection/staging only, not PostgreSQL query execution. Timings include ZSTD payload creation, exclude SHA sealing.'}
        dump(proof, result)
        print(table, n, round(elapsed, 2), 'seconds', round(result['bytes'] / 1e9, 3), 'GB', flush=True)
    d.close()


if __name__ == '__main__':
    main()
