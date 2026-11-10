"""Enforce study's40GiB diskreserve duringPGload/index/query, ownDB/driveronly."""
import json,time,shutil,signal
from pathlib import Path
import psutil
from pg_helpers import HERE,connect,dump
while True:
 proc=psutil.Process(60081) if psutil.pid_exists(60081) else None
 if proc is None or 'run_targeted_trials.py' not in ' '.join(proc.cmdline()):break
 free=shutil.disk_usage(HERE).free
 if free<40*(1<<30):
  event={'at':time.time(),'free_bytes':free,'reserve_bytes':40*(1<<30),'action':'CancelactiveclientsofthisdedicatedstudyDB,terminateonlyverifiedPGstudydriver','driver_pid':proc.pid}
  dump(HERE/'results/disk-reserve-stop.json',event)
  with connect() as pg:
   targets=pg.execute("SELECT pid,left(query,100),pg_cancel_backend(pid) FROM pg_stat_activity WHERE datname=current_database() AND pid<>pg_backend_pid() AND backend_type='client backend' AND state='active'").fetchall()
  proc.send_signal(signal.SIGTERM);event['cancelled']=targets;dump(HERE/'results/disk-reserve-stop.json',event);break
 time.sleep(2)
