#!/usr/bin/env python3
"""m25_partition_closure.py — machine-checkable closure artifact for the m=25
deficient-space partition (three-row q4 lane, 2026-11-28 session).

Same semantics as the m=24 closure (partition_closure.py, byte-lineage):
- row-k piece:    sat3 rowfixed-kex R_k(Y) = "row Y has exactly k stones" (k in {0,1});
                  row2 covered by V-image of row0 pieces.
- sum piece:      sat4 rspec S(a,b,c) = exact row sums.
- V-isomorphism:  (r0,r1,r2) -> (r2,r1,r0) board isomorphism preserves safety/maximality.

Pieces read from a records JSON (path as argv[1], schema: list of
{"piece": "k:Y:K" | "s:a,b,c", "verdict": "UNSAT"|"SAT"|"INDET", "conflicts": int}).
Verifies every one of the 63 deficient triples is decided by a UNSAT/SAT record
or explicitly PENDING/INDET; uncovered-by-decided-set is a hard failure (exit 1).
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

def m25_decide(trip, R):
    r0, r1, r2 = trip
    # row-k pieces: any row with 0/1 stones; row2 via V of row0
    for y, r in zip((0, 1, 2), trip):
        if r in (0, 1):
            key = 'k:%d:%d' % (y if y == 1 else 0, r)
            if key not in R:
                return None, None, None
            v, c = R[key]
            return key, v, c
    # all rows in {2,3}, some 2 present: sum piece or V-image
    for cand in (trip, (r2, r1, r0)):
        key = 's:%d,%d,%d' % cand
        if key in R:
            v, c = R[key]
            return key, v, c
    return None, None, None

def main():
    R = load_records(sys.argv[1])
    trips = [(a, b, c) for a in range(4) for b in range(4) for c in range(4)
             if (a, b, c) != (3, 3, 3)]
    cov = []
    decided = 0
    pend = []
    uncov = []
    sat_found = []
    for t in trips:
        key, v, c = m25_decide(t, R)
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
        'board_tag': 'm25',
        'question': 'does a deficient maximal safe config exist on 3x25? (P(25) refutes all 63 triples)',
        'coverage': cov,
        'summary': {'decided': decided, 'pending': pend, 'uncovered': uncov,
                    'total': len(trips), 'sat_triples': sat_found},
    }
    print(json.dumps(out, indent=1))
    if uncov:
        sys.exit(1)

if __name__ == '__main__':
    main()
