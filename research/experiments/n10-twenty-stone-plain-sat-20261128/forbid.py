#!/usr/bin/env python3
"""Fresh forbidden-4-set enumerator for the standard q=4 game on n x n integer grids.

A 4-point set is forbidden iff the points are concyclic or collinear,
i.e. iff det[[x_i^2+y_i^2, x_i, y_i, 1]] == 0 (exact integer arithmetic;
a line is a degenerate circle). No repo code is used.
"""
import json, sys, time
from itertools import combinations

def det4(m):
    d = 0
    for p in range(4):
        sub = [[m[r][c] for c in range(4) if c != p] for r in range(1, 4)]
        s = (sub[0][0] * (sub[1][1] * sub[2][2] - sub[1][2] * sub[2][1])
             - sub[0][1] * (sub[1][0] * sub[2][2] - sub[1][2] * sub[2][0])
             + sub[0][2] * (sub[1][0] * sub[2][1] - sub[1][1] * sub[2][0]))
        if p % 2 == 0:
            d += m[0][p] * s
        else:
            d -= m[0][p] * s
    return d

def enumerate_forbidden(n):
    pts = [(x, y) for y in range(n) for x in range(n)]  # index = x + n*y
    sq = [x * x + y * y for (x, y) in pts]
    forb = []
    for quad in combinations(range(n * n), 4):
        a, b, c, dd = quad
        m = [[sq[a], pts[a][0], pts[a][1], 1],
             [sq[b], pts[b][0], pts[b][1], 1],
             [sq[c], pts[c][0], pts[c][1], 1],
             [sq[dd], pts[dd][0], pts[dd][1], 1]]
        if det4(m) == 0:
            forb.append(list(quad))
    return forb

def main():
    n = int(sys.argv[1]); out = sys.argv[2]
    t0 = time.time()
    forb = enumerate_forbidden(n)
    with open(out, "w") as f:
        json.dump({"n": n, "num_points": n * n, "num_forbidden": len(forb),
                   "wall_s": round(time.time() - t0, 3), "forbidden": forb}, f)
    print(json.dumps({"n": n, "num_forbidden": len(forb),
                      "wall_s": round(time.time() - t0, 3)}))

if __name__ == "__main__":
    main()
