"""Seal the approved cached input and forecast scans without changing AWS."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import time

import pyarrow.parquet as pq

HERE = Path(__file__).resolve().parent
CACHE = Path('/Users/yorrickjansen/work/openalex/.worktrees/clickhouse-repeatability/.data')
EXPECTED_BYTES = 98_301_763_421
EXPECTED_FILES = 2771


def main():
    approval = json.loads((HERE / 'APPROVAL.json').read_text())
    assert approval['input_bytes_max'] == EXPECTED_BYTES
    selection = json.loads((CACHE / 'selection.json').read_text())
    verification = json.loads((CACHE / 'download-verification-stage2_large.json').read_text())
    objects = {}
    for group, document in verification['tiers'].items():
        if not group.startswith('stage2_large/'):
            continue
        entity = group.split('/', 1)[1]
        for f in document['files']:
            assert f['url'].startswith(f's3://openalex/data/parquet/{entity}/')
            assert f['url'] not in objects
            objects[f['url']] = {**f, 'entity': entity}
    assert len(objects) == EXPECTED_FILES
    assert sum(f['content_length'] for f in objects.values()) == EXPECTED_BYTES
    schema_dir = HERE / 'schemas'
    schema_dir.mkdir(exist_ok=True)
    schema_examples = {}
    for f in objects.values():
        schema_examples.setdefault(f['entity'], f['path'])
    for entity, path in schema_examples.items():
        schema = pq.read_schema(path)
        (schema_dir / (entity + '.arrow')).write_bytes(schema.serialize().to_pybytes())

    started = time.monotonic()

    def inspect(f):
        path = Path(f['path'])
        before = path.stat()
        assert before.st_size == f['content_length'], path
        metadata = pq.read_metadata(path)
        assert metadata.num_rows == f['record_count'], path
        digest = hashlib.sha256()
        with path.open('rb') as source:
            for chunk in iter(lambda: source.read(4 << 20), b''):
                digest.update(chunk)
        after = path.stat()
        assert (after.st_size, after.st_mtime_ns) == (before.st_size, before.st_mtime_ns), path
        columns = {}
        for i in range(metadata.num_row_groups):
            rg = metadata.row_group(i)
            for j in range(rg.num_columns):
                c = rg.column(j)
                root = c.path_in_schema.split('.')[0]
                columns[root] = columns.get(root, 0) + c.total_compressed_size
        return {'entity': f['entity'], 'original_url': f['url'],
                'local_path': str(path), 'local_mtime_ns': after.st_mtime_ns,
                'bytes': after.st_size, 'rows': metadata.num_rows,
                'sha256': digest.hexdigest(),
                'key': 'raw/' + hashlib.sha256(f['url'].encode()).hexdigest() + '.parquet',
                'compressed_columns': columns}

    reports = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for report in pool.map(inspect, objects.values()):
            reports.append(report)
            if len(reports) % 200 == 0:
                print(json.dumps({'hashed_files': len(reports), 'elapsed_seconds': time.monotonic() - started}), flush=True)
    by_url = {f['original_url']: f for f in reports}
    tiers = {}
    forecasts = {}
    support = [f for f in reports if f['entity'] != 'works']
    for tier in ('stage2_small', 'stage2_medium', 'stage2_large'):
        works = [by_url[f['url']] for f in selection['tiers'][tier]['files']]
        chosen = works + support
        totals = {}
        for f in chosen:
            entity = totals.setdefault(f['entity'], {})
            for name, size in f['compressed_columns'].items():
                entity[name] = entity.get(name, 0) + size
        def cols(entity, names):
            return sum(totals[entity].get(name, 0) for name in names)
        work = cols('works', ['id', 'publication_year', 'type', 'open_access', 'is_xpac', 'cited_by_count'])
        wa = cols('works', ['id', 'authorships'])
        edge = cols('works', ['id', 'publication_year', 'referenced_works'])
        topic = cols('works', ['id', 'topics'])
        author = cols('authors', ['id', 'display_name'])
        institution = cols('institutions', ['id', 'country_code'])
        topic_dim = cols('topics', ['id', 'display_name'])
        q = {'q01': work, 'q02': work + topic + topic_dim,
             'q03': wa + work + author, 'q04': 2 * wa + work + 2 * institution,
             'q05': 2 * edge, 'q06': 2 * edge, 'q07': edge}
        # Three shared graph seeds, three repeats each; other queries three repeats.
        forecast = sum(size * (9 if name in ('q05', 'q06') else 3) for name, size in q.items())
        raw_probes = sum(cols(e, names) for e, names in {
            'works': ['id', 'publication_year', 'type', 'authorships', 'primary_topic', 'topics', 'open_access', 'is_xpac', 'cited_by_count', 'referenced_works'],
            'authors': ['id', 'display_name'], 'institutions': ['id', 'country_code'],
            'sources': ['id', 'display_name'], 'topics': ['id', 'display_name']}.items())
        forecasts[tier] = {'queries': q, 'repeated_query_bytes': forecast,
                          'raw_probe_bytes': raw_probes,
                          'conservative_total_bytes': forecast + raw_probes,
                          'note': 'Compressed column chunks times table references, before row-group pruning; planner behavior still enforced by live cutoff.'}
        tiers[tier] = {'work_rows': selection['tiers'][tier]['record_count'],
                       'work_bytes': selection['tiers'][tier]['actual_bytes'],
                       'bytes': sum(f['bytes'] for f in chosen),
                       'keys': [f['key'] for f in chosen]}
    manifest = {'sealed': True, 'source_date': '2026-06-26',
                'bytes': EXPECTED_BYTES, 'files': reports, 'tiers': tiers,
                'selection_sha256': hashlib.sha256((CACHE / 'selection.json').read_bytes()).hexdigest(),
                'elapsed_seconds': time.monotonic() - started}
    (HERE / 'source-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (HERE / 'scan-forecast.json').write_text(json.dumps(forecasts, indent=2) + '\n')
    print(json.dumps({'sealed_files': len(reports), 'bytes': EXPECTED_BYTES,
                      'elapsed_seconds': manifest['elapsed_seconds'],
                      'forecast_all_tiers_bytes': sum(f['conservative_total_bytes'] for f in forecasts.values())}), flush=True)


if __name__ == '__main__':
    main()
