"""PGL(3,9) orbits of the 5-caps of PG(2,9), via the stabilizer of a frame.

Every 5-cap contains a 4-cap; all 4-caps are one PGL(3,9)-orbit (K1304), so the
PGL-orbits of 5-caps correspond to the orbits of the stabilizer S4 of a fixed
frame ({0,1,10,20}) on the 42 five-caps containing it.  A 5-cap containing the
frame is {frame} U {p}; the S4 action on the 42 extra points gives the orbits.
By orbit-stabilizer, a PGL orbit has size (#4-caps) * s / 5, where s is the
S4-orbit size (each 5-cap contains 5 four-subsets).

The Grundy value of one representative per orbit is computed by a full DP over
its upset.

Usage:
    python cap5_orbits_s4.py
"""

from __future__ import annotations

import itertools
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def add(a, b):
    return ((a[0] + b[0]) % 3, (a[1] + b[1]) % 3)


def mul(a, b):
    return ((a[0] * b[0] - a[1] * b[1]) % 3, (a[0] * b[1] + a[1] * b[0]) % 3)


E = [(a, b) for a in range(3) for b in range(3)]
Z, ONE = (0, 0), (1, 0)
NZ = [e for e in E if e != Z]


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


def frame_stabilizer(frame):
    """The 24 projectivities realizing the permutations of the frame."""
    stabs = set()
    for sigma in itertools.permutations(range(4)):
        found = False
        for c1 in NZ:
            for c2 in NZ:
                for c3 in NZ:
                    c = [ONE, c1, c2, c3]
                    cols = {1: tuple(mul(c[2], frame[sigma[2]][k]) for k in range(3)),
                            2: tuple(mul(c[1], frame[sigma[1]][k]) for k in range(3)),
                            3: tuple(mul(c[0], frame[sigma[0]][k]) for k in range(3))}
                    M = [[cols[1][0], cols[2][0], cols[3][0]],
                         [cols[1][1], cols[2][1], cols[3][1]],
                         [cols[1][2], cols[2][2], cols[3][2]]]
                    w = pmul(M, frame[3])
                    tgt = frame[sigma[3]]
                    s = None
                    for k in range(3):
                        if tgt[k] != Z:
                            s = mul(w[k], inv(tgt[k]))
                            break
                    if s is None or not all(mul(s, tgt[k]) == w[k] for k in range(3)):
                        continue
                    first = None
                    for r in range(3):
                        for col in range(3):
                            if M[r][col] != Z:
                                first = M[r][col]
                                break
                        if first is not None:
                            break
                    si = inv(first)
                    stabs.add(tuple(tuple(mul(si, M[r][col]) for col in range(3)) for r in range(3)))
                    found = True
                    break
                if found:
                    break
            if found:
                break
    return stabs


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
    frame = [idx2pt[i] for i in [0, 1, 10, 20]]
    stabs = frame_stabilizer(frame)
    print("stabilizer matrices:", len(stabs))
    # 42 extra points p with frame + p a cap
    extra = []
    for p in range(n):
        S = {0, 1, 10, 20, p}
        if len(S) < 5:
            continue
        if all(len(S & set(B)) <= 2 for B in blocks):
            extra.append(p)
    assert len(extra) == 42
    # union-find orbits of S4 on the extra points
    parent = {p: p for p in extra}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for p in extra:
        v = idx2pt[p]
        for M in stabs:
            q = pt2idx[canon(pmul(M, v))]
            if q in parent:
                a, b = find(p), find(q)
                if a != b:
                    parent[a] = b
    groups = defaultdict(list)
    for p in extra:
        groups[find(p)].append(p)
    orbits = []
    for rep, members in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        s = len(members)
        size = 1769040 * s // 5
        S = [0, 1, 10, 20, members[0]]
        G, positions = grundy(n, blocks, S)
        orbits.append({"s4_orbit_size": s, "pgl_orbit_size": size,
                       "stabilizer_order": 42456960 // size,
                       "representative": S, "grundy": G,
                       "upset_positions": positions})
    data = {"frame": [0, 1, 10, 20], "s4_stabilizer_order": len(stabs),
            "total_5caps": sum(o["pgl_orbit_size"] for o in orbits),
            "orbits": orbits}
    (OUT / "cap5_orbits.json").write_text(json.dumps(data, indent=1), encoding="utf-8")
    print(json.dumps(data, indent=1))


if __name__ == "__main__":
    main()
