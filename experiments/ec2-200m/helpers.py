from pathlib import Path
import json,time,threading,subprocess,hashlib,shutil,psutil,psycopg,duckdb
HERE=Path(__file__).resolve().parent
NAME='oa200-pg'
def dump(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);q=p.with_suffix(p.suffix+'.new');q.write_text(json.dumps(v,indent=2,default=str)+'\n');q.replace(p)
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  while b:=f.read(8<<20):h.update(b)
 return h.hexdigest()
def run(args,**kw):return subprocess.run(args,check=True,capture_output=True,text=True,**kw)
def docker(*args,**kw):return run(['docker',*args],**kw)
def guard():
 if shutil.disk_usage(HERE).free<80*2**30:raise RuntimeError('Dedicated EBS free below 80 GiB phase preflight reserve')
def connect():return psycopg.connect(host='127.0.0.1',port=15432,dbname='openalex',user='openalex',password=(HERE/'secrets/password').read_text(),autocommit=True,options='-c statement_timeout=300000 -c track_io_timing=on')
def cg():
 info=json.loads(docker('inspect',NAME).stdout)[0];pid=info['State']['Pid'];assert pid>0
 rel=next(x.split(':',2)[2] for x in Path(f'/proc/{pid}/cgroup').read_text().splitlines() if x.startswith('0::'))
 base=Path('/sys/fs/cgroup')/rel.lstrip('/')
 def pairs(name):return {a:int(b) for a,b in (line.split() for line in (base/name).read_text().splitlines())}
 out={'at':time.monotonic(),'wall_at':time.time(),'cpu':pairs('cpu.stat'),'memory_current':int((base/'memory.current').read_text()),'memory':pairs('memory.stat'),'memory_events':pairs('memory.events'),'io':{},'pressure':{},'host_io':{k:v._asdict() for k,v in psutil.disk_io_counters(perdisk=True).items() if k.startswith('nvme')},'disk_free':shutil.disk_usage(HERE).free}
 for line in (base/'io.stat').read_text().splitlines():
  a,*bs=line.split();out['io'][a]={k:int(v) for k,v in (b.split('=') for b in bs)}
 out['pressure']['io']=(base/'io.pressure').read_text();out['pressure']['memory']=(base/'memory.pressure').read_text()
 return out
class Monitor:
 def __init__(self):self.samples=[];self.event=threading.Event()
 def sample(self):
  try:return cg()
  except Exception as e:return {'at':time.monotonic(),'error':str(e)}
 def start(self):
  self.samples=[self.sample()];self.thread=threading.Thread(target=self.loop,daemon=True);self.thread.start();return self
 def loop(self):
  while not self.event.wait(.5):self.samples.append(self.sample())
 def stop(self):self.event.set();self.thread.join();self.samples.append(self.sample());return self.samples

def summary(xs):
 good=[x for x in xs if 'cpu' in x]
 if not good:return {'error':'no valid cgroup samples','sample_count':len(xs)}
 a,b=good[0],good[-1];dt=b['at']-a['at'];cpu=(b['cpu']['usage_usec']-a['cpu']['usage_usec'])/1e6
 ios={k:sum(x.get(k,0) for x in b['io'].values())-sum(x.get(k,0) for x in a['io'].values()) for k in ['rbytes','wbytes','rios','wios']}
 return {'window_seconds':dt,'cpu_seconds':cpu,'average_busy_cores':cpu/dt if dt else None,'memory_current_peak_bytes':max(x['memory_current'] for x in good),'memory_anon_peak_bytes':max(x['memory'].get('anon',0) for x in good),'memory_file_peak_bytes':max(x['memory'].get('file',0) for x in good),'memory_shmem_peak_bytes':max(x['memory'].get('shmem',0) for x in good),'io_delta':ios,'average_io_mib_s':{k:ios[k]/dt/2**20 if dt else None for k in ['rbytes','wbytes']},'memory_events_delta':{k:b['memory_events'][k]-a['memory_events'].get(k,0) for k in b['memory_events']},'samples':len(good),'scope':'Dedicated native Linux container cgroup client window; memory includes file cache; shmem overlaps file; short graph queries have coarse attribution; disk counters include load/background activity in this window.'}

def duck(memory='12GB'):
 (HERE/'duckdbhome').mkdir(exist_ok=True);d=duckdb.connect();d.execute('SET home_directory=?',[str(HERE/'duckdbhome')]);d.execute('SET memory_limit=?',[memory]);d.execute('SET threads=16');d.execute('SET temp_directory=?',[str(HERE/'temp')]);return d

def background_guard():
 while True:
  if shutil.disk_usage(HERE).free<40*2**30:
   dump(HERE/'results/disk-guard.json',{'at':time.time(),'free':shutil.disk_usage(HERE).free,'action':'Stop only own engine containers'})
   for name in ['oa200-pg','oa200-ch']:subprocess.run(['docker','stop','-t','10',name],capture_output=True)
   return
  time.sleep(2)
