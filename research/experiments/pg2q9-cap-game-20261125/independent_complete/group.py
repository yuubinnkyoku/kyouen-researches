"""PGL(3,9): matrices, permutations, orbits, frame counts."""

from __future__ import annotations

import itertools
import random

import pg
from game import bits


def mat_identity():
    return (1, 0, 0, 0, 1, 0, 0, 0, 1)


def mat_mul(A, B):
    C = [0] * 9
    for i in range(3):
        for j in range(3):
            s = 0
            for k in range(3):
                s = pg.GF_ADD[s][pg.GF_MUL[A[3 * i + k]][B[3 * k + j]]]
            C[3 * i + j] = s
    return tuple(C)


def mat_vec(A, v):
    out = []
    for i in range(3):
        s = 0
        for k in range(3):
            s = pg.GF_ADD[s][pg.GF_MUL[A[3 * i + k]][v[k]]]
        out.append(s)
    return tuple(out)


def mat_det(A):
    # explicit 3x3 determinant over GF(9)
    a, b, c, d, e, f, g, h, i = A
    # a(ei - fh) - b(di - fg) + c(dh - eg)
    def m(x, y):
        return pg.GF_MUL[x][y]

    def s(x, y):
        return pg.GF_ADD[x][y]

    def n(x):
        return pg.GF_ADD[0][pg.GF_ADD[0][x]]  # additive inverse in char 3
    # use explicit multiplication: -1 = 2
    def neg(x):
        return pg.GF_MUL[2][x]

    t1 = m(a, s(m(e, i), neg(m(f, h))))
    t2 = neg(m(b, s(m(d, i), neg(m(f, g)))))
    t3 = m(c, s(m(d, h), neg(m(e, g))))
    return s(s(t1, t2), t3)


def mat_transvection(i, j, a):
    M = list(mat_identity())
    M[3 * i + j] = a
    return tuple(M)


def mat_diag(a, b, c):
    return (a, 0, 0, 0, b, 0, 0, 0, c)


def matrix_perm(M, points, index):
    perm = []
    for v in points:
        w = mat_vec(M, v)
        c = pg.canonical_vector(w)
        assert c is not None
        perm.append(index[c])
    assert sorted(perm) == list(range(len(points)))
    return tuple(perm)


def generators():
    """14 generators: 12 elementary transvections + diagonal + 3-cycle.

    The transvections E_ij(1), E_ij(x) for all ordered pairs i != j generate
    SL(3,9) (standard elementary-matrix theorem), and for q = 9,
    SL(3,9) = PGL(3,9) in its action on points because |SL| = |PGL| and the
    scalar matrices act trivially; the extra two generators are included as a
    safety net.
    """
    gens = []
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            for a in (1, 3):  # 1 and x
                gens.append(mat_transvection(i, j, a))
    gens.append(mat_diag(3, 1, 1))
    # (x,y,z) -> (y,z,x)
    gens.append((0, 1, 0, 0, 0, 1, 1, 0, 0))
    return gens


def board_generators(points, index, phi):
    """Return (matrix list, model permutation list, board permutation list).

    phi maps board point label -> model point index.
    """
    inv_phi = {phi[b]: b for b in range(len(phi))}
    assert sorted(inv_phi) == list(range(len(points)))
    mats = generators()
    model_perms = []
    board_perms = []
    for M in mats:
        assert mat_det(M) != 0, M
        pm = matrix_perm(M, points, index)
        pb = tuple(inv_phi[pm[phi[b]]] for b in range(len(phi)))
        model_perms.append(pm)
        board_perms.append(pb)
    return mats, model_perms, board_perms


def is_line_permutation(perm, blocks):
    target = {frozenset(B) for B in blocks}
    for B in blocks:
        if frozenset(perm[p] for p in B) not in target:
            return False
    return True


# ---------------------------------------------------------------------------
# Orbit BFS on k-subsets (canonical order fixed by sorted point labels)
# ---------------------------------------------------------------------------


def encode_sorted(pts):
    code = 0
    for i, p in enumerate(pts):
        code |= p << (7 * i)
    return code


def decode_sorted(code, k):
    return [(code >> (7 * i)) & 127 for i in range(k)]


def orbit_size(start, perms, k):
    """BFS orbit of the sorted k-subset `start` under the permutations."""
    start = tuple(sorted(start))
    code0 = encode_sorted(start)
    seen = {code0}
    frontier = [code0]
    while frontier:
        nxt = []
        for code in frontier:
            vals = decode_sorted(code, k)
            for P in perms:
                img = sorted(P[v] for v in vals)
                nc = encode_sorted(img)
                if nc not in seen:
                    seen.add(nc)
                    nxt.append(nc)
        frontier = nxt
    return len(seen)


# ---------------------------------------------------------------------------
# Ordered frames and |PGL|
# ---------------------------------------------------------------------------


def count_ordered_frames_bruteforce(n, blocks):
    """Count ordered 4-tuples with no three collinear (all C(n,4) subsets)."""
    # line of pair
    line_of_pair = {}
    for li, B in enumerate(blocks):
        for a, b in itertools.combinations(B, 2):
            line_of_pair[(a, b) if a < b else (b, a)] = li
    order = list(range(n))
    n4 = 0
    for S in itertools.combinations(order, 4):
        a, b, c, d = S
        lines = [
            line_of_pair[(a, b)],
            line_of_pair[(a, c)],
            line_of_pair[(a, d)],
            line_of_pair[(b, c)],
            line_of_pair[(b, d)],
            line_of_pair[(c, d)],
        ]
        if len(set(lines)) == 6:
            n4 += 1
    return n4


def count_ordered_triples_extensions(n, blocks):
    """For every 3-cap, count addable points; verify it is always 64.

    Returns (number of ordered 3-caps, multiset of extension counts, total
    ordered frames).
    """
    line_of_pair = {}
    line_sets = [frozenset(B) for B in blocks]
    for li, B in enumerate(blocks):
        for a, b in itertools.combinations(B, 2):
            line_of_pair[(a, b) if a < b else (b, a)] = li
    all_mask = (1 << n) - 1
    line_mask = []
    for B in line_sets:
        m = 0
        for p in B:
            m |= 1 << p
        line_mask.append(m)
    total_ordered = 0
    counts = {}
    total_frames = 0
    for a, b, c in itertools.permutations(range(n), 3):
        lab = line_of_pair[(min(a, b), max(a, b))]
        lac = line_of_pair[(min(a, c), max(a, c))]
        lbc = line_of_pair[(min(b, c), max(b, c))]
        if lab == lac or lab == lbc or lac == lbc:
            continue  # collinear
        total_ordered += 1
        union = line_mask[lab] | line_mask[lac] | line_mask[lbc]
        avail = all_mask & ~union & ~(1 << a) & ~(1 << b) & ~(1 << c)
        cnt = avail.bit_count()
        counts[cnt] = counts.get(cnt, 0) + 1
        total_frames += cnt
    return total_ordered, counts, total_frames
