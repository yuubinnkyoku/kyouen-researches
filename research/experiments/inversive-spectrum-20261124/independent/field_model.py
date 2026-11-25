#!/usr/bin/env python3
"""Reconstruct a GF(49)+infinity coordinate model for board_q7.json from scratch.

We do not read the builder.  Hypothesis (to be checked):
  label L in 0..48  <->  field element a + b*alpha with a=L//7, b=L%7
  label 49          <->  infinity
  circles           <->  images of PG(1,7) under PGL(2,49)

The script tries all three possible alpha^2 = c in GF(7) (the nonsquares
3,5,6), builds all 350 Baer sublines by a BFS orbit under PGL(2,49)
generators, and compares with the board block set.
"""
import json
import sys
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "output"
Q = 7
INF = 49


def load_blocks():
    with open(OUT / f"board_q{Q}.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return frozenset(frozenset(bl) for bl in data["blocks"])


# field arithmetic, element = (a,b) meaning a + b*alpha, alpha^2 = C
def fadd(x, y):
    return ((x[0] + y[0]) % Q, (x[1] + y[1]) % Q)


def fneg(x):
    return ((-x[0]) % Q, (-x[1]) % Q)


def fsub(x, y):
    return fadd(x, fneg(y))


def fmul(x, y, C):
    a, b = x
    d, e = y
    return ((a * d + b * e * C) % Q, (a * e + b * d) % Q)


def finv(x, C):
    a, b = x
    norm = (a * a - C * b * b) % Q
    assert norm != 0, "inverse of zero"
    inv_norm = pow(norm, Q - 2, Q)
    return ((a * inv_norm) % Q, ((-b) * inv_norm) % Q)


def fdiv(x, y, C):
    return fmul(x, finv(y, C), C)


def fpow(x, n, C):
    r = (1, 0)
    while n:
        if n & 1:
            r = fmul(r, x, C)
        x = fmul(x, x, C)
        n >>= 1
    return r


def label_to_field(L):
    assert 0 <= L < Q * Q
    return (L // Q, L % Q)


def field_to_label(x):
    a, b = x
    return (b + Q * a) % (Q * Q)


def mobius_apply(M, L, C):
    """Apply 2x2 matrix M over GF(49) to point L (label) in PG(1,49)."""
    a, b, c, d = M
    if L == INF:
        # infinity maps to a/c (or infinity if c == 0)
        if c == (0, 0):
            return INF
        return field_to_label(fdiv(a, c, C))
    x = label_to_field(L)
    num = fadd(fmul(a, x, C), b)
    den = fadd(fmul(c, x, C), d)
    if den == (0, 0):
        return INF
    return field_to_label(fdiv(num, den, C))


def image_set(M, S, C):
    return frozenset(mobius_apply(M, L, C) for L in S)


def build_subline_orbit(C, M_gens, verbose=False):
    # standard Baer subline PG(1,7) = GF(7) union {inf}
    start = frozenset({INF} | {Q * t for t in range(Q)})
    seen = {start}
    dq = deque([start])
    while dq:
        S = dq.popleft()
        for M in M_gens:
            T = image_set(M, S, C)
            assert len(T) == Q + 1
            if T not in seen:
                seen.add(T)
                dq.append(T)
    if verbose:
        print("  orbit size", len(seen))
    return seen


def find_primitive(C):
    for a in range(Q):
        for b in range(Q):
            x = (a, b)
            if x == (0, 0):
                continue
            if fpow(x, 48, C) == (1, 0):
                # check no proper divisor order (48 = 2^4*3)
                if fpow(x, 24, C) != (1, 0) and fpow(x, 16, C) != (1, 0):
                    return x
    raise RuntimeError("no primitive element found")


def main():
    board = load_blocks()
    print("board blocks:", len(board))
    for C in (3, 5, 6):
        print(f"--- trying alpha^2 = {C} ---")
        lam = find_primitive(C)
        print("  primitive lambda =", lam, "label", field_to_label(lam))
        # generators: x -> x+1, x -> lambda*x, x -> 1/x
        M_gens = [
            ((1, 0), (1, 0), (0, 0), (1, 0)),
            (lam, (0, 0), (0, 0), (1, 0)),
            ((0, 0), (1, 0), (1, 0), (0, 0)),
        ]
        sublines = build_subline_orbit(C, M_gens, verbose=True)
        match = sublines == set(board)
        print("  equals board block set:", match)
        if match:
            # sanity: stabilize standard subline count
            print("  MATCH.  alpha^2 =", C, " primitive lambda =", lam)
            return C, lam
    print("no match")
    return None


if __name__ == "__main__":
    main()
