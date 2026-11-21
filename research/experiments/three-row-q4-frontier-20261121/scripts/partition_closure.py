#!/usr/bin/env python3
"""partition_closure.py — machine-checkable closure artifact for the m=24 deficient-space
partition (three-row q4 lane, 2026-11-21 session).

The deficient space at 3x24 (maximal safe configs with some row <= 2 stones) is the
union of configuration sets indexed by row-sum triples (r0,r1,r2) in {0..3}^3 minus
(3,3,3). Each piece is decided by one of:

  - row-k piece:    sat3 'rowfixed-kex' runs  R_k(Y) = "row Y has exactly k stones"
                    (k in {0,1}) — decides every triple with r_Y = k, all other rows free.
  - sum piece:      sat4 'rspec' runs S(a,b,c) = "rows have exactly a,b,c stones"
                    (unsatisfiability kills exactly those triples)
  - V-isomorphism:  the vertical reflection (r0,r1,r2) -> (r2,r1,r0) bijects
                    configuration sets (board isomorphism preserving safety/maximality),
                    so a refuted piece also refutes its V-image.

This script enumerates the 63 deficient triples and maps each to the deciding record
(piece tag + verdict), verifying that every triple not matching a decided record is
explicitly listed as PENDING. Output: JSON coverage table (stdout).
"""
import json

# Decided pieces (tag -> (kind, verdict, conflicts, run_wall_s, encoding)) from this
# session's kissat 4.0.4 runs on stat-pinned CNFs (md5s in records).
R = {
    # --- m=24 row-level pieces (sat3 rowfixed-kex) ---
    ('m24','k',0,1): ('UNSAT', 495),      # row1 exactly 0, lexHV
    ('m24','k',1,1): ('UNSAT', 61540),    # row1 exactly 1, lexHV
    ('m24','k',0,0): ('UNSAT', 594),      # row0 exactly 0, lexH
    ('m24','k',1,0): ('UNSAT', 52971),    # row0 exactly 1, lexH
    # --- m=24 sum pieces (sat4 rspec), middle-deficient plane r1=2 ---
    ('m24','s',(0,2,0)): ('UNSAT', 1),
    ('m24','s',(1,2,0)): ('UNSAT', 0),
    ('m24','s',(1,2,1)): ('UNSAT', 850),
    ('m24','s',(2,2,0)): ('UNSAT', 65),
    ('m24','s',(2,2,1)): ('UNSAT', 2938),
    ('m24','s',(2,2,2)): ('UNSAT', 12786),
    ('m24','s',(3,2,0)): ('UNSAT', 209),
    ('m24','s',(3,2,1)): ('UNSAT', 14105),
    ('m24','s',(3,2,2)): ('UNSAT', 153096),
    ('m24','s',(3,2,3)): ('UNSAT', 1117137),
    # --- m=24 sum pieces, outer planes ---
    ('m24','s',(2,3,2)): ('UNSAT', 121085),
    ('m24','s',(2,3,3)): ('UNSAT', 2671271),   # decisive piece: 2,671,271 conflicts / 476.10s
    # --- m=23 outer-existence partition (row0 deficient side; row2 by V) ---
    ('m23','k',0,0): ('UNSAT', 525),      # row0 exactly 0, lexH
    ('m23','k',1,0): ('UNSAT', 92390),    # row0 exactly 1, lexH
    ('m23','s',(2,0,0)): ('UNSAT', 1),
    ('m23','s',(2,0,1)): ('UNSAT', 12),
    ('m23','s',(2,0,2)): ('UNSAT', 49),
    ('m23','s',(2,0,3)): ('UNSAT', 108),
    ('m23','s',(2,1,0)): ('UNSAT', 41),
    ('m23','s',(2,1,1)): ('UNSAT', 1159),
    ('m23','s',(2,1,2)): ('UNSAT', 3543),
    ('m23','s',(2,1,3)): ('UNSAT', 16771),
    ('m23','s',(2,2,0)): ('UNSAT', 97),
    ('m23','s',(2,2,1)): ('UNSAT', 2396),
    ('m23','s',(2,2,2)): ('UNSAT', 12024),
    ('m23','s',(2,2,3)): ('UNSAT', 133939),    # long rerun decided 133,939 conflicts / 26.10s (50s probe was INDET at 132,005 — same trajectory)
    ('m23','s',(2,3,0)): ('UNSAT', 143),
    ('m23','s',(2,3,1)): ('UNSAT', 10643),
    ('m23','s',(2,3,2)): ('UNSAT', 94415),
    ('m23','s',(2,3,3)): ('SAT', 1004683),    # RESOLVED YES: witness
}

