"""Audit all retained scalar-column footers against the actual ClickHouse DDL."""
from pathlib import Path
import json,re,time
import pyarrow.parquet as pq
from helpers import HERE,dump

def main():
 st=time.monotonic();ddl=(HERE/'sql/clickhouse-schema.sql').read_text();tables={}
 for table,body in re.findall(r'CREATE TABLE\s+\w+\.(\w+)\s*\((.*?)\)\s*ENGINE',ddl,re.S):
  cols={}
  for line in body.splitlines():
   m=re.match(r'\s*(\w+)\s+(.+?)\s*,?\s*$',line)
   if m:cols[m[1]]=m[2].rstrip(',')
  tables[table]=cols
 counts=json.loads((HERE/'results/projection-complete.json').read_text())['counts'];assert set(tables)==set(counts)
 result={};problems=[];files=0
 for table,columns in tables.items():
  stat={c:{'target_type':typ,'rows':0,'nulls':0,'unknown_null_statistics':0,'min':None,'max':None} for c,typ in columns.items()}
  for path in (HERE/'projected'/table).glob('*.parquet'):
   files+=1;meta=pq.ParquetFile(path).metadata;assert meta.schema.names==list(columns),(table,meta.schema.names,list(columns))
   for r in range(meta.num_row_groups):
    rg=meta.row_group(r)
    for i,name in enumerate(columns):
     x=stat[name];s=rg.column(i).statistics;x['rows']+=rg.num_rows
     if s is None or s.null_count is None:x['unknown_null_statistics']+=1
     else:x['nulls']+=s.null_count
     if s is not None and s.has_min_max and isinstance(s.min,(int,float)):
      if x['min'] is None or s.min<x['min']:x['min']=s.min
      if x['max'] is None or s.max>x['max']:x['max']=s.max
  for name,x in stat.items():
   assert x['rows']==counts[table]
   if x['unknown_null_statistics']:problems.append([table,name,'NULL statistics unavailable'])
   if 'Nullable(' not in x['target_type'] and x['nulls']:problems.append([table,name,'NULL values target nonnullable',x['nulls']])
   m=re.search(r'UInt(8|16|32|64)',x['target_type'])
   if m and x['min'] is not None:
    if not 0<=x['min']<=x['max']<=2**int(m[1])-1:problems.append([table,name,'unsigned conversion would lose values',x['min'],x['max']])
  result[table]=stat
 proof={'passed':not problems,'method':'All6999retained Parquet fragment row-group NULL counts and integer extrema compared with pinnedCH DDL. No silent NULL defaults or signed-to-unsigned wrap accepted. Footer audit, not full native-value row audit.','files':files,'columns':sum(len(c) for c in result.values()),'problems':problems,'tables':result,'seconds':time.monotonic()-st};dump(HERE/'results/field-range-null-qa.json',proof);assert not problems,problems;print('FIELD RANGE/NULL AUDIT PASS',files,'files',proof['columns'],'columns',flush=True)
if __name__=='__main__':main()
