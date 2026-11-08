from pathlib import Path
import json,psycopg,duckdb,datetime,time,subprocess,threading
HERE=Path(__file__).resolve().parent
NAME='openalex-pg-bench-20261108'
def connect():return psycopg.connect(host='127.0.0.1',port=15432,dbname='openalex',user='openalex',password=(HERE/'secrets/password').read_text(),autocommit=True)
def dump(path,value):
 p=Path(path);tmp=p.with_suffix(p.suffix+'.new');tmp.write_text(json.dumps(value,indent=2,default=str)+'\n');tmp.replace(p)
def duck():
 d=duckdb.connect();d.execute("SET memory_limit='4GB'");d.execute('SET threads=8');d.execute("SET temp_directory=?",[str(HERE/'temp')]);d.execute('LOAD postgres');pw=(HERE/'secrets/password').read_text();d.execute('ATTACH ? AS pg (TYPE postgres)',[f'host=127.0.0.1 port=15432 dbname=openalex user=openalex password={pw}']);return d
def cg():
 cmd=['docker','exec',NAME,'sh','-c','cat /sys/fs/cgroup/cpu.stat; echo MEMORY_CURRENT; cat /sys/fs/cgroup/memory.current; echo MEMORY_STAT; cat /sys/fs/cgroup/memory.stat; echo IO_STAT; cat /sys/fs/cgroup/io.stat; echo IO_PRESSURE; cat /sys/fs/cgroup/io.pressure']
 r=subprocess.run(cmd,text=True,capture_output=True,check=True);out={'at':time.monotonic(),'raw':r.stdout};section='cpu';data={'cpu':{},'memory':{},'io':{},'pressure':{}}
 for line in r.stdout.splitlines():
  if line=='MEMORY_CURRENT':section='current';continue
  if line=='MEMORY_STAT':section='memory';continue
  if line=='IO_STAT':section='io';continue
  if line=='IO_PRESSURE':section='pressure';continue
  if section=='current':out['memory_current']=int(line);continue
  z=line.split()
  if section in ('cpu','memory') and len(z)==2:data[section][z[0]]=int(z[1])
  elif section in ('io','pressure') and z:data[section][z[0]]={k:int(v) if v.isdigit() else float(v) for k,v in (a.split('=') for a in z[1:])}
 out.update(data);return out
class Monitor:
 def __init__(self,interval=.5):self.interval=interval;self.samples=[];self.event=threading.Event();self.thread=None
 def start(self):
  self.samples=[cg()];self.thread=threading.Thread(target=self.loop,daemon=True);self.thread.start();return self
 def loop(self):
  while not self.event.wait(self.interval):
   try:self.samples.append(cg())
   except Exception as e:self.samples.append({'at':time.monotonic(),'error':type(e).__name__+':'+str(e)})
 def stop(self):self.event.set();self.thread.join();self.samples.append(cg());return self.samples
