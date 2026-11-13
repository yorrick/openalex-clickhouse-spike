"""Fresh-process default remote-cache variant; original disabled-cache results retained."""
import sys,json,subprocess,time,os
from pathlib import Path
import psutil
import run_spike as probe
S=probe.S
if len(sys.argv)>1:
 original=probe.connection
 def conn(profile=None):
  c=original(profile);c.execute('SET enable_external_file_cache=true');c.execute("SET max_temp_directory_size='4GB'");return c
 probe.connection=conn;probe.child(sys.argv[1],int(sys.argv[2]))
else:
 ref=json.loads((S/'summary.json').read_text())['reference'];rows=[]
 for run in range(1,4):
  for mode in ['s3_default_narrow','s3_default_full']:
   print('START',mode,run,flush=True);p=subprocess.Popen([sys.executable,__file__,mode,str(run)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);st=time.monotonic();samples=[]
   while p.poll() is None:
    try:
     q=psutil.Process(p.pid);rss=q.memory_info().rss;samples.append({'seconds':time.monotonic()-st,'rss_bytes':rss})
     if rss>12*2**30 or time.monotonic()-st>240:p.kill();raise RuntimeError('Watchdog limit')
    except psutil.NoSuchProcess:pass
    time.sleep(.1)
   stdout,stderr=p.communicate();(S/f'{mode}-{run}.stderr').write_text(stderr);assert p.returncode==0,stderr[-1800:];print(stdout.strip(),flush=True)
   z=json.loads((S/f'{mode}-{run}.json').read_text());qa=probe.value_hash(z['output_file'],narrow=mode.endswith('narrow'));assert qa==ref['narrow' if mode.endswith('narrow') else 'full'];z['independent_value_qa']=qa;probe.dump(f'{mode}-{run}.json',z);probe.dump(f'{mode}-{run}-samples.json',samples);rows.append(z)
 probe.dump('default-cache-summary.json',{'runs':rows,'scope':'Separate follow-up arm: default within-query remote cache enabled, fresh process every execution; same source/filter/settings/output and independent PyArrow reference as disabled-cache arm.'})
