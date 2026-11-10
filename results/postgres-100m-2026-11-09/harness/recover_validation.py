"""VerifycommittedcitationCOPYwithmaintenance deadline; no replay or inferrednativeCOPYtime."""
import json,time
from pg_helpers import HERE,connect,dump,Monitor
from benchmark_helpers import summarize_monitor
FOLDER=HERE/'results/postgres'
def main():
 proof=json.loads((HERE/'results/project-citation_edge.json').read_text());old=json.loads((FOLDER/'load-citation_edge-first-attempt.json').read_text());assert old['state']=='failed'
 xs=json.loads((FOLDER/'load-citation_edge-telemetry-first-attempt.json').read_text())
 assert xs[-1]['at']-xs[-2]['at']>290,'Expectedfinalsampleafterfailedcount,previoussampleafterCOPY'
 copy_samples=xs[:-1];dump(FOLDER/'citation-copy-only-telemetry.json',copy_samples)
 with connect() as pg:
  pg.execute("SET statement_timeout='30min'");m=Monitor().start();st=time.monotonic()
  try:n=pg.execute('SELECT count(*) FROM citation_edge').fetchone()[0]
  finally:count_samples=m.stop();dump(FOLDER/'citation-recovered-count-telemetry.json',count_samples)
  elapsed=time.monotonic()-st;assert n==proof['rows'],(n,proof['rows'])
  heap=pg.execute("SELECT pg_relation_size('citation_edge')").fetchone()[0]
 result={**old,'state':'complete','rows':n,'heap_bytes':heap,'seconds':None,'copy_elapsed_seconds_unavailable':True,'copy_monitor_window_seconds':copy_samples[-1]['at']-copy_samples[0]['at'],'resources':summarize_monitor(copy_samples),'validation_recovered_after_300s_timeout':True,'validation_seconds':elapsed,'validation_resources':summarize_monitor(count_samples),'input_sha256':proof['sha256'],'no_copy_replayed':True}
 dump(FOLDER/'load-citation_edge.json',result);print('Recoveredcitationcount',n,elapsed,'s; noCOPYreplayed',flush=True)
if __name__=='__main__':main()
