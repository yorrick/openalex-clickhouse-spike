"""Conservative rates x lifecycle bounds, separate from future retained storage."""
from pathlib import Path
from datetime import datetime,timezone
import json
from controls import write
from export_report import HERE,DEST

def main():
 rows=[];compute=0;root=0;ip=0
 tiernames={}
 for name in ('small','medium','large'):
  d=json.loads((HERE/('stage2_'+name+'-state.json')).read_text());tiernames[d['ch_run']]=f'{name} baseline'
 tuning=json.loads((HERE/'tuning-state.json').read_text());tiernames[tuning['ch_run']]='31.89m q02 tuning'
 for f in sorted(HERE.glob('oaspike-*/state.json')):
  d=json.loads(f.read_text())
  if not d.get('instance_id'):continue
  if d.get('instance_termination_verified') is not True or d.get('cleanup_errors'):raise RuntimeError('Compute teardown unverified: '+str(f))
  started=datetime.fromisoformat(d['launched_at']).timestamp()
  # Add60s for API/create-to-launched_at rounding; cleanup record mtime is a
  # conservative end bound that includes resource deletion after termination.
  sec=max(60,f.stat().st_mtime-started+60)
  hours=sec/3600
  if d['instance_type']=='m7g.8xlarge':rate=1.3056;rootrate=47/730
  elif d['instance_type']=='t4g.small':rate=.0168;rootrate=16*.08/730
  else:raise RuntimeError('Unknown instance rate')
  c=hours*rate;e=hours*rootrate;v=hours*.005;compute+=c;root+=e;ip+=v
  rows.append({'run':d['run_id'],'purpose':tiernames.get(d['run_id'],'source preparation/probe'),'type':d['instance_type'],'lifecycle_upper_seconds':sec,'ec2_usd_upper':c,'root_usd_upper':e,'ipv4_usd_upper':v,'total_usd_upper':c+e+v,'termination_verified':True})
 budget=json.loads((HERE/'scan-budget.json').read_text());scan_bytes=sum(t['used'] for t in budget['tiers'].values());scanfee=scan_bytes*5/1e12
 allowance=1.0
 total=compute+root+ip+scanfee+allowance
 if total>=15:raise RuntimeError('Temporary total budget exceeded')
 result={'computed_at':datetime.now(timezone.utc).isoformat(),'currency':'USD','ec2_compute_upper':compute,'temporary_root_ebs_upper':root,'public_ipv4_upper':ip,'athena_rounded_bytes':scan_bytes,'athena_scan_fee_conservative':scanfee,'other_allowance':allowance,'total_conservative_estimate':total,'retained_raw_ebs_gib':120,'retained_raw_usd_month':9.6,'rows':rows,'rates':{'m7g.8xlarge_usd_hour':1.3056,'t4g.small_usd_hour':.0168,'scratch_400gib_500mibps_usd_month':47,'gp3_usd_gib_month':.08,'additional_gp3_mibps_usd_month':.04,'ipv4_usd_hour':.005,'athena_usd_per_decimal_TB':5},'limitations':['Lifecycle bounds are not an invoice','60 seconds added per VM to cover create-to-record timing','EBS root creation/deletion boundaries and small requests/copy/list/GET/result storage/data return/CPU credits/old pilot are covered by the other allowance','Scan pricing uses a conservative decimal TB assumption, not a verified invoice billing-unit interpretation','The intentionally retained raw input EBS is ongoing and separately authorized','Tax/credits excluded']}
 write(DEST/'costs.json',result)
 rr=[]
 for r in rows:rr.append(f"| {r['purpose']} | {r['type']} | {r['lifecycle_upper_seconds']/60:.2f} min | ${r['ec2_usd_upper']:.4f} | ${r['root_usd_upper']:.4f} | ${r['ipv4_usd_upper']:.4f} |")
 text=f'''## Costs and teardown

The conservative temporary experiment total is **US${total:.2f}**, below the
approved US$15 envelope. This includes **US${scanfee:.5f}** of estimated Athena
scan fees across **{scan_bytes/1e9:.3f} GB** of rounded statements, and a full
**US$1 allowance** for requests, S3 copies/storage, returned results, CPU credits,
minor boundary timing and the earlier US$0.081 pilot. This is a rate-based
estimate with an unmetered allowance, not a proven invoice upper bound; credits and tax are excluded.

| Run | Instance | Bounded lifetime | EC2 upper | Scratch upper | Public IPv4 upper |
|---|---|---:|---:|---:|---:|
'''+ '\n'.join(rr)+f'''

Compute subtotal: ${compute:.4f}; temporary root EBS: ${root:.4f}; public IPv4:
${ip:.4f}. Bounds run from the recorded launch to the durable cleanup record,
plus 60 seconds per VM for launch-record timing. Root storage uses $0.08/GiB-month
and $0.04/additional MiB/s-month above the included 125 MiB/s; the 400 GiB / 500 MiB/s
configuration is $47/month while provisioned, prorated for these brief runs.
EC2 m7g.8xlarge is $1.3056/hour on demand; this is the host charge even though
Docker has only 18 of its 32 CPUs. Query latency alone is not the total cost of
an ephemeral run: boot, loading, priming, QA and teardown also consume time.
Keeping that host running continuously would be a different cost model.

Every study instance is terminated and all temporary root disks, security groups,
instance roles/profiles and termination schedules are removed. Athena workgroups
and Glue databases are removed. The private 98.302 GB source copy is explicitly
deleted after QA. Evidence/result buckets have seven-day expiration; public reports
and complete telemetry are also retained in Git and the local study directory.
The only intentional ongoing disk is the encrypted **120 GiB raw EBS volume**,
kept detached in us-east-1a at approximately **US$9.60/month** until explicitly
removed. Its source data remain available for future tests without laptop upload.

Details: [cost calculation](../../results/aws-scaling-2026-11-06/costs.json),
[final cleanup inventory](../../results/aws-scaling-2026-11-06/cleanup.json).
Rates: [Athena](https://aws.amazon.com/athena/pricing/),
[EBS](https://aws.amazon.com/ebs/pricing/),
[public IPv4](https://aws.amazon.com/vpc/pricing/).
'''
 (HERE/'cost-report.md').write_text(text)
 print(json.dumps({'estimate_usd':total,'scan_fee_usd':scanfee,'rows':len(rows)}))

if __name__=='__main__':main()
