"""Conic transitivity and exhaustion of conic 6-subsets.

If PGL(3,9) is transitive on conics, then checking all 210 six-subsets of one
conic proves that every 6-subset of every conic has Grundy 0.  This supplies
the 'conic 6-child' step in the claimed proof that every 5-cap has G = 1.
"""

from __future__ import annotations

import json
import itertools
import time
from collections import Counter

import game
import group
import pg
from t8_conic_mechanism import nullspace

CONIC = [6, 9, 27, 32, 34, 37, 45, 75, 77, 82]


def eval_quadratic(coeffs, v):
    a, b, c, d, e, f = coeffs
    x, y, z = v
    terms = [
        pg.GF_MUL[a][pg.GF_MUL[x][x]],
        pg.GF_MUL[b][pg.GF_MUL[y][y]],
        pg.GF_MUL[c][pg.GF_MUL[z][z]],
        pg.GF_MUL[d][pg.GF_MUL[x][y]],
        pg.GF_MUL[e][pg.GF_MUL[x][z]],
        pg.GF_MUL[f][pg.GF_MUL[y][z]],
    ]
    s = 0
    for t in terms:
        s = pg.GF_ADD[s][t]
    return s


def encode(pts):
    code = 0
    for i, p in enumerate(sorted(pts)):
        code |= p << (7 * i)
    return code


def decode(code, k):
    return [(code >> (7 * i)) & 127 for i in range(k)]


def main():
    t0 = time.time()
    n, b, blocks = pg.load_board()
    g = game.CapGame(n, blocks)
    m_points, m_index, m_lines = pg.build_model()
    phi, _, _, _ = pg.find_isomorphism(n, blocks, m_points, m_lines)
    _, _, board_perms = group.board_generators(m_points, m_index, phi)

    conic_mask = sum(1 << p for p in CONIC)
    assert g.is_cap(conic_mask)
    assert g.available(conic_mask) == 0, "chosen conic is not maximal"

    # The chosen 10-cap is really a conic: solve for the quadratic form
    # vanishing on its ten points and check its zero set exactly.
    rows = []
    for p in CONIC:
        x, y, z = m_points[phi[p]]
        rows.append([
            pg.GF_MUL[x][x], pg.GF_MUL[y][y], pg.GF_MUL[z][z],
            pg.GF_MUL[x][y], pg.GF_MUL[x][z], pg.GF_MUL[y][z],
        ])
    basis = nullspace(rows)
    assert len(basis) == 1, len(basis)
    zero_set = [
        p for p in range(n)
        if eval_quadratic(basis[0], m_points[phi[p]]) == 0
    ]
    assert sorted(zero_set) == sorted(CONIC), (zero_set, CONIC)

    # Standard order bookkeeping for the conic count.
    gl2 = (9 ** 2 - 1) * (9 ** 2 - 9)
    pgl2 = gl2 // 8
    gl3 = (9 ** 3 - 1) * (9 ** 3 - 9) * (9 ** 3 - 9 ** 2)
    pgl3 = gl3 // 8
    conic_count = pgl3 // pgl2
    assert (pgl2, conic_count) == (720, 58968)

    # Orbit of the conic under the generators (10-subsets).
    start = encode(CONIC)
    seen = {start}
    frontier = [start]
    while frontier:
        nxt = []
        for code in frontier:
            vals = decode(code, 10)
            for P in board_perms:
                img = sorted(P[v] for v in vals)
                c = encode(img)
                if c not in seen:
                    seen.add(c)
                    nxt.append(c)
        frontier = nxt
    print("conic orbit size:", len(seen))

    # All 210 six-subsets of this conic: each must have Grundy 0.
    vals = []
    child_data = []
    for T in itertools.combinations(CONIC, 6):
        tm = sum(1 << p for p in T)
        assert g.is_cap(tm)
        levels = g.enumerate_upset(tm)
        gr = g.grundy_from_levels(levels)
        vals.append(gr[tm])
        c = g.child_grundy_counts(tm, g.secant_union(tm), gr)
        child_data.append({str(k): v for k, v in sorted(c.items())})
    counts = Counter(vals)
    print("conic 6-subset Grundy values:", dict(counts))
    print("seconds:", round(time.time() - t0, 3))

    out = {
        "conic": CONIC,
        "chosen_10cap_is_conic": True,
        "conic_form": basis[0],
        "conic_orbit_size": len(seen),
        "conic_count_expected": 58968,
        "conic_count_formula": conic_count,
        "pgl2_order": pgl2,
        "transitive_on_conics": len(seen) == conic_count,
        "six_subsets_checked": len(vals),
        "six_subset_grundy_counts": {str(k): v for k, v in sorted(counts.items())},
        "all_zero": set(vals) == {0},
        "child_distributions": child_data,
        "seconds": round(time.time() - t0, 3),
    }
    (pg.HERE / "out").mkdir(exist_ok=True)
    (pg.HERE / "out" / "t9_conic_orbits.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8"
    )
    assert len(seen) == conic_count
    assert set(vals) == {0}


if __name__ == "__main__":
    main()
