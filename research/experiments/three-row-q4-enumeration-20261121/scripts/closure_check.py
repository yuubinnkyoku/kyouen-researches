#!/usr/bin/env python3
"""Closure ledger for deficient row profiles on 3 x m, q=4 (def-mode, M_{3,4} lane).

Every deficient row profile (r0,r1,r2), 0<=ri<=3, min<=2 (63 of them, excluding
the full-capacity (3,3,3)) is assigned to exactly one classification:

  family  (9): exactly two rows full; the third has a in {0,1,2} stones.
               Covered by wsearch34.js exhaustive structural search
               (validated against brute force at m=4..8, all 3 row positions).
  fast    (13): exactly one full row and the other two in {1,2}  (12 perms of
               (3,a,b)), plus (2,2,2).  Covered by dx34.js fast path
               (exhaustive circle-class enumeration; fast==direct validated
               m=4..8 vs brute, plus direct==fast at mid widths).
  lemma   (41): the rest. All have k = r0+r1+r2 <= 5, killed by the
               crossing-supply lemma (arithmetic, see below).

Crossing-supply lemma (for any def profile with k <= 5, width m):
  Maximality forces every empty cell of a DEFICIENT row (a row with <= 2
  stones) to sit on a curve carrying >= q-1 = 3 stones.
    - The row line of a deficient row carries <= 2 stones: never blocks.
    - Any non-horizontal line meets the 3-row board in <= 1 point per row, so
      through an empty cell it carries <= 2 stones: never blocks.
    - A blocking circle in a SAFE config carries exactly 3 stones (safety
      forbids 4 on a curve), and any 3 stones determine at most one circle,
      so there are at most C(k,3) blocking circles in a k-stone config.
    - A circle meets a horizontal row in <= 2 grid points, so it blocks
      <= 2 cells per deficient row.
  Hence #blockable deficient-row cells <= 2 * nDef * C(k,3), while the
  number of deficient-row cells that must be blocked is
      D(m) = sum over deficient rows of (m - ri).
  If D(m) > 2 * nDef * C(k,3), no def-maximal-safe config exists.

Classification completeness: nfull==3 is (3,3,3) (not deficient); nfull==2 is
family; nfull==1 with both other rows nonzero is fast; (2,2,2) is fast;
nfull==1 with a zero among the other rows has k <= 3+2+0 = 5; nfull==0 other
than (2,2,2) has k <= 2+2+1 = 5. So every non-family non-fast profile has
k <= 5 and is subject to the lemma.

Usage (from the experiment root):
  python3 scripts/closure_check.py check <m> [<m> ...]   per-m ledger + verdict
  python3 scripts/closure_check.py validate               m=4..12: profiles killed
      by the lemma must have zero counts in the exhaustive direct ground truth
      (consistency: the lemma never contradicts exhaustive enumeration).
"""
import os
import sys
from math import comb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def classify(r0, r1, r2):
    prof = (r0, r1, r2)
    nfull = sum(1 for r in prof if r == 3)
    if min(prof) == 3:
        return None  # (3,3,3), not deficient
    if nfull == 2:
        return 'family'
    if nfull == 1:
        others = [r for r in prof if r != 3]
        return 'fast' if others[0] >= 1 and others[1] >= 1 else 'lemma'
    return 'fast' if prof == (2, 2, 2) else 'lemma'


def ledger():
    led = {}
    for r0 in range(4):
        for r1 in range(4):
            for r2 in range(4):
                c = classify(r0, r1, r2)
                if c is not None:
                    led[(r0, r1, r2)] = c
    return led


def lemma_kill(r0, r1, r2, m):
    prof = (r0, r1, r2)
    k = r0 + r1 + r2
    nDef = sum(1 for r in prof if r <= 2)
    D = sum(m - r for r in prof if r <= 2)
    supply = 2 * nDef * comb(k, 3)
    return D > supply, D, supply


def main():
    led = ledger()
    assert len(led) == 63, f"expected 63 deficient profiles, got {len(led)}"
    from collections import Counter
    cnt = Counter(led.values())
    cmd = sys.argv[1]
    if cmd == 'check':
        for m in [int(a) for a in sys.argv[2:]]:
            bad = []
            killed = 0
            for prof, c in led.items():
                if c == 'lemma':
                    kill, D, supply = lemma_kill(*prof, m)
                    if not kill:
                        bad.append([list(prof), D, supply])
                    else:
                        killed += 1
            verdict = 'closed' if not bad else 'not_closed_by_lemma'
            print(f"""{{"m": {m}, "def_profiles": 63, "family": {cnt['family']}, "fast": {cnt['fast']}, "lemma": {cnt['lemma']}, "lemma_killed_at_m": {killed}, "lemma_not_killed": {bad if bad else 0}, "verdict": "{verdict}"}}""")
    elif cmd == 'validate':
        import json
        ok = True
        for m in range(4, 13):
            path = os.path.join(ROOT, 'output', 'selftest', f'selftest_{m}.json')
            if not os.path.exists(path):
                continue
            d = json.load(open(path))['direct']
            for prof, c in led.items():
                if c == 'lemma':
                    kill, D, supply = lemma_kill(*prof, m)
                    key = f"{prof[0]},{prof[1]},{prof[2]}"
                    real = d.get(key, 0)
                    if kill and real != 0:
                        print(f"LEMMA CONTRADICTED m={m} prof={key}: D={D} > supply={supply} but direct={real}")
                        ok = False
            print(f"m={m}: lemma-vs-direct consistency {'OK' if ok else 'FAIL'}")
        print('VALIDATE PASS' if ok else 'VALIDATE FAIL')
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
