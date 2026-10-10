"""Prevent withdrawn cache ancestry from silently re-entering a current union.

Raw exact replays are evaluated separately; this filter only applies to cache
rows. Rehabilitation requires explicit, hash-bound proof and registry update.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
REGISTRY=ROOT/'results/n11-s5-evidence-quarantine.json'

def quarantined_cache_keys():
    doc=json.loads(REGISTRY.read_text(encoding='utf-8'))
    if doc.get('schema')!='n11-s5-evidence-quarantine-v1':
        raise ValueError('invalid S5 quarantine registry')
    return {tuple(r['key']) for r in doc['entries'] if r['active']}
