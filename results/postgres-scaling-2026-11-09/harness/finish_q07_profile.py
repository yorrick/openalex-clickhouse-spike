"""One reserved hash-aggregation arm after the sequential common profiles."""
import json
import sys
import time
import psutil

from pg_helpers import HERE, dump
from tune_large import run


def main():
    path = HERE / 'scaling-decision.json'
    if not path.exists():
        pid = int(sys.argv[1])
        created = psutil.Process(pid).create_time()
        while not path.exists():
            if not psutil.pid_exists(pid) or psutil.Process(pid).create_time() != created:
                raise RuntimeError('Primary tuner ended without decision; inspect its failure')
            time.sleep(5)
    decision = json.loads(path.read_text())
    old = decision['selected_best_observed_cases']['q07']
    if old['median_seconds'] is None or old['median_seconds'] >= 60:
        label = 'q07_hash8gb_single_worker'
        settings = {'work_mem': '8GB', 'max_parallel_workers_per_gather': '0', 'enable_indexonlyscan': 'off'}
        value = run(label, 'q07', HERE / 'sql/q07-postgres.sql', settings)
        if value['state'] == 'complete' and (old['median_seconds'] is None or value['median_seconds'] < old['median_seconds']):
            decision['selected_best_observed_cases']['q07'] = {
                'label': label, 'median_seconds': value['median_seconds'], 'warm_seconds': value['warm_seconds'],
                'settings': settings, 'qa_matched': value['qa']['matched']}
    selected = decision['selected_best_observed_cases']
    failures = [name for name, value in selected.items() if value['median_seconds'] is None or value['median_seconds'] >= 60]
    decision.update(still_failing_cases=failures, all_required_warm_medians_under_60_seconds=not failures,
                    volume_growth_stopped=bool(failures), query_specific_q07_arm_considered=True)
    decision['conclusion'] = (
        'Volume growth stopped at 31.89m Works because the bounded tests did not establish a sub-60-second warm median for these required cases: ' + ', '.join(failures) + '. No 100m or full-corpus PostgreSQL run was attempted.'
        if failures else 'The bounded tuning profiles meet the warm-median criterion at 31.89m Works; a 100m run still requires a source and peak-disk preflight.')
    dump(path, decision)
    dump(HERE / 'scaling-tuning-final.json', {'finished': True, 'decision': decision})
    print(json.dumps(decision, indent=2), flush=True)


if __name__ == '__main__':
    main()
