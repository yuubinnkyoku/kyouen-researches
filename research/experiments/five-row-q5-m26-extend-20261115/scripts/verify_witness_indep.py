#!/usr/bin/env python3
# Independent census-free verifier for deficient maximal safe configurations.
# Pure integer/Fraction geometry: no solver, no census table, no JS reuse.
# Checks: (1) row capacity (<= q-1 per row), (2) safety: no q stones on a line or circle,
# (3) maximality: every empty cell completes a line or circle with q-1 existing stones.
import sys, json
from fractions import Fraction
from itertools import combinations

def collinear(pts):
    if len(pts) < 3: return True
    (x0,y0),(x1,y1) = pts[0], pts[1]
    for (x,y) in pts[2:]:
        if (x1-x0)*(y-y0) != (y1-y0)*(x-x0): return False
    return True

def on_circle(pts):
    n = len(pts)
    for tri in combinations(range(n), 3):
        a, b, c = (pts[tri[0]], pts[tri[1]], pts[tri[2]])
        if collinear([a,b,c]): continue
        ax, ay = a; bx, by = b; cx, cy = c
        d = 2*(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))
        if d == 0: continue
        ux = ((ax*ax+ay*ay)*(by-cy) + (bx*bx+by*by)*(cy-ay) + (cx*cx+cy*cy)*(ay-by)) / d
        uy = ((ax*ax+ay*ay)*(cx-bx) + (bx*bx+by*by)*(ax-cx) + (cx*cx+cy*cy)*(bx-ax)) / d
        r2 = (ax-ux)**2 + (ay-uy)**2
        if all((x-ux)**2 + (y-uy)**2 == r2 for (x,y) in pts): return True
    return False

def forbidden(pts, q):
    return len(pts) >= q and (collinear(list(pts)) or on_circle(list(pts)))

def main():
    w, m, q = map(int, sys.argv[1:4])
    stones = [tuple(s) for s in json.load(open(sys.argv[4]))]
    cells = [(x,y) for y in range(w) for x in range(m)]
    st = set(stones)
    rows = [0]*w
    for (x,y) in stones:
        assert 0 <= x < m and 0 <= y < w, f"stone out of board {x},{y}"
        rows[y] += 1
    assert len(st) == len(stones), "duplicate stones"
    assert all(r <= q-1 for r in rows), f"row capacity violated {rows}"
    for comb in combinations(stones, q):
        if forbidden(list(comb), q):
            print(f"UNSAFE: q-subset on curve: {comb}"); return 2
    blocked = 0
    for c in cells:
        if c in st: continue
        others = [s for s in stones if s != c]
        ok = False
        for comb in combinations(others, q-1):
            if forbidden(list(comb) + [c], q): ok = True; break
        if not ok:
            print(f"NOT MAXIMAL: cell {c} can be added safely"); return 3
        blocked += 1
    print(json.dumps({"ok": True, "size": len(stones), "rows": rows,
                     "empty_blocked": blocked, "cells": w*m, "full": w*(q-1),
                     "deficient": len(stones) < w*(q-1)}))
    return 0

if __name__ == "__main__":
    sys.exit(main())
