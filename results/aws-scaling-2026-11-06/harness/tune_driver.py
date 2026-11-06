"""One bounded q02 tuning experiment, same dataset/image/18CPU/50GiB, no Athena scans."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
from cloud_job import Job
from controls import write
from scope import validate_scope,manifest_identity
from source_copy import Sources
from tier_sql import canonical_rows,clickhouse_result_columns

HERE=Path(__file__).resolve().parent

def main():
    path=HERE/'tuning-state.json'
    if path.exists():raise RuntimeError('Tuning already recorded; inspect and resume explicitly')
    source=Sources();source.fresh()
    baseline=json.loads((HERE/'stage2_large-state.json').read_text())
    baseline_dir=HERE/baseline['ch_run']
    state=json.loads((baseline_dir/'state.json').read_text())
    if state.get('instance_termination_verified') is not True or state.get('cleanup_errors'):
        raise RuntimeError('Baseline compute cleanup must finish before tuning')
    summary=json.loads((baseline_dir/'cloud/summary.json').read_text())
    if summary.get('primary_complete') is not True or summary.get('merges_quiescent') is not True or 'q02' not in summary['qa']:
        raise RuntimeError('Baseline primary q02 oracle incomplete')
    remote=json.loads((HERE/'remote-manifest.json').read_text());validate_scope(remote)
    if manifest_identity(remote)!=json.loads((HERE/'approved-source-identity.json').read_text())['manifest_identity']:
        raise RuntimeError('Source identity changed')
    raw=json.loads((HERE/'retained-volume.json').read_text())
    if raw['state']!='complete':raise RuntimeError('Retained input incomplete')
    rows=json.loads((baseline_dir/'cloud/q02-rows.json').read_text())
    oracle=hashlib.sha256('\n'.join(canonical_rows('q02',clickhouse_result_columns('q02',rows))).encode()).hexdigest()
    if oracle!='49bfb17b7f7f884cd6e0295d03329621b22364dd02314dc1b6605753fe488d9e' or len(rows)!=838464:raise RuntimeError('Baseline oracle changed')
    build=json.loads((baseline_dir/'cloud/build.json').read_text())
    env=json.loads((baseline_dir/'cloud/environment.json').read_text())
    config=remote|{'raw_volume_id':raw['volume_id'],'series_id':raw['series_id'],'tier':'stage2_large','seeds':summary['seeds'],
        'optimized_sql':(HERE/'q02_preaggregate_topic_names.sql').read_text(),'expected_ami':state['ami'],
        'expected_normalized_sha256':build['correctness']['normalized_sha256'],
        'expected_q02_sha256':oracle,'expected_q02_rows':len(rows),'image_digest':env['repo_digests'][0]}
    validate_scope(config)
    if manifest_identity(config)!=manifest_identity(remote):raise RuntimeError('Merged config changed input scope')
    # Terminated prior compute is bounded by its durable cleanup record time.
    # New run is bounded independently to two hours; use full scan-envelope $5,
    # not merely current Athena usage. Raw retained EBS is separately authorized.
    prior_compute=0.0
    for f in HERE.glob('oaspike-*/state.json'):
        record=json.loads(f.read_text())
        if not record.get('instance_id'):continue
        if record.get('instance_termination_verified') is not True:raise RuntimeError('Prior compute termination unverified: '+str(f))
        launch=datetime.fromisoformat(record['launched_at']).timestamp()
        hours=max(1/60,(f.stat().st_mtime-launch)/3600)
        if record['instance_type']=='m7g.8xlarge':rate=1.3056;diskrate=(400*.08+375*.04)/730
        elif record['instance_type']=='t4g.small':rate=.0168;diskrate=16*.08/730
        else:raise RuntimeError('Unknown prior instance price')
        prior_compute+=hours*(rate+diskrate+.005)  # public IPv4
    cap=prior_compute+2*(1.3056+(400*.08+375*.04)/730+.005)+5+1.0
    if cap>=15:raise RuntimeError('Tuning would exceed $15 conservative envelope: '+str(cap))
    job=Job(config,instance_type='m7g.8xlarge',guest_path=HERE/'tune_guest.py',az=raw['az'],raw_volume_id=raw['volume_id'],disk_gib=400,throughput=500)
    result={'state':'starting','started_at':datetime.now(timezone.utc),'ch_run':job.name,'budget_upper_usd':cap,'prior_compute_upper_usd':prior_compute,'other_allowance_usd':1,'new_athena_scans':0,'baseline_ch_run':baseline['ch_run'],'oracle_sha256':oracle}
    write(path,result)
    try:
        job.create_bucket();job.launch();result.update(state='running',instance_id=job.state['instance_id']);write(path,result)
        print(json.dumps({'run':job.name,'instance':job.state['instance_id'],'budget_upper_usd':cap}),flush=True)
        evidence=job.wait()
        if evidence.get('experiment')!='targeted_q02':raise RuntimeError('Unexpected tuning summary')
        result.update(state=evidence['state'],all_cases_validated=evidence['all_cases_validated'],finished_at=datetime.now(timezone.utc));write(path,result)
    except BaseException as exc:
        result.update(state='failed',error=str(exc));write(path,result)
        try:job.fetch()
        except Exception as fetch_error:result['fetch_error']=str(fetch_error);write(path,result)
        raise
    finally:
        errors=job.cleanup()
        if errors:raise RuntimeError('Tuning cleanup requires inspection: '+str(errors))

if __name__=='__main__':main()
