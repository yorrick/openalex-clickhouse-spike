"""Additional anonymous S3 observation; reconcile HTTP payload with macOS nettop."""
from pathlib import Path
import os,sys,csv,subprocess,json,threading,time
import run_spike as probe
S=probe.S

def snapshot():
    output=subprocess.check_output(['nettop','-n','-P','-L','1','-p',str(os.getpid()),'-J','bytes_in,bytes_out','-x'],text=True,timeout=10)
    values=[(int(r[1]),int(r[2])) for r in csv.reader(output.splitlines()) if r and r[0].endswith('.'+str(os.getpid()))]
    return {'bytes_in':max((x[0] for x in values),default=0),'bytes_out':max((x[1] for x in values),default=0),'raw_csv':output,'matched_process':bool(values)}

if __name__=='__main__':
    mode=sys.argv[1];timer=threading.Timer(240,lambda:os._exit(124));timer.daemon=True;timer.start();before=snapshot();original=probe.connection;receipts={}
    class Observed:
        def __init__(self,c):self.c=c
        def __getattr__(self,k):return getattr(self.c,k)
        def close(self):
            receipts['after']=snapshot();self.c.close()
    def observed_connection(profile=None):
        c=original(profile);c.execute("SET max_temp_directory_size='4GB'")
        receipts['secret_selection']=c.execute("SELECT name FROM which_secret('s3://openalex/data/parquet/works/test','s3')").fetchall()
        receipts['configured_secret_metadata']=c.execute('SELECT name,provider,persistent FROM duckdb_secrets()').fetchall()
        return Observed(c)
    probe.connection=observed_connection
    probe.child(mode,4)
    record=json.loads((S/f'{mode}-4.json').read_text());after=receipts['after'];assert after['matched_process']
    received=after['bytes_in']-before['bytes_in'];expected=record['s3_successful_get_payload_bytes'];assert received>=expected*.99,(received,expected)
    receipts.update(before=before,os_bytes_received=received,successful_get_payload_bytes=expected,os_bytes_minus_payload=received-expected,os_to_payload_ratio=received/expected,scope='Dedicated fresh process, nettop TCP/UDP per-process cumulative counters before S3 and before connection close; OS count includes protocol overhead, unlike HTTP body Content-Length sum.')
    probe.dump(f'{mode}-4-network-reconciliation.json',receipts)
    qa=probe.value_hash(record['output_file'],narrow=mode.endswith('narrow'));ref=probe.value_hash(S/'raw.parquet',narrow=mode.endswith('narrow'),raw=True);assert qa==ref
    print(json.dumps(receipts,indent=2),flush=True);timer.cancel()
