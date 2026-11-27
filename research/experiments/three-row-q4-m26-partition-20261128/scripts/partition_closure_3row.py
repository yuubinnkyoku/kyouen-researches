#!/usr/bin/env python3
"""partition_closure_3row.py — machine-checkable closure artifact for the 3xM
deficient-space partition (three-row q4 lane; generalization of the m=24
partition_closure.py and m=25 m25_partition_closure.py semantics).

Pieces read from a records JSONL (path argv[1], schema: one JSON object per
line with {"piece": "k:Y:K" | "s:a,b,c", "verdict": "UNSAT"|"SAT"|"INDET",
"conflicts": int}); board tag argv[2] (default m25) is a label only.
Verifies every one of the 63 deficient triples (r0,r1,r2) in {0..3}^3 minus
(3,3,3) is decided by a UNSAT/SAT record or explicitly PENDING/INDET;
uncovered-by-decided-set is a hard failure (exit 1).
"""
import json
import sys

def load_records(path):
    recs = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            recs[r['piece']] = (r['verdict'], r.get('conflicts'))
    return recs

def decide(trip, R):
    r0, r1, r2 = trip
    for y, r in zip((0, 1, 2), trip):
        if r in (0, 1):
            key = 'k:%d:%d' % (y if y == 1 else 0, r)
            if key not in R:
                return None, None, None
            v, c = R[key]
            return key, v, c
    for cand in (trip, (r2, r1, r0)):
        key = 's:%d,%d,%d' % cand
        if key in R:
            v, c = R[key]
            return key, v, c
    return None, None, None

def main():
    R = load_records(sys.argv[1])
    tag = sys.argv[2] if len(sys.argv) > 2 else 'm25'
    trips = [(a, b, c) for a in range(4) for b in range(4) for c in range(4)
             if (a, b, c) != (3, 3, 3)]
    cov = []
    decided = 0
    pend = []
    uncov = []
    sat_found = []
    for t in trips:
        key, v, c = decide(t, R)
        if v in ('UNSAT', 'SAT'):
            decided += 1
            cov.append({'triple': list(t), 'piece': key, 'verdict': v, 'conflicts': c})
            if v == 'SAT':
                sat_found.append(list(t))
        elif v in ('PENDING', 'INDET'):
            pend.append(list(t))
            cov.append({'triple': list(t), 'piece': key, 'verdict': v, 'conflicts': c})
        else:
            uncov.append(list(t))
            cov.append({'triple': list(t), 'piece': key, 'verdict': 'UNCOVERED-BY-DECIDED-SET', 'conflicts': None})
    out = {
        'board_tag': tag,
        'question': 'does a deficient maximal safe config exist on 3x%s? (P(%s) refutes all 63 triples)'
                     % (tag.lstrip('m'), tag.lstrip('m')),
        'coverage': cov,
        'summary': {'decided': decided, 'pending': pend, 'uncovered': uncov,
                    'total': len(trips), 'sat_triples': sat_found},
    }
    print(json.dumps(out, indent=1))
    if uncov:
        sys.exit(1)

if __name__ == '__main__':
    main()
