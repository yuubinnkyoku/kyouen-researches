#!/usr/bin/env python3
"""verify3.py — independent third-system witness verifier (subset-based, no census,
no candidate-curve enumeration from pairs/triples of stones; different algorithm from
sat.js verifyConfig and verify_witness.py).

Usage: verify3.py w m q < stones.json   (JSON: [[x,y],...])

Checks, exact integer arithmetic only:
  (1) safety: no q-subset of the stones is collinear or concyclic
      (a curve with >= q stones exists iff some q-subset lies on one line/circle);
  (2) maximality: for every empty cell p there is a (q-1)-subset T of stones
      with T + {p} collinear or concyclic (early exit at first blocking subset);
  (3) row deficiency: some row has <= q-2 stones.

Prints JSON {pass, n, rows, min_row, safe, maximal, row_deficient}; exit 0 iff pass.
"""
import json, sys
from itertools import combinations


def collinear(pts):
    for i in range(2, len(pts)):
        (x0, y0), (x1, y1), (xi, yi) = pts[0], pts[1], pts[i]
        if (x1 - x0) * (yi - y0) - (y1 - y0) * (xi - x0) != 0:
            return False
    return True


def concyclic(pts):
    # find a non-collinear triple, build its circle (D,E,F) in x^2+y^2+Dx+Ey+F=0
    # scaled by det; then check all remaining points.
    base = None
    for i in range(len(pts) - 2):
        tri = (pts[i], pts[i + 1], pts[i + 2])
        (x0, y0), (x1, y1), (x2, y2) = tri
        det = (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)
        if det != 0:
            base = tri
            break
    if base is None:
        return False  # all collinear handled separately
    (x0, y0), (x1, y1), (x2, y2) = base
    s0, s1, s2 = x0 * x0 + y0 * y0, x1 * x1 + y1 * y1, x2 * x2 + y2 * y2
    # solve x^2+y^2+Dx+Ey+F=0 through the triple; scale rows by det to stay integral
    M = [((x1 - x0), (y1 - y0), (s1 - s0)),
         ((x2 - x0), (y2 - y0), (s2 - s0))]
    det2 = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    if det2 == 0:
        return False
    # D, E, F as rationals with common denominator det2; use cross-multiplied test
    # D = -( (s1-s0)(y2-y0) - (y1-y0)(s2-s0) ) / det2, similarly E
    Dn = -((s1 - s0) * (y2 - y0) - (y1 - y0) * (s2 - s0))
    En = -((x1 - x0) * (s2 - s0) - (s1 - s0) * (x2 - x0))
    # F = -(s0 + D*x0 + E*y0) with denominator det2
    Fn = -(s0 * det2 + Dn * x0 + En * y0)
    for (x, y) in pts:
        if x * x * det2 + y * y * det2 + Dn * x + En * y + Fn != 0:
            return False
    return True


def on_common_curve(pts):
    return collinear(pts) or concyclic(pts)


def main():
    w, m, q = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    stones = [tuple(p) for p in json.load(sys.stdin)]
    n = len(stones)
    out = {"pass": False, "n": n, "rows": None, "min_row": None,
           "safe": None, "maximal": None, "row_deficient": None}
    assert len(set(stones)) == n
    S = set(stones)
    assert all(0 <= x < m and 0 <= y < w for x, y in stones)

    # (1) safety
    safe = True
    for sub in combinations(stones, q):
        if on_common_curve(sub):
            safe = False
            out["unsafe_subset"] = sub
            break

    # (2) maximality (subset-based, early exit)
    maximal = True
    uncovered = None
    if safe:
        for y in range(w):
            for x in range(m):
                if (x, y) in S:
                    continue
                blocked = False
                for sub in combinations(stones, q - 1):
                    if on_common_curve(sub + ((x, y),)):
                        blocked = True
                        break
                if not blocked:
                    maximal = False
                    uncovered = (x, y)
                    break

    # (3) row deficiency
    rows = [0] * w
    for _, y in stones:
        rows[y] += 1
    min_row = min(rows)
    row_def = min_row <= q - 2

    out["rows"] = rows
    out["min_row"] = min_row
    out["safe"] = safe
    out["maximal"] = maximal
    out["row_deficient"] = row_def
    if not maximal:
        out["uncovered"] = uncovered
    capacity_mode = len(sys.argv) > 4 and sys.argv[4] == "--capacity"
    if capacity_mode:
        out["mode"] = "capacity"
        out["capacity"] = bool(n == (q - 1) * w and min_row == q - 1)
        out["pass"] = bool(safe and maximal and out["capacity"])
    else:
        out["pass"] = bool(safe and maximal and row_def)
    print(json.dumps(out))
    sys.exit(0 if out["pass"] else 1)


main()
