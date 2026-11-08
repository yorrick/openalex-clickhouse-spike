from pg_helpers import HERE,connect,dump
from index_and_benchmark import ROOT,INDEXES,snapshot
from pathlib import Path
import sys,json,shutil,time

def main():
 tier=sys.argv[1];assert tier in ('stage2_medium','stage2_large')
 if shutil.disk_usage(HERE).free < 80*(1<<30):raise RuntimeError('Insufficienthostdisk')
 assert (HERE/'results/stage2_small/q07.json').exists()
 with connect() as pg:
  dump(HERE/'results'/f'pre-reset-{tier}.json',snapshot(pg))
  if tier=='stage2_medium':
   expected={x['table']:x['rows'] for x in json.loads((ROOT/'results/aws-scaling-2026-11-06/stage2_small.json').read_text())['table_bytes']}
   counts={t:pg.execute(f'SELECT count(*) FROM {t}').fetchone()[0] for t in expected};assert counts==expected,(counts,expected);dump(HERE/'results/small-table-count-qa.json',{'matched':True,'actual':counts,'expected':expected,'note':'After updateprobes ROLLBACK, before resettingWorkstables'})
  pg.execute('ALTER TABLE works DROP CONSTRAINT IF EXISTS works_pk')
  for name,sql in INDEXES:
   if name.endswith('_pk') and name!='works_pk':continue
   if name!='works_pk':pg.execute('DROP INDEX IF EXISTS '+name)
  pg.execute('TRUNCATE works,work_author,work_institution,work_topic,citation_edge')
 dump(HERE/'results'/f'scale-start-{tier}.json',{'time':time.time(),'retained_dimensions':['authors','institutions','sources','topics'],'reset_tables':['works','work_author','work_institution','work_topic','citation_edge'],'host_free_bytes':shutil.disk_usage(HERE).free})
 print('Prepared',tier,'retaining complete dimension tables',flush=True)
if __name__=='__main__':main()
