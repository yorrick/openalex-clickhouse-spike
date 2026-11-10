"""Resume persisted rawAthena cases; keep300s timeddeadline, longerexactSQLQAifneeded."""
import hashlib,json,time
from athena_reference import Reference
from pg_helpers import HERE,dump
from tier_sql import queries,canonical_rows

def fingerprint(name,rows,record):
 canon=canonical_rows(name[:3],rows)
 return {'query_id':record['id'],'statistics':record['statistics'],'rows':len(rows),'canonical_sha256':hashlib.sha256('\n'.join(canon).encode()).hexdigest()}
def main():
 r=Reference();assert r.state['setup_complete'];assert (HERE/'results/projection-complete.json').exists()
 path=HERE/'athena-cases.json';cases=json.loads(path.read_text()) if path.exists() else {};catalog={}
 for seed in [51557542,24222542,2003585639]:
  for name,sql in queries(seed).items():catalog[name+('-s'+str(seed) if name in ('q05','q06') else '')]=sql
 for name,sql in catalog.items():
  result=cases.setdefault(name,{'sql':sql,'runs':[]});assert result['sql']==sql
  deadline=[x for x in r.records if x['sql']==sql and x.get('state')=='CANCELLED' and x.get('client_seconds',0)>=300]
  if deadline and len(result['runs'])<3:result['state']='timed_timeout';result['timeout_record']=deadline[-1];dump(path,cases)
  while len(result['runs'])<3 and result.get('state')!='timed_timeout':
   try:rows,record=r.query(sql)
   except RuntimeError:
    x=r.records[-1]
    if x.get('state')=='CANCELLED' and x.get('client_seconds',0)>=300:
     result['state']='timed_timeout';result['timeout_record']=x;dump(path,cases);break
    raise
   value=fingerprint(name,rows,record)
   if result['runs']:assert (value['rows'],value['canonical_sha256'])==(result['runs'][0]['rows'],result['runs'][0]['canonical_sha256'])
   result['runs'].append(value);dump(path,cases);print('Athena',name,'run',len(result['runs']),record['statistics']['TotalExecutionTimeInMillis']/1000,flush=True)
  if result['runs']:result['reference']=result['runs'][0]
  elif 'reference' not in result:
   print('ExactSQL validationonly,1200sdeadline:',name,flush=True);rows,record=r.query(sql,timeout=1200);value=fingerprint(name,rows,record);value['scope']='Exactsame rawSQL,validationonly aftertimed300stimeout,excludedfromtimedmedian';result['reference']=value
  if len(result['runs'])==3:result['state']='complete'
  dump(path,cases)
 r.state['athena_complete']=True;r.save();print('ALLATHENACASESREFERENCECOMPLETE',flush=True)
if __name__=='__main__':main()
