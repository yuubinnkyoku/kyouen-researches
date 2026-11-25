#!/usr/bin/env python3
"""verify_witness.py — exact-integer verifier for maximal safe sets on the n x n
standard kyouen board (q = 4 rule: forbidden = 4 stones on a common circle or line).

Semantics (independent of any quartet catalogue):
  safe:      no 4-subset of stones is collinear or cocircular
             (equivalently the 4x4 determinant |x^2+y^2 x y 1| (4 rows) != 0
              for every 4-subset: det == 0 <=> (all 4 collinear) or (cocircular))
  maximal:   every empty cell p is attacked: some 3-subset T of stones with
             T + {p} on a common circle or line (same determinant test).

Output: JSON with full empty-point certificates (attacking stone triple + canonically
reduced integer curve coefficients), safety audit counts, and the verdict.

Usage: python3 verify_witness.py witness.json    ({"n": 12, "stones": [[x,y],...]})
"""
import json, sys
from itertools import combinations
from math import gcd

def det4(p1, p2, p3, p4):
    # |x^2+y^2  x  y  1| four rows, integral, arbitrary precision
    M = [ [ x*x + y*y, x, y, 1 ] for (x, y) in (p1, p2, p3, p4) ]
    total = 0
    for perm in __import__('itertools').permutations(range(4)):
        sgn = 1
        # parity of perm
        inv = sum(1 for i in range(4) for j in range(i+1, 4) if perm[i] > perm[j])
        sgn = -1 if inv % 2 else 1
        prod = 1
        for i in range(4):
            prod *= M[i][perm[i]]
        total += sgn * prod
    return total

def det3(p1, p2, p3):
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    return x1*(y2-y3) - y1*(x2-x3) + (x2*y3 - x3*y2)

def canon_circle(p1, p2, p3):
    # circle through 3 non-collinear points: x^2+y^2 + D x + E y + F = 0
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    s1, s2, s3 = x1*x1+y1*y1, x2*x2+y2*y2, x3*x3+y3*y3
    det = x1*(y2-y3) - y1*(x2-x3) + (x2*y3 - x3*y2)
    if det == 0:
        return None
    D = -(s1*(y2-y3) - y1*(s2-s3) + (s2*y3 - s3*y2))
    E = -(x1*(s2-s3) - s1*(x2-x3) + (x2*s3 - x3*s2))
    F = -(x1*(y2*s3 - y3*s2) - y1*(x2*s3 - x3*s2) + s1*(x2*y3 - x3*y2))
    g = gcd(gcd(abs(D), abs(E)), gcd(abs(F), abs(det)))
    D, E, F, det = D//g, E//g, F//g, det//g
    if det < 0:
        D, E, F, det = -D, -E, -F, -det
    return (D, E, F, det)

def canon_line(p1, p2):
    # canonical line through 2 points: ax + by + c = 0, gcd(a,b,c)=1, sign-normalized
    (x1, y1), (x2, y2) = p1, p2
    a = y2 - y1
    b = x1 - x2
    c = -(a*x1 + b*y1)
    g = gcd(gcd(abs(a), abs(b)), abs(c))
    if g:
        a, b, c = a//g, b//g, c//g
    # sign: first nonzero positive
    for v in (a, b, c):
        if v:
            if v < 0:
                a, b, c = -a, -b, -c
            break
    return (a, b, c)

def main():
    wit = json.load(open(sys.argv[1]))
    n, stones = wit["n"], [tuple(s) for s in wit["stones"]]
    k = len(stones)
    cells = [(x, y) for y in range(n) for x in range(n)]
    S = set(stones)
    assert len(S) == k, "duplicate stones"
    def in_bounds(p): return 0 <= p[0] < n and 0 <= p[1] < n
    for p in stones:
        assert in_bounds(p), f"stone out of bounds: {p}"
    # safety: every 4-subset of stones must have det != 0
    viol = []
    min_abs = None
    for comb in combinations(stones, 4):
        d = det4(*comb)
        if d == 0:
            viol.append([list(c) for c in comb])
        else:
            if min_abs is None or abs(d) < min_abs:
                min_abs = abs(d)
    # maximality: every empty cell attacked by some stone triple
    uncovered = []
    certs = []
    three_stone_lines = []
    for comb in combinations(stones, 3):
        if det3(*comb) == 0:
            three_stone_lines.append(canon_line(comb[0], comb[1]))
    for p in cells:
        if p in S:
            continue
        att = None
        for comb in combinations(stones, 3):
            if det4(p, *comb) == 0:
                if det3(*comb) == 0:
                    curve = ("line", canon_line(comb[0], comb[1]))
                else:
                    curve = ("circle", canon_circle(*comb))
                att = (comb, curve)
                break
        if att is None:
            uncovered.append(list(p))
        else:
            certs.append({
                "point": list(p),
                "triple": [list(c) for c in att[0]],
                "curve_type": att[1][0],
                "curve": list(att[1][1]),
            })
    ok = (not viol) and (not uncovered)
    out = {
        "n": n, "k": k,
        "checked_safe_quadruples": len(list(combinations(stones, 4))),
        "violating_quadruples": viol,
        "empty_points": n*n - k,
        "blocked_empty_points": len(certs),
        "uncovered_points": uncovered,
        "min_abs_nonzero_determinant": min_abs,
        "three_stone_lines": three_stone_lines,
        "certificates": certs,
        "verdict": "SAFE+MAXIMAL" if ok else "NOT-MAXIMAL-SAFE",
    }
    print(json.dumps(out, indent=1))
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
