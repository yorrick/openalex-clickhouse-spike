"""Archive the real scaling observations, including partial/timeout cases."""
from pathlib import Path
import datetime
import gzip
import hashlib
import json
import shutil
import statistics

from pg_helpers import HERE, dump
from index_and_benchmark import ROOT
from write_report import FAMILIES, metrics

WT = ROOT / '.claude/worktrees/postgres-scaling'
OUT = WT / 'results/postgres-scaling-2026-11-09'
TIERS = ('stage2_small', 'stage2_medium', 'stage2_large')


def read(path):
    return json.loads(path.read_text())


def seconds(value):
    return f'{value:.6f}' if value < .01 else f'{value:.3f}'


def compressed(name, value):
    with gzip.open(OUT / name, 'wt', encoding='utf-8') as f:
        json.dump(value, f, separators=(',', ':'), default=str)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    folder = HERE / 'results/stage2_large'
    cases, telemetry, storage, loading = {}, {}, {}, {}
    for p in sorted(folder.glob('*.json')):
        if '-canonical' in p.stem:
            continue
        value = read(p)
        if '-telemetry' in p.stem:
            telemetry[p.name] = value
        elif p.name.startswith('q'):
            cases[p.stem] = value
        else:
            storage[p.name] = value
    for p in sorted((HERE / 'results').glob('load-stage2_large-*.json')):
        value = read(p)
        if '-telemetry' in p.stem:
            telemetry[p.name] = value
        else:
            loading[p.name] = value
    compressed('cases.json.gz', cases)
    compressed('telemetry.json.gz', telemetry)
    compressed('storage-and-indexes.json.gz', storage)
    compressed('loading.json.gz', loading)
    for name in ('scaling-plan-20261109.json', 'scaling-progress.md',
                 'scaling-decision.json', 'scaling-final-state.json',
                 'scaling-tuning-plan.json', 'scaling-tuning-commands.jsonl',
                 'scaling-tuning-final.json',
                 'scaling-plan-review-prompt.txt', 'scaling-plan-review.txt',
                 'scaling-plan-review-glm.txt', 'scaling-review-status.json'):
        if (HERE / name).exists():
            shutil.copyfile(HERE / name, OUT / name)
    for name in ('index-maintenance-deadline-adjustment.json', 'large-index-validation.json', 'variant-settings-scope-probe.json', 'q04-country-pairs-estimated-plan.json', 'q07-hash-profile-estimated-plan.json'):
        if (HERE / 'results' / name).exists():
            shutil.copyfile(HERE / 'results' / name, OUT / name)
    (OUT / 'harness').mkdir(exist_ok=True)
    for name in ('archive_scaling.py', 'pg_helpers.py', 'load_data.py',
                 'scale_to.py', 'run_large.py', 'finish_large.py', 'tune_large.py', 'finish_q07_profile.py', 'load_streaming.py', 'write_report.py', 'index_and_benchmark.py', 'variant_bench.py'):
        shutil.copyfile(HERE / name, OUT / 'harness' / name)
    (OUT / 'sql').mkdir(exist_ok=True)
    for p in (HERE / 'sql').glob('*.sql'):
        if p.name.startswith(('load-stage2_large-', 'q')):
            shutil.copyfile(p, OUT / 'sql' / p.name)
    for name, value in cases.items():
        if value.get('sql'):
            (OUT / 'sql' / (name + '.sql')).write_text(value['sql'])
    for name in ('loader-stream-probe.json', 'loader-stream-all-relations-probe.json',
                 'work-author-loader-plan.json', 'scaling-host-during-load.json'):
        if (HERE / name).exists():
            shutil.copyfile(HERE / name, OUT / name)
    if (HERE / 'results/loader-attempt-original').exists():
        shutil.copytree(HERE / 'results/loader-attempt-original', OUT / 'loader-attempt-original', dirs_exist_ok=True)

    summary, qa = {}, []
    old = read(ROOT / 'results/postgres-local-2026-11-08/summary.json')
    cloud = read(ROOT / 'results/aws-scaling-2026-11-06/visual-data.json')['tiers']
    oracle = read(ROOT / 'results/aws-scaling-2026-11-06/stage2_large.json')
    for name, value in cases.items():
        if value.get('qa'):
            assert value['state'] == 'complete' and value['qa']['matched'], name
            qa.append({'case': name, **value['qa']})
    expected_cases = set(oracle['cases'])
    assert expected_cases.issubset(cases), expected_cases - set(cases)
    assert all(cases[n]['state'] in ('complete', 'timeout') for n in expected_cases)
    for q, label in FAMILIES.items():
        members = {n: cases[n] for n in expected_cases if n[:3] == q}
        complete = {n: x for n, x in members.items() if x['state'] == 'complete'}
        worst = max(complete, key=lambda n: complete[n]['median_seconds']) if complete else None
        summary[q] = {'label': label, 'all_cases_complete': len(complete) == len(members),
                      'cases': {n: {'state': x['state'], 'runs': [r['execution_seconds'] for r in x['runs']],
                                    'median_seconds': x.get('median_seconds'), 'qa': x.get('qa')}
                                for n, x in members.items()},
                      'selected_worst_seed': worst,
                      'median_seconds': complete[worst]['median_seconds'] if worst else None,
                      'resources': metrics(complete[worst]) if worst else None}
    dump(OUT / 'summary.json', summary)
    dump(OUT / 'qa.json', {'typed_output_comparisons': qa, 'all_compared_outputs_match': True,
                          'baseline_complete': sum(cases[n]['state'] == 'complete' for n in expected_cases),
                          'baseline_expected': len(expected_cases),
                          'table_counts': read(HERE / 'results/large-table-count-qa.json')})

    lines = ['# PostgreSQL scaling on the local laptop', '',
             'Measured 9 November 2026. The next tier contains **31,885,241 Works** (6.247% of the historical 510,372,821-Work snapshot), with all **119,129,660 Authors**, 127,784 Institutions, 283,287 Sources and 4,516 Topics retained. This is every record in those selected cohorts and the same 42 selected analytical columns as the prior comparison, not all available fields or every OpenAlex entity type.', '',
             '## Decision', '']
    decision_path = HERE / 'scaling-decision.json'
    best_families = {}
    if decision_path.exists():
        decision = read(decision_path)
        lines += [decision['conclusion'], '', decision['limits'], '']
        selected = decision['selected_best_observed_cases']
        for q in FAMILIES:
            members = [(name, value) for name, value in selected.items() if name[:3] == q]
            if all(value['median_seconds'] is not None for _, value in members):
                name, value = max(members, key=lambda item: item[1]['median_seconds'])
                best_families[q] = (name, value)
        lines += ['| Family | Best observed profile | Warm median s | Three warm observations s | Busy cores, median | Sampled container peak GiB | Requested settings |',
                  '|---|---|---:|---|---:|---:|---|']
        for q, (name, value) in best_families.items():
            case = cases[value['label']]
            m = metrics(case)
            label = value['label']
            settings = json.dumps(value['settings'], sort_keys=True)
            warm = ' / '.join(seconds(t) for t in value['warm_seconds'])
            lines.append(f"| {q} | [{label}](../results/postgres-scaling-2026-11-09/sql/{label}.sql) | {seconds(value['median_seconds'])} | {warm} | {m['average_busy_cores_median']:.2f} | {m['container_peak_gib']:.2f} | `{settings}` |")
        lines += ['', 'The best-profile table selects from the declared experiments. Graph rows use the largest seed median; tiny-query CPU averages are coarse. It is not an unchanged-configuration growth series. Empty settings mean the 128-MB baseline; exact SQL is linked for every profile.', '']
    lines += ['## Query performance', '',
              'Seconds below are warm medians. PostgreSQL has one initial observation plus three warm runs; initial observations are not deliberately cold-cache measurements. Statements have a 300-second timeout; a canceled case is incomplete, not a measured 300-second native execution. The two graph families show the largest of three seed medians independently for each engine. The complete per-seed results, plans, exact SQL and typed output hashes are archived. Separate QA-fetch durations include another execution, fetching and canonicalization, not transfer alone.', '',
              '| Query | PG baseline 2.00m s | PG baseline 10.11m s | PG baseline 31.89m s | PG best profile 31.89m s | Local CH 31.89m s | EC2 CH 31.89m s | Athena 31.89m s |',
              '|---|---:|---:|---:|---:|---:|---:|---:|']
    for q, label in FAMILIES.items():
        a = old['stage2_small']['families'][q]['median_seconds']
        b = old['stage2_medium']['families'][q]['median_seconds']
        x = summary[q]
        c = seconds(x['median_seconds']) if x['all_cases_complete'] else 'Timeout / partial'
        tuned = seconds(best_families[q][1]['median_seconds']) if q in best_families else 'Not completed'
        v = cloud[2]['queries'][q]
        lines.append(f"| {q}: {label} | {seconds(a)} | {seconds(b)} | {c} | {tuned} | {v['local_s']:.3f} | {v['ec2_s']:.3f} | {v['athena_s']:.3f} |")
    lines += ['', 'These compare observed setups: historical local ClickHouse had different image/settings and five warm repeats; EC2 ClickHouse had 18 CPUs / 50 GiB versus local PostgreSQL at 16 CPUs / 32 GiB. Athena service time includes S3 result materialization. This is not an isolated hardware-matched engine comparison.', '',
              '| Case | First observation s | Three warm observations s | Median s | Exact output QA |',
              '|---|---:|---|---:|---|']
    for name, x in cases.items():
        if not (x.get('name') or x.get('variant')):
            continue
        runs = x['runs']
        first = seconds(runs[0]['execution_seconds']) if runs else 'None completed'
        warm = ' / '.join(seconds(r['execution_seconds']) for r in runs if r['kind'] != 'primer')
        median = seconds(x['median_seconds']) if x.get('state') == 'complete' else x['state']
        sql_link = f'[{name}](../results/postgres-scaling-2026-11-09/sql/{name}.sql)'
        lines.append(f"| {sql_link} | {first} | {warm or 'None completed'} | {median} | {'MATCH' if x.get('qa', {}).get('matched') else 'Not completed'} |")
    bracket = [cases.get(n) for n in ('q03', 'q03_preaggregate_authors', 'q03_control_b')]
    if all(x and x.get('state') == 'complete' for x in bracket):
        a, variant, b = bracket
        ratio = max(a['median_seconds'], b['median_seconds']) / min(a['median_seconds'], b['median_seconds'])
        lines += ['', f"q03 original A / rewrite / original B warm medians: **{a['median_seconds']:.3f} / {variant['median_seconds']:.3f} / {b['median_seconds']:.3f} s**. The symmetric original-control ratio is **{ratio:.4f}**, {'within' if ratio <= 1.20 else 'outside'} the planned 1.20 stability bound. This check addresses order/cache drift, not all confounding."]
    lines += ['', '## Bounded query tuning', '',
              'Additional profiles were declared before their tests: first, work_mem = 512 MB on failing families (using the existing q03 pre-aggregation rewrite); then at most one query-specific arm for each still-failing q03/q04/q07 family. The reserved arms change q03 join planning, generate q04 country pairs from per-Work sets, or encourage a q07 hash aggregate with 8-GB work_mem and no parallel workers to bound its memory. The container stays at 16 CPUs / 32 GiB and shared_buffers stays at 8 GiB. work_mem applies per operation and potentially per worker, not as a whole-query cap. Settings are scoped to each trial connection; separate connections keep the 128-MB baseline. These exploratory trials are not all bracketed controls, so their observed differences are not isolated causal estimates.', '',
              '| Variant or control | Requested settings | Median s | Median busy CPU cores | Sampled peak container GiB | PG shared reads GB | PG temporary writes GB |',
              '|---|---|---:|---:|---:|---:|---:|']
    for name, value in cases.items():
        if not value.get('variant'):
            continue
        settings = json.dumps(value.get('requested_settings', {}), sort_keys=True) or '{}'
        if value['state'] != 'complete':
            lines.append(f"| {name} | `{settings}` | {value['state']} | Not completed | Not completed | Not completed | Not completed |")
            continue
        m = metrics(value)
        lines.append(f"| {name} | `{settings}` | {seconds(value['median_seconds'])} | {m['average_busy_cores_median']:.2f} | {m['container_peak_gib']:.2f} | {m['shared_read_gb_median']:.3f} | {m['temp_written_gb_median']:.3f} |")
    lines += ['', '## Resources and storage', '',
              'The existing container remains capped at **16 CPUs / 32 GiB**, with 8 GiB shared buffers, 128 MiB work memory and up to eight parallel workers per Gather. The laptop has 18 cores / 128 GiB; Docker exposes 16 cores / approximately 47 GiB. PGDATA uses the existing host bind mount through VirtioFS. Unrelated containers and Docker settings were left unchanged.', '',
              '| Family, baseline | Median busy CPU cores | Sampled peak container GiB | PG shared-buffer reads GB, median | PG temporary writes GB, median | Maximum parallel workers launched |',
              '|---|---:|---:|---:|---:|---:|']
    for q, x in summary.items():
        m = x['resources']
        if m:
            coarse = ' (coarse)' if m['short_query_cpu_caution'] else ''
            lines.append(f"| {q} | {m['average_busy_cores_median']:.2f}{coarse} | {m['container_peak_gib']:.2f} | {m['shared_read_gb_median']:.3f} | {m['temp_written_gb_median']:.3f} | {m['max_workers_launched_in_any_gather']} |")
    before = storage.get('storage-before-queries.json')
    canceled = [(name, value) for name, value in cases.items()
                if value.get('state') == 'timeout' and value.get('resources')]
    if canceled:
        lines += ['', 'Canceled initial observations below are not warm medians. Their cgroup summaries remain available even though EXPLAIN did not return an actual plan; no physical-read or temporary-byte count is invented for them.', '',
                  '| Canceled case | Monitored seconds | Average busy cores | CPU seconds | Sampled peak container GiB |',
                  '|---|---:|---:|---:|---:|']
        for name, value in canceled:
            r = value['resources']
            lines.append(f"| {name} | {r['window_seconds']:.2f} | {r['average_busy_cores_in_monitor_window']:.2f} | {r['cpu_seconds']:.2f} | {r['memory_current_peak_bytes']/(1<<30):.2f} |")
    if before:
        lines += ['', f"Database after indexing: **{before['database_bytes']/1e9:.3f} GB**, including **{sum(t['indexes_bytes'] for t in before['tables'])/1e9:.3f} GB of indexes**. This excludes WAL and temporary workspace."]
    lines += ['', f"Five Works-derived tables took **{sum(x['seconds'] for x in loading.values() if x.get('state') == 'complete'):.2f} s** of bulk insert time in total; dimensions were retained. Index creation took **{sum(x.get('seconds', 0) for n, x in storage.items() if 'sql' in x):.2f} s**, followed by VACUUM/ANALYZE. Load traces include post-copy validation; the reported insert seconds exclude it.", '',
              'The initial authorship import was interrupted after the correlated UNNEST plan materialized and hashed wide nested lists; 71 GiB of scratch was observed during that load. The explicit revised loader uses SELECT-list UNNEST. Before replacement, both projections were executed on two real source files and compared with symmetric EXCEPT ALL: all four relationship multisets matched exactly. Final full table-count and query-output comparisons validate the complete loaded cohort. Completed load seconds above exclude the interrupted attempt, whose elapsed time and last resource sample are archived. A 10-second standalone count probe during rollback cleanup timed out; the loader subsequently performed its own empty-target check before inserting. No timing from that failed probe is used.', '',
              'The first citation index took 294.234 s, close to the query deadline. The unfinished second citation index was deliberately canceled and rebuilt with a separate 30-minute maintenance deadline; query statements remained capped at 300 s. The completed index-time sum excludes that interrupted partial build, whose elapsed time is archived. All 14 indexes were checked valid and ready before query execution.', '',
              'CPU is container usage over each instrumented client window, including background PostgreSQL and monitoring overhead. Memory is container occupancy, not query allocation or minimum RAM; file cache includes shared memory, so those categories must not be added. Host filesystem cache can help outside the container accounting, so the 32-GiB cap is not a total RAM budget for the whole stack. Shared-buffer reads can hit OS/host cache and are not physical disk bytes. Cgroup block I/O can miss VirtioFS traffic, while the separate host I/O counters include unrelated activity. No minimum SSD bandwidth is inferred.', '',
              '## Evidence and limitations', '',
              '- [Original 2m/10m PostgreSQL report](postgres-local-benchmark.md), [ClickHouse/Athena report](superpowers/2026-08-05-single-user-resource-benchmark-results.md), and [field coverage](openalex-field-inventory.md).',
              '- [Archived scaling evidence](../results/postgres-scaling-2026-11-09/): exact SQL, plans, repeated timings, cgroup traces, loading/indexing/storage and full typed-result QA. Raw source files, passwords and PGDATA are excluded.',
              '- No additional AWS or Athena runs were made: the exact existing 31.9m cohort and its recorded Athena/ClickHouse outputs were reused. Additional billed cloud cost is $0; local electricity and machine opportunity cost were not measured.',
              '- Growth ratios from three nested, non-random cohorts do not establish a scaling law or full-corpus SLA. Complete Authors are fixed at every tier, so latency cannot be scaled uniformly by Work count.',
              '- The relationship loader differs from the earlier tiers. Its revised projection is logically equivalent, but load-time growth is not an unchanged-loader comparison, and physical heap row order can differ. Query schema, indexes, PostgreSQL settings and resource caps remain unchanged for the baseline.',
              '- No Claude Code validation was invoked, as requested. DeepSeek V4.1 Flash and GLM 5.3 Flash review attempts through the personal OpenRouter key both failed with a total key limit error; neither completed a review. The exact commands and failure evidence are archived in scaling-review-status.json and the review logs.', '']
    (WT / 'docs/postgres-scaling-benchmark.md').write_text('\n'.join(lines))
    (OUT / 'README.md').write_text('# PostgreSQL scaling evidence\n\nSee [the report](../../docs/postgres-scaling-benchmark.md). Compressed archives retain complete observations and traces, including timeout cases. Prior 2m/10m evidence remains in ../postgres-local-2026-11-08/. No credentials, source Parquet or PGDATA are included.\n')
    print('Archived', len(qa), 'full output checks;', len(cases), 'case records')


if __name__ == '__main__':
    main()
