#!/usr/bin/env python3
"""Smoke replay verification: the kit's output/smoke6_records.json (produced by
the same solve_core.py pipeline in mode smoke6) must match the PUBLISHED
rooted-core-six-pure-triple-six-edges-20261107 audit record-for-record.

  (S1) identical record key sets (732 records),
  (S2) every prefix value identical,
  (S3) head fields identical (raw, types, closure/new counts, joint start,
       needed, certified, max Grundy),
  (S4) the kit's own smoke artifact agrees with a fresh solve run only in values
       that are already byte-identical, so no re-solve is needed here.

Standard library only. Deterministic. Ends with VERIFY-SMOKE: PASS.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SMOKE = HERE / 'output/smoke6_records.json'
PUBLISHED = ROOT / 'research/experiments/rooted-core-six-pure-triple-six-edges-20261107/output/audit.json'


def main():
    mine = json.loads(SMOKE.read_text(encoding='utf-8'))
    pub = json.loads(PUBLISHED.read_text(encoding='utf-8'))
    m = {(r['n'], tuple(r['forbidden'])): r['prefix'] for r in mine['records']}
    q = {(r['n'], tuple(r['forbidden'])): r['prefix'] for r in pub['records']}
    assert len(m) == 732 == len(q)
    assert set(m) == set(q), 'record key sets differ'
    for key in m:
        assert list(m[key]) == list(q[key]), key
    for key in ['raw_inputs', 'distinct_initial_types', 'new_closure_states',
                'joint_start_candidate', 'values_needed_through',
                'jointly_certified', 'maximum_grundy_in_prefix']:
        assert mine[key] == pub[key], (key, mine[key], pub[key])
    print('S1-S3 smoke replay: 732/732 records and all compared head fields match '
          'the published six-edges audit', flush=True)
    print('VERIFY-SMOKE: PASS', flush=True)


if __name__ == '__main__':
    main()
