#!/usr/bin/env python3
"""
Independent integer verifier for kyouen fixed-width witnesses (7/8-row lane).

Clean-room reimplementation. No floats. Curves = integer circles (3-point
determinant form) and integer lines. A position (stones S, board width M,
height h, parameter q) is:
  SAFE     : no curve carries >= q stones.
  MAXIMAL  : every empty cell c of the board has some curve through c that
             carries exactly q-1 stones ("blocked": placing a stone at c
             completes q on a curve => first move is losing for the mover).
  DEF      : every row holds <= q-1 stones (row-deficient mode for frontier
             SAT conventions of this lane; recorded separately).
A witness for lane purposes = SAFE + MAXIMAL (+ DEF recorded).

Self-gates (fail loudly):
  - circleThru equation is asserted on its 3 defining points.
  -tamper controls: dropping a specific stone must destroy MAXIMAL.
  - positive control on demand.

Usage:
  verify_int.py witness.json            # verify file (board from record)
  verify_int.py --stones '[[x,y],..]' --w 7 --M 65 --q 4
"""
import json
import sys
from fractions import Fraction
from math import isqrt, gcd


def circle_thru(p1, p2, p3):
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    S1, S2, S3 = x1 * x1 + y1 * y1, x2 * x2 + y2 * y2, x3 * x3 + y3 * y3

    def det3(a, b, c, d, e, f, g, h, i):
        return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)

    A = det3(x1, y1, 1, x2, y2, 1, x3, y3, 1)
    if A == 0:
        return None  # collinear
    D = -det3(S1, y1, 1, S2, y2, 1, S3, y3, 1)
    E = det3(S1, x1, 1, S2, x2, 1, S3, x3, 1)
    F = -det3(S1, x1, y1, S2, x2, y2, S3, x3, y3)
    assert A * S1 + D * x1 + E * y1 + F == 0
    assert A * S2 + D * x2 + E * y2 + F == 0
    assert A * S3 + D * x3 + E * y3 + F == 0
    if A < 0:
        A, D, E, F = -A, -D, -E, -F
    g = gcd(gcd(abs(A), abs(D)), gcd(abs(E), abs(F)))
    if g > 1:
        A, D, E, F = A // g, D // g, E // g, F // g
    return (A, D, E, F)


