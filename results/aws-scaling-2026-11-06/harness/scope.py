"""Pure identity checks shared by controller and EC2, before any disk operation."""
import hashlib
import json
import re

ROWS={'stage2_small':2002982,'stage2_medium':10109733,'stage2_large':31885241}
ENTITY_ROWS={'authors': 119129660, 'concepts': 65026, 'continents': 7, 'countries': 247, 'domains': 4, 'fields': 26, 'funders': 45640, 'institution-types': 8, 'institutions': 127784, 'keywords': 65004, 'languages': 179, 'licenses': 10, 'publishers': 10703, 'sdgs': 17, 'source-types': 6, 'sources': 283287, 'subfields': 252, 'topics': 4516, 'work-types': 19, 'works': 31885241}
ENTITY_BYTES={'authors': 52769910496, 'concepts': 10309811, 'continents': 16552, 'countries': 107042, 'domains': 9079, 'fields': 19238, 'funders': 11920211, 'institution-types': 3626, 'institutions': 95649205, 'keywords': 3711973, 'languages': 123126, 'licenses': 10637, 'publishers': 3703704, 'sdgs': 9649, 'source-types': 3522, 'sources': 170336587, 'subfields': 174417, 'topics': 2589362, 'work-types': 8840, 'works': 45233146344}


def validate_scope(config,files=None):
    files=config['files'] if files is None else files
    if len(files)!=2771 or sum(f['bytes'] for f in files)!=98301763421:
        raise ValueError('Approved input union differs')
    indexed={}
    names=set()
    for f in files:
        name=hashlib.sha256(f['original_url'].encode()).hexdigest()+'.parquet'
        if not re.fullmatch('[a-z-]+',f['entity']) or not f['original_url'].startswith('s3://openalex/data/parquet/'+f['entity']+'/'):
            raise ValueError('Unrecognized source entity or URL')
        if 'source_key' in f and f['original_url']!='s3://openalex/'+f['source_key']:
            raise ValueError('Version source key does not match approved URL')
        if f['key']!='raw/'+name or f['key'] in indexed or name in names:
            raise ValueError('Duplicate or invalid source identity')
        if f['bytes']<=0 or f['rows']<=0 or not re.fullmatch('[0-9a-f]{64}',f['sha256']):
            raise ValueError('Invalid file size, rows or hash')
        indexed[f['key']]=f;names.add(name)
    if {f['entity'] for f in files}!=set(ENTITY_ROWS):
        raise ValueError('Entity coverage differs')
    for entity,expected in ENTITY_ROWS.items():
        if sum(f['rows'] for f in files if f['entity']==entity)!=expected:
            raise ValueError('Complete entity row scope differs: '+entity)
        if sum(f['bytes'] for f in files if f['entity']==entity)!=ENTITY_BYTES[entity]:
            raise ValueError('Complete entity byte scope differs: '+entity)
    if set(config['tiers'])!=set(ROWS):
        raise ValueError('Unexpected tiers')
    support={k for k,f in indexed.items() if f['entity']!='works'}
    previous=set()
    for tier,expected in ROWS.items():
        t=config['tiers'][tier]; keys=set(t['keys'])
        if len(keys)!=len(t['keys']) or not keys<=indexed.keys() or not previous<=keys or not support<=keys:
            raise ValueError('Tier nesting, uniqueness or complete dimensions differ')
        rows=sum(indexed[k]['rows'] for k in keys if indexed[k]['entity']=='works')
        if rows!=expected or t['work_rows']!=expected or t['bytes']!=sum(indexed[k]['bytes'] for k in keys):
            raise ValueError('Tier volume differs')
        previous=keys
    if previous!=set(indexed):
        raise ValueError('Largest tier does not cover complete union')
    return indexed


def manifest_identity(config):
    fields=('key','entity','original_url','bytes','rows','sha256')
    records=[{k:f[k] for k in fields} for f in sorted(config['files'],key=lambda f:f['key'])]
    return hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest()
