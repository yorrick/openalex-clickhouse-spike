from pg_helpers import HERE,connect,dump,Monitor
from index_and_benchmark import summarize_monitor
import time,hashlib,json,sys

def check(pg,ids):
 rows=pg.execute('SELECT work_id,cited_by_count FROM works WHERE work_id=ANY(%s) ORDER BY work_id',[ids]).fetchall();return hashlib.sha256(json.dumps(rows).encode()).hexdigest()
def main():
 folder=HERE/'results/update-probes';folder.mkdir(exist_ok=True)
 for size in (1000,10000):
  with connect() as pg:
   ids=[r[0] for r in pg.execute('SELECT work_id FROM works ORDER BY work_id LIMIT %s',[size]).fetchall()];before=check(pg,ids)
   pg.execute('BEGIN')
   try:
    pg.execute('CREATE TEMP TABLE changed_works ON COMMIT DROP AS SELECT * FROM works WHERE work_id=ANY(%s)',[ids]);pg.execute('UPDATE changed_works SET cited_by_count=cited_by_count+1');pg.execute('CREATE UNIQUE INDEX ON changed_works(work_id)')
    for table,col in [('work_author','work_id'),('work_institution','work_id'),('work_topic','work_id'),('citation_edge','citing_work_id')]:pg.execute(f'CREATE TEMP TABLE changed_{table} ON COMMIT DROP AS SELECT * FROM {table} WHERE {col}=ANY(%s)',[ids])
    apply=[]
    apply.append('INSERT INTO works SELECT * FROM changed_works ON CONFLICT(work_id) DO UPDATE SET canonical_id=excluded.canonical_id,publication_year=excluded.publication_year,work_type=excluded.work_type,source_id=excluded.source_id,is_oa=excluded.is_oa,is_xpac=excluded.is_xpac,cited_by_count=excluded.cited_by_count,primary_topic_id=excluded.primary_topic_id')
    for table,col in [('work_author','work_id'),('work_institution','work_id'),('work_topic','work_id'),('citation_edge','citing_work_id')]:apply += [f'DELETE FROM {table} t USING changed_works w WHERE t.{col}=w.work_id',f'INSERT INTO {table} SELECT * FROM changed_{table}']
    rowsizes={t:pg.execute('SELECT count(*) FROM changed_'+t).fetchone()[0] for t in ('works','work_author','work_institution','work_topic','citation_edge')};runs=[]
    for i in range(3):
     m=Monitor().start();st=time.monotonic();stats=[]
     for sql in apply:
      p=pg.execute('EXPLAIN (ANALYZE, BUFFERS, WAL, TIMING OFF, FORMAT JSON) '+sql).fetchone()[0][0];stats.append(p)
     elapsed=time.monotonic()-st;xs=m.stop();after=check(pg,ids);runs.append({'iteration':i,'client_apply_seconds':elapsed,'native_statement_execution_seconds':sum(p['Execution Time']/1000 for p in stats),'output_hash':after,'plans':stats,'resources':summarize_monitor(xs)});dump(folder/f'update-{size}-{i}-telemetry.json',xs)
    assert len(set(x['output_hash'] for x in runs))==1,'Replay changed finalvalues'
    assert runs[0]['output_hash']!=before,'Updated citationcount unchanged'
    idsdel=ids[:100];st=time.monotonic()
    for table,col in [('work_author','work_id'),('work_institution','work_id'),('work_topic','work_id'),('citation_edge','citing_work_id'),('works','work_id')]:pg.execute(f'DELETE FROM {table} WHERE {col}=ANY(%s)',[idsdel])
    missing=pg.execute('SELECT count(*) FROM works WHERE work_id=ANY(%s)',[idsdel]).fetchone()[0];assert missing==0
    deletion_seconds=time.monotonic()-st
    dump(folder/f'update-{size}.json',{'synthetic':True,'batch_works':size,'staged_rows':rowsizes,'apply_sql':apply,'runs':runs,'replay_value_idempotent':True,'tombstone_batch_works':100,'tombstone_apply_seconds':deletion_seconds,'tombstone_rows_remaining':missing,'scope':'Synthetic staged realrows with citationcount+1;3replays samebatch in one transaction, no per-replay COMMIT/fsync; excludes Parquet extraction/staging, network/snapshot reconciliation; entireexperimentROLLBACK after measurement; leaves incomingreferences from unaffectedworks; statementEXPLAINinstrumentationincluded'})
   finally:pg.execute('ROLLBACK')
   assert check(pg,ids)==before,'Rollback did notrestorebaselinevalues'
   print('Update probe',size,'replays idempotent; tombstones witnessed; baseline restored',flush=True)
if __name__=='__main__':main()
