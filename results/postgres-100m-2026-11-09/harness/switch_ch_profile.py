"""Save12GiBfirst/warmobservations,thenmeasureexplicit24GiBhashprofileonsamecontainer."""
from pathlib import Path
import hashlib,json,os,psutil,shutil,signal,subprocess,sys,time
from pg_helpers import HERE,dump
NAME='openalex-ch100-bench-20261109';FOLDER=HERE/'results/clickhouse';PID=68094

def read(p):return json.loads(Path(p).read_text())
def main():
 proc=psutil.Process(PID);assert 'run_clickhouse.py' in ' '.join(proc.cmdline())
 while True:
  p=FOLDER/'q02.json'
  if p.exists() and len(read(p).get('runs',[]))>=2:break
  if not proc.is_running():raise RuntimeError('CHdriverendedbeforecontrolledswitch')
  time.sleep(.2)
 proc.send_signal(signal.SIGSTOP)
 archive=FOLDER/'profile12-partial';archive.mkdir(exist_ok=True)
 # Settleonlya possible already-startedthirdq02execution, never a differentquery.
 active=subprocess.run(['docker','exec',NAME,'clickhouse-client','--query',"SELECT query_id FROM system.processes WHERE startsWith(query_id,'oapg100-q02-') FORMAT JSONEachRow"],capture_output=True,text=True,check=True)
 killed=[]
 for line in active.stdout.splitlines():
  qid=json.loads(line)['query_id'];assert qid.startswith('oapg100-q02-')
  subprocess.run(['docker','exec',NAME,'clickhouse-client','--query',"KILL QUERY WHERE query_id='"+qid+"' SYNC"],capture_output=True,text=True,check=True);killed.append(qid)
 for f in list(FOLDER.glob('q02*')):
  if f.is_file():shutil.move(str(f),str(archive/f.name))
 proc.send_signal(signal.SIGKILL)
 old=read(archive/'q02.json');assert len(old['runs'])>=2
 script=HERE/'run_clickhouse.py';shutil.copy2(script,HERE/'run_clickhouse-executed-profile12.py');s=script.read_text()
 # Currentliveprofile12codeprecededthemanualprivatehostnamefix.
 code=s.replace("'max_memory_usage':12*(1<<30)","'max_memory_usage':24*(1<<30)").replace("'join_algorithm':'auto'","'join_algorithm':'hash'")
 start=code.index(' # Finishall backgroundmerges');end=code.index(' catalog={}',start)
 block=code[start:end];code=code[:start]+" if not (FOLDER/'storage-before-queries.json').exists():\n"+''.join(' '+line if line.strip() else line for line in block.splitlines(keepends=True))+code[end:]
 script.write_text(code)
 plan={'at':time.time(),'reason':'q02at12GiBcompletedprimer228.282sandused1531externaljoinparts;firstwarmalsoover60s. Avoidrepeatingknownslowprofile,explicitHashwith24GiBquerycapwithinunchanged16CPU32GiBcontainer.','old_partial_observations':[{'kind':r['kind'],'seconds':r['query_log']['seconds'],'state':r['state']} for r in old['runs']],'old_profile_has_no_3warm_median_or_full_QA':True,'settled_extra_query_ids':killed,'profile24':{'max_memory_usage':24*(1<<30),'join_algorithm':'hash','max_threads':16,'spill_threshold_bytes':4*(1<<30)},'all_loaded_data_and_existing_q01_result_retained':True,'inputs_readonly':True,'no_larger_dataset':True,'skip_repeated_data_merges_on_already_prepared_dataset':True}
 dump(HERE/'results/ch-profile24-plan.json',plan);print('SWITCHEDTO24GiBHASH',flush=True)
 subprocess.run([sys.executable,'-m','py_compile',str(script)],check=True)
 with (HERE/'clickhouse-profile24.log').open('w') as log:
  child=subprocess.Popen([sys.executable,str(script)],stdout=log,stderr=subprocess.STDOUT)
  watch=HERE/'watch_ch_disk.py';ws=watch.read_text().replace('68094',str(child.pid));watch.write_text(ws)
  with (HERE/'ch-disk-watch-profile24.log').open('w') as wlog:
   guard=subprocess.Popen([sys.executable,str(watch)],stdout=wlog,stderr=subprocess.STDOUT)
   dump(HERE/'results/ch-profile24-process.json',{'pid':child.pid,'guard_pid':guard.pid,'at':time.time()})
   code=child.wait()
   try:guard.wait(timeout=5)
   except subprocess.TimeoutExpired:guard.terminate()
 dump(HERE/'results/ch-profile24-driver-exit.json',{'exit_code':code,'at':time.time()});assert code==0,code
 print('CHPROFILE24COMPLETE',flush=True)
if __name__=='__main__':main()
