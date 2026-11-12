from pathlib import Path
import json,statistics
HERE=Path(__file__).resolve().parent
DOC=Path('/Users/yorrickjansen/work/openalex/.claude/worktrees/ec2-200m/docs/ec2-200m-benchmark.md')
ROOT=HERE/'cloud-results'
FAMILIES=['q01','q02','q03','q04','q05','q06','q07']
LABELS=['Year/type/open-access counts','Topic/year metrics','Top 1000 authors','International collaboration','One-hop citations, 3 seeds','Two-hop citations, 3 seeds','Top cited Works/year']
def read(p):return json.loads(p.read_text())
def native(engine):
 for name in [engine+'-selected.json',engine+'-cases.json']:
  if (ROOT/name).exists():return read(ROOT/name)
 result={}
 if (ROOT/engine).exists():
  for p in (ROOT/engine).glob('q*.json'):
   d=read(p)
   if isinstance(d,dict) and 'name' in d and 'state' in d and 'runs' in d and '-execution' not in p.name:result[d['name']]=d
 return result

def summary(cases,family,athena=False):
 group=[v for k,v in cases.items() if k[:3]==family and ('_trial' not in k and '_tuned' not in k)]
 required=3 if family in ['q05','q06'] else 1
 if len(group)!=required:return 'Pending'
 times=[]
 for c in group:
  if athena:
   if len(c.get('runs',[]))!=3:return 'Pending'
   times.append(statistics.median(r['statistics']['TotalExecutionTimeInMillis']/1000 for r in c['runs']))
  else:
   if c.get('state')!='complete':return c.get('state','Pending')
   times.append(c['median_seconds'])
 value=max(times);return f'{value:.6f}' if value<1 else f'{value:.3f}'

def main():
 pg=native('postgres');ch=native('clickhouse');athena=read(HERE/'athena-cases.json') if (HERE/'athena-cases.json').exists() else {}
 lines=['| Family | PostgreSQL EC2 200m median s | ClickHouse EC2 200m median s | Raw Athena 200m median s |','|---|---|---|---|']
 for f,label in zip(FAMILIES,LABELS):lines.append('| '+f+' '+label+' | '+summary(pg,f)+' | '+summary(ch,f)+' | '+summary(athena,f,True)+' |')
 s=DOC.read_text();start=s.index('| Family |');end=s.index('\n\n',start);s=s[:start]+'\n'.join(lines)+s[end:]
 if athena:s=s.replace('No 200m database-query latency is claimed yet.','The table includes completed raw Athena measurements; native results are pending until each three-warm case finishes.')
 DOC.write_text(s)
 print('\n'.join(lines))
if __name__=='__main__':main()
