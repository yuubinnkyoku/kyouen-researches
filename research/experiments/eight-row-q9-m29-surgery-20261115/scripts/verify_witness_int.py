#!/usr/bin/env python3
"""Fast integer-exact independent witness verifier (second implementation).

Usage: verify_witness_int.py w m q < stones.json   (JSON: [[x,y],...])

Same claim as verify_witness.py (exact, no census, no floating point):
  (1) safety: no line/circle contains >= q stones;
  (2) maximality: every empty cell lies on some line/circle with >= q-1 stones;
  (3) deficiency: some row has <= q-2 stones.
All circle/line membership tests use integer cross-multiplication only, so this is
exact. Speed comes from enumerating curves through stone pairs/triples and counting
with plain ints instead of Fraction objects.

Validation protocol (see experiment README): this verifier must reproduce
verify_witness.py's ok=True on the known band witnesses and on the py-verified
cluster sample before its results are used for any remaining witnesses.
"""
import json, sys
from math import gcd

def main():
    w, m, q = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    stones = [tuple(s) for s in json.load(sys.stdin)]
    N = len(stones)
    S = set(stones)
    assert len(S) == N
    assert all(0 <= x < m and 0 <= y < w for x, y in stones)

    # ---- rows and deficiency ----
    rows = [sum(1 for x, y in stones if y == r) for r in range(w)]
    min_row = min(rows)
    def_ok = min_row <= q - 2

    # ---- collect curves (lines and circles) with >= q-1 stones ----
    # circles through stone triples, integer key (dx, dy, dz scale trick):
    # circle through 3 points: x^2+y^2+Dx+Ey+F=0 with D,E,F rational.
    # scale by det -> integer tuple (D*, E*, F*, det), normalize by gcd and sign.
    curves = set()  # (kind, key tuple)
    stone_list = stones

    # lines through stone pairs
    for i in range(N):
        x1, y1 = stone_list[i]
        for j in range(i + 1, N):
            x2, y2 = stone_list[j]
            a, b, c = y2 - y1, x1 - x2, x2 * y1 - x1 * y2
            g = gcd(gcd(abs(a), abs(b)), abs(c)) or 1
            a //= g; b //= g; c //= g
            if a < 0 or (a == 0 and b < 0):
                a, b, c = -a, -b, -c
            curves.add(("L", (a, b, c)))

    # circles through stone triples (skip collinear triples)
    for i in range(N):
        x1, y1 = stone_list[i]
        s1 = x1 * x1 + y1 * y1
        for j in range(i + 1, N):
            x2, y2 = stone_list[j]
            s2 = x2 * x2 + y2 * y2
            for k in range(j + 1, N):
                x3, y3 = stone_list[k]
                det = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
                if det == 0:
                    continue
                s3 = x3 * x3 + y3 * y3
                b1, b2, b3 = -s1, -s2, -s3
                Dx = b1 * (y2 - y3) + b2 * (y3 - y1) + b3 * (y1 - y2)
                Dy = x1 * (b2 - b3) + x2 * (b3 - b1) + x3 * (b1 - b2)
                # circle: det*(x^2+y^2) + Dx*x + Dy*y + (det-scaled F) = 0
                # F* = -(x1^2+y1^2)*det - Dx*x1 - Dy*y1
                Fs = -s1 * det - Dx * x1 - Dy * y1
                g = gcd(gcd(gcd(abs(det), abs(Dx)), abs(Dy)), abs(Fs)) or 1
                det //= g; Dx //= g; Dy //= g; Fs //= g
                if det < 0:
                    det, Dx, Dy, Fs = -det, -Dx, -Dy, -Fs
                curves.add(("C", (det, Dx, Dy, Fs)))

    # ---- count stones on each curve; check safety; record >= q-1 curves ----
    safe = True
    blocking = []  # curves with >= q-1 stones
    for kind, key in curves:
        cnt = 0
        if kind == "L":
            a, b, c = key
            for x, y in stone_list:
                if a * x + b * y + c == 0:
                    cnt += 1
        else:
            det, Dx, Dy, Fs = key
            for x, y in stone_list:
                if det * (x * x + y * y) + Dx * x + Dy * y + Fs == 0:
                    cnt += 1
        if cnt >= q:
            safe = False
            break
        if cnt >= q - 1:
            blocking.append((kind, key))

    # ---- maximality: every empty cell on some >= q-1 curve ----
    maximal = True
    if safe:
        for yy in range(w):
            for xx in range(m):
                if (xx, yy) in S:
                    continue
                ok = False
                for kind, key in blocking:
                    if kind == "L":
                        a, b, c = key
                        if a * xx + b * yy + c == 0:
                            ok = True
                            break
                    else:
                        det, Dx, Dy, Fs = key
                        if det * (xx * xx + yy * yy) + Dx * xx + Dy * yy + Fs == 0:
                            ok = True
                            break
                if not ok:
                    maximal = False
                    break
            if not maximal:
                break

    print(json.dumps({
        "ok": bool(safe and maximal and def_ok),
        "n": N, "rows": rows, "min_row": min_row,
        "safe": bool(safe), "maximal": bool(maximal), "deficiency": bool(def_ok),
        "nBlockingCurves": len(blocking),
    }))

if __name__ == "__main__":
    main()
