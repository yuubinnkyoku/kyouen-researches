#!/usr/bin/env python3
"""Independent verifier for (3,m,4) deficient-maximal witnesses (system #2).
Geometry: K0318 curve_packing_fixed_width.py curve_key lift (circles + lines).
Checks: SAFE (no forbidden curve fully occupied), MAXIMAL (every empty point shares
a forbidden curve whose other q-1 points are all occupied), DEFICIENT (some row
has <= q-2 = 2 stones). Also prints the row profile and stone set."""
import sys
import json
import importlib.util
import itertools
import os

CP_CANDIDATES = [
    '/home/user/work/curve_packing_fixed_width.py',
    os.path.expanduser('~/knowledge/kyouen-research/q34-lane-kit/curve_packing_fixed_width.py'),
]


def load_cp():
    for c in CP_CANDIDATES:
        if os.path.exists(c):
            spec = importlib.util.spec_from_file_location('cp', c)
            cp = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cp)
            return cp
    raise SystemExit('curve_packing not found')


cp = load_cp()


def main():
    w, m, q = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    stones = set()
    for tok in sys.argv[4].split(','):
        x, y = map(int, tok.split(':'))
        stones.add((x, y))
    points = [(x, y) for y in range(w) for x in range(m)]
    curves = []
    seen = set()
    for tri in itertools.combinations(points, 3):
        k = cp.curve_key(tri)
        seen.add(k)
    for k in seen:
        pts = [p for p in points if cp.on_curve(k, p)]
        if len(pts) >= q:
            curves.append(pts)
    # SAFE: every forbidden curve carries at most q-1 stones
    def stons(c):
        return sum(1 for pt in c if pt in stones)
    bad = [c for c in curves if stons(c) >= q]
    safe = not bad
    # MAXIMAL: every empty point p shares a forbidden curve carrying >= q-1 stones
    nonmax = []
    for p in points:
        if p in stones:
            continue
        covered = any((p in c) and stons(c) >= q - 1 for c in curves)
        if not covered:
            nonmax.append(p)
    maximal = not nonmax
    # DEFICIENT
    rows = {}
    for (x, y) in stones:
        rows[y] = rows.get(y, 0) + 1
    deficient = any(rows.get(y, 0) <= q - 2 for y in range(w))
    print(json.dumps({
        'w': w, 'm': m, 'q': q, 'stones': len(stones),
        'safe': 1 if safe else 0, 'maximal': 1 if maximal else 0,
        'deficient': 1 if deficient else 0, 'rows': [rows.get(y, 0) for y in range(w)],
        'pass': 1 if (safe and maximal and deficient) else 0,
    }))


if __name__ == '__main__':
    main()
