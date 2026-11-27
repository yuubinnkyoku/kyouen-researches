#!/usr/bin/env python3
"""Independent brute-force spot-check (method-disjoint from surgery_general.py).

For each sampled candidate final state S' = seed - R + A on the BXxBY board:
rebuild ALL curves from the stones of S' itself with an integer-conic
representation (lines: ax+by+c=0; circles: x^2+y^2+ux+vy+w=0 through 3 stones,
integer coefficients, membership tested by exact integer evaluation) -- no
seed tables, no T-case split, no Fraction arithmetic:
  safe    := no curve holds >= Q stones of S';
  maximal := every empty cell lies on some curve with >= Q-1 stones of S'.
Every sampled candidate was rejected by the engine; this checker must agree
(report no safe-maximal candidate) on all of them.
"""
import json, sys, itertools, random

def curves_int(stones):
    out = {}
    n = len(stones)
    for i, j in itertools.combinations(range(n), 2):
        (x1, y1), (x2, y2) = stones[i], stones[j]
        a, b, c = y1 - y2, x2 - x1, x1*y2 - x2*y1
        out[("L", a, b, c)] = None
    for i, j, k in itertools.combinations(range(n), 3):
        (x1, y1), (x2, y2), (x3, y3) = stones[i], stones[j], stones[k]
        A, B = x2-x1, y2-y1
        C, D = x3-x1, y3-y1
        det = A*D - B*C
        if det == 0: continue
        s1, s2, s3 = x1*x1+y1*y1, x2*x2+y2*y2, x3*x3+y3*y3
        E, F = -(s2-s1), -(s3-s1)
        U = E*D - B*F
        V = A*F - E*C
        W = -s1*det - U*x1 - V*y1
        # curve equation: det*(x^2+y^2) + U*x + V*y + W = 0; verify on the 3
        def f(x, y): return det*(x*x + y*y) + U*x + V*y + W
        assert f(x1, y1) == 0 and f(x2, y2) == 0 and f(x3, y3) == 0
        out[("C", det, U, V, W)] = None
    res = []
    for key in out:
        cells = []
        for x in range(BXG):
            for y in range(BYG):
                if key[0] == "L":
                    on = key[1]*x + key[2]*y + key[3] == 0
                else:
                    _, d, u, v, w = key
                    on = d*(x*x + y*y) + u*x + v*y + w == 0
                if on: cells.append((x, y))
        res.append(frozenset(cells))
    return res

def verdict(Sp, Q):
    S = set(map(tuple, Sp))
    stones = sorted(S)
    curves = [c for c in curves_int(stones) if sum(1 for p in c if p in S) >= 3]
    counts = [(sum(1 for p in c if p in S), c) for c in curves]
    if any(cnt >= Q for cnt, _ in counts): return False
    for x in range(BXG):
        for y in range(BYG):
            e = (x, y)
            if e in S: continue
            if not any(cnt >= Q-1 and e in c for cnt, c in counts):
                return False
    return True

def main():
    global BXG, BYG
    rec = json.load(open(sys.argv[1]))
    BXG, BYG = rec["board"]
    Q = rec["q"]
    seed = set(map(tuple, rec["seed"]))
    rows = [json.loads(l) for l in open(sys.argv[2])]
    full = random.Random(20261127).sample(rows, min(int(sys.argv[3]), len(rows)))
    start = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    cnt = int(sys.argv[5]) if len(sys.argv) > 5 else len(full)
    sample = full[start:start+cnt]
    missed = 0
    for k, row in enumerate(sample):
        R = set(map(tuple, row["R"])); A = set(map(tuple, row["A"]))
        if verdict((seed - R) | A, Q):
            missed += 1
            print("ENGINE MISSED WITNESS:", sorted(map(list, (seed - R) | A)))
        if (k+1) % 100 == 0: print(f"  {k+1}/{len(sample)} checked, missed {missed}", flush=True)
    print(f"spot-check: {len(sample)} sampled candidates, engine rejections confirmed {len(sample)-missed}, missed witnesses {missed}")
    assert missed == 0

if __name__ == "__main__":
    main()
