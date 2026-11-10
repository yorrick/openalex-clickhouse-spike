"""FinishPGmeasurement, stopPG, thenrunmatchedCH; failopenlyonanyunexpectederror."""
import json,subprocess,sys,time
from pathlib import Path
import psutil
from pg_helpers import HERE,dump

def main():
 parent=psutil.Process(60081) if not (HERE/'postgres-aggregate-decision-final.json').exists() else None
 born=parent.create_time() if parent else None
 while not (HERE/'postgres-aggregate-decision-final.json').exists():
  if not psutil.pid_exists(parent.pid) or psutil.Process(parent.pid).create_time()!=born:raise RuntimeError('Targeteddriverendedwithoutfinaldecision')
  time.sleep(2)
 decision=json.loads((HERE/'postgres-aggregate-decision-final.json').read_text());assert decision['volume_growth_stopped']
 dump(HERE/'results/local-comparison-orchestration.json',{'at':time.time(),'pid':__import__('os').getpid(),'phase':'finalizePGthenCH','engines_sequential':True})
 with (HERE/'pg-finalization.log').open('w') as f:subprocess.run([sys.executable,str(HERE/'finalize_postgres.py')],stdout=f,stderr=subprocess.STDOUT,check=True)
 print('PGstopped;startingCH',flush=True)
 with (HERE/'clickhouse.log').open('w') as f:subprocess.run([sys.executable,str(HERE/'run_clickhouse.py')],stdout=f,stderr=subprocess.STDOUT,check=True)
 dump(HERE/'results/local-comparison-complete.json',{'at':time.time(),'complete':True});print('LOCALCOMPARISONCOMPLETE',flush=True)
if __name__=='__main__':main()
