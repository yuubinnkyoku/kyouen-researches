"""Conic layer of PG(2,8): k-subsets of a conic, PGL(2,8) orbits and Grundy.

A conic of PG(2,8) is a 9-cap; the 32,704 = 8^5-8^2 conics form one PGL(3,8)
orbit with stabilizer PGL(2,8) (order 504).  The k-subsets of a conic (k=3..8)
are caps; their PGL(3,8) classes are the PGL(2,8) classes on k-subsets of the 9
conic points.  We parameterise the conic by a line through a conic point,
compute the classes and, for one representative per class, the exact Grundy
value by a full DP over its upset.

Usage:
    python conic_layer_q8.py
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


# ------------------------------------------------------------------ GF(8)
def gmul(a, b):
    r = 0
    for i in range(3):
        if (b >> i) & 1:
            r ^= a << i
    for bit in (5, 4, 3):
        if (r >> bit) & 1:
            r ^= 0b1011 << (bit - 3)
    return r & 7


def gadd(a, b):
    return a ^ b


def ginv(a):
    for y in range(1, 8):
        if gmul(a, y) == 1:
            return y
    raise ValueError(a)


def canon(v):
    for x in v:
        if x:
            ix = ginv(x)
            return tuple(gmul(ix, z) for z in v)
    return None


def load(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    n, b = map(int, lines[0].split())
    return n, [tuple(map(int, l.split()[1:])) for l in lines[1:]]


def qeval(Q, v):
    # char 2: cross terms appear once (Q is the upper-triangular form)
    x, y, z = v
    s = 0
    s ^= gmul(Q[0][0], gmul(x, x))
    s ^= gmul(Q[1][1], gmul(y, y))
    s ^= gmul(Q[2][2], gmul(z, z))
    s ^= gmul(Q[0][1], gmul(x, y))
    s ^= gmul(Q[0][2], gmul(x, z))
    s ^= gmul(Q[1][2], gmul(y, z))
    return s


def det3(M):
    d = 0
    for perm, sign in [((0, 1, 2), 1), ((1, 2, 0), 1), ((2, 0, 1), 1),
                       ((0, 2, 1), 1), ((1, 0, 2), 1), ((2, 1, 0), 1)]:
        p = 1
        for r, c in enumerate(perm):
            p = gmul(p, M[r][c])
        d ^= p
    return d


def conic_through(idx2pt, pts):
    for q in itertools.product(range(8), repeat=6):
        Q = [[0] * 3 for _ in range(3)]
        Q[0][0], Q[0][1], Q[0][2] = q[0], q[1], q[2]
        Q[1][0], Q[1][1], Q[1][2] = q[1], q[3], q[4]
        Q[2][0], Q[2][1], Q[2][2] = q[2], q[4], q[5]
        if det3(Q) == 0:
            continue
        if all(qeval(Q, v) == 0 for v in pts):
            zeros = sorted(i for i in range(73) if qeval(Q, idx2pt[i]) == 0)
            return Q, zeros
    raise RuntimeError("no conic")


# ------------------------------------------------------------- PGL(2,8)
PG1 = [(1, t) for t in range(8)] + [(0, 1)]


def act2(M, p):
    a, b, c, d = M
    s, t = p
    num_s = gadd(gmul(a, s), gmul(b, t))
    num_t = gadd(gmul(c, s), gmul(d, t))
    return canon((num_s, num_t))


def pgl2_8():
    perms = set()
    for a in range(8):
        for b in range(8):
            for c in range(8):
                for d in range(8):
                    if gadd(gmul(a, d), gmul(b, c)) == 0:
                        continue
                    perm = tuple(PG1.index(act2((a, b, c, d), p)) for p in PG1)
                    perms.add(perm)
    return sorted(perms)


def orbits_on_k_subsets(perms, k):
    subsets = list(combinations(range(9), k))
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
        out.append((len(orbit), min(orbit)))
    return out


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
    ss = set(order)
    maximal = [m for m in order if not any((m | (1 << p)) in ss for p in range(n)
                                           if not (m >> p) & 1)]
    g = {}
    for m in sorted(order, key=lambda x: -x.bit_count()):
        ch = set()
        for p in range(n):
            if (m >> p) & 1:
                continue
            nm = m | (1 << p)
            if nm in g:
                ch.add(g[nm])
        v = 0
        while v in ch:
            v += 1
        g[m] = v
    return (g[sum(1 << p for p in S)],
            sorted({m.bit_count() for m in maximal}), len(order))


def main() -> None:
    n, blocks = load(OUT / "board_pg2q8.txt")
    vecs = [(a, b, c) for a in range(8) for b in range(8) for c in range(8)
            if (a, b, c) != (0, 0, 0)]
    pts = sorted({canon(v) for v in vecs})
    idx2pt = {i: p for i, p in enumerate(pts)}
    pt2idx = {p: i for i, p in enumerate(pts)}
    S5 = [10, 16, 29, 47, 48]
    Q, conic = conic_through(idx2pt, [idx2pt[i] for i in S5])
    assert len(conic) == 9
    # line L: x = 0 (does it avoid P0?); choose a normal vector n with n.P0 != 0
    P0 = idx2pt[conic[0]]
    normal = None
    for nvec in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1)]:
        if gadd(gmul(nvec[0], P0[0]), gadd(gmul(nvec[1], P0[1]), gmul(nvec[2], P0[2]))) != 0:
            normal = nvec
            break
    # basis of the line {p : normal.p = 0}
    Lpts = [p for p in pts
            if gadd(gmul(normal[0], p[0]), gadd(gmul(normal[1], p[1]), gmul(normal[2], p[2]))) == 0]
    assert len(Lpts) == 9
    # projective coordinates [s:t] on L: pick A,B and enumerate canon(sA+tB)
    A, B = Lpts[0], Lpts[1]
    coord = {}
    for s in range(8):
        for t in range(8):
            if (s, t) == (0, 0):
                continue
            coord[(s, t)] = pt2idx[canon(tuple(gadd(gmul(s, A[k]), gmul(t, B[k])) for k in range(3)))]
    # psi: L point -> second intersection of line P0-R with the conic
    psi = {}
    for (s, t), Ridx in coord.items():
        R = idx2pt[Ridx]
        hits = []
        for tt in range(8):
            v = tuple(gadd(P0[k], gmul(tt, R[k])) for k in range(3))
            if qeval(Q, v) == 0:
                hits.append(pt2idx[canon(v)])
        if qeval(Q, R) == 0:
            hits.append(Ridx)
        hits = sorted(set(hits))
        other = [h for h in hits if h != conic[0]]
        psi[(s, t)] = other[0] if other else conic[0]
    assert len(set(psi.values())) == 9, (psi, len(set(psi.values())))
    psi_idx = {i: psi[PG1[i]] for i in range(9)}
    perms = pgl2_8()
    conics = 8 ** 5 - 8 ** 2
    result = {"conic": conic, "conics": conics, "pgl2_8_order": len(perms), "k": {}}
    for k in range(3, 9):
        rows = []
        for count, rep in orbits_on_k_subsets(perms, k):
            S = [psi_idx[rep[x]] for x in range(k)]
            G, msz, tot = grundy(n, blocks, S)
            rows.append({"count_per_conic": count, "orbit_size": conics * count,
                         "representative": S, "grundy": G,
                         "maximal_sizes": msz, "upset": tot})
            print(k, "count", count, "G", G, "maximal", msz, "upset", tot)
        result["k"][str(k)] = {"caps": conics * len(list(combinations(range(9), k))),
                               "orbits": rows}
    (OUT / "conic_layer_q8.json").write_text(json.dumps(result, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
