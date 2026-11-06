"""Fail-closed, durable controls for the approved three-tier experiment."""
from pathlib import Path
import hashlib
import json
import re
import os
import fcntl

GIB = 1 << 30
CAP = 40 * GIB
RESERVATION = ((CAP + 999_999) // 1_000_000) * 1_000_000
TIERS = {'stage2_small': 100_000_000_000, 'stage2_medium': 250_000_000_000,
         'stage2_large': 650_000_000_000}
ROWS = {'stage2_small': 2_002_982, 'stage2_medium': 10_109_733,
        'stage2_large': 31_885_241}


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.writing')
    with temporary.open('w') as output:
        output.write(json.dumps(value, indent=2, default=str) + '\n')
        output.flush()
        os.fsync(output.fileno())
    temporary.replace(path)
    directory = os.open(path.parent, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0))
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


class ScanBudget:
    @classmethod
    def create(cls, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        initial = {'cap': sum(TIERS.values()), 'queries': {}, 'halted': False,
                   'tiers': {t: {'cap': cap, 'used': 0, 'reserved': 0, 'queries': 0}
                             for t, cap in TIERS.items()}}
        with path.open('x') as output:
            json.dump(initial, output)
            output.flush()
            os.fsync(output.fileno())
        return cls(path)

    def __init__(self, path):
        self.path = Path(path)
        if not self.path.exists():
            raise RuntimeError('Budget ledger missing; refusing to reset spend')
        self.lock = self.path.with_suffix('.lock').open('a')
        try:
            fcntl.flock(self.lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            self.lock.close()
            raise RuntimeError('Another budget writer is active') from exc
        self.state = json.loads(self.path.read_text())
        if self.state['cap'] != sum(TIERS.values()) or set(self.state['tiers']) != set(TIERS) or any(self.state['tiers'][t]['cap'] != cap for t, cap in TIERS.items()):
            self.close()
            raise RuntimeError('Unexpected experiment budget')

    def close(self):
        if hasattr(self, 'lock') and not self.lock.closed:
            fcntl.flock(self.lock.fileno(), fcntl.LOCK_UN)
            self.lock.close()

    def __del__(self):
        self.close()

    def reserve(self, tier, token, amount=RESERVATION):
        if self.state.get('halted'):
            raise RuntimeError('Budget is halted after an overrun')
        if token in self.state['queries'] or amount != RESERVATION:
            raise RuntimeError('Duplicate query token or invalid reservation')
        t = self.state['tiers'][tier]
        total = sum(x['used'] + x['reserved'] for x in self.state['tiers'].values())
        if t['queries'] >= 42 or t['used'] + t['reserved'] + amount > t['cap'] or total + amount > self.state['cap']:
            raise RuntimeError('Ring-fenced Athena scan budget exhausted')
        t['reserved'] += amount
        t['queries'] += 1
        self.state['queries'][token] = {'tier': tier, 'reserved': amount, 'state': 'reserved'}
        write(self.path, self.state)

    def settle(self, token, scanned):
        q = self.state['queries'][token]
        if q['state'] != 'reserved':
            raise RuntimeError('Reservation was already settled')
        actual = q['reserved'] if scanned is None else int(scanned)
        if actual < 0:
            raise RuntimeError('Invalid reported scan size')
        t = self.state['tiers'][q['tier']]
        t['reserved'] -= q['reserved']
        t['used'] += max(10_000_000, ((actual + 999_999) // 1_000_000) * 1_000_000)
        q.update(state='settled', scanned=actual, unknown_scan=scanned is None)
        overrun = actual > q['reserved'] or t['used'] > t['cap']
        if overrun:
            self.state['halted'] = True
        write(self.path, self.state)
        if overrun:
            raise RuntimeError('Athena exceeded its reservation; further work stopped')


def validate_manifest(m, objects_root):
    if m.get('sealed') is not True:
        raise ValueError('Source manifest is not sealed')
    root = Path(objects_root).resolve()
    files = m.get('files', [])
    by_key = {}
    for f in files:
        path = Path(f['local_path']).resolve()
        if not path.is_relative_to(root):
            raise ValueError('Local source is outside the approved cache')
        expected_key = 'raw/' + hashlib.sha256(f['original_url'].encode()).hexdigest() + '.parquet'
        if f['key'] != expected_key or f['key'] in by_key:
            raise ValueError('Unexpected or duplicate source key')
        if not f['original_url'].startswith(f"s3://openalex/data/parquet/{f['entity']}/"):
            raise ValueError('Unexpected original source')
        if not re.fullmatch('[0-9a-f]{64}', f['sha256']) or f['bytes'] <= 0 or f['rows'] <= 0:
            raise ValueError('Invalid source identity')
        by_key[f['key']] = f
    if len(files) != 2771 or sum(f['bytes'] for f in files) != 98_301_763_421 or m.get('bytes') != 98_301_763_421:
        raise ValueError('Input scope differs from approval')
    support = {k for k, f in by_key.items() if f['entity'] != 'works'}
    previous = set()
    for tier, n in ROWS.items():
        t = m['tiers'][tier]
        keys = set(t['keys'])
        if len(keys) != len(t['keys']) or not keys <= by_key.keys() or not support <= keys or not previous <= keys:
            raise ValueError('Tiers are not the approved nested inputs')
        works = [by_key[k] for k in keys if by_key[k]['entity'] == 'works']
        if sum(f['rows'] for f in works) != n or t['work_rows'] != n or sum(by_key[k]['bytes'] for k in keys) != t['bytes']:
            raise ValueError('Tier rows or bytes do not reconcile')
        previous = keys
    if previous != set(by_key):
        raise ValueError('The largest tier does not cover all approved input files')
    return by_key


def classify(*, cpu_fraction, io_stall_fraction, spill_bytes, io_fraction):
    if any(v is None for v in (cpu_fraction,io_stall_fraction,spill_bytes,io_fraction)):
        return 'unknown'
    io_bound = io_fraction >= .8 or io_stall_fraction >= .2
    if spill_bytes > 0 and io_bound:
        return 'mixed-memory-io'
    if io_bound:
        return 'io'
    if cpu_fraction >= .7 and io_stall_fraction < .1:
        return 'cpu'
    return 'unknown'


def outcome(seconds, *, matched, timeout=False):
    if timeout:
        return 'FAIL_LATENCY_CENSORED'
    if matched is False:
        return 'FAIL_CORRECTNESS'
    if matched is None:
        return 'INCONCLUSIVE_QA'
    if len(seconds) < 3:
        return 'INCONCLUSIVE_REPETITIONS'
    return 'PASS' if max(seconds) < 60 else 'FAIL_LATENCY'
