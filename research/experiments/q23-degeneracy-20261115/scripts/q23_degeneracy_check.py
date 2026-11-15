#!/usr/bin/env python3
"""q in {2,3} complete degeneracy checker (independent pure-Python Fraction).

Theorem (K0855). In the standard integer rectangle game with the forbidden
family = {lines, circles}:
  - q=2: any 2 distinct points lie on a line;
  - q=3: any 3 distinct points are collinear (a line) or concyclic
    (the circumcircle of non-collinear triples).
Hence for q in {2,3} on any board with at least q cells:
  (1) safe(S)  iff |S| <= q-1;
  (2) maximal safe iff |S| = q-1 (every empty cell is blocked: some census
      curve through it already holds q-1 stones);
  (3) w >= 2 : every (q-1)-stone config is row-deficient (some row holds
      <= q-2 stones), so row-deficient maximal witnesses exist at EVERY
      width m >= 1: witness band [1, inf), M_{w,q} = INF (full-capacity
      stabilization never happens);
  (4) w = 1  : every maximal config is full-capacity (q-1 stones in the
      single row) at every width: M_{1,q} = 1;
  (5) Grundy: all maximal configs share one size q-1, so the normal-play
      value of any safe position is g(S) = ((q-1) - |S|) mod 2.

Machine audit (this file). For small boards the full curve census (all
lines through >= 2 board points, all circles through >= 3 board points,
exact Fractions) is built, then:
  (A) census degeneracy: every q-subset of cells lies on >= 1 census curve
      (no violating subset escapes the census — encoding soundness at q);
  (B) subset sweep: for EVERY subset S of the board,
        safe(S)  <=> |S| <= q-1, and
        maximal(S) <=> |S| = q-1;
  (C) blocked: for every (q-1)-stone S and every empty cell c, c is blocked
      in the K0853 sense (a census curve through c holding >= q-1 stones);
  (D) deficiency: w>=2 — every (q-1)-stone S has a row with <= q-2 stones;
      w=1 — no maximal S is deficient;
  (E) Grundy retrograde: mex DAG values equal ((q-1)-|S|) mod 2 on every
      safe position (boards with >= q cells).

Circles are constructed independently of prior repo checkers: circumcenter
by perpendicular-bisector intersection in exact Fractions, membership by
squared-distance equality (no determinant form, no floating point).

Usage: q23_degeneracy_check.py
Output: JSON to stdout; exit 0 iff every check passes on every board.
"""
import json, sys, itertools
from fractions import Fraction

BOARDS = [(1, 3), (1, 6), (2, 3), (2, 4), (3, 3), (3, 4), (4, 3)]
QS = [2, 3]


def cells(w, m):
    return [(x, y) for y in range(w) for x in range(m)]


def line_canon(a, b):
    (x1, y1), (x2, y2) = a, b
    A, B, C = y2 - y1, x1 - x2, x2 * y1 - x1 * y2
    if A < 0 or (A == 0 and B < 0):
        A, B, C = -A, -B, -C
    return (A, B, C)


def on_line(A, B, C, p):
    return A * p[0] + B * p[1] + C == 0


def circumcenter(p, r, s):
    """Center of the circle through 3 non-collinear points, exact Fractions."""
    (x1, y1), (x2, y2), (x3, y3) = p, r, s
    # perpendicular bisectors of p-r and p-s:
    #   2(x2-x1) u + 2(y2-y1) v = (x2^2+y2^2)-(x1^2+y1^2)   etc.
    a11, a12 = Fraction(2 * (x2 - x1)), Fraction(2 * (y2 - y1))
    a21, a22 = Fraction(2 * (x3 - x1)), Fraction(2 * (y3 - y1))
    det = a11 * a22 - a12 * a21
    if det == 0:
        return None
    f = lambda t: Fraction(t[0] * t[0] + t[1] * t[1])
    b1, b2 = f(r) - f(p), f(s) - f(p)
    u = (b1 * a22 - b2 * a12) / det
    v = (a11 * b2 - a21 * b1) / det
    return (u, v)


def build_census(cs):
    """All lines (>=2 board points) and circles (>=3 board points) as cell-
    index frozensets, deduped canonically."""
    lines = {}
    for i, j in itertools.combinations(range(len(cs)), 2):
        key = line_canon(cs[i], cs[j])
        lines.setdefault(key, set()).update((i, j))
    circles = {}
    for t in itertools.combinations(range(len(cs)), 3):
        p, r, s = cs[t[0]], cs[t[1]], cs[t[2]]
        ctr = circumcenter(p, r, s)
        if ctr is None:
            continue
        u, v = ctr
        rsq = Fraction((p[0]) ** 2 + (p[1]) ** 2) - 2 * (u * p[0] + v * p[1]) + u * u + v * v
        # squared distance from center must be rsq for member cells
        mem = [k for k, c in enumerate(cs)
               if (Fraction(c[0]) - u) ** 2 + (Fraction(c[1]) - v) ** 2 == rsq]
        if len(mem) >= 3:
            key = (u, v, rsq)
            circles.setdefault(key, set()).update(mem)
    L = [frozenset(v) for v in lines.values() if len(v) >= 2]
    C = [frozenset(v) for v in circles.values() if len(v) >= 3]
    return L, C


