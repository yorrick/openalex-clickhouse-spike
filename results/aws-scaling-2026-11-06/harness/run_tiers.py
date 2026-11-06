"""Sequential approved EC2/independent Athena runs, stop compute before QA scans."""
from pathlib import Path
from datetime import datetime,timezone
import argparse
import json

from cloud_job import Job
from athena_tier import Athena
from controls import ScanBudget,write
from scope import validate_scope, manifest_identity
from source_copy import Sources

HERE=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('tier',choices=['stage2_small','stage2_medium','stage2_large']);args=parser.parse_args()
    source=Sources(); source.fresh()
    retained=json.loads((HERE/'retained-volume.json').read_text())
    remote=json.loads((HERE/'remote-manifest.json').read_text())
    validate_scope(remote)
    if manifest_identity(remote)!=json.loads((HERE/'approved-source-identity.json').read_text())['manifest_identity']:
        raise RuntimeError('Approved input fingerprint differs')
    if retained['state']!='complete' or not all(f['server_full_sha256_verified'] for f in remote['files']):
        raise RuntimeError('Retained input or Athena copy not verified')
    results_path=HERE/(args.tier+'-state.json')
    if results_path.exists():
        raise RuntimeError('Tier already recorded; inspect and resume explicitly')
    config=remote|{'raw_volume_id':retained['volume_id'],'series_id':retained['series_id'],'tier':args.tier}
    if args.tier!='stage2_small':
        small=json.loads((HERE/'stage2_small-state.json').read_text())
        if small['state']!='complete' or small.get('all_qa_matched') is not True or small.get('latency_evidence_valid') is not True:
            raise RuntimeError('2m tier must finish before subsequent tiers')
        config['seeds']=json.loads((HERE/small['ch_run']/'cloud/summary.json').read_text())['seeds']
    budget_path=HERE/'scan-budget.json'
    budget=ScanBudget(budget_path) if budget_path.exists() else ScanBudget.create(budget_path)
    state={'tier':args.tier,'state':'starting','started_at':datetime.now(timezone.utc)}
    job=Job(config,instance_type='m7g.8xlarge',guest_path=HERE/'baseline_guest.py',az=retained['az'],raw_volume_id=retained['volume_id'],disk_gib=400,throughput=500)
    state.update(ch_run=job.name);write(results_path,state)
    try:
        job.create_bucket();job.launch();state['state']='clickhouse_running';write(results_path,state)
        print(json.dumps({'tier':args.tier,'instance':job.state['instance_id'],'run':job.name}),flush=True)
        cloud=job.wait()
        state.update(ch_optional_outcome=cloud.get('optional_phase'),ch_controller_stop=cloud.get('controller_stop_reason'),merges_quiescent=cloud.get('merges_quiescent'))
        if not cloud['qa']:
            raise RuntimeError('No CH queries completed; do not spend Athena scans')
        state['missing_ch_qa']=sorted(set(cloud['timings'])-set(cloud['qa']))
        write(results_path,state)
    except BaseException as exc:
        state.update(state='failed',error=str(exc));write(results_path,state)
        try:
            job.fetch()
        except Exception as artifact_error:
            state['artifact_fetch_error']=str(artifact_error);write(results_path,state)
        raise
    finally:
        errors=job.cleanup()
        if errors:
            raise RuntimeError('Compute cleanup errors require inspection: '+str(errors))
    state.update(state='athena_starting');write(results_path,state)
    athena=Athena(remote,args.tier,budget);state['athena_run']=athena.name;write(results_path,state)
    try:
        athena.setup();athena.compare(job.out/'cloud')
        qa=json.loads((athena.out/'summary.json').read_text())
        state.update(all_qa_matched=qa['all_matched'],not_compared=qa['not_compared'],latency_evidence_valid=bool(cloud.get('merges_quiescent')))
        state.update(state='complete',finished_at=datetime.now(timezone.utc),billable_bytes=budget.state['tiers'][args.tier]['used']);write(results_path,state)
    except BaseException as exc:
        state.update(state='failed',error=str(exc));write(results_path,state);raise
    finally:
        errors=athena.cleanup();budget.close()
        if errors:
            raise RuntimeError('Athena cleanup errors require inspection: '+str(errors))


if __name__=='__main__':
    main()
