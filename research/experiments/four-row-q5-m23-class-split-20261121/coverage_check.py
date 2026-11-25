#!/usr/bin/env python3
"""Coverage audit for the (4,23,5) class-split sweep (m=23 lane, declaration d92c8f51).

Parses output/records.jsonl and audits the complete-cover decomposition of the
row-deficient maximal safe configuration space on 4x23 (q=5):

- 9 canonical deficiency classes mod row mirror V (0<->3, 1<->2):
  singletons {0},{1} (exact count k in 0..3; k>=1 split by minpos p in 0..11,
  sound H-split min(x1, 22-x_k) <= 11) and 7 multi classes run direct.
- c0k3p0/p1/p2: direct attempts skipped by design; decided by the x2 second-stone
  split alone (B in p+1..21, disjoint complete case analysis; sat4.js).

All decided instance keys must be UNSAT. Any SAT is a witness (claim switches to
the witness form). Any INDET/genfail leaves the bucket undecided.
Output JSON: per-bucket states, undecided set, and the claim string.
"""
import json, sys
from collections import defaultdict

M, PMAX = 23, 11
MULTI = ['01', '02', '03', '12', '012', '013', '0123']
X2_BY_DESIGN = {'c0k3p0', 'c0k3p1', 'c0k3p2'}

def expected_x2(bucket):
    k, p = int(bucket[3]), int(bucket[5:])
    bmax = (M - 2) if k >= 3 else (M - 1)
    return [f'{bucket}b{B}' for B in range(p + 1, bmax + 1)]

def main(path):
    recs = defaultdict(list)
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        res = r.get('kissat', {}).get('result') or ('GENFAIL' if r.get('genfail') else '?')
        recs[r['key']].append({'result': res, 'cap': r.get('cap'),
                               'conflicts': r.get('kissat', {}).get('conflicts')})
    def final(key):
        if key not in recs:
            return None
        for e in recs[key]:
            if e['result'] == 'SAT':
                return 'SAT'
        if any(e['result'] == 'UNSAT' for e in recs[key]):
            return 'UNSAT'
        if any(e['result'] == 'INDET' for e in recs[key]):
            return 'INDET'
        return 'GENFAIL' if any(e['result'] == 'GENFAIL' for e in recs[key]) else None
    coverage, undecided, sat_keys = {}, [], []
    for y in (0, 1):
        for k in range(0, 4):
            keys = [f'c{y}k0'] if k == 0 else [f'c{y}k{k}p{p}' for p in range(PMAX + 1)]
            for key in keys:
                if key in X2_BY_DESIGN:
                    subs = expected_x2(key)
                    sub_states = [final(s) for s in subs]
                    if all(s == 'UNSAT' for s in sub_states):
                        coverage[key] = f'UNSAT_BY_X2 ({len(subs)} sub-buckets all UNSAT)'
                    else:
                        miss = [s for s, st in zip(subs, sub_states) if st != 'UNSAT']
                        coverage[key] = f'x2 partial: {len(miss)}/{len(subs)} undecided'
                        undecided.extend(miss)
                    continue
                st = final(key)
                coverage[key] = st
                if st != 'UNSAT':
                    undecided.append(key)
                    if st == 'SAT':
                        sat_keys.append(key)
    for mm in MULTI:
        key = 'c' + mm
        st = final(key)
        coverage[key] = st
        if st != 'UNSAT':
            undecided.append(key)
            if st == 'SAT':
                sat_keys.append(key)
    out = {'m': M, 'records': sum(len(v) for v in recs.values()), 'keys_seen': len(recs),
           'coverage': coverage, 'undecided': undecided, 'sat_keys': sat_keys,
           'claim_complete': not undecided and not sat_keys}
    if out['claim_complete']:
        out['claim'] = ('witness-free width set {21,22,23}; '
                        'M_{4,5} = 21 or >= 25 (M=22,23,24 impossible; upper bound 140 unchanged)')
    elif sat_keys:
        out['claim'] = 'witness found at (4,23,5): M_{4,5} in [24,140] (pending witness verification)'
    else:
        out['claim'] = 'incomplete: %d buckets undecided' % len(undecided)
    print(json.dumps(out, indent=1, ensure_ascii=False))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'output/records.jsonl')
