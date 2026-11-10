"""Seal100mPGcoverageandstopgrowthaftertheboundedaggregateprobe."""
import hashlib,json,subprocess,time
from pg_helpers import HERE,connect,dump,NAME

def read(p):return json.loads(p.read_text())
def main():
 decision=read(HERE/'postgres-aggregate-decision-final.json');assert decision['volume_growth_stopped'],'Allaggregatespass:needcitationtestsbeforescopingfinaldecision'
 selected=read(HERE/'postgres-selected-aggregates.json');assert set(selected)=={'q01','q02','q03','q04'}
 expected=['q01','q02','q03','q04','q05-s51557542','q06-s51557542','q07','q05-s24222542','q06-s24222542','q05-s2003585639','q06-s2003585639']
 for name in expected:
  if name in selected:continue
  sql=(HERE/'sql'/(name+'-postgres.sql')).read_text();selected[name]={'name':name,'state':'not_run','sql':sql,'sql_sha256':hashlib.sha256(sql.encode()).hexdigest(),'runs':[],'reason':'Host80GiBguardstoppedcitationindexcreation. Aggregatefamiliesalreadyfailed60sevenafteroneboundedprofile,sovolumegrowthandadditionalPGcitationworkstopped. No100mPGgraphlatencyclaimed.'}
 dump(HERE/'postgres-cases.json',selected)
 final={**decision,'required_families_unmeasured_at_100m':['q05','q06','q07'],'unmeasured_not_timeouts':True,'schema_index_count':12,'all_table_rows_loaded':True,'measured_scope':'q01-q04,same8noncitationWorkindexesand4dimensionPKsas32m','full_7_family_60s_criterion_failed':True,'larger_datasets_not_started':True,'limits':'DoesnotruleoutPostgreSQLonlargerhardware,differentindexes/queryalgorithms,nativeLinuxorpreaggregatedlayouts. No100mPGcitationperformanceor14-indexstorageclaim.'}
 dump(HERE/'postgres-decision-final.json',final)
 schema=subprocess.run(['docker','exec',NAME,'pg_dump','-U','openalex','-d','openalex','--schema-only'],capture_output=True,text=True,check=True).stdout;(HERE/'sql/postgres-100m-measured-schema.sql').write_text(schema)
 with connect() as pg:
  assert not pg.execute("SELECT pid FROM pg_stat_activity WHERE datname=current_database() AND pid<>pg_backend_pid() AND state='active' AND backend_type='client backend'").fetchall()
  pg.execute('ALTER TABLE citation_edge RESET (autovacuum_enabled)')
  dump(HERE/'results/postgres/post-measurement-state.json',{'at':time.time(),'citation_autovacuum_restored_to_default':True,'measured_table_heaps_and12_indexes_retained':True,'normalized_inputs_retained':True,'schema_dump':'sql/postgres-100m-measured-schema.sql'})
 subprocess.run(['docker','stop',NAME],capture_output=True,text=True,check=True)
 state=json.loads(subprocess.run(['docker','inspect',NAME],capture_output=True,text=True,check=True).stdout)[0];assert not state['State']['Running']
 dump(HERE/'results/postgres/stopped.json',{'at':time.time(),'container':NAME,'state':state['State'],'all_data_retained':True})
 print(json.dumps({'stopped':True,'selected':final['selected'],'unmeasured':final['required_families_unmeasured_at_100m']},indent=2))
if __name__=='__main__':main()
