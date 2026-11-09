"""Run the two prospective tuning profiles sequentially, never concurrent queries."""
import json
import shutil
import subprocess
import sys
import time

import psutil

from pg_helpers import HERE, dump
from index_and_benchmark import ROOT

TIER = 'stage2_large'
FOLDER = HERE / 'results' / TIER


def read(path):
    return json.loads(path.read_text())


def run(label, query, sql_path, settings):
    out = FOLDER / (label + '.json')
    if out.exists() and read(out).get('state') in ('complete', 'timeout'):
        return read(out)
    if shutil.disk_usage(HERE).free < 80 * (1 << 30):
        raise RuntimeError('Host disk below 80GiB guard')
    command = [sys.executable, str(HERE / 'variant_bench.py'), TIER,
               label, query, str(sql_path), json.dumps(settings)]
    with (HERE / 'scaling-tuning-commands.jsonl').open('a') as f:
        f.write(json.dumps({'time': time.time(), 'argv': command}) + '\n')
    print('Trial', label, settings, flush=True)
    subprocess.run(command, check=True)
    value = read(out)
    assert value['state'] in ('complete', 'timeout'), value['state']
    if value['state'] == 'complete':
        assert value['qa']['matched'], label
    return value


def nodes(node):
    yield node
    for child in node.get('Plans', []):
        yield from nodes(child)


def main():
    done = FOLDER / 'storage-after-queries.json'
    pid = int(sys.argv[1])
    if not done.exists():
        process = psutil.Process(pid)
        created = process.create_time()
        while not done.exists():
            if not psutil.pid_exists(pid) or psutil.Process(pid).create_time() != created:
                raise RuntimeError('Baseline process ended without final storage snapshot')
            time.sleep(5)
    oracle = read(ROOT / 'results/aws-scaling-2026-11-06/stage2_large.json')
    selected = {}
    candidates = {}
    for name in oracle['cases']:
        baseline = read(FOLDER / (name + '.json'))
        assert baseline['state'] in ('complete', 'timeout'), (name, baseline['state'])
        if baseline['state'] == 'complete':
            assert baseline['qa']['matched'], name
        candidates[name] = [(name, baseline)]
    rewrite_path = HERE / 'sql/q03_preaggregate_authors.sql'
    default_rewrite = run('q03_preaggregate_authors', 'q03', rewrite_path, {})
    candidates['q03'].append(('q03_preaggregate_authors', default_rewrite))

    # Profile 1: one common work_mem increase, only for families that miss 60 s.
    failing_families = set()
    for name, values in candidates.items():
        times = [value['median_seconds'] for _, value in values if value['state'] == 'complete']
        if not times or min(times) >= 60:
            failing_families.add(name[:3])
    for name in oracle['cases']:
        if name[:3] not in failing_families:
            continue
        sql_path = rewrite_path if name == 'q03' else HERE / 'sql' / (name + '-postgres.sql')
        label = ('q03_preaggregate_authors' if name == 'q03' else name) + '_wm512'
        value = run(label, name, sql_path, {'work_mem': '512MB'})
        candidates[name].append((label, value))

    # Profile 2 is reserved for the observed serial Works index-lookup plan.
    q03_values = candidates['q03']
    completed = [(label, value) for label, value in q03_values if value['state'] == 'complete']
    best = min(completed, key=lambda item: item[1]['median_seconds']) if completed else None
    if best and best[1]['median_seconds'] >= 60:
        observed = any(node.get('Relation Name') == 'works' and node.get('Actual Loops', 0) > 1_000_000
                       and node['Node Type'] in ('Index Scan', 'Index Only Scan')
                       for _, candidate in completed for observation in candidate['runs']
                       for node in nodes(observation['plan']['Plan']))
        if observed:
            label = 'q03_preaggregate_authors_wm512_no_nestloop'
            value = run(label, 'q03', rewrite_path, {'work_mem': '512MB', 'enable_nestloop': 'off'})
            candidates['q03'].append((label, value))
        else:
            print('Reserved profile 2 not applicable: no million-loop Works index lookup observed', flush=True)

    # Second query-shape arm: country-set pairs instead of materialized self-join.
    q04_complete = [value for _, value in candidates['q04'] if value['state'] == 'complete']
    if not q04_complete or min(value['median_seconds'] for value in q04_complete) >= 60:
        label = 'q04_country_pairs_wm512'
        value = run(label, 'q04', HERE / 'sql/q04_country_pairs.sql', {'work_mem': '512MB'})
        candidates['q04'].append((label, value))

    for name, values in candidates.items():
        completed = [(label, value) for label, value in values if value['state'] == 'complete']
        if completed:
            label, value = min(completed, key=lambda item: item[1]['median_seconds'])
            selected[name] = {'label': label, 'median_seconds': value['median_seconds'],
                              'warm_seconds': value['warm_seconds'],
                              'settings': value.get('requested_settings', {}), 'qa_matched': value['qa']['matched']}
        else:
            selected[name] = {'label': None, 'median_seconds': None, 'qa_matched': False}
    passes = all(value['median_seconds'] is not None and value['median_seconds'] < 60 for value in selected.values())
    failing = [name for name, value in selected.items() if value['median_seconds'] is None or value['median_seconds'] >= 60]
    decision = {'date': '2026-11-09', 'tier': TIER, 'selected_best_observed_cases': selected,
                'all_required_warm_medians_under_60_seconds': passes, 'still_failing_cases': failing,
                'volume_growth_stopped': not passes,
                'conclusion': ('The bounded tuning profiles meet the warm-median criterion at 31.89m Works; a 100m run still requires a source and peak-disk preflight.' if passes else
                               'Volume growth stopped at 31.89m Works because the bounded tests did not establish a sub-60-second warm median for these required cases: ' + ', '.join(failing) + '. No 100m or full-corpus PostgreSQL run was attempted.'),
                'limits': 'This tests one 16-CPU / 32-GiB Docker configuration and selected analytical fields on a shared laptop with VirtioFS. It does not rule out PostgreSQL on a larger native Linux server, establish a scaling law or a full-corpus SLA. Best observed settings across exploratory profiles are reported explicitly; no isolated causal speedup is claimed without controls.'}
    dump(HERE / 'scaling-decision.json', decision)
    print(json.dumps(decision, indent=2), flush=True)


if __name__ == '__main__':
    main()
