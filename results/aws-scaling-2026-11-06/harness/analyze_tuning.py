"""Interpret the completed experiment; preserve guest policy and apply stricter report rule."""
from pathlib import Path
from statistics import median
import gzip,hashlib,json
from analyze_series import resources
from controls import write
from export_report import DEST,HERE


def main():
 state=json.loads((HERE/'tuning-state.json').read_text());root=HERE/state['ch_run'];lifecycle=json.loads((root/'state.json').read_text())
 if not lifecycle.get('instance_termination_verified') or lifecycle.get('cleanup_errors'):raise RuntimeError('Tuning compute teardown not yet verified')
 d=json.loads((root/'cloud/summary.json').read_text());policy=json.loads((HERE/'tuning-adoption-policy.json').read_text());cc=d['cases'];controls=[cc[k] for k in ('original_a','original_b')]
 controlvalid=all(c['state']=='complete' and (c.get('qa') or {}).get('matched') is True and len(c['runs'])==3 for c in controls)
 ratio=max(median(r['seconds'] for r in c['runs']) for c in controls)/min(median(r['seconds'] for r in c['runs']) for c in controls) if controlvalid else None
 ratio_text=f'{ratio:.4f}' if ratio is not None else 'n/a'
 stable=ratio is not None and ratio<=policy['conservative_report_control_ratio']
 cases={};rows=[]
 for name,c in cc.items():
  complete=c['state']=='complete' and len(c['runs'])==3 and all(r['state']=='complete' for r in c['runs']) and (c.get('qa') or {}).get('matched') is True and c.get('settings_verified') is True
  times=[r['seconds'] for r in c['runs'] if r.get('state')=='complete'];rr=[resources(r) for r in c['runs'] if r.get('state')=='complete']
  outcome='INCONCLUSIVE' if not complete else ('INCONCLUSIVE_COMPARISON' if not stable else ('PASS' if max(times)<60 else 'FAIL_LATENCY'))
  cases[name]={k:v for k,v in c.items() if k not in ('primer','runs')};cases[name].update(warm_seconds=times,median_seconds=median(times) if times else None,max_seconds=max(times) if times else None,resources=rr,report_target_outcome=outcome)
  cpu=median(r['average_cpu_cores'] for r in rr) if rr and all(r['average_cpu_cores'] is not None for r in rr) else None
  memory=max((r['query_peak_bytes'] for r in rr if r.get('query_peak_bytes') is not None),default=None)
  fs=max((r['sampled_scratch_used_peak_bytes'] for r in rr if r.get('sampled_scratch_used_peak_bytes') is not None),default=None)
  writes=median(r['physical_write_bytes_s'] for r in rr) if rr and all(r['physical_write_bytes_s'] is not None for r in rr) else None
  spills=median(r['spill_compressed_bytes'] for r in rr) if rr and all(r['spill_compressed_bytes'] is not None for r in rr) else None
  def fmt(v,scale=1,digits=3):return 'n/a' if v is None else f'{v/scale:.{digits}f}'
  rows.append(f"| {name} | {c['query_memory_gib']} / {c['spill_gib']} GiB, {c['join_algorithm']} | {', '.join(fmt(t) for t in times) or 'none'} | {fmt(cpu,digits=2)} | {fmt(memory,2**30,2)} | {fmt(writes,2**20,2)} | {fmt(spills,1e9)} | {fmt(fs,1e9,2)} | {outcome} |")
 result={'source_identity':d['source_identity'],'normalized_sha256':d['normalized_sha256'],'baseline_q02_sha256':d['expected_q02_sha256'],'guest_experiment_state':d['state'],'guest_control_policy':d['policy'],'report_policy':policy,'controls_median_ratio':ratio,'controls_stable_stricter_rule':stable,'cases':cases,'compute_teardown_verified':True}
 # Compare explicit recorded IDs, not tags or current latest image.
 baseline=json.loads((HERE/'stage2_large-state.json').read_text());bs=json.loads((HERE/baseline['ch_run']/'state.json').read_text());result['same_ubuntu_ami']=lifecycle['ami']==bs['ami']
 env=json.loads((root/'cloud/environment.json').read_text());benv=json.loads((HERE/baseline['ch_run']/'cloud/environment.json').read_text())
 result['same_oci_image']=(env['image_id']==benv['image_id'] and set(env['repo_digests'])==set(benv['repo_digests']))
 if not result['same_oci_image']:raise RuntimeError('Tuning OCI artifact mismatch')
 result['clickhouse_image']={k:env[k] for k in ('image','repo_digests','image_id','image_architecture','resource_limits')}
 result['repository_commit']=lifecycle['source_commit']
 result['deployed_tuning_payload_sha256']=hashlib.sha256((HERE/'deployed-tune-31m.py').read_bytes()).hexdigest()
 if not result['same_ubuntu_ami']:raise RuntimeError('Tuning AMI mismatch')
 write(DEST/'q02-tuning.json',result)
 trace=json.dumps({'cases':cc},sort_keys=True,separators=(',',':')).encode();(DEST/'telemetry-q02-tuning.json.gz').write_bytes(gzip.compress(trace,mtime=0))
 text='''## Focused q02 tuning, 31.89 million Works

This follow-up keeps the **18 CPU / 50 GiB container, same Ubuntu AMI and OCI
image, input identity, normalized-table hash and 400 GiB gp3 disk**. It tests a
24 GiB query-memory / 8 GiB spill-threshold bundle, then forced parallel_hash
with that bundle, and a SQL rewrite under the original 12 / 4 GiB
query settings. The rewrite aggregates numeric topic IDs before joining names. It is output-identical
on the full tested cohort and the three-Work fixture; topic-ID uniqueness was verified.
All 838,464 output rows must hash to the baseline result independently validated
by Athena. Original-SQL controls bracket the variants. A three-Work native
preflight exercised all five cases, settings, telemetry and typed QA before the
large load. No smaller cohort was rerun and no new Athena scans were needed.

| Arm | Query memory / spill threshold, join | Three warm seconds | CPU cores, median | Peak query GiB | Host write MiB/s, median | Compressed external GB, median | Sampled root occupancy GB, max | Target result |
|---|---|---|---:|---:|---:|---:|---:|---|
'''+ '\n'.join(rows)+f'''

The original guest policy allowed a 1.20 control-median ratio. External review
pointed out that this exceeds the roughly 8% baseline-to-target gap. A stricter
**1.08 ratio** was recorded at **{policy['recorded_at_utc']}**, after launch and
before observing any large-cohort variant or closing-control results. This is
a disclosed secondary analysis rule; the original policy, guest outcomes and
measurements are preserved. The measured control ratio is **{ratio_text}**.
A report PASS requires all three observations under 60 seconds, exact QA,
verified effective settings and stable controls under the stricter rule.

Scratch occupancy is sampled root-filesystem use during timed warm windows,
including OS, logs, tables and temporary files. It depends on run order and
deletions, so these arm values cannot be compared as incremental query allocations
or used to infer minimum disk capacity. Load-phase peak occupancy is unrecorded.
Peak per-query allocation and container cache are separate in the evidence.
The memory24 arm changes both query memory and spill thresholds, so it does not
isolate the effect of RAM alone. CPU count and disk bandwidth are held fixed.
The SQL rewrite and forced join choice are experiments, not automatic fallback
behavior in the application. Original benchmark medians remain unchanged. The tuned arms have warm measurements
only; no cache-cleared or concurrent-user tuning trial was performed.

Evidence: [tuning measurements](../../results/aws-scaling-2026-11-06/q02-tuning.json)
and [full tuning trace](../../results/aws-scaling-2026-11-06/telemetry-q02-tuning.json.gz).
'''

 if cases.get('parallel_hash24',{}).get('report_target_outcome')=='PASS' and cases.get('preaggregate12',{}).get('report_target_outcome')=='PASS':
  ph=cases['parallel_hash24'];rw=cases['preaggregate12'];mem=cases['memory24']
  phmem=max(r['query_peak_bytes'] for r in ph['resources'])/2**30;rwmem=max(r['query_peak_bytes'] for r in rw['resources'])/2**30
  phcpu=median(r['average_cpu_cores'] for r in ph['resources']);rwcpu=median(r['average_cpu_cores'] for r in rw['resources'])
  text+=f"""
The query-memory/spill bundle alone has median **{mem['median_seconds']:.3f} s**.
Changing only the join algorithm within that bundle gives **{ph['median_seconds']:.3f} s**,
about **{mem['median_seconds']/ph['median_seconds']:.1f} times faster**, using about
**{phcpu:.2f} cores** and **{phmem:.2f} GiB peak query allocation**. The rewrite gives
**{rw['median_seconds']:.3f} s**, about **{rwcpu:.2f} cores** and **{rwmem:.2f} GiB**,
under the original query limits. Both are measured working choices for this
31.89m tier; neither required a larger CPU allocation or container RAM limit.
The rewrite is the lower-memory option, while the forced hash join is faster.
These per-query experiments do not establish smaller-container minima or full-corpus latency.

The captured settings show max_bytes_in_join=0 and
**default_max_bytes_in_join=1,000,000,000 bytes**, distinct from the 12/24 GiB
query-memory limit. The official 26.3.12.3 [JoinSwitcher source](https://github.com/ClickHouse/ClickHouse/blob/v26.3.12.3-lts/src/Interpreters/JoinSwitcher.cpp)
uses that default when no explicit join limit exists and switches from a hash
join to a merge join when exceeded. This mechanism is consistent with the
observed external-join transition and the unchanged automatic-join latency when
query memory and spill thresholds are raised together. The threshold itself was not varied, so the exact
breakpoint is not an independently validated causal measurement. The forced
hash arm still has some external aggregation; it must not be called spill-free.
"""
 (HERE/'tuning-report.md').write_text(text)
 print(json.dumps({'control_ratio':ratio,'stable':stable,'arms':{k:{'median':v['median_seconds'],'outcome':v['report_target_outcome']} for k,v in cases.items()}}))

if __name__=='__main__':main()
