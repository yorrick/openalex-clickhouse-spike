import json,subprocess,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
p=HERE/'results/postgres/memory-events.jsonl'
with p.open('a') as f:
 while True:
  r=subprocess.run(['docker','exec','openalex-pg-bench-20261108','sh','-c','cat /sys/fs/cgroup/memory.events; echo PEAK; cat /sys/fs/cgroup/memory.peak; echo CURRENT; cat /sys/fs/cgroup/memory.current'],capture_output=True,text=True)
  f.write(json.dumps({'at':time.time(),'exit':r.returncode,'raw':r.stdout,'error':r.stderr[:200]})+'\n');f.flush()
  if r.returncode:break
  time.sleep(2)
