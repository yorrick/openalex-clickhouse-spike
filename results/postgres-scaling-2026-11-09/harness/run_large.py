"""Continue only after the explicit load process finishes successfully."""
import json
import shutil
import subprocess
import sys
import time

import psutil

from pg_helpers import HERE, connect, dump
from index_and_benchmark import ROOT


def main():
    pid = int(sys.argv[1])
    creator_time = psutil.Process(pid).create_time()
    tables = ('works', 'work_author', 'work_institution', 'work_topic', 'citation_edge')
    while True:
        free = shutil.disk_usage(HERE).free
        if free < 80 * (1 << 30):
            process = psutil.Process(pid)
            if process.create_time() == creator_time:
                process.terminate()
            raise RuntimeError('Host disk below 80GiB guard; stopped dedicated loader')
        states = {}
        for table in tables:
            path = HERE / 'results' / f'load-stage2_large-{table}.json'
            states[table] = json.loads(path.read_text())['state'] if path.exists() else 'not_started'
        if all(state == 'complete' for state in states.values()):
            break
        if any(state == 'failed' for state in states.values()):
            raise RuntimeError(f'Load failed: {states}')
        if not psutil.pid_exists(pid) or psutil.Process(pid).create_time() != creator_time:
            raise RuntimeError(f'Load process ended without complete data: {states}')
        time.sleep(5)
    oracle = json.loads((ROOT / 'results/aws-scaling-2026-11-06/stage2_large.json').read_text())
    expected = {row['table']: row['rows'] for row in oracle['table_bytes']}
    actual = {}
    with connect() as pg:
        for table in expected:
            actual[table] = pg.execute(f'SELECT count(*) FROM {table}').fetchone()[0]
            print('Table QA', table, actual[table], flush=True)
    dump(HERE / 'results/large-table-count-qa.json',
         {'matched': actual == expected, 'actual': actual, 'expected': expected})
    assert actual == expected, (actual, expected)
    print('All nine table counts match; starting indexes and benchmarks', flush=True)
    subprocess.run([sys.executable, str(HERE / 'index_and_benchmark.py'),
                    'stage2_large', 'all', '--bracket-q03'], check=True)


if __name__ == '__main__':
    main()