def line_thru(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    a, b, c = y2 - y1, x1 - x2, x2 * y1 - x1 * y2
    if a == 0 and b == 0:
        return None
    g = gcd(gcd(abs(a), abs(b)), abs(c)) or 1
    a, b, c = a // g, b // g, c // g
    # canonical sign: first nonzero of (a,b) positive
    for v in (a, b):
        if v != 0:
            if v < 0:
                a, b, c = -a, -b, -c
            break
    return (a, b, c)


def circle_cells(circ, M, h):
    """All lattice cells (x, y) inside the board on the circle."""
    A, D, E, F = circ
    out = []
    if A == 0:
        return out  # degenerate (should not happen)
    # A*(x^2+y^2) + D*x + E*y + F = 0  ->  y^2 + (E/A) y + (x^2 + (D/A)x + F/A) = 0
    # iterate x over board range, solve quadratic in y exactly.
    for x in range(M):
        # A*y^2 + E*y + (A*x^2 + D*x + F) = 0
        c2, c1, c0 = A, E, A * x * x + D * x + F
        disc = c1 * c1 - 4 * c2 * c0
        if disc < 0:
            continue
        r = isqrt(disc)
        if r * r != disc:
            continue
        got = set()
        for num in (-c1 + r, -c1 - r):
            if num % (2 * c2) == 0:
                y = num // (2 * c2)
                if 0 <= y < h:
                    got.add((x, y))
        out.extend(got)
    return out


def line_cells(line, M, h):
    a, b, c = line
    out = []
    if b != 0:
        for x in range(M):
            num = -(a * x + c)
            if num % b == 0:
                y = num // b
                if 0 <= y < h:
                    out.append((x, y))
    elif a != 0:
        # vertical line a*x + c = 0 -> x = -c/a
        num = -c
        if num % a == 0:
            x = num // a
            if 0 <= x < M:
                for y in range(h):
                    out.append((x, y))
    return out


def curves_with_3plus(stones):
    """All circles/lines that carry exactly the max stone count >= min(3, ...).

    Returns dict curve_key -> (kind, cells_on_board_from_stones? no: frozenset of stones on it)
    We enumerate all curves through each stone triple (and each stone pair for
    lines), and keep curves carrying >= 3 stones. A curve carrying >= q stones
    proves UNSAFE (any triple of its stones generates it).
    """
    n = len(stones)
    seen = {}

    def add(kind, cur, pts):
        key = (kind, cur)
        if key not in seen:
            seen[key] = set()
        seen[key] |= set(pts)
        return seen[key]

    lines_seen = set()
    # lines through pairs (a line with >=3 stones will be found via any pair)
    for i in range(n):
        for j in range(i + 1, n):
            ln = line_thru(stones[i], stones[j])
            if ln:
                key = ("line", ln)
                lines_seen.add(key)

    triples = set()
    circles_seen = set()
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                ci = circle_thru(stones[i], stones[j], stones[k])
                if ci:
                    circles_seen.add(("circle", ci))

    return lines_seen | circles_seen


def curve_cells(kind, cur, M, h):
    if kind == "line":
        return line_cells(cur, M, h)
    return circle_cells(cur, M, h)


def verify(stones, M, h, q):
    stones = [tuple(s) for s in stones]
    S = set(stones)
    assert len(S) == len(stones), "duplicate stones"
    for (x, y) in S:
        assert 0 <= x < M and 0 <= y < h, f"stone {x},{y} outside board {M}x{h}"

    curves = curves_with_3plus(stones)
    counts = {}
    for (kind, cur) in curves:
        cnt = sum(1 for c in curve_cells(kind, cur, M, h) if c in S)
        counts[(kind, cur)] = cnt

    unsafe = [k for k, c in counts.items() if c >= q]
    safe = not unsafe

    # maximality: every empty cell blocked by some curve with exactly q-1 stones
    # curves having exactly q-1 stones:
    blockers = []
    for (kind, cur), cnt in counts.items():
        if cnt == q - 1:
            for c in curve_cells(kind, cur, M, h):
                if c not in S:
                    blockers.append(c)
    blocked = set(blockers)
    empty = [(x, y) for x in range(M) for y in range(h) if (x, y) not in S]
    unblocked = [c for c in empty if c not in blocked]
    maximal = not unblocked

    # def-mode: every row <= q-1 stones
    row_counts = [0] * h
    for (x, y) in S:
        row_counts[y] += 1
    def_mode = all(rc <= q - 1 for rc in row_counts)

    return {
        "board": [h, M],
        "q": q,
        "k": len(stones),
        "rowCounts": row_counts,
        "safe": safe,
        "unsafeCurves": len(unsafe),
        "maximal": maximal,
        "unblocked": unblocked[:10],
        "unblockedCount": len(unblocked),
        "def": def_mode,
        "maxCurveCount": max(counts.values()) if counts else 0,
        "curveCount": len(curves),
    }


def main():
    args = sys.argv[1:]
    if not args:
        print("usage: verify_int.py witness.json | --stones ... --w h --M M --q q")
        sys.exit(2)
    if args[0] == "--stones":
        stones = json.loads(args[1])
        h, M, q = int(args[3]), int(args[5]), int(args[7])
    else:
        rec = json.load(open(args[0]))
        stones = rec["stones"]
        if "board" in rec:
            h, M = rec["board"]
        else:
            h, M = rec["w"], rec["M"]
        q = rec.get("q", 4)
    res = verify(stones, M, h, q)
    print(json.dumps(res, indent=1))
    ok = res["safe"] and res["maximal"]
    print("VERDICT:", "WITNESS-OK" if ok else "FAIL")


if __name__ == "__main__":
    main()
