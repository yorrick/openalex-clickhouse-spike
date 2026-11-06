"""Engine3 independent raw Parquet reference, bounded scans, typed multiset QA."""
from datetime import datetime, timedelta, timezone
from pathlib import Path
from time import monotonic, sleep
import hashlib
from collections import Counter
import json
import sys
import uuid
from urllib.parse import urlparse

import pyarrow as pa
import pyarrow.csv as pc

from cloud_job import Job, Experiment, ACCOUNT, REGION
from controls import ScanBudget, CAP, write
from source_copy import Sources
from tier_sql import PROJECTION, external_table, views, queries, canonical_rows, clickhouse_result_columns

HERE=Path(__file__).resolve().parent


class AthenaQueryIncomplete(RuntimeError):
    def __init__(self,message,record):
        super().__init__(message)
        self.record=dict(record)


class Athena(Experiment):
    def __init__(self,remote,tier,budget):
        super().__init__({})
        self.out=HERE/self.name
        self.remote=remote
        self.tier=tier
        self.budget=budget
        self.deadline=datetime.now(timezone.utc)+timedelta(hours=2)
        self.records=[]
        self.sources=Sources()
        self.sources.fresh()

    def query(self,sql,*,use_db=True):
        self.sources.fresh()
        dml=sql.lstrip().upper().startswith(('SELECT','WITH'))
        token=uuid.uuid4().hex+uuid.uuid4().hex
        ledger={'token':token,'sql':sql,'dml':dml,'state':'starting'}
        if dml:
            self.budget.reserve(self.tier,token)
        self.records.append(ledger); write(self.out/'athena-statements.json',self.records)
        args={'QueryString':sql,'WorkGroup':self.name,'ClientRequestToken':token,
              'ResultReuseConfiguration':{'ResultReuseByAgeConfiguration':{'Enabled':False}}}
        if use_db:
            args['QueryExecutionContext']={'Database':self.db,'Catalog':'AwsDataCatalog'}
        a=self.clients['athena']; started=monotonic(); scanned=None
        try:
            qid=a.start_query_execution(**args)['QueryExecutionId']
            self.running_queries.add(qid); ledger.update(id=qid,state='started')
            write(self.out/'athena-statements.json',self.records)
            cancelled=False
            while True:
                q=a.get_query_execution(QueryExecutionId=qid)['QueryExecution']
                status=q['Status']['State']
                if status in ('SUCCEEDED','FAILED','CANCELLED'):
                    break
                if monotonic()-started>300 or datetime.now(timezone.utc)>self.deadline:
                    if not cancelled:
                        a.stop_query_execution(QueryExecutionId=qid); cancelled=True
                if monotonic()-started>360:
                    raise RuntimeError('Athena cancellation unresolved, budget retains cap')
                sleep(1)
            self.running_queries.remove(qid)
            scanned=q.get('Statistics',{}).get('DataScannedInBytes')
            ledger.update(state=status,statistics=q.get('Statistics',{}),status=q['Status'],engine=q.get('EngineVersion'),client_seconds=monotonic()-started)
            write(self.out/'athena-statements.json',self.records)
            if q['WorkGroup']!=self.name or q['EngineVersion']['EffectiveEngineVersion']!='Athena engine version 3':
                raise RuntimeError('Athena isolation/engine guard failed')
            if status!='SUCCEEDED' or cancelled:
                raise AthenaQueryIncomplete('Athena query incomplete: '+json.dumps(q['Status'],default=str),ledger)
            if not dml:
                return [],ledger
            columns=[x['Name'] for x in a.get_query_results(QueryExecutionId=qid,MaxResults=1)['ResultSet']['ResultSetMetadata']['ColumnInfo']]
            location=urlparse(q['ResultConfiguration']['OutputLocation'])
            if location.netloc!=self.bucket or not location.path.startswith('/athena/'):
                raise RuntimeError('Athena result path differs')
            data=self.clients['s3'].get_object(Bucket=self.bucket,Key=location.path.lstrip('/'),ExpectedBucketOwner=ACCOUNT)['Body'].read()
            table=pc.read_csv(pa.BufferReader(data),parse_options=pc.ParseOptions(newlines_in_values=True),
                convert_options=pc.ConvertOptions(column_types={c:pa.string() for c in columns},
                 strings_can_be_null=True,quoted_strings_can_be_null=False,null_values=['']))
            if table.column_names!=columns:
                raise RuntimeError('Athena CSV headers differ from metadata')
            return table.to_pylist(),ledger
        finally:
            if dml:
                self.budget.settle(token,scanned)

    def setup(self):
        Job.create_bucket(self)
        a=self.clients['athena']
        a.create_work_group(Name=self.name,Tags=self.tags,Configuration={
            'EnforceWorkGroupConfiguration':True,'BytesScannedCutoffPerQuery':CAP,
            'EngineVersion':{'SelectedEngineVersion':'Athena engine version 3'},
            'ResultConfiguration':{'OutputLocation':f's3://{self.bucket}/athena/','ExpectedBucketOwner':ACCOUNT,
                'EncryptionConfiguration':{'EncryptionOption':'SSE_S3'}}})
        self.record(workgroup_created=True)
        got=a.get_work_group(WorkGroup=self.name)['WorkGroup']['Configuration']
        if got['BytesScannedCutoffPerQuery']!=CAP or got['EnforceWorkGroupConfiguration'] is not True:
            raise RuntimeError('Athena scan cap not enforced')
        self.query('CREATE DATABASE '+self.db,use_db=False); self.record(database_created=True)
        sentinel="SELECT CAST(NULL AS varchar) AS n,'' AS e,true AS b,CAST('9007199254740993' AS bigint) AS i,concat('a',chr(10),'b\"c') AS s,'null' AS literal"
        rows,_=self.query(sentinel)
        if rows!=[{'n':None,'e':'','b':'true','i':'9007199254740993','s':'a\nb"c','literal':'null'}]:
            raise RuntimeError('Real Athena CSV null/empty/newline/quote probe failed')
        write(self.out/'csv-probe.json',{'passed':True,'rows':rows})
        keys=set(self.remote['tiers'][self.tier]['keys'])
        selected=[f for f in self.remote['files'] if f['key'] in keys]
        for entity in PROJECTION:
            files=[f for f in selected if f['entity']==entity]
            self.clients['s3'].put_object(Bucket=self.bucket,Key=f'manifests/{entity}/files.txt',
                Body=('\n'.join(f['url'] for f in files)+'\n').encode())
            schema=pa.ipc.read_schema(pa.BufferReader((HERE/'schemas'/f'{entity}.arrow').read_bytes()))
            self.query(external_table(entity,schema,f's3://{self.bucket}/manifests/{entity}/'))
            projected=','.join('"'+name+'"' for name in PROJECTION[entity])
            sql=f'''SELECT "$path" AS path,count(*) AS n_rows,count(DISTINCT id) AS distinct_ids,
                sum(length(json_format(CAST(ROW({projected}) AS JSON)))) AS decoded_bytes
                FROM raw_{entity} GROUP BY GROUPING SETS (("$path"),())'''
            actual,_=self.query(sql)
            totals=[r for r in actual if r['path'] is None]
            if len(totals)!=1 or int(totals[0]['n_rows'])!=sum(f['rows'] for f in files):
                raise RuntimeError('Raw global row count mismatch')
            if any(int(r['n_rows'])!=int(r['distinct_ids']) or int(r['decoded_bytes'])<=0 for r in actual):
                raise RuntimeError('Raw IDs not unique or projection not decoded')
            if {r['path']:int(r['n_rows']) for r in actual if r['path'] is not None}!={f['url']:f['rows'] for f in files}:
                raise RuntimeError('Athena source path/row scope mismatch')
        for name,sql in views().items():
            self.query(f'CREATE VIEW {name} AS {sql}')
        self.record(source_probes_passed=True)

    def compare(self,cloud_path):
        cloud=json.loads((cloud_path/'summary.json').read_text())
        catalog={}
        for seed in cloud['seeds']:
            for name,sql in queries(seed).items():
                catalog[name+('-s'+str(seed) if name in ('q05','q06') else '')]=sql
        catalog={name:catalog[name] for name in cloud['timings']}
        if set(cloud['qa'])-set(catalog):
            raise RuntimeError('Unexpected CH QA query identities')
        for name in cloud['qa']:
            if not (cloud_path/(name+'-rows.json')).is_file():
                raise RuntimeError('A sealed CH QA artifact is missing: '+name)
        expected={name:canonical_rows(name[:3],clickhouse_result_columns(name[:3],json.loads((cloud_path/(name+'-rows.json')).read_text()))) for name in cloud['qa']}
        timings={name:[] for name in catalog}
        failed=set()
        for iteration in range(3):
            for name,sql in catalog.items():
                if name in failed:
                    continue
                try:
                    rows,record=self.query(sql)
                except AthenaQueryIncomplete as exc:
                    timings[name].append({'iteration':iteration,'matched':None,'state':'INCONCLUSIVE_QA','error':str(exc),'record':exc.record})
                    failed.add(name);write(self.out/'comparison.json',timings);continue
                actual=canonical_rows(name[:3],rows)
                if name in expected and actual!=expected[name]:
                    write(self.out/'mismatch.json',{'query':name,'expected_rows':len(expected[name]),'actual_rows':len(actual),'expected_sha256':hashlib.sha256('\n'.join(expected[name]).encode()).hexdigest(),'actual_sha256':hashlib.sha256('\n'.join(actual).encode()).hexdigest(),'expected_only':list((Counter(expected[name])-Counter(actual)).items())[:10],'actual_only':list((Counter(actual)-Counter(expected[name])).items())[:10]})
                    raise RuntimeError(name+' ClickHouse/Athena typed multiset mismatch')
                timings[name].append({'iteration':iteration,'statistics':record['statistics'],'id':record['id'],'rows':len(rows),'matched':True if name in expected else None,'canonical_sha256':hashlib.sha256('\n'.join(actual).encode()).hexdigest()})
                write(self.out/'comparison.json',timings)
        write(self.out/'summary.json',{'tier':self.tier,'all_matched':all(len(runs)==3 and all(r.get('matched') is True for r in runs) for runs in timings.values()),'not_compared':sorted((set(catalog)-set(expected))|failed),'missing_ch_qa':sorted(set(catalog)-set(expected)),'timings':timings,
              'billable_bytes':self.budget.state['tiers'][self.tier]['used']})
        return timings
