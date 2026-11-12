"""Transparent estimate, never represented as an AWS invoice."""
from pathlib import Path
import json,datetime,math
HERE=Path(__file__).resolve().parent
c=json.loads((HERE/'cloud-state.json').read_text());end=json.loads((HERE/'results/aws-cleanup.json').read_text())['at'] if (HERE/'results/aws-cleanup.json').exists() else datetime.datetime.now(datetime.timezone.utc).isoformat()
start=datetime.datetime.fromisoformat(c['aws_launch_time']);stop=datetime.datetime.fromisoformat(end);hours=(stop-start).total_seconds()/3600
# November has 720 hours. EBS root and scratch begin at run provisioning,
# approximated by launch to verified cleanup; no incremental EBS storage is retained.
rates={'ec2_usd_hour':.6528,'ipv4_usd_hour':.005,'ebs_storage_gib_month':.08,'ebs_additional_iops_month':.005,'ebs_additional_mib_s_month':.04,'billing_month_hours':720,'athena_usd_decimal_tb':5.0}
items={'ec2':hours*rates['ec2_usd_hour'],'public_ipv4':hours*rates['ipv4_usd_hour'],'ebs_1056_gib':hours/720*1056*.08,'ebs_extra_3000_iops':hours/720*3000*.005,'ebs_extra_375_mib_s':hours/720*375*.04}
# The complete official query receipts are the authoritative billing-byte source.
receipts=json.loads((HERE/'results/athena-full-query-receipts.json').read_text())
assert all(q['Status']['State']=='SUCCEEDED' for q in receipts)
# Include the six successful metadata/scalar SELECTs at the stated minimum;
# the fourteen DDL statements do not receive this per-query scan charge.
billable=sum(max(10_000_000,math.ceil(q['Statistics'].get('DataScannedInBytes',0)/1_000_000)*1_000_000) for q in receipts if q['StatementType']=='DML')
items['athena']=billable/1e12*5
out={'invoice':False,'launch':start.isoformat(),'end':stop.isoformat(),'hours':hours,'rates':rates,'estimated_usd':items,'subtotal_usd':sum(items.values()),'unreconciled_s3_requests_storage_other_reserve_usd':1,'estimate_with_reserve_usd':sum(items.values())+1,'athena_rounded_billable_bytes':billable,'excludes':'Taxes, local hardware/electricity, older retained EBS and any unobserved account-level billing. EC2/EBS/IPv4 are approximated launch to verified cleanup; final invoice is authoritative.'}
(HERE/'results/cost-estimate.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
