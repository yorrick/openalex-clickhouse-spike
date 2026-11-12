from pathlib import Path
import json,time,datetime,boto3
from botocore import UNSIGNED
from botocore.config import Config
HERE=Path(__file__).resolve().parent
s=boto3.Session(profile_name='certification',region_name='us-east-1')
ident=s.client('sts').get_caller_identity();assert ident['Account']=='502425560524'
ec=s.client('ec2');price=s.client('pricing',region_name='us-east-1')
filters={'instanceType':'m7g.4xlarge','location':'US East (N. Virginia)','operatingSystem':'Linux','tenancy':'Shared','preInstalledSw':'NA','capacitystatus':'Used'}
r=price.get_products(ServiceCode='AmazonEC2',Filters=[{'Type':'TERM_MATCH','Field':k,'Value':v} for k,v in filters.items()],MaxResults=100)
rates=[]
for raw in r['PriceList']:
 p=json.loads(raw)
 for term in p['terms']['OnDemand'].values():
  for d in term['priceDimensions'].values():
   if d['unit']=='Hrs':rates.append({'sku':p['product']['sku'],'usd_per_hour':float(d['pricePerUnit']['USD']),'description':d['description']})
assert len(rates)==1 and 0<rates[0]['usd_per_hour']<1
vpcs=ec.describe_vpcs(Filters=[{'Name':'is-default','Values':['true']}])['Vpcs'];assert len(vpcs)==1
subnets=ec.describe_subnets(Filters=[{'Name':'vpc-id','Values':[vpcs[0]['VpcId']]}])['Subnets'];subnets=sorted((x for x in subnets if x['AvailableIpAddressCount']>8),key=lambda x:x['AvailabilityZone'])
offerings={x['Location'] for x in ec.describe_instance_type_offerings(LocationType='availability-zone',Filters=[{'Name':'instance-type','Values':['m7g.4xlarge']}])['InstanceTypeOfferings']}
subnet=next(x for x in subnets if x['AvailabilityZone'] in offerings)
amis=ec.describe_images(Owners=['099720109477'],Filters=[{'Name':'name','Values':['ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-arm64-server-*']},{'Name':'state','Values':['available']},{'Name':'architecture','Values':['arm64']}])['Images'];ami=max(amis,key=lambda x:x['CreationDate'])
manifest=json.loads((HERE/'input-manifest.json').read_text());prior=480
pub=boto3.client('s3',region_name='us-east-1',config=Config(signature_version=UNSIGNED,retries={'max_attempts':2}))
f=next(f for f in manifest['files'][prior:] if f.get('version_id'))
a=pub.get_object(Bucket='openalex',Key=f['source_key'],VersionId=f['version_id'],Range='bytes=0-3');magic=a['Body'].read();assert magic==b'PAR1';assert a.get('VersionId')==f['version_id']
cost={'ec2_hourly':rates[0]['usd_per_hour'],'hours_max':12,'root_gib':32,'scratch_gib':1024,'gp3_storage_gib_month':.08,'gp3_extra_iops':3000,'gp3_iops_month':.005,'gp3_extra_throughput_mibs':375,'gp3_throughput_month':.04,'public_ipv4_hourly':.005,'athena_reserved_usd':8,'other_requests_reserved_usd':1,'budget_usd':25}
cost['infrastructure_upper_estimate_usd']=12*(cost['ec2_hourly']+cost['public_ipv4_hourly']+((32+1024)*.08+3000*.005+375*.04)/730)
cost['total_reserved_estimate_usd']=cost['infrastructure_upper_estimate_usd']+cost['athena_reserved_usd']+cost['other_requests_reserved_usd'];assert cost['total_reserved_estimate_usd']<25
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'account':ident['Account'],'region':'us-east-1','price_source':'AWS Price List API GetProducts','ec2_rates':rates,'cost':cost,'instance_type':ec.describe_instance_types(InstanceTypes=['m7g.4xlarge'])['InstanceTypes'][0],'vpc':vpcs[0]['VpcId'],'subnet':subnet['SubnetId'],'az':subnet['AvailabilityZone'],'ami':ami['ImageId'],'ami_name':ami['Name'],'public_historical_probe':{'key':f['source_key'],'version':f['version_id'],'magic':'PAR1','range':a['ContentRange']}}
(HERE/'results/preflight.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:out[k] for k in ['account','az','ami','cost','public_historical_probe']},indent=2))
