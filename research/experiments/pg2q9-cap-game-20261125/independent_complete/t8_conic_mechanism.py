"""Check the claimed conic-child mechanism for 5-caps and conic 6-subsets.

Every 5-cap lies on a unique conic (5 points, no three collinear, q odd).
The claim says the five 6-children obtained by adding a remaining conic point
have Grundy 0.  We solve for the conic over GF(9) and test this.
"""

from __future__ import annotations

import json
import random
import time
from collections import Counter

import game
import pg


def gf_sub(a, b):
    return pg.GF_ADD[a][pg.gf_neg(b)]


def nullspace(A, ncols=6):
    """Basis of the nullspace of the GF(9) matrix A (list of rows)."""
    A = [list(row) for row in A]
    m = len(A)
    pivots = []
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, m):
            if A[i][c]:
                piv = i
                break
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pg.GF_INV[A[r][c]]
        A[r] = [pg.GF_MUL[inv][x] for x in A[r]]
        for i in range(m):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [
                    gf_sub(A[i][j], pg.GF_MUL[f][A[r][j]])
                    for j in range(ncols)
                ]
        pivots.append(c)
        r += 1
    free = [c for c in range(ncols) if c not in pivots]
    basis = []
    for f in free:
        v = [0] * ncols
        v[f] = 1
        for i, p in enumerate(pivots):
            v[p] = gf_sub(0, A[i][f])
        basis.append(v)
    return basis


def conic_of_five(game_, points):
    pts = [game_.points[p] for p in points]
    A = []
    for v in pts:
        x, y, z = v
        A.append([
            pg.GF_MUL[x][x], pg.GF_MUL[y][y], pg.GF_MUL[z][z],
            pg.GF_MUL[x][y], pg.GF_MUL[x][z], pg.GF_MUL[y][z],
        ])
    basis = nullspace(A)
    assert len(basis) == 1, ("conic not unique", len(basis))
    coeffs = basis[0]
    a, b, c, d, e, f = coeffs
    zero = []
    for i, (x, y, z) in enumerate(game_.points):
        q = 0
        terms = [
            pg.GF_MUL[a][pg.GF_MUL[x][x]],
            pg.GF_MUL[b][pg.GF_MUL[y][y]],
            pg.GF_MUL[c][pg.GF_MUL[z][z]],
            pg.GF_MUL[d][pg.GF_MUL[x][y]],
            pg.GF_MUL[e][pg.GF_MUL[x][z]],
            pg.GF_MUL[f][pg.GF_MUL[y][z]],
        ]
        for t in terms:
            q = pg.GF_ADD[q][t]
        if q == 0:
            zero.append(i)
    assert len(zero) == 10, (len(zero), zero)
    assert set(points) <= set(zero)
    return zero


def main():
    t0 = time.time()
    n, b, blocks = pg.load_board()
    g = game.CapGame(n, blocks)
    m_points, m_index, m_lines = pg.build_model()
    # We need the model point vectors aligned with board labels through phi.
    phi, _, _, _ = pg.find_isomorphism(n, blocks, m_points, m_lines)
    g.points = [m_points[phi[i]] for i in range(n)]

    rng = random.Random(777001)
    out = {}
    five = []
    all_conic_children_zero = True
    for _ in range(25):
        while True:
            S = rng.sample(range(n), 5)
            m = sum(1 << p for p in S)
            if g.is_cap(m):
                break
        conic = conic_of_five(g, S)
        assert len(conic) == 10
        extra = [p for p in conic if p not in S]
        assert len(extra) == 5
        vals = []
        for p in extra:
            cm = m | (1 << p)
            gv = g.grundy_from_levels(g.enumerate_upset(cm))[cm]
            vals.append(gv)
        all5 = g.grundy_from_levels(g.enumerate_upset(m))[m]
        rec = {
            "cap": sorted(S),
            "conic": sorted(conic),
            "conic_child_values": vals,
            "all_conic_children_G0": all(v == 0 for v in vals),
            "G5": all5,
        }
        five.append(rec)
        if not rec["all_conic_children_G0"]:
            all_conic_children_zero = False
        print("5-cap", sorted(S), "conic child G:", vals, "G5:", all5)
    out["five_caps"] = five
    out["all_conic_children_G0"] = all_conic_children_zero

    # Random 6-subsets of conics: what Grundy values occur?
    six = []
    for _ in range(25):
        while True:
            S = rng.sample(range(n), 5)
            m = sum(1 << p for p in S)
            if g.is_cap(m):
                break
        conic = conic_of_five(g, S)
        T = rng.sample(conic, 6)
        tm = sum(1 << p for p in T)
        assert g.is_cap(tm)
        gv = g.grundy_from_levels(g.enumerate_upset(tm))[tm]
        six.append({"cap": sorted(T), "G6": gv})
        print("conic 6-subset", sorted(T), "G:", gv)
    out["conic_six_subsets"] = six
    out["six_value_counts"] = dict(Counter(x["G6"] for x in six))

    out["seconds"] = round(time.time() - t0, 3)
    (pg.HERE / "out").mkdir(exist_ok=True)
    (pg.HERE / "out" / "t8_conic_mechanism.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8"
    )
    print("all 5-cap conic children G0:", all_conic_children_zero)
    print("conic-6 values:", out["six_value_counts"])
    print("seconds:", out["seconds"])


if __name__ == "__main__":
    main()