def main():
    report = {"boards": [], "all_pass": True}
    for (w, m) in BOARDS:
        cs = cells(w, m)
        n = len(cs)
        L, C = build_census(cs)
        curves = L + C
        row_of = [c[1] for c in cs]
        for q in QS:
            b = {"w": w, "m": m, "q": q, "n_cells": n, "n_lines": len(L),
                 "n_circles": len(C), "checks": {}}
            ok = True
            # (A) census degeneracy: every q-subset on >= 1 census curve
            bad = []
            for t in itertools.combinations(range(n), q):
                ts = frozenset(t)
                if not any(ts <= cu for cu in curves):
                    bad.append(list(t))
            b["checks"]["A_census_degeneracy"] = {"violating_subsets_missed": len(bad)}
            ok &= (bad == [])
            # (B) subset sweep: safe <=> |S|<=q-1 ; maximal <=> |S|=q-1
            bad_safe, bad_max = [], []
            nmax = 0
            for mask in range(1 << n):
                S = [i for i in range(n) if mask >> i & 1]
                k = len(S)
                ss = frozenset(S)
                violating = any(len(cu & ss) >= q for cu in curves)
                safe = not violating
                if safe != (k <= q - 1):
                    bad_safe.append(sorted(S))
                    continue
                if not safe:
                    continue
                # maximality: exists empty cell with S+c safe
                maximal = True
                for c in range(n):
                    if c in ss:
                        continue
                    s2 = ss | {c}
                    if not any(len(cu & s2) >= q for cu in curves):
                        maximal = False
                        break
                if maximal:
                    nmax += 1
                    if k != q - 1:
                        bad_max.append(sorted(S))
                elif k == q - 1:
                    bad_max.append(sorted(S))
            b["checks"]["B_subset_sweep"] = {
                "subsets_checked": 1 << n,
                "safe_class_errors": len(bad_safe),
                "maximal_class_errors": len(bad_max),
                "maximal_count": nmax,
                "expected_maximal_count": 1 if n < q - 1 else __import__("math").comb(n, q - 1),
            }
            ok &= (bad_safe == [] and bad_max == [])
            # (C) blocked census for (q-1)-stone sets (only if n >= q-1)
            badc = 0
            if n >= q - 1:
                for S in itertools.combinations(range(n), q - 1):
                    ss = frozenset(S)
                    for c in range(n):
                        if c in ss:
                            continue
                        blocked = any(c in cu and len(cu & ss) >= q - 1 for cu in curves)
                        if not blocked:
                            badc += 1
            b["checks"]["C_blocked"] = {"unblocked_cases": badc}
            ok &= (badc == 0)
            # (D) deficiency structure
            if w >= 2:
                bad_d = 0
                for S in itertools.combinations(range(n), q - 1):
                    counts = [0] * w
                    for i in S:
                        counts[row_of[i]] += 1
                    if not any(c <= q - 2 for c in counts):
                        bad_d += 1
                b["checks"]["D_deficiency"] = {
                    "mode": "w>=2: every (q-1)-set has a row <= q-2 stones",
                    "non_deficient_maximal_sets": bad_d,
                    "witnesses_at_this_width": __import__("math").comb(n, q - 1) if n >= q - 1 else 0,
                }
                ok &= (bad_d == 0)
            else:
                bad_d = 0
                for S in itertools.combinations(range(n), q - 1):
                    counts = [0] * w
                    for i in S:
                        counts[row_of[i]] += 1
                    if any(c <= q - 2 for c in counts):
                        bad_d += 1
                b["checks"]["D_deficiency"] = {
                    "mode": "w=1: no maximal set is deficient (row capacity q-1)",
                    "deficient_maximal_sets": bad_d,
                }
                ok &= (bad_d == 0)
            # (E) Grundy retrograde (only feasible for small DAGs)
            if n <= 13:
                safe_masks = []
                for mask in range(1 << n):
                    ss = frozenset(i for i in range(n) if mask >> i & 1)
                    if len(ss) <= q - 1 and not any(len(cu & ss) >= q for cu in curves):
                        safe_masks.append(mask)
                g = {}
                # memo over safe positions, moves = add one cell keeping safe
                import functools
                def grundy(mask):
                    if mask in g:
                        return g[mask]
                    ss = frozenset(i for i in range(n) if mask >> i & 1)
                    succ = set()
                    for c in range(n):
                        if mask >> c & 1:
                            continue
                        m2 = mask | (1 << c)
                        s2 = ss | {c}
                        if not any(len(cu & s2) >= q for cu in curves):
                            succ.add(grundy(m2))
                    val = 0
                    while val in succ:
                        val += 1
                    g[mask] = val
                    return val
                bad_g = 0
                formula_errs = []
                target = q - 1 if n >= q - 1 else n
                for mask in safe_masks:
                    k = bin(mask).count("1")
                    if grundy(mask) != (target - k) % 2:
                        bad_g += 1
                        formula_errs.append([k, grundy(mask)])
                b["checks"]["E_grundy"] = {
                    "safe_positions": len(safe_masks),
                    "formula_violations": bad_g,
                    "formula": "g(S) = (%d - |S|) mod 2" % target,
                }
                ok &= (bad_g == 0)
            b["pass"] = bool(ok)
            report["all_pass"] &= bool(ok)
            report["boards"].append(b)
            print(json.dumps(b), file=sys.stderr)
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["all_pass"] else 1)


if __name__ == "__main__":
    main()
