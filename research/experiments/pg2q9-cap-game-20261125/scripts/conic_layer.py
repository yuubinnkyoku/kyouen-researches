"""The conic layer of PG(2,9): caps lying on a conic, by PGL(3,9) orbit.

Every conic is a 10-cap; the conics form one PGL(3,9) orbit (58,968), with
stabilizer PGL(2,9) (720) acting on the 10 conic points as PGL(2,9) on PG(1,9).
Hence the k-subsets of conics (k = 3..9) are caps, and their PGL(3,9) orbits are
the PGL(2,9) orbits on k-subsets of 10 points.  We compute those orbits and, for
one representative per orbit, the exact Grundy value by a full DP over its upset.

Usage:
    python conic_layer.py
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def add(a, b):
    return ((a[0] + b[0]) % 3, (a[1] + b[1]) % 3)


def sub(a, b):
    return ((a[0] - b[0]) % 3, (a[1] - b[1]) % 3)


def mul(a, b):
    return ((a[0] * b[0] - a[1] * b[1]) % 3, (a[0] * b[1] + a[1] * b[0]) % 3)


E = [(a, b) for a in range(3) for b in range(3)]
Z, ONE = (0, 0), (1, 0)


def inv(a):
    for y in E:
        if mul(a, y) == ONE:
            return y
    raise ValueError(a)


def canon(v):
    for x in v:
        if x != Z:
            ix = inv(x)
            return tuple(mul(ix, z) for z in v)
    return None


def elem(k):
    return (k // 3, k % 3)


def point_map():
    idx2pt = {}
    for j in range(9):
        idx2pt[1 + j] = (Z, ONE, elem(j))
    for p in range(9):
        for j in range(9):
            idx2pt[10 + 9 * p + j] = (ONE, elem(p), elem(j))
    idx2pt[0] = (Z, Z, ONE)
    pt2idx = {canon(v): k for k, v in idx2pt.items()}
    assert len(pt2idx) == 91
    return idx2pt, pt2idx


def qeval(Q, v):
    s = Z
    for i in range(3):
        for j in range(3):
            s = add(s, mul(Q[i][j], mul(v[i], v[j])))
    return s


def det3(M):
    d = Z
    for perm in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
        p = ONE
        for r, c in enumerate(perm):
            p = mul(p, M[r][c])
        d = add(d, p)
    for perm in [(0, 2, 1), (1, 0, 2), (2, 1, 0)]:
        p = ONE
        for r, c in enumerate(perm):
            p = mul(p, M[r][c])
        d = sub(d, p)
    return d


def conic_through(idx2pt, pts):
    for q in itertools.product(range(9), repeat=6):
        Q = [[Z] * 3 for _ in range(3)]
        vals = [elem(x) for x in q]
        Q[0][0] = vals[0]
        Q[0][1] = Q[1][0] = vals[1]
        Q[0][2] = Q[2][0] = vals[2]
        Q[1][1] = vals[3]
        Q[1][2] = Q[2][1] = vals[4]
        Q[2][2] = vals[5]
        if det3(Q) == Z:
            continue
        if all(qeval(Q, v) == Z for v in pts):
            return Q
    raise RuntimeError("no conic")


# PGL(2,9) on PG(1,9)
PG1 = [None] + E


def act2(M, t):
    a, b, c, d = M
    if t is None:
        return None if c == Z else mul(a, inv(c))
    num = add(mul(a, t), b)
    den = add(mul(c, t), d)
    if den == Z:
        return None
    return mul(num, inv(den))


def pgl2_9():
    perms = set()
    for a in E:
        for b in E:
            for c in E:
                for d in E:
                    if sub(mul(a, d), mul(b, c)) == Z:
                        continue
                    perms.add(tuple(PG1.index(act2((a, b, c, d), t)) for t in PG1))
    return sorted(perms)


def orbits_on_k_subsets(perms, k):
    subsets = list(combinations(range(10), k))
    idx = {s: i for i, s in enumerate(subsets)}
    visited = [False] * len(subsets)
    out = []
    for i, S in enumerate(subsets):
        if visited[i]:
            continue
        orbit = set()
        stack = [S]
        while stack:
            T = stack.pop()
            if T in orbit:
                continue
            orbit.add(T)
            for perm in perms:
                U = tuple(sorted(perm[x] for x in T))
                if U not in orbit:
                    stack.append(U)
        for T in orbit:
            visited[idx[T]] = True
        out.append((len(orbit), sorted(orbit)[0]
                    if False else min(orbit)))
    return out


def load(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    n, b = map(int, lines[0].split())
    return n, [tuple(map(int, l.split()[1:])) for l in lines[1:]]


def grundy(n, blocks, S):
    pc = [[] for _ in range(n)]
    for c, B in enumerate(blocks):
        for p in B:
            pc[p].append(c)
    used = [False] * n
    counts = [0] * len(blocks)
    for p in S:
        used[p] = True
        for c in pc[p]:
            counts[c] += 1
    order = []

    def rec(mask, size, start):
        order.append(mask)
        for p in range(start, n):
            if used[p]:
                continue
            if all(counts[c] < 2 for c in pc[p]):
                used[p] = True
                for c in pc[p]:
                    counts[c] += 1
                rec(mask | (1 << p), size + 1, p + 1)
                for c in pc[p]:
                    counts[c] -= 1
                used[p] = False

    rec(sum(1 << p for p in S), len(S), 0)
    g = {}
    for mask in sorted(order, key=lambda m: -m.bit_count()):
        ch = set()
        for p in range(n):
            if (mask >> p) & 1:
                continue
            nm = mask | (1 << p)
            if nm in g:
                ch.add(g[nm])
        v = 0
        while v in ch:
            v += 1
        g[mask] = v
    return g[sum(1 << p for p in S)], len(order)


def main() -> None:
    n, blocks = load(OUT / "board_pg2q9.txt")
    idx2pt, pt2idx = point_map()
    rep5 = [0, 1, 10, 20, 31]
    Q = conic_through(idx2pt, [idx2pt[i] for i in rep5])
    conic = sorted(i for i in range(91) if qeval(Q, idx2pt[i]) == Z)
    assert len(conic) == 10
    perms = pgl2_9()
    conics = 9 ** 5 - 9 ** 2
    result = {"conic": conic, "conics": conics, "pgl2_9_order": len(perms), "k": {}}
    for k in range(3, 10):
        orbs = orbits_on_k_subsets(perms, k)
        rows = []
        for count, rep_sub in orbs:
            S = [conic[x] for x in rep_sub]
            G, pos = grundy(n, blocks, S)
            rows.append({"orbit_size": conics * count, "count_per_conic": count,
                         "representative": S, "grundy": G, "upset_positions": pos})
        result["k"][str(k)] = {"caps": conics * len(list(combinations(range(10), k))),
                               "orbits": rows}
        print(k, "caps", conics * len(list(combinations(range(10), k))),
              "orbits", [(r["count_per_conic"], r["grundy"]) for r in rows])
    (OUT / "conic_layer.json").write_text(json.dumps(result, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
