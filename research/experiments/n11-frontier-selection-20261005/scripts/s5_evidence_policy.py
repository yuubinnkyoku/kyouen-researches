"""Prevent withdrawn cache ancestry from silently re-entering a current union.

Raw exact replays are evaluated separately; this filter only applies to cache
rows. Rehabilitation requires explicit, hash-bound proof and registry update.
The registry is proof-critical: absence or corruption must fail closed.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REGISTRY = ROOT / 'results/n11-s5-evidence-quarantine.json'


def quarantined_cache_keys():
    try:
        doc = json.loads(REGISTRY.read_text(encoding='utf-8'))
    except FileNotFoundError as exc:
        raise FileNotFoundError(f'required S5 evidence quarantine registry missing: {REGISTRY}') from exc
    if doc.get('schema') != 'n11-s5-evidence-quarantine-v1':
        raise ValueError('invalid S5 quarantine registry schema')
    entries = doc.get('entries')
    if not isinstance(entries, list):
        raise ValueError('invalid S5 quarantine entries')
    seen = set()
    quarantine = set()
    for row in entries:
        if not isinstance(row, dict):
            raise ValueError('invalid S5 quarantine row')
        key = row.get('key')
        if (not isinstance(key, list) or len(key) != 2
                or any(type(x) is not int for x in key)
                or not (0 <= key[0] < 2**64 and 0 <= key[1] < 2**57)
                or key[0].bit_count() + key[1].bit_count() != 5):
            raise ValueError(f'invalid S5 quarantine key: {key}')
        pair = tuple(key)
        if pair in seen:
            raise ValueError(f'duplicate S5 quarantine key: {pair}')
        seen.add(pair)
        if type(row.get('active')) is not bool:
            raise ValueError(f'invalid S5 quarantine active flag: {pair}')
        if type(row.get('unsupported_verdict')) is not int or row['unsupported_verdict'] not in (1, 2):
            raise ValueError(f'invalid S5 quarantine verdict: {pair}')
        if row['active']:
            quarantine.add(pair)
    return quarantine
