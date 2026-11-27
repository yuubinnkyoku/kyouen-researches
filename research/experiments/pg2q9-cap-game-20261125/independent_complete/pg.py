"""Independent utilities for the PG(2,9) cap-game verification.

Everything here is written from scratch (Python standard library only).
No parent code is imported.  The published board file is treated as an
unlabelled incidence structure: its axioms are checked, and an explicit
line-preserving bijection to an independently constructed PG(2,9) is found.

Field model: GF(9) = GF(3)[x]/(x^2+1), elements 0..8 encode a + b*x with
a = e % 3, b = e // 3.  Thus x = 3 and x^2 = -1 = 2.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
BOARD_PATH = EXP / "output" / "board_pg2q9.txt"
CENSUS_PATH = EXP / "output" / "census_pg2q9.txt"

# ---------------------------------------------------------------------------
# GF(9)
# ---------------------------------------------------------------------------

GF_Q = 9


def gf_add(a: int, b: int) -> int:
    return ((a % 3 + b % 3) % 3) + 3 * (((a // 3) + (b // 3)) % 3)


def gf_neg(a: int) -> int:
    return ((-(a % 3)) % 3) + 3 * ((-(a // 3)) % 3)


def gf_mul(a: int, b: int) -> int:
    a0, a1 = a % 3, a // 3
    b0, b1 = b % 3, b // 3
    # (a0 + a1 x)(b0 + b1 x) = a0 b0 - a1 b1 + (a0 b1 + a1 b0) x
    return ((a0 * b0 - a1 * b1) % 3) + 3 * ((a0 * b1 + a1 * b0) % 3)


GF_MUL = [[gf_mul(a, b) for b in range(9)] for a in range(9)]
GF_ADD = [[gf_add(a, b) for b in range(9)] for a in range(9)]


def gf_inv(a: int) -> int:
    if a == 0:
        raise ZeroDivisionError
    for b in range(1, 9):
        if GF_MUL[a][b] == 1:
            return b
    raise AssertionError


GF_INV = [None] + [gf_inv(a) for a in range(1, 9)]


def gf_pow(a: int, n: int) -> int:
    r = 1
    while n:
        if n & 1:
            r = GF_MUL[r][a]
        a = GF_MUL[a][a]
        n >>= 1
    return r


def check_field() -> dict:
    """Exhaustively verify the GF(9) axioms for the 9-element table."""
    ok_add = all(
        GF_ADD[a][b] == GF_ADD[b][a] for a in range(9) for b in range(9)
    )
    ok_add_assoc = all(
        GF_ADD[GF_ADD[a][b]][c] == GF_ADD[a][GF_ADD[b][c]]
        for a in range(9)
        for b in range(9)
        for c in range(9)
    )
    ok_mul = all(
        GF_MUL[a][b] == GF_MUL[b][a] for a in range(9) for b in range(9)
    )
    ok_mul_assoc = all(
        GF_MUL[GF_MUL[a][b]][c] == GF_MUL[a][GF_MUL[b][c]]
        for a in range(9)
        for b in range(9)
        for c in range(9)
    )
    ok_distrib = all(
        GF_MUL[a][GF_ADD[b][c]] == GF_ADD[GF_MUL[a][b]][GF_MUL[a][c]]
        for a in range(9)
        for b in range(9)
        for c in range(9)
    )
    ok_inv = all(GF_MUL[a][GF_INV[a]] == 1 for a in range(1, 9))
    ok_no_zero_div = all(
        GF_MUL[a][b] != 0 for a in range(1, 9) for b in range(1, 9)
    )
    # x^2 = -1, x^2+1 has no root in GF(3)
    x = 3
    ok_x = GF_MUL[x][x] == 2
    # x^2+1 must have no root in the base field GF(3)
    ok_irred = all(GF_ADD[GF_MUL[t][t]][1] != 0 for t in (0, 1, 2))
    # multiplicative group cyclic of order 8, with the expected order profile
    orders = {}
    for a in range(1, 9):
        o = 1
        v = a
        while v != 1:
            v = GF_MUL[v][a]
            o += 1
        orders[a] = o
    from collections import Counter

    profile = Counter(orders.values())
    ok_cyclic = profile.get(1, 0) == 1 and profile.get(2, 0) == 1 and \
        profile.get(4, 0) == 2 and profile.get(8, 0) == 4
    return {
        "add_commutative": ok_add,
        "add_associative": ok_add_assoc,
        "mul_commutative": ok_mul,
        "mul_associative": ok_mul_assoc,
        "distributive": ok_distrib,
        "inverses": ok_inv,
        "no_zero_divisors": ok_no_zero_div,
        "x_squared_is_minus_one": ok_x,
        "x2_plus_1_irreducible_over_F3": ok_irred,
        "mult_group_profile": {str(k): v for k, v in sorted(profile.items())},
        "mult_group_cyclic_order_8": ok_cyclic,
    }


# ---------------------------------------------------------------------------
# PG(2,9) model: points = canonical nonzero vectors, lines = kernels
# ---------------------------------------------------------------------------


def canonical_vector(v):
    """Normalise a nonzero 3-vector: first nonzero coordinate becomes 1."""
    for c in v:
        if c:
            inv = GF_INV[c]
            return tuple(GF_MUL[inv][x] for x in v)
    return None


def build_model():
    """Return (points, point_index, lines) for the GF(9) model of PG(2,9).

    points: list of canonical 3-tuples in a fixed order.
    lines:  list of tuples of point indices (the zero sets of the canonical
            nonzero covectors, in the same order as the covectors).
    """
    vecs = {}
    for v in itertools.product(range(9), repeat=3):
        if v == (0, 0, 0):
            continue
        c = canonical_vector(v)
        vecs[c] = True
    points = sorted(vecs)
    assert len(points) == 91, len(points)
    point_index = {p: i for i, p in enumerate(points)}

    covs = {}
    for u in itertools.product(range(9), repeat=3):
        if u == (0, 0, 0):
            continue
        c = canonical_vector(u)
        covs[c] = True
    covectors = sorted(covs)
    assert len(covectors) == 91

    lines = []
    for u in covectors:
        pts = []
        for i, v in enumerate(points):
            # dot product over GF(9)
            s = 0
            for a, b in zip(u, v):
                s = GF_ADD[s][GF_MUL[a][b]]
            if s == 0:
                pts.append(i)
        assert len(pts) == 10, (u, pts)
        lines.append(tuple(pts))
    return points, point_index, lines


# ---------------------------------------------------------------------------
# Board / incidence structure
# ---------------------------------------------------------------------------


def load_board(path=BOARD_PATH):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    n, b = map(int, lines[0].split())
    blocks = []
    for ln in lines[1:]:
        vals = list(map(int, ln.split()))
        assert vals[0] == len(vals) - 1, ln
        blocks.append(tuple(vals[1:]))
    return n, b, blocks


def incidence_data(n, blocks):
    """Validate basic shape and compute point->lines, line sets, pair lines."""
    assert len(blocks) == len(set(blocks)), "duplicate lines"
    for B in blocks:
        assert len(B) == len(set(B)), "repeated point on a line"
        assert all(0 <= p < n for p in B), "point out of range"
    line_sets = [frozenset(B) for B in blocks]
    point_lines = [[] for _ in range(n)]
    for li, B in enumerate(blocks):
        for p in B:
            point_lines[p].append(li)
    line_of_pair = {}
    for li, B in enumerate(blocks):
        for p, q in itertools.combinations(B, 2):
            key = (p, q) if p < q else (q, p)
            assert key not in line_of_pair, ("pair on two lines", key)
            line_of_pair[key] = li
    return {
        "line_sets": line_sets,
        "point_lines": point_lines,
        "line_of_pair": line_of_pair,
    }


def check_plane(n, b, blocks, expected_q=9):
    """Exhaustively check the axioms of a projective plane of order q."""
    res = {}
    res["n_points"] = n
    res["n_lines"] = b
    res["expected_n"] = expected_q * expected_q + expected_q + 1
    res["n_ok"] = n == b == res["expected_n"]
    sizes = sorted({len(B) for B in blocks})
    res["line_sizes"] = sizes
    res["line_sizes_ok"] = sizes == [expected_q + 1]
    assert len(blocks) == len(set(blocks))
    data = incidence_data(n, blocks)
    pl = data["point_lines"]
    res["point_degrees"] = sorted({len(x) for x in pl})
    res["point_degrees_ok"] = res["point_degrees"] == [expected_q + 1]
    # every point pair on exactly one line
    pairs = 0
    for p in range(n):
        seen = set()
        for li in pl[p]:
            for q in blocks[li]:
                if q != p:
                    seen.add(q)
        assert len(seen) == n - 1, (p, len(seen))
        pairs += len(seen)
    # line pairs meet exactly once
    bad_line_pairs = 0
    for i, j in itertools.combinations(range(b), 2):
        inter = len(data["line_sets"][i] & data["line_sets"][j])
        if inter != 1:
            bad_line_pairs += 1
    res["point_pairs_total"] = pairs // 2
    res["point_pairs_expected"] = n * (n - 1) // 2
    res["point_pairs_ok"] = pairs // 2 == n * (n - 1) // 2
    res["line_pairs_bad"] = bad_line_pairs
    res["line_pairs_ok"] = bad_line_pairs == 0
    res["all_ok"] = all(
        res[k]
        for k in [
            "n_ok",
            "line_sizes_ok",
            "point_degrees_ok",
            "point_pairs_ok",
            "line_pairs_ok",
        ]
    )
    return res, data


# ---------------------------------------------------------------------------
# Isomorphism board -> model
# ---------------------------------------------------------------------------


def _find_frame(points, line_of_pair):
    """First four points (in index order) with no three collinear."""
    for a, b, c, d in itertools.combinations(points, 4):
        pairs = [
            tuple(sorted((a, b))),
            tuple(sorted((a, c))),
            tuple(sorted((a, d))),
            tuple(sorted((b, c))),
            tuple(sorted((b, d))),
            tuple(sorted((c, d))),
        ]
        lines = [line_of_pair[p] for p in pairs]
        if len(set(lines)) == 6:
            return (a, b, c, d)
    raise AssertionError("no frame found")


def find_isomorphism(n, blocks, m_points, m_lines):
    """Find a bijection phi: board points -> model point indices preserving lines.

    Fixes an arbitrary ordered frame on each side (any frame extends uniquely
    when both planes are PG(2,9)) and propagates forced incidences, with
    backtracking on the most constrained unmapped point.
    """
    bdata = incidence_data(n, blocks)
    mdata = incidence_data(len(m_points), m_lines)
    b_line_of_pair = bdata["line_of_pair"]
    m_linesets = mdata["line_sets"]
    m_line_of_pair = mdata["line_of_pair"]
    b_frames = _find_frame(list(range(n)), b_line_of_pair)
    m_frames = _find_frame(list(range(len(m_points))), m_line_of_pair)

    b_lines = [tuple(B) for B in blocks]
    m_lines_l = [tuple(B) for B in m_lines]

    def pair(a, b):
        return (a, b) if a < b else (b, a)

    m_pair_line = {}
    for li, B in enumerate(m_lines_l):
        for a, b in itertools.combinations(B, 2):
            m_pair_line[pair(a, b)] = li

    m_linesets_set = frozenset(m_linesets)
    all_m = frozenset(range(len(m_points)))
    nodes = 0

    def propagate(assign, cand, used):
        """Close a partial map under forced incidences.  Mutates assign/cand/used."""
        while True:
            changed = False
            known = {}
            for li, B in enumerate(b_lines):
                mapped = [assign[p] for p in B if p in assign]
                if len(mapped) < 2:
                    continue
                ml = m_pair_line.get(pair(mapped[0], mapped[1]))
                if ml is None:
                    return False
                for x, y in itertools.combinations(mapped, 2):
                    if m_pair_line.get(pair(x, y)) != ml:
                        return False
                known[li] = ml
            for li, ml in known.items():
                target = set(m_linesets[ml]) - used
                unmapped = [p for p in b_lines[li] if p not in assign]
                if len(unmapped) != len(target):
                    return False
                for p in unmapped:
                    new = cand[p] & target
                    if not new:
                        return False
                    if new != cand[p]:
                        cand[p] = new
                        changed = True
            for p in range(n):
                if p in assign:
                    continue
                if not cand[p]:
                    return False
                if len(cand[p]) == 1:
                    mp = next(iter(cand[p]))
                    if mp in used:
                        return False
                    assign[p] = mp
                    used.add(mp)
                    changed = True
            if changed:
                for p in range(n):
                    if p in assign:
                        continue
                    if cand[p] & used:
                        cand[p] -= used
            if not changed:
                break
        if len(set(assign.values())) != len(assign):
            return False
        return True

    def rec(assign, cand, used):
        nonlocal nodes
        nodes += 1
        if nodes > 100000:
            raise RuntimeError("isomorphism search too large")
        if not propagate(assign, cand, used):
            return False
        if len(assign) == n:
            return all(
                frozenset(assign[p] for p in B) in m_linesets_set for B in b_lines
            )
        p = min(
            (q for q in range(n) if q not in assign),
            key=lambda q: len(cand[q]),
        )
        for mp in sorted(cand[p]):
            if mp in used:
                continue
            na = dict(assign)
            na[p] = mp
            nu = set(used)
            nu.add(mp)
            nc = [None if cand[i] is None else set(cand[i]) for i in range(n)]
            if rec(na, nc, nu):
                assign.clear()
                assign.update(na)
                used.clear()
                used.update(nu)
                return True
        return False

    assignment = {}
    used = set()
    for bp, mp in zip(b_frames, m_frames):
        assignment[bp] = mp
        used.add(mp)
    cand = [None] * n
    for p in range(n):
        if p not in assignment:
            cand[p] = set(all_m - used)
    if not rec(assignment, cand, used):
        raise RuntimeError("no isomorphism found")
    return assignment, b_frames, m_frames, nodes


def verify_isomorphism(phi, n, blocks, m_lines):
    """Check that phi maps every board line onto a model line and is bijective."""
    m_blocks = m_lines
    m_line_sets = {frozenset(B) for B in m_blocks}
    assert len(phi) == n
    assert len(set(phi.values())) == len(phi)
    for B in blocks:
        img = frozenset(phi[p] for p in B)
        if img not in m_line_sets:
            return False
    return True
