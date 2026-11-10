"""Protect40GiBhostreserve, stoponlythenewlabelledCHbenchmarkcontainerifneeded."""
import json,shutil,subprocess,time,psutil
from pathlib import Path
from pg_helpers import HERE,dump
NAME='openalex-ch100-bench-20261109'
while True:
 if not psutil.pid_exists(80997):
  break
 r=subprocess.run(['docker','inspect',NAME],capture_output=True,text=True)
 if r.returncode:time.sleep(2);continue
 c=json.loads(r.stdout)[0];assert c['Config']['Labels'].get('openalex.study')=='postgres-100m-20261109'
 if not c['State']['Running']:break
 free=shutil.disk_usage(HERE).free
 if free<40*(1<<30):
  event={'at':time.time(),'free_bytes':free,'reserve_bytes':40*(1<<30),'action':'StoponlyownedlabelledCHbenchmarkcontainer','container':NAME};dump(HERE/'results/ch-disk-reserve-stop.json',event)
  stopped=subprocess.run(['docker','stop','-t','5',NAME],capture_output=True,text=True);event['stop_exit']=stopped.returncode;dump(HERE/'results/ch-disk-reserve-stop.json',event);break
 time.sleep(2)