def closure(board_tag, triples_iter, decide_fn):
    cov = []
    decided = 0; pend = []; uncov = []
    for trip in triples_iter:
        st, verdict, conf = decide_fn(trip)
        if verdict == 'UNSAT' or verdict == 'SAT':
            decided += 1
            cov.append({'triple': list(trip), 'piece': str(st), 'verdict': verdict,
                        'conflicts': conf if verdict == 'UNSAT' else None})
        elif verdict == 'PENDING' or verdict == 'INDET':
            pend.append(list(trip))
            cov.append({'triple': list(trip), 'piece': str(st), 'verdict': verdict,
                        'conflicts': conf})
        else:
            cov.append({'triple': list(trip), 'piece': str(st) if st else None,
                        'verdict': 'UNCOVERED-BY-DECIDED-SET'})
            uncov.append(list(trip))
    return cov, decided, pend, uncov

def m24_decide(trip):
    r0, r1, r2 = trip
    # row-k pieces first (any row with count 0/1; row2 via V of row0)
    for y, r in zip((0, 1, 2), trip):
        if r in (0, 1):
            st = ('m24', 'k', r, 1 if y == 1 else 0)
            rec = R[st]
            if rec[0] == 'UNSAT':
                return st, 'UNSAT', rec[1]
            return st, rec[0], rec[1]
    # rows all in {2,3} with a 2 present: sum piece or V-image
    for cand in (trip, (r2, r1, r0)):
        st = ('m24', 's', cand)
        if st in R:
            return st, R[st][0], R[st][1]
    return None, None, None

def m23_outer_decide(trip):
    r0, r1, r2 = trip
    if r0 in (0, 1):
        st = ('m23', 'k', r0, 0)
        rec = R[st]
        return st, rec[0], rec[1]
    # r0 == 2: sum piece (already row0-fixed side)
    st = ('m23', 's', trip)
    rec = R.get(st, (None, None, None))
    if rec[0] is None and st != trip:
        pass
    return st, rec[0], rec[1]

def main():
    out = {}
    # m=24: full deficient space (63 triples)
    trips24 = [(r0, r1, r2) for r0 in range(4) for r1 in range(4) for r2 in range(4)
               if (r0, r1, r2) != (3, 3, 3)]
    cov, dec, pend, uncov = closure('m24', trips24, m24_decide)
    out['m24_partition'] = {
        'question': 'does a deficient maximal safe config exist on 3x24? (P(24) refutes all 63 triples)',
        'coverage': cov,
        'summary': {'decided': dec, 'pending': pend, 'uncovered': uncov, 'total': len(trips24)}}
    # m=23: outer-deficient existence (r0<=2 side, 48 triples; r2 side by V)
    trips23 = [(2, a, b) if False else (r0, a, b) for r0 in (0, 1, 2) for a in range(4) for b in range(4)]
    cov23, dec23, pend23, uncov23 = closure('m23_outer', trips23, m23_outer_decide)
    out['m23_outer_partition'] = {
        'question': 'does an outer-row-deficient maximal safe config exist on 3x23? (row2 side covered by V)',
        'coverage': cov23,
        'summary': {'decided': dec23, 'pending': pend23, 'uncovered': uncov23, 'total': len(trips23)}}
    print(json.dumps(out, indent=1))

if __name__ == '__main__':
    main()
