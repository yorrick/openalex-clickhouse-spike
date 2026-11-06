"""Export compact, non-sensitive measured evidence into the report worktree."""
from pathlib import Path
from statistics import median
import json
import hashlib
import gzip
from controls import write
from analyze_series import main as analyze

HERE=Path(__file__).resolve().parent
REPO=Path('/Users/yorrickjansen/work/openalex/.claude/worktrees/aws-athena-benchmark-results')
DEST=REPO/'results/aws-scaling-2026-11-06'
REPORT=REPO/'docs/superpowers/2026-08-05-single-user-resource-benchmark-results.md'


def main():
    analyze();analysis=json.loads((HERE/'series-analysis.json').read_text());DEST.mkdir(exist_ok=True)
    remote=json.loads((HERE/'remote-manifest.json').read_text())
    prep=json.loads((HERE/'retained-volume.json').read_text())['summary']
    readback_ok=(prep['state']=='complete' and prep['files']==len(remote['files']) and prep['bytes']==sum(f['bytes'] for f in remote['files']) and prep['all_sha256_match'] is True and prep['filesystem_readback_sha256_verified'] is True and prep['manifest_identity']==json.loads((HERE/'approved-source-identity.json').read_text())['manifest_identity'] and prep['tiers']==remote['tiers'])
    if not readback_ok:raise RuntimeError('EBS preparation proof incomplete')
    proof={'snapshot_date':'2026-06-26','manifest_identity':json.loads((HERE/'approved-source-identity.json').read_text())['manifest_identity'],
        'file_count':len(remote['files']),'bytes':sum(f['bytes'] for f in remote['files']),
        'every_server_copy_full_object_sha256_matches':all(f['server_full_sha256_verified'] for f in remote['files']),
        'every_ec2_filesystem_readback_sha256_and_footer_count_matches':readback_ok,
        'raw_download_seconds':1402.649967288,'retained_raw_ebs_gib':120,'retained_raw_estimated_usd_month':9.60,
        'data_path':'S3 server-side historical version copy for Athena; direct OpenAlex version downloads into EC2 EBS',
        'full_snapshot':analysis['full_reference']}
    write(DEST/'input-proof.json',proof)
    completed={}
    for tier,data in analysis['tiers'].items():
        if data['state']!='complete' or data['athena_all_matched'] is not True:continue
        state=json.loads((HERE/(tier+'-state.json')).read_text());chroot=HERE/state['ch_run']/'cloud'
        core=json.loads((chroot/'summary.json').read_text());build=json.loads((chroot/'build.json').read_text());env=json.loads((chroot/'environment.json').read_text());fio=json.loads((chroot/'disk-control.json').read_text())
        trace={'timings':core['timings'],'cold_tests':core['cold_tests']}
        trace_bytes=json.dumps(trace,sort_keys=True,separators=(',',':')).encode()
        (DEST/('telemetry-'+tier+'.json.gz')).write_bytes(gzip.compress(trace_bytes,mtime=0))
        cases={}
        for name,c in data['cases'].items():
            scans=[r['statistics']['DataScannedInBytes'] for r in c['athena_runs']]
            cases[name]={k:c[k] for k in ('warm_seconds','median_seconds','min_seconds','max_seconds','status','resources','qa_matched','athena_median_seconds')}
            cases[name].update(athena_total_seconds=[r['statistics']['TotalExecutionTimeInMillis']/1000 for r in c['athena_runs']],athena_scan_bytes=scans,
                canonical_result_sha256=c['athena_runs'][0]['canonical_sha256'],result_rows=c['athena_runs'][0]['rows'],
                observations=[{k:v for k,v in r.items() if k!='telemetry'}|{'telemetry_endpoints':[r['telemetry'][0],r['telemetry'][-1]] if r.get('telemetry') else []} for r in core['timings'][name] if r.get('block','').startswith('warm')],
                cold_seconds=c.get('cold',{}).get('seconds'),cold_resources=c.get('cold_resources'))
        localpath=REPO/f'results/stage2-single-memory50-cpu18/tiers/{tier}-memory50gib/correctness.json'
        local=json.loads(localpath.read_text());assert local['normalized_sha256']==build['correctness']['normalized_sha256']
        result={'tier':tier,'snapshot_date':'2026-06-26','work_records':data['works'],'selected_raw_bytes':data['input_bytes'],'works_raw_bytes':data['works_bytes'],
            'complete_author_records':119129660,'complete_authors_raw_bytes':52769910496,
            'percent_full_works':data['percent_full_works'],'percent_full_raw_bytes':data['percent_full_bytes'],
            'normalized_bytes':data['normalized_bytes'],'table_bytes':data['table_bytes'],'normalized_sha256':build['correctness']['normalized_sha256'],
            'normalized_sha256_matches_historical_local':True,'container_cpus':18,'container_memory_gib':50,'host_instance_type':'m7g.8xlarge','host_vcpus':32,'host_memory_gib':128,
            'scratch_gib':400,'scratch_type':'gp3','scratch_iops':3000,'scratch_throughput_mib_s':500,
            'fio_sequential_read_bytes_s':fio['read']['jobs'][0]['read']['bw_bytes'],'load_dimensions_seconds':data['dimensions_seconds'],'load_works_seconds':data['works_load_seconds'],
            'merges_quiescent':data['merges_quiescent'],'graph':data['graph'],'cases':cases,'athena_billable_bytes_all_checks':data['athena_billable_bytes'],
            'athena_scan_cost_usd_all_checks':data['athena_billable_bytes']*5/1e12,'clickhouse_image':{k:env.get(k) for k in ('image','repo_digests','image_architecture')},
            'timing_method':'one primer plus three warm roundrobin FORMAT Null observations, server query_log seconds; separate JSON QA; one guest-cache-cleared observation per case',
            'athena_timing_method':'three repeated engine3 TotalExecutionTime observations, result reuse disabled, excludes CSV fetch',
            'query_settings':core['settings'],'optional_phase':core['optional_phase']}
        write(DEST/(tier+'.json'),result);completed[tier]=result
    print(json.dumps({'exported':list(completed)}))


if __name__=='__main__':main()
