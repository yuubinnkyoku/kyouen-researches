#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independent verification of orbit/structural claims for the blocking-set
game on PG(2,3) and PG(2,4).

This program is self-contained (Python standard library only).  It reads only
the two board files named in the task and writes its outputs next to itself.
It does NOT import anything from the experiment's ``scripts/`` directory and
does NOT read ``output/orbits.json``.

Method
------
1.  Implement F_3 and GF(4) = {0, 1, w, w+1} from scratch (w^2 = w+1, encoded
    as a | (b << 1)) and build PG(2,q) from the 1-dimensional subspaces of
    F_q^3 with canonical representatives (first non-zero coordinate 1).
2.  Parse the two board files, verify the projective-plane axioms, and find an
    explicit point bijection onto the independently constructed PG(2,q).
3.  Generate PGL(3,q) from an own generator set (elementary transvections with
    coefficients 1 and a primitive element, plus one diagonal matrix) and
    certify the generated group order by BFS over projective matrices.  The
    expected orders are 5616 for q=3 and 60480 for q=4.
4.  Enumerate safe sets by brute force over all combinations, filter them by
    "at most three points on every line", determine maximality by inclusion,
    take complements, and compute PGL orbits by BFS with the certified
    generator images.
5.  Check claims A, B, C and write JSON files plus a console summary.
"""

from __future__ import annotations

import itertools
import json
import math
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENT = HERE.parent.parent
OUTPUT = EXPERIMENT / "output"

EXPECTED_PGL_ORDER = {3: 5616, 4: 60480}


# ---------------------------------------------------------------------------
# Finite fields
# ---------------------------------------------------------------------------

class Field:
    """The field F_3 or GF(4) with a fixed encoding.

    GF(4) elements are encoded as ``a + b*w`` -> ``a | (b << 1)`` with
    ``w^2 = w + 1``; hence 0, 1, 2=w, 3=w+1.  Addition is XOR.
    """

    def __init__(self, q: int) -> None:
        self.q = q
        if q == 3:
            els = [0, 1, 2]
            self.elements = els
            self.add = [[(a + b) % 3 for b in els] for a in els]
            self.mul = [[(a * b) % 3 for b in els] for a in els]
            self.neg = [0, 2, 1]
            self.inv = [None, 1, 2]
            self.primitive = 2
        elif q == 4:
            els = [0, 1, 2, 3]
            self.elements = els
            self.add = [[a ^ b for b in els] for a in els]
            mul = [[0] * 4 for _ in range(4)]
            for a in range(4):
                a0, a1 = a & 1, (a >> 1) & 1
                for b in range(4):
                    b0, b1 = b & 1, (b >> 1) & 1
                    # (a0 + a1 w)(b0 + b1 w) = a0 b0 + a1 b1
                    #     + (a0 b1 + a1 b0 + a1 b1) w   over F_2
                    c0 = (a0 & b0) ^ (a1 & b1)
                    c1 = (a0 & b1) ^ (a1 & b0) ^ (a1 & b1)
                    mul[a][b] = c0 | (c1 << 1)
            self.mul = mul
            self.neg = [0, 1, 2, 3]  # characteristic 2
            self.inv = [None, 1, 3, 2]  # 1/1=1, 1/w=w+1, 1/(w+1)=w
            self.primitive = 2  # w generates F_4^*
        else:
            raise ValueError("only q=3 and q=4 are supported")


def self_test_fields() -> None:
    F3 = Field(3)
    for a in range(3):
        for b in range(3):
            assert F3.add[a][b] == (a + b) % 3
            assert F3.mul[a][b] == (a * b) % 3
    for a in (1, 2):
        assert F3.mul[a][F3.inv[a]] == 1

    F4 = Field(4)
    assert F4.mul[2][2] == 3, "w*w must be w+1"
    assert F4.mul[2][3] == 1, "w*(w+1) must be 1"
    assert F4.mul[3][3] == 2, "(w+1)^2 must be w"
    for a in (1, 2, 3):
        assert F4.mul[a][F4.inv[a]] == 1
    for a in range(4):
        for b in range(4):
            assert F4.add[a][b] == F4.add[b][a]
            assert F4.mul[a][b] == F4.mul[b][a]
    # distributivity spot checks
    for a in range(4):
        for b in range(4):
            for c in range(4):
                assert F4.mul[a][F4.add[b][c]] == (
                    F4.add[F4.mul[a][b]][F4.mul[a][c]]
                )


def vec_norm(v, F: Field):
    """Normalize a non-zero 3-vector so its first non-zero entry is 1."""
    for x in v:
        if x:
            ix = F.inv[x]
            m = F.mul
            return (m[v[0]][ix], m[v[1]][ix], m[v[2]][ix])
    raise ValueError("zero vector has no projective representative")


def dot(u, v, F: Field):
    add, mul = F.add, F.mul
    return add[add[mul[u[0]][v[0]]][mul[u[1]][v[1]]]][mul[u[2]][v[2]]]


def build_canonical_pg2(F: Field):
    """Build PG(2,q) from the 1-dimensional subspaces of F_q^3."""
    q = F.q
    els = F.elements
    points = []
    for a in els:
        for b in els:
            for c in els:
                if a == 0 and b == 0 and c == 0:
                    continue
                v = (a, b, c)
                if vec_norm(v, F) == v:
                    points.append(v)
    if len(points) != q * q + q + 1:
        raise AssertionError("wrong number of projective points")
    index = {v: i for i, v in enumerate(points)}

    lines = []
    line_sets = []
    for normal in points:
        n0, n1, n2 = normal
        L = []
        for i, p in enumerate(points):
            if dot(normal, p, F) == 0:
                L.append(i)
        L = tuple(L)
        if len(L) != q + 1:
            raise AssertionError("canonical line does not have q+1 points")
        lines.append(L)
        line_sets.append(frozenset(L))
    if len(set(line_sets)) != len(lines):
        raise AssertionError("duplicate canonical line")

    pair_line = {}
    for li, L in enumerate(lines):
        for u, v in itertools.combinations(L, 2):
            pair_line[(u, v)] = li
    point_lines = [[] for _ in points]
    for li, L in enumerate(lines):
        for p in L:
            point_lines[p].append(li)
    return {
        "points": points,
        "index": index,
        "lines": lines,
        "line_sets": line_sets,
        "pair_line": pair_line,
        "point_lines": point_lines,
    }


# ---------------------------------------------------------------------------
# Board files and plane axioms
# ---------------------------------------------------------------------------

def parse_board(path: Path):
    tokens = path.read_text(encoding="utf-8").split()
    if len(tokens) < 2:
        raise ValueError(f"empty board file: {path}")
    n = int(tokens[0])
    b = int(tokens[1])
    pos = 2
    lines = []
    for _ in range(b):
        k = int(tokens[pos])
        pos += 1
        L = tuple(int(x) for x in tokens[pos:pos + k])
        pos += k
        if len(L) != k:
            raise ValueError("truncated line")
        lines.append(L)
    if pos != len(tokens):
        raise ValueError("trailing tokens in board file")
    return n, lines


def verify_plane_axioms(n: int, lines, q: int):
    b = len(lines)
    line_sets = [frozenset(L) for L in lines]
    covered = set()
    for S in line_sets:
        covered |= S
    pair_count = Counter()
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2):
            pair_count[(u, v)] += 1
    deg = Counter()
    for L in lines:
        for p in L:
            deg[p] += 1
    inter_hist = Counter()
    for i in range(b):
        for j in range(i + 1, b):
            inter_hist[len(line_sets[i] & line_sets[j])] += 1

    expected_n = q * q + q + 1
    every_pair_once = (
        len(pair_count) == n * (n - 1) // 2
        and all(c == 1 for c in pair_count.values())
    )
    ok = (
        n == expected_n
        and b == expected_n
        and all(len(L) == q + 1 for L in lines)
        and len(set(line_sets)) == b
        and covered == set(range(n))
        and every_pair_once
        and all(deg[p] == q + 1 for p in range(n))
        and set(inter_hist) == {1}
    )
    return {
        "n": n,
        "b": b,
        "expected_n": expected_n,
        "expected_b": expected_n,
        "line_lengths": sorted(set(len(L) for L in lines)),
        "expected_line_length": q + 1,
        "distinct_lines": len(set(line_sets)),
        "all_points_covered": covered == set(range(n)),
        "point_pair_total": len(pair_count),
        "expected_point_pair_total": n * (n - 1) // 2,
        "every_point_pair_on_exactly_one_line": every_pair_once,
        "point_degree_values": sorted(set(deg.values())),
        "every_point_on_q_plus_1_lines": all(deg[p] == q + 1 for p in range(n)),
        "every_line_pair_meets_in_exactly_one_point": set(inter_hist) == {1},
        "line_pair_intersection_size_histogram": {
            str(k): v for k, v in sorted(inter_hist.items())
        },
        "ok": ok,
    }


def find_isomorphism(n: int, board_lines, F: Field, plane):
    """Find an explicit bijection board points -> canonical PG(2,q) points.

    Four board points in general position are fixed to the standard canonical
    frame; all remaining images are then found by constraint propagation with
    backtracking (MRV).
    """
    point_lines = [[] for _ in range(n)]
    pair_line_b = {}
    for li, L in enumerate(board_lines):
        for p in L:
            point_lines[p].append(li)
        for u, v in itertools.combinations(sorted(L), 2):
            pair_line_b[(u, v)] = li

    def line_of(u, v):
        if u > v:
            u, v = v, u
        return pair_line_b[(u, v)]

    a1, a2 = 0, 1
    l12 = line_of(a1, a2)
    set12 = set(board_lines[l12])
    a3 = next(p for p in range(n) if p not in set12)
    l13 = line_of(a1, a3)
    l23 = line_of(a2, a3)
    forbidden = set12 | set(board_lines[l13]) | set(board_lines[l23])
    a4 = next(p for p in range(n) if p not in forbidden)
    frame_board = [a1, a2, a3, a4]
    frame_canonical = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]

    index = plane["index"]
    mapping = {}
    used = set()
    for p, v in zip(frame_board, frame_canonical):
        ci = index[v]
        mapping[p] = ci
        used.add(ci)

    canon_line_sets = plane["line_sets"]
    canon_pair_line = plane["pair_line"]

    def candidates(p):
        required = []
        for li in point_lines[p]:
            imgs = [mapping[q] for q in board_lines[li] if q in mapping]
            if len(imgs) >= 2:
                u, v = imgs[0], imgs[1]
                if u > v:
                    u, v = v, u
                required.append(canon_pair_line[(u, v)])
        out = []
        for c in range(n):
            if c in used:
                continue
            ok = True
            for cl in required:
                if c not in canon_line_sets[cl]:
                    ok = False
                    break
            if ok:
                out.append(c)
        return out

    def dfs():
        if len(mapping) == n:
            return True
        best_p = -1
        best = None
        for p in range(n):
            if p in mapping:
                continue
            cc = candidates(p)
            if best is None or len(cc) < len(best):
                best_p, best = p, cc
                if not cc:
                    return False
                if len(cc) == 1:
                    break
        for c in best:
            mapping[best_p] = c
            used.add(c)
            if dfs():
                return True
            del mapping[best_p]
            used.remove(c)
        return False

    if not dfs():
        return None

    phi = [mapping[p] for p in range(n)]
    coords = [plane["points"][phi[p]] for p in range(n)]
    all_canonical_lines = set(canon_line_sets)
    verified = sorted(phi) == list(range(n))
    for L in board_lines:
        if frozenset(phi[p] for p in L) not in all_canonical_lines:
            verified = False
            break
    return {
        "phi": phi,
        "coords": coords,
        "frame_board": frame_board,
        "frame_canonical": [list(v) for v in frame_canonical],
        "verified": verified,
    }


# ---------------------------------------------------------------------------
# Projective matrices and PGL(3,q)
# ---------------------------------------------------------------------------

def canon_mat(M, F: Field):
    """Canonical representative of a non-zero matrix up to a scalar."""
    inv, mul = F.inv, F.mul
    for x in M:
        if x:
            ix = inv[x]
            return tuple(mul[y][ix] for y in M)
    raise ValueError("zero matrix")


def matmul(A, B, add, mul):
    C = [0] * 9
    for i in range(3):
        ai = 3 * i
        a0, a1, a2 = A[ai], A[ai + 1], A[ai + 2]
        for j in range(3):
            C[ai + j] = add[add[mul[a0][B[j]]][mul[a1][B[3 + j]]]][mul[a2][B[6 + j]]]
    return tuple(C)


def pgl_generators(F: Field):
    """Elementary transvections x_i <- x_i + a x_j plus diag(g,1,1).

    Coefficients 1 and a primitive element are used, so that for q=4 the
    generated group contains elementary transvections for every coefficient
    and hence all of SL(3,4); the diagonal matrix adds the scalars, giving GL
    and projectively PGL(3,q).
    """
    I = (1, 0, 0, 0, 1, 0, 0, 0, 1)
    coeffs = [1, F.primitive]
    gens = []
    desc = []
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            for a in coeffs:
                M = list(I)
                M[3 * i + j] = a
                gens.append(canon_mat(tuple(M), F))
                desc.append(f"x{i}_new = x{i} + {a}*x{j}")
    M = list(I)
    M[0] = F.primitive
    gens.append(canon_mat(tuple(M), F))
    desc.append("diag(g,1,1), g a generator of F_q^*")

    ugens, udesc = [], []
    seen = set()
    for M, d in zip(gens, desc):
        if M in seen:
            continue
        seen.add(M)
        ugens.append(M)
        udesc.append(d)
    return ugens, udesc


def projective_group_order(F: Field, gens):
    """BFS over projective matrices; returns the order of the generated group."""
    inv, mul, add = F.inv, F.mul, F.add
    ident = canon_mat((1, 0, 0, 0, 1, 0, 0, 0, 1), F)
    seen = {ident}
    frontier = [ident]
    while frontier:
        new = []
        for A in frontier:
            for B in gens:
                C = matmul(B, A, add, mul)
                for x in C:
                    if x:
                        ix = inv[x]
                        C = (
                            mul[C[0]][ix], mul[C[1]][ix], mul[C[2]][ix],
                            mul[C[3]][ix], mul[C[4]][ix], mul[C[5]][ix],
                            mul[C[6]][ix], mul[C[7]][ix], mul[C[8]][ix],
                        )
                        break
                if C not in seen:
                    seen.add(C)
                    new.append(C)
        frontier = new
    return len(seen)


def matrix_perm(M, coords, index, n: int, F: Field):
    """Permutation of the board points induced by the projective matrix M."""
    add, mul, inv = F.add, F.mul, F.inv
    m0, m1, m2, m3, m4, m5, m6, m7, m8 = M
    perm = [0] * n
    for p, (x, y, z) in enumerate(coords):
        u0 = add[add[mul[m0][x]][mul[m1][y]]][mul[m2][z]]
        u1 = add[add[mul[m3][x]][mul[m4][y]]][mul[m5][z]]
        u2 = add[add[mul[m6][x]][mul[m7][y]]][mul[m8][z]]
        if u0:
            i0 = inv[u0]
            v = (1, mul[u1][i0], mul[u2][i0])
        elif u1:
            i1 = inv[u1]
            v = (0, 1, mul[u2][i1])
        else:
            v = (0, 0, 1)
        perm[p] = index[v]
    return perm


# ---------------------------------------------------------------------------
# Set enumeration, blocking sets, group orbits
# ---------------------------------------------------------------------------

def enumerate_safe(n: int, line_masks, size: int, cap: int):
    """All ``size``-subsets of the n points meeting every line in <= cap points."""
    bits = [1 << p for p in range(n)]
    safe = []
    for comb in itertools.combinations(bits, size):
        m = sum(comb)
        for lm in line_masks:
            if (m & lm).bit_count() > cap:
                break
        else:
            safe.append(m)
    return safe


def maximal_safe(safe_masks, line_masks, n: int, cap: int):
    """Filter safe masks that are maximal by inclusion among all safe sets."""
    all_mask = (1 << n) - 1
    maximal = []
    for m in safe_masks:
        blocked = 0
        for lm in line_masks:
            if (m & lm).bit_count() == cap:
                blocked |= lm
        outside = all_mask ^ m
        if (outside & (all_mask ^ blocked)) == 0:
            maximal.append(m)
    return maximal


def line_profile(mask: int, line_masks):
    hist = Counter()
    for lm in line_masks:
        hist[(mask & lm).bit_count()] += 1
    return {k: hist[k] for k in sorted(hist)}


def profile_str(history) -> str:
    return ",".join(f"{k}:{history[k]}" for k in sorted(history))


def mask_points(mask: int):
    pts = []
    p = 0
    while mask:
        if mask & 1:
            pts.append(p)
        mask >>= 1
        p += 1
    return pts


def is_blocking(mask: int, line_masks) -> bool:
    return all((mask & lm) != 0 for lm in line_masks)


def is_minimal_blocking(mask: int, line_masks) -> bool:
    if not is_blocking(mask, line_masks):
        return False
    rest = mask
    while rest:
        b = rest & -rest
        rest ^= b
        if is_blocking(mask ^ b, line_masks):
            return False
    return True


def enumerate_minimal_fold_blocking(n: int, line_masks, size: int, fold: int):
    """Directly enumerate minimal ``fold``-fold blocking sets of given size.

    A set X is fold-fold blocking if every line meets it in at least ``fold``
    points; it is minimal if for every x in X some line meets X in exactly
    ``fold`` points at x.  This is an independent route that does not go
    through safe-set enumeration or complementation.
    """
    bits = [1 << p for p in range(n)]
    found = []
    for comb in itertools.combinations(bits, size):
        m = sum(comb)
        ok = True
        tight = 0
        for lm in line_masks:
            k = (m & lm).bit_count()
            if k < fold:
                ok = False
                break
            if k == fold:
                tight |= lm
        if ok and (tight & m) == m:
            found.append(m)
    return found


def image_mask(mask: int, perm, n: int) -> int:
    out = 0
    i = 0
    while mask:
        if mask & 1:
            out |= 1 << perm[i]
        mask >>= 1
        i += 1
    return out


def compute_orbits(masks, perms, n: int):
    """Orbits of a set of masks under the permutation group generated by perms."""
    unvisited = set(masks)
    orbits = []
    while unvisited:
        start = next(iter(unvisited))
        unvisited.remove(start)
        orb = [start]
        stack = [start]
        while stack:
            m = stack.pop()
            for perm in perms:
                im = image_mask(m, perm, n)
                if im in unvisited:
                    unvisited.remove(im)
                    orb.append(im)
                    stack.append(im)
        orb.sort()
        orbits.append(orb)
    orbits.sort(key=len, reverse=True)
    return orbits


# ---------------------------------------------------------------------------
# Verification driver
# ---------------------------------------------------------------------------

def ck(checks, name, actual, expected):
    checks[name] = {
        "actual": actual,
        "expected": expected,
        "pass": bool(actual == expected),
    }
    return actual == expected


def verdict_of(checks) -> str:
    return "PASS" if all(item["pass"] for item in checks.values()) else "FAIL"


def failed_checks(claim_name, checks):
    out = []
    for name, item in checks.items():
        if not item["pass"]:
            out.append(
                f"{claim_name}.{name}: expected {item['expected']!r}, "
                f"got {item['actual']!r}"
            )
    return out


def write_json(path: Path, obj) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main() -> int:
    t0 = time.perf_counter()
    print("=" * 74)
    print("Independent verification: PGL orbits and structures in PG(2,3), PG(2,4)")
    print("=" * 74)

    self_test_fields()
    print("[1/7] F_3 / GF(4) arithmetic self-tests: ok")

    F3 = Field(3)
    F4 = Field(4)
    plane3 = build_canonical_pg2(F3)
    plane4 = build_canonical_pg2(F4)
    print(
        f"[2/7] canonical construction: PG(2,3) "
        f"{len(plane3['points'])} points / {len(plane3['lines'])} lines; "
        f"PG(2,4) {len(plane4['points'])} points / {len(plane4['lines'])} lines"
    )

    # -- boards ------------------------------------------------------------
    n3, lines3 = parse_board(OUTPUT / "board_pg2q3.txt")
    n4, lines4 = parse_board(OUTPUT / "board_pg2q4.txt")
    ax3 = verify_plane_axioms(n3, lines3, 3)
    ax4 = verify_plane_axioms(n4, lines4, 4)
    if not ax3["ok"]:
        raise RuntimeError("board_pg2q3.txt fails the PG(2,3) axioms")
    if not ax4["ok"]:
        raise RuntimeError("board_pg2q4.txt fails the PG(2,4) axioms")
    print("[3/7] board files satisfy the projective-plane axioms: ok")

    iso3 = find_isomorphism(n3, lines3, F3, plane3)
    iso4 = find_isomorphism(n4, lines4, F4, plane4)
    if iso3 is None or not iso3["verified"]:
        raise RuntimeError("board_pg2q3.txt is not isomorphic to F_3^3 construction")
    if iso4 is None or not iso4["verified"]:
        raise RuntimeError("board_pg2q4.txt is not isomorphic to F_4^3 construction")
    print("[4/7] explicit isomorphisms to F_q^3 construction found and verified: ok")

    # -- PGL ---------------------------------------------------------------
    gens3, desc3 = pgl_generators(F3)
    gens4, desc4 = pgl_generators(F4)
    order3 = projective_group_order(F3, gens3)
    print(f"      generated projective matrix group for q=3: order {order3}")
    order4 = projective_group_order(F4, gens4)
    print(f"      generated projective matrix group for q=4: order {order4}")
    if order3 != EXPECTED_PGL_ORDER[3]:
        raise RuntimeError(f"generated group for q=3 has order {order3}, not 5616")
    if order4 != EXPECTED_PGL_ORDER[4]:
        raise RuntimeError(f"generated group for q=4 has order {order4}, not 60480")

    perms3 = [matrix_perm(M, iso3["coords"], plane3["index"], n3, F3) for M in gens3]
    perms4 = [matrix_perm(M, iso4["coords"], plane4["index"], n4, F4) for M in gens4]
    for perms, n in ((perms3, n3), (perms4, n4)):
        for perm in perms:
            assert sorted(perm) == list(range(n)), "generator does not induce a permutation"
    print("      generator matrices induce point permutations: ok")

    line_masks3 = [sum(1 << p for p in L) for L in lines3]
    line_masks4 = [sum(1 << p for p in L) for L in lines4]
    all3 = (1 << n3) - 1
    all4 = (1 << n4) - 1

    # =====================================================================
    # Claim A : PG(2,3)
    # =====================================================================
    print("-" * 74)
    print("[5/7] claim A: PG(2,3), maximal safe 7-sets and complete quadrilaterals")
    safe7 = enumerate_safe(n3, line_masks3, 7, 3)
    max7 = maximal_safe(safe7, line_masks3, n3, 3)
    comps6 = [all3 ^ m for m in max7]
    print(
        f"      safe 7-sets: {len(safe7)}; maximal safe 7-sets: {len(max7)}; "
        f"complement six-sets: {len(comps6)}"
    )

    tri_hist = Counter()
    all_exactly_four = True
    all_general_position = True
    all_vertex_union = True
    quad_lines_for = {}
    for S in comps6:
        tri = [li for li, lm in enumerate(line_masks3) if (S & lm).bit_count() == 3]
        tri_hist[len(tri)] += 1
        if len(tri) != 4:
            all_exactly_four = False
            all_general_position = False
            all_vertex_union = False
            continue
        inter_masks = []
        ok = True
        for a, b in itertools.combinations([line_masks3[li] for li in tri], 2):
            pm = a & b
            if pm.bit_count() != 1:
                ok = False
                break
            inter_masks.append(pm)
        if not ok or len(set(inter_masks)) != 6:
            all_general_position = False
            continue
        v = 0
        for pm in inter_masks:
            v |= pm
        if v != S:
            all_vertex_union = False
        quad_lines_for[S] = tri

    quad_general = 0
    quad_vertices = set()
    for quad in itertools.combinations(range(n3), 4):
        inter_masks = []
        ok = True
        for a, b in itertools.combinations(quad, 2):
            pm = line_masks3[a] & line_masks3[b]
            if pm.bit_count() != 1:
                ok = False
                break
            inter_masks.append(pm)
        if ok and len(set(inter_masks)) == 6:
            quad_general += 1
            v = 0
            for pm in inter_masks:
                v |= pm
            quad_vertices.add(v)

    blocking_count = sum(1 for S in comps6 if is_blocking(S, line_masks3))
    minimal_count = sum(1 for S in comps6 if is_minimal_blocking(S, line_masks3))
    minblock6_direct = enumerate_minimal_fold_blocking(n3, line_masks3, 6, 1)
    print(
        f"      direct enumeration of 6-point minimal blocking sets: "
        f"{len(minblock6_direct)}"
    )
    formula_A = math.comb(13, 4) - 13 * math.comb(4, 3) * 9 - 13
    orbits3 = compute_orbits(comps6, perms3, n3)

    checks_A = {}
    ck(checks_A, "board_satisfies_PG_2_3_axioms", ax3["ok"], True)
    ck(checks_A, "board_isomorphic_to_F3_cubed_construction", iso3["verified"], True)
    ck(checks_A, "PGL_3_3_order_computed", order3, 5616)
    ck(checks_A, "maximal_safe_7_set_count", len(max7), 234)
    ck(checks_A, "complement_six_sets_distinct", len(set(comps6)), 234)
    ck(
        checks_A,
        "three_point_line_count_histogram",
        {str(k): tri_hist[k] for k in sorted(tri_hist)},
        {"4": 234},
    )
    ck(checks_A, "every_six_set_has_exactly_four_three_point_lines", all_exactly_four, True)
    ck(checks_A, "those_four_lines_are_in_general_position", all_general_position, True)
    ck(checks_A, "six_set_equals_the_six_pairwise_intersections", all_vertex_union, True)
    ck(checks_A, "general_position_line_quadruple_count", quad_general, 234)
    ck(checks_A, "distinct_quadrilateral_vertex_sets", len(quad_vertices), 234)
    ck(
        checks_A,
        "complements_equal_quadrilateral_vertex_sets",
        set(comps6) == quad_vertices,
        True,
    )
    ck(checks_A, "formula_C13_4_minus_13C43_9_minus_13", formula_A, 234)
    ck(checks_A, "all_complements_are_blocking", blocking_count, 234)
    ck(checks_A, "all_complements_are_minimal_blocking", minimal_count, 234)
    ck(checks_A, "direct_minimal_blocking_six_set_count", len(minblock6_direct), 234)
    ck(
        checks_A,
        "direct_minimal_blocking_sets_equal_complements",
        set(minblock6_direct) == set(comps6),
        True,
    )
    ck(checks_A, "orbit_count_under_PGL_3_3", len(orbits3), 1)
    ck(checks_A, "single_orbit_size", len(orbits3[0]) if orbits3 else None, 234)

    rep_A = min(comps6)
    data_A = {
        "board": "PG(2,3)",
        "n_points": n3,
        "n_lines": len(lines3),
        "pgl_order_computed": order3,
        "pgl_order_expected": 5616,
        "generator_count": len(gens3),
        "generator_descriptions": desc3,
        "safe_7_sets": len(safe7),
        "maximal_safe_7_sets": len(max7),
        "complement_six_sets": len(comps6),
        "three_point_line_count_histogram": {
            str(k): tri_hist[k] for k in sorted(tri_hist)
        },
        "general_position_line_quadruples": quad_general,
        "distinct_quadrilateral_vertex_sets": len(quad_vertices),
        "blocking_six_sets": blocking_count,
        "minimal_blocking_six_sets": minimal_count,
        "direct_minimal_blocking_six_sets": len(minblock6_direct),
        "direct_minimal_blocking_equals_complements": set(minblock6_direct) == set(comps6),
        "quadrilateral_count_formula": {
            "C(13,4)": math.comb(13, 4),
            "subtract_triples_concurrent": 13 * math.comb(4, 3) * 9,
            "subtract_all_four_concurrent": 13,
            "value": formula_A,
        },
        "orbit_sizes": [len(o) for o in orbits3],
        "representative": {
            "mask": rep_A,
            "points": mask_points(rep_A),
            "three_point_lines_as_point_sets": [
                list(lines3[li]) for li in quad_lines_for.get(rep_A, [])
            ],
        },
    }
    A = {"claim": "A", "verdict": verdict_of(checks_A), "checks": checks_A, "data": data_A}
    print(f"      claim A: {A['verdict']}")

    # =====================================================================
    # Claim B : PG(2,4)
    # =====================================================================
    print("-" * 74)
    print("[6/7] claim B: PG(2,4), maximal safe 9-sets and their three PGL orbits")
    safe9 = enumerate_safe(n4, line_masks4, 9, 3)
    print(f"      safe 9-sets: {len(safe9)}")
    max9 = maximal_safe(safe9, line_masks4, n4, 3)
    comps12 = [all4 ^ m for m in max9]
    print(
        f"      maximal safe 9-sets: {len(max9)}; complement twelve-sets: "
        f"{len(comps12)}"
    )

    prof_hist = Counter()
    min_line_intersection = 99
    for S in comps12:
        prof = line_profile(S, line_masks4)
        prof_hist[profile_str(prof)] += 1
        min_line_intersection = min(min_line_intersection, min(prof))
    prof_hist_json = {k: prof_hist[k] for k in sorted(prof_hist)}
    print(f"      complement profiles: {prof_hist_json}")

    orbits4 = compute_orbits(comps12, perms4, n4)
    orbit_info = []
    for orb in orbits4:
        prof = line_profile(orb[0], line_masks4)
        uniform = all(line_profile(m, line_masks4) == prof for m in orb)
        orbit_info.append(
            {
                "size": len(orb),
                "profile": {str(k): v for k, v in prof.items()},
                "profile_string": profile_str(prof),
                "profile_uniform_in_orbit": uniform,
                "representative_mask": orb[0],
                "representative_points": mask_points(orb[0]),
            }
        )
    print(
        "      PGL(3,4) orbits: "
        + ", ".join(f"{o['size']} ({o['profile_string']})" for o in orbit_info)
    )

    expected_profile_hist = {
        "2:10,3:6,4:3,5:2": 10080,
        "2:9,3:9,5:3": 1120,
        "2:12,4:9": 280,
    }
    actual_size_profiles = sorted(
        (len(orb), profile_str(line_profile(orb[0], line_masks4)))
        for orb in orbits4
    )
    expected_size_profiles = sorted(
        [(10080, "2:10,3:6,4:3,5:2"),
         (1120, "2:9,3:9,5:3"),
         (280, "2:12,4:9")]
    )
    triangle_orbit = next((o for o in orbits4 if len(o) == 1120), None)

    # Independent route: directly enumerate minimal 2-fold blocking 12-sets.
    minblock12_direct = enumerate_minimal_fold_blocking(n4, line_masks4, 12, 2)
    print(
        f"      direct enumeration of 12-point minimal 2-fold blocking sets: "
        f"{len(minblock12_direct)}"
    )

    checks_B = {}
    ck(checks_B, "board_satisfies_PG_2_4_axioms", ax4["ok"], True)
    ck(checks_B, "board_isomorphic_to_F4_cubed_construction", iso4["verified"], True)
    ck(checks_B, "PGL_3_4_order_computed", order4, 60480)
    ck(checks_B, "maximal_safe_9_set_count", len(max9), 11480)
    ck(checks_B, "complement_twelve_sets_distinct", len(set(comps12)), 11480)
    ck(checks_B, "complement_profile_multiplicities", prof_hist_json, expected_profile_hist)
    ck(checks_B, "orbit_count_under_PGL_3_4", len(orbits4), 3)
    ck(checks_B, "orbit_sizes", sorted(len(o) for o in orbits4), [280, 1120, 10080])
    ck(checks_B, "orbit_size_profile_multiset", actual_size_profiles, expected_size_profiles)
    ck(
        checks_B,
        "profile_uniform_within_each_orbit",
        all(o["profile_uniform_in_orbit"] for o in orbit_info),
        True,
    )
    ck(checks_B, "minimum_line_intersection_of_complements", min_line_intersection, 2)
    ck(checks_B, "triangle_orbit_exists", triangle_orbit is not None, True)
    ck(checks_B, "direct_minimal_2fold_blocking_12_set_count", len(minblock12_direct), 11480)
    ck(
        checks_B,
        "direct_minimal_2fold_blocking_sets_equal_complements",
        set(minblock12_direct) == set(comps12),
        True,
    )

    data_B = {
        "board": "PG(2,4)",
        "n_points": n4,
        "n_lines": len(lines4),
        "pgl_order_computed": order4,
        "pgl_order_expected": 60480,
        "generator_count": len(gens4),
        "generator_descriptions": desc4,
        "safe_9_sets": len(safe9),
        "maximal_safe_9_sets": len(max9),
        "complement_twelve_sets": len(comps12),
        "complement_profile_histogram": prof_hist_json,
        "direct_minimal_2fold_blocking_12_sets": len(minblock12_direct),
        "direct_minimal_2fold_blocking_equals_complements": set(minblock12_direct) == set(comps12),
        "orbit_count": len(orbits4),
        "orbits": orbit_info,
    }
    B = {"claim": "B", "verdict": verdict_of(checks_B), "checks": checks_B, "data": data_B}
    print(f"      claim B: {B['verdict']}")

    # =====================================================================
    # Claim C : PG(2,4) triangles
    # =====================================================================
    print("-" * 74)
    print("[7/7] claim C: PG(2,4), unions of three lines in general position")
    triangle_unions = []
    triangle_triples = []
    concurrent_triples = 0
    for comb in itertools.combinations(range(n4), 3):
        a, b, c = comb
        if line_masks4[a] & line_masks4[b] & line_masks4[c]:
            concurrent_triples += 1
            continue
        triangle_unions.append(
            line_masks4[a] | line_masks4[b] | line_masks4[c]
        )
        triangle_triples.append(comb)
    print(
        f"      concurrent line triples: {concurrent_triples}; "
        f"general-position line triples: {len(triangle_unions)}"
    )

    formula_C = math.comb(21, 3) - 21 * math.comb(5, 3)
    all_twelve_points = all(u.bit_count() == 12 for u in triangle_unions)
    distinct_unions = len(set(triangle_unions))
    triangle_set = set(triangle_unions)
    complement_set = set(comps12)
    triangle_profile = {str(k): v for k, v in line_profile(triangle_unions[0], line_masks4).items()}
    all_triangle_profile = all(
        line_profile(u, line_masks4) == line_profile(triangle_unions[0], line_masks4)
        for u in triangle_unions
    )
    triangle_complements_maximal = all((all4 ^ u) in set(max9) for u in triangle_unions)

    checks_C = {}
    ck(checks_C, "board_satisfies_PG_2_4_axioms", ax4["ok"], True)
    ck(checks_C, "board_isomorphic_to_F4_cubed_construction", iso4["verified"], True)
    ck(checks_C, "PGL_3_4_order_computed", order4, 60480)
    ck(checks_C, "triangle_count", len(triangle_unions), 1120)
    ck(checks_C, "concurrent_line_triple_count", concurrent_triples, 210)
    ck(checks_C, "formula_C21_3_minus_21C53", formula_C, 1120)
    ck(checks_C, "all_unions_are_twelve_points", all_twelve_points, True)
    ck(checks_C, "distinct_triangle_unions", distinct_unions, 1120)
    ck(checks_C, "triangle_unions_subset_of_maximal_complements", triangle_set <= complement_set, True)
    ck(checks_C, "triangle_complements_are_maximal_safe", triangle_complements_maximal, True)
    ck(checks_C, "triangle_union_profile", triangle_profile, {"2": 9, "3": 9, "5": 3})
    ck(checks_C, "all_triangle_unions_have_same_profile", all_triangle_profile, True)
    ck(checks_C, "triangles_equal_1120_orbit", triangle_set == set(triangle_orbit) if triangle_orbit else False, True)
    ck(checks_C, "triangles_form_single_PGL_orbit", len(triangle_set) == 1120, True)

    data_C = {
        "board": "PG(2,4)",
        "pgl_order_computed": order4,
        "pgl_order_expected": 60480,
        "triangle_count": len(triangle_unions),
        "concurrent_line_triples": concurrent_triples,
        "formula": {
            "C(21,3)": math.comb(21, 3),
            "21*C(5,3)": 21 * math.comb(5, 3),
            "value": formula_C,
        },
        "distinct_unions": distinct_unions,
        "all_unions_have_12_points": all_twelve_points,
        "triangle_union_profile": triangle_profile,
        "triangles_equal_orbit_size_1120": triangle_set == set(triangle_orbit) if triangle_orbit else False,
        "representatives": [
            {"lines": list(tri), "union_mask": line_masks4[tri[0]] | line_masks4[tri[1]] | line_masks4[tri[2]]}
            for tri in triangle_triples[:5]
        ],
    }
    C = {"claim": "C", "verdict": verdict_of(checks_C), "checks": checks_C, "data": data_C}
    print(f"      claim C: {C['verdict']}")

    # -- output ------------------------------------------------------------
    runtime = time.perf_counter() - t0
    discrepancies = []
    discrepancies += failed_checks("A", checks_A)
    discrepancies += failed_checks("B", checks_B)
    discrepancies += failed_checks("C", checks_C)
    group_ok = order3 == 5616 and order4 == 60480
    if not group_ok:
        discrepancies.append(
            f"group order mismatch: q=3 {order3} (want 5616), q=4 {order4} (want 60480)"
        )
    overall = "PASS" if (A["verdict"] == B["verdict"] == C["verdict"] == "PASS" and group_ok) else "FAIL"

    board_info = {
        "q3": {
            "file": str(OUTPUT / "board_pg2q3.txt"),
            "axioms": ax3,
            "isomorphic_to_F3_cubed_construction": iso3["verified"],
            "frame_board_points": iso3["frame_board"],
            "frame_canonical_vectors": iso3["frame_canonical"],
        },
        "q4": {
            "file": str(OUTPUT / "board_pg2q4.txt"),
            "axioms": ax4,
            "isomorphic_to_F4_cubed_construction": iso4["verified"],
            "frame_board_points": iso4["frame_board"],
            "frame_canonical_vectors": iso4["frame_canonical"],
        },
    }
    summary = {
        "meta": {
            "title": "Independent verification of PGL orbits for minimal blocking sets in PG(2,3), PG(2,4)",
            "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "runtime_seconds": round(runtime, 2),
            "python_version": sys.version.split()[0],
            "script": str(Path(__file__).resolve()),
            "standard_library_only": True,
            "reads_experiment_scripts": False,
            "reads_output_orbits_json": False,
        },
        "group_orders": {
            "PGL(3,3)": {
                "computed": order3,
                "expected": 5616,
                "generator_count": len(gens3),
                "pass": order3 == 5616,
            },
            "PGL(3,4)": {
                "computed": order4,
                "expected": 60480,
                "generator_count": len(gens4),
                "pass": order4 == 60480,
            },
        },
        "boards": board_info,
        "claims": {
            "A": {"verdict": A["verdict"], "checks": checks_A},
            "B": {"verdict": B["verdict"], "checks": checks_B},
            "C": {"verdict": C["verdict"], "checks": checks_C},
        },
        "discrepancies": discrepancies,
        "overall_verdict": overall,
        "files": ["results_A.json", "results_B.json", "results_C.json", "results_summary.json"],
    }
    write_json(HERE / "results_A.json", A)
    write_json(HERE / "results_B.json", B)
    write_json(HERE / "results_C.json", C)
    write_json(HERE / "results_summary.json", summary)

    print("=" * 74)
    print(f"group order PGL(3,3): {order3} (expected 5616)")
    print(f"group order PGL(3,4): {order4} (expected 60480)")
    print(f"claim A: {A['verdict']}")
    print(f"claim B: {B['verdict']}")
    print(f"claim C: {C['verdict']}")
    print(f"overall: {overall}")
    if discrepancies:
        print("DISCREPANCIES:")
        for d in discrepancies:
            print("  - " + d)
    else:
        print("No discrepancies.")
    print(f"runtime: {runtime:.2f} s")
    print(f"outputs written to: {HERE}")
    print("=" * 74)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
