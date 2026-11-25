"""Corrected PGL(3,9) orbit classification of the 5-caps of PG(2,9).

The earlier attempt (cap5_orbits_s4.py) inferred PGL-orbit sizes from the
orbits of the frame stabilizer S4 on the 42 five-caps through the frame.  That
inference is invalid: a projectivity taking F+{p} to F+{q} need not fix the
frame F.  (Explicit witness below: M maps {0,1,10,20,31} onto {0,1,10,20,41}
while M(F) = {0,10,20,41} != F.)

Correct route: every 5-cap lies on a unique conic; the 58,968 conics form one
PGL(3,9) orbit with stabilizer PGL(2,9) (order 720); the PGL(2,9) orbits on the
C(10,5)=252 five-subsets of a conic are 180 and 72.  Hence the 5-cap orbits have
sizes 58,968*180 = 10,614,240 and 58,968*72 = 4,245,696 (stabilizers 4 and 10).

Usage:
    python cap5_orbits.py
"""

from __future__ import annotations

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


def pmul(M, v):
    return tuple(add(add(mul(M[r][0], v[0]), mul(M[r][1], v[1])), mul(M[r][2], v[2]))
                 for r in range(3))


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


# ---------------------------------------------------------------- PGL(2,9)
# PG(1,9): the 10 points (1:t) for t in GF(9), plus (0:1) = infinity.
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
                    det = sub(mul(a, d), mul(b, c))
                    if det == Z:
                        continue
                    perms.add(tuple(PG1.index(act2((a, b, c, d), t)) for t in PG1))
    return perms


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
    # witness that the frame stabilizer is not the right invariant
    M = [(8, Z), (0, Z), (4, Z)],  # placeholder replaced below
    # explicit witness from the verification: M = [[8,0,4],[5,0,4],[5,5,2]]
    num = lambda k: (k // 3, k % 3)  # noqa: E731
    M = [[num(8), num(0), num(4)], [num(5), num(0), num(4)], [num(5), num(5), num(2)]]
    cap = [0, 1, 10, 20, 31]
    img = sorted(pt2idx[canon(pmul(M, idx2pt[p]))] for p in cap)
    frame_img = sorted(pt2idx[canon(pmul(M, idx2pt[p]))] for p in [0, 1, 10, 20])
    witness = {"matrix": [[list(x) for x in row] for row in M],
               "det": list(det3(M)), "image_of_cap": img,
               "image_of_frame": frame_img,
               "maps_31_to_41": img == sorted([0, 1, 10, 20, 41]),
               "frame_fixed": frame_img == [0, 1, 10, 20]}

    perms = pgl2_9()
    subsets = list(combinations(range(10), 5))
    visited = [False] * len(subsets)
    orbit_sizes = []
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
            visited[subsets.index(T)] = True
        orbit_sizes.append(len(orbit))
    conics = 9 ** 5 - 9 ** 2
    cap_orbits = [{"count_of_five_subsets": o, "orbit_size": conics * o,
                   "stabilizer_order": 42456960 // (conics * o)} for o in sorted(orbit_sizes, reverse=True)]
    data = {
        "total_5caps": sum(o["orbit_size"] for o in cap_orbits),
        "conics": conics,
        "pgl2_9_order": len(perms),
        "pgl2_9_orbits_on_5subsets": sorted(orbit_sizes, reverse=True),
        "orbits": cap_orbits,
        "witness_two_s4_orbits_fuse": witness,
        "grundy": {},
    }
    for S in ([0, 1, 10, 20, 31], [0, 1, 10, 20, 42]):
        G, pos = grundy(n, blocks, S)
        data["grundy"][",".join(map(str, S))] = {"grundy": G, "upset_positions": pos}
    (OUT / "cap5_orbits.json").write_text(json.dumps(data, indent=1), encoding="utf-8")
    print(json.dumps(data, indent=1))


if __name__ == "__main__":
    main()
