"""Per-flow OS counter cross-check, observed from before any S3 request."""
import csv,subprocess,os,time,threading,json,hashlib,signal
import run_spike as probe
S=probe.S;mode='s3_full';peaks={};process_peaks=[];raw=S/'nettop-full-continuous.csv';fp=raw.open('w');nt=subprocess.Popen(['nettop','-n','-m','tcp','-p',str(os.getpid()),'-L','0','-s','1','-J','bytes_in,bytes_out','-x'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1)
def capture():
 for line in nt.stdout:
  fp.write(line);fp.flush()
  try:
   row=next(csv.reader([line]));key=row[0].strip()
   if len(row)<3 or not row[1].isdigit():continue
   if key.startswith(('tcp4','tcp6')):peaks[key]=max(peaks.get(key,0),int(row[1]))
   elif key.endswith('.'+str(os.getpid())):process_peaks.append(int(row[1]))
  except (ValueError,IndexError):pass
thread=threading.Thread(target=capture,daemon=True);thread.start();time.sleep(1.1);original=probe.connection;diagnostics={}
class Wrapper:
 def __init__(self,c):self.c=c
 def __getattr__(self,k):return getattr(self.c,k)
 def close(self):
  time.sleep(1.2);self.c.close()
def connection(profile=None):
 c=original(profile);c.execute("SET max_temp_directory_size='4GB'");diagnostics['selected_secret']=c.execute("SELECT name FROM which_secret('s3://openalex/data/parquet/works/test','s3')").fetchall();diagnostics['secret_metadata']=c.execute('SELECT name,provider,persistent FROM duckdb_secrets()').fetchall();return Wrapper(c)
probe.connection=connection;timer=threading.Timer(240,lambda:os._exit(124));timer.daemon=True;timer.start()
try:probe.child(mode,5)
finally:
 nt.send_signal(signal.SIGINT)
 try:nt.wait(timeout=5)
 except subprocess.TimeoutExpired:nt.kill();nt.wait()
 thread.join(timeout=5);fp.close();timer.cancel()
z=json.loads((S/'s3_full-5.json').read_text());diagnostics.update({'os_unique_flow_peak_bytes_in':sum(peaks.values()),'os_process_peak_bytes_in':max(process_peaks,default=0),'os_process_last_bytes_in':process_peaks[-1] if process_peaks else None,'flow_count':len(peaks),'successful_get_payload_bytes':z['s3_successful_get_payload_bytes'],'per_flow_peak_bytes_by_hash':{hashlib.sha256(k.encode()).hexdigest():v for k,v in peaks.items()},'scope':'Continuous nettop snapshots at1s per flow, starting before S3 access. Max counters retain flows that later close; snapshots can still miss short-lived flows; OS bytes include protocol overhead. Raw connection addresses stay local.'});diagnostics['os_flow_to_http_payload_ratio']=sum(peaks.values())/z['s3_successful_get_payload_bytes'];probe.dump('network-continuous-summary.json',diagnostics);print(json.dumps(diagnostics,indent=2),flush=True)
qa=probe.value_hash(z['output_file']);ref=probe.value_hash(S/'raw.parquet',raw=True);assert qa==ref
