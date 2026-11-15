#!/usr/bin/env python3
"""Free-column extension probe: place an existing witness on a wider board (same
stones, appended empty columns) and check safety + maximality by exact arithmetic.

Pure Fraction arithmetic, independent of repo census code. Usage:
  python3 probe_free_column.py <stones.json> <w> <h> <q> <m_lo> <m_hi>
Checks every width m in [m_lo, m_hi]; prints per-width unblocked cells.
Exit code 0 iff some width in range is fully maximal (prints the largest such m).
"""
import json, sys
from fractions import Fraction

def on_line(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]) == 0

def circum(a, b, c):
    # standard circumcenter; uy a^2 term is (cx-bx) (an early transcription of this
    # formula as (cy-by) silently produced wrong circles - self-test below guards it)
    ax, ay = a; bx, by = b; cx, cy = c
    d = 2*(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))
    if d == 0: return None
    a2, b2, c2 = ax*ax+ay*ay, bx*bx+by*by, cx*cx+cy*cy
    return (Fraction(a2*(by-cy) + b2*(cy-ay) + c2*(ay-by), d),
            Fraction(a2*(cx-bx) + b2*(ax-cx) + c2*(bx-ax), d))

def _selftest():
    # (0,0),(1,0),(0,1),(1,1) are concyclic on center (0.5,0.5) r^2=0.5
    u = circum((0,0), (1,0), (0,1))
    assert u == (Fraction(1,2), Fraction(1,2)), u
    r2 = Fraction(1,2)
    for p in [(0,0),(1,0),(0,1),(1,1)]:
        assert (Fraction(p[0])-u[0])**2 + (Fraction(p[1])-u[1])**2 == r2, p
    # negative control: (2,2) is not on that circle
    assert (Fraction(2)-u[0])**2 + (Fraction(2)-u[1])**2 != r2
    # regression for the exact transcription bug: circle through (0,2),(13,2),(12,3)
    # has center (6.5,-3.5), r^2=72.5, and passes through (1,3)
    u2 = circum((0,2), (13,2), (12,3))
    assert u2 == (Fraction(13,2), Fraction(-7,2)), u2
    assert (Fraction(1)-u2[0])**2 + (Fraction(3)-u2[1])**2 == Fraction(145,2)
    print("selftest PASS")

_selftest()

def curves_of(pts):
    n = len(pts)
    lines = {}
    for i, j in __import__('itertools').combinations(range(n), 2):
        a, b = pts[i], pts[j]
        A, B = b[1]-a[1], a[0]-b[0]
        C = -(A*a[0] + B*a[1])
        if A < 0 or (A == 0 and B < 0): A, B, C = -A, -B, -C
        lines[(A, B, C)] = None
    for key in lines:
        A, B, C = key
        lines[key] = set(p for p in pts if A*p[0] + B*p[1] + C == 0)
    circs = {}
    for i, j, k in __import__('itertools').combinations(range(n), 3):
        if on_line(pts[i], pts[j], pts[k]): continue
        u = circum(pts[i], pts[j], pts[k])
        if u is None: continue
        r2 = (Fraction(pts[i][0])-u[0])**2 + (Fraction(pts[i][1])-u[1])**2
        circs.setdefault((u[0], u[1], r2), None)
    for key in circs:
        ux, uy, r2 = key
        circs[key] = set(p for p in pts if (Fraction(p[0])-ux)**2 + (Fraction(p[1])-uy)**2 == r2)
    return lines, circs

def main():
    stones = [tuple(s) for s in json.load(open(sys.argv[1]))]
    w, h, q, m_lo, m_hi = map(int, sys.argv[2:7])
    lines, circs = curves_of(stones)
    maxline = max(len(v) for v in lines.values())
    maxcirc = max(len(v) for v in circs.values())
    print(f"stones={len(stones)} maxLine={maxline} maxCircle={maxcirc} "
          f"curves={len(lines)+len(circs)}")
    if maxline >= q or maxcirc >= q:
        print("UNSAFE"); sys.exit(2)
    best = None
    for m in range(m_lo, m_hi + 1):
        blocked = set()
        for (A, B, C), v in lines.items():
            if len(v) == q - 1:
                for x in range(m):
                    for y in range(h):
                        if A*x + B*y + C == 0: blocked.add((x, y))
        for (ux, uy, r2), v in circs.items():
            if len(v) == q - 1:
                for x in range(m):
                    for y in range(h):
                        if (Fraction(x)-ux)**2 + (Fraction(y)-uy)**2 == r2: blocked.add((x, y))
        S = set(stones)
        unb = [(x, y) for x in range(m) for y in range(h)
               if (x, y) not in S and (x, y) not in blocked]
        print(f"m={m}: empty={m*h-len(S)} blocked={len(blocked & {(x,y) for x in range(m) for y in range(h)})} unblocked={unb}")
        if not unb: best = m
    if best is not None:
        print(f"MAXIMAL_THROUGH_m={best}")
        sys.exit(0)
    sys.exit(1)

if __name__ == "__main__":
    main()
