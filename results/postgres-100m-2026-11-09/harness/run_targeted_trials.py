"""Onecandidatepermissedaggregatefamily, sameCPU/memorycaps, fullresultQA."""
import json,time
from pg_helpers import HERE,dump,connect
from run_postgres import one
from benchmark_helpers import snapshot

def read(p):return json.loads(p.read_text())
def main():
 baseline=read(HERE/'postgres-aggregate-cases.json');plan=read(HERE/'targeted-tuning-plan.json');selected=dict(baseline);trials={}
 for name,filename in plan['cases'].items():
  original=baseline[name]
  if original['state']=='complete' and original['median_seconds']<60:continue
  sql=(HERE/'sql'/filename).read_text();label=name+'_targeted_100m';oracle=read(HERE/'athena-cases.json')[name]
  value=one(name,sql,plan['settings'],oracle,label);trials[name]=value
  if value['state']=='complete' and (original['state']!='complete' or value['median_seconds']<original['median_seconds']):selected[name]=value
  dump(HERE/'postgres-targeted-trials.json',trials);dump(HERE/'postgres-selected-aggregates.json',selected)
 with connect() as pg:dump(HERE/'results/postgres/storage-after-aggregates.json',snapshot(pg))
 failed=[name for name,v in selected.items() if v['state']!='complete' or v['median_seconds']>=60]
 decision={'at':time.time(),'cohort_works':100087422,'scope':'Fouraggregatefamilieswithcompleteunchangedrelatedindexes;citationfamiliesnotyetmeasuredat100m','selected':{k:{'label':v.get('label',k),'state':v['state'],'median_seconds':v.get('median_seconds'),'settings':v.get('requested_settings')} for k,v in selected.items()},'missed_60_seconds':failed,'volume_growth_stopped':bool(failed),'one_trial_per_failed_family':True,'no_larger_cohort_started':True,'citation_indexes_not_completed_due_host_disk_guard':True}
 dump(HERE/'postgres-aggregate-decision-final.json',decision);print('TARGETEDTRIALSDONE',json.dumps(decision,indent=2),flush=True)
if __name__=='__main__':main()
