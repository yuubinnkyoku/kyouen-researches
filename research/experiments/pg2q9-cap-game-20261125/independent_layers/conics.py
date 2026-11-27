"""Conics of PG(2,9), built from GF(9) using the verified coordinate labelling.

A conic is the zero set of a non-degenerate homogeneous quadratic form
Q(x,y,z) = a11 x^2 + a22 y^2 + a33 z^2 + 2 a12 xy + 2 a13 xz + 2 a23 yz.
Canonical forms have first non-zero coefficient equal to 1 (GF(9) has 8
non-zero scalars); there are (9^6-1)/8 = 66,430 of them.  Non-degenerate ones
have 10 points (q+1 for q=9) and are maximal caps.

This module is independent of the parent's conic_layer.py: it enumerates every
canonical quadratic form and evaluates it directly on the 91 points.
"""

from __future__ import annotations

from itertools import combinations

from common import ADD, ELEMS, INV, MUL, ONE, TWO, ZERO, Board, bits, standard_pg


def det3(M) -> int:
    d = ZERO
    for perm in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
        p = ONE
        for r, c in enumerate(perm):
            p = MUL[p][M[r][c]]
        d = ADD[d][p]
    for perm in ((0, 2, 1), (1, 0, 2), (2, 1, 0)):
        p = ONE
        for r, c in enumerate(perm):
            p = MUL[p][M[r][c]]
        d = ADD[d][MUL[6][p]]  # subtract = add (-1)*p, -1 = 2 encodes 6
    return d


def canonical_forms():
    forms = []
    for a11 in ELEMS:
        for a12 in ELEMS:
            for a13 in ELEMS:
                for a22 in ELEMS:
                    for a23 in ELEMS:
                        for a33 in ELEMS:
                            vals = (a11, a12, a13, a22, a23, a33)
                            if vals == (0, 0, 0, 0, 0, 0):
                                continue
                            if next(x for x in vals if x != ZERO) != ONE:
                                continue
                            forms.append(vals)
    return forms


def point_monomials(pts):
    out = []
    for x, y, z in pts:
        out.append(
            (
                MUL[x][x],
                MUL[y][y],
                MUL[z][z],
                MUL[x][y],
                MUL[x][z],
                MUL[y][z],
            )
        )
    return out


def evaluate_form(form, monos) -> int:
    a11, a12, a13, a22, a23, a33 = form
    mask = 0
    for i, (x2, y2, z2, xy, xz, yz) in enumerate(monos):
        s = ADD[MUL[a11][x2]][MUL[a22][y2]]
        s = ADD[s][MUL[a33][z2]]
        s = ADD[s][MUL[a12][xy]]
        s = ADD[s][MUL[a13][xz]]
        s = ADD[s][MUL[a23][yz]]
        if s == ZERO:
            mask |= 1 << i
    return mask


def form_matrix(form):
    a11, a12, a13, a22, a23, a33 = form
    h = 6  # inverse of 2 in GF(9): 2*2 = 4 = 1 mod 3, so 2 is self-inverse
    return [
        [a11, MUL[h][a12], MUL[h][a13]],
        [MUL[h][a12], a22, MUL[h][a23]],
        [MUL[h][a13], MUL[h][a23], a33],
    ]


def conic_through5(pts, indices):
    """Find one non-degenerate conic through the 5 given point labels.

    Solves the 5x6 linear system for the conic coefficients over GF(9) and
    returns the canonical coefficient tuple.
    """
    monos = point_monomials(pts)
    rows = []
    for i in indices:
        x2, y2, z2, xy, xz, yz = monos[i]
        # column order must match the form tuple (a11, a12, a13, a22, a23, a33)
        rows.append([x2, xy, xz, y2, yz, z2])
    # Gaussian elimination, 5 equations, 6 unknowns (homogeneous)
    pivots = []
    r = 0
    for c in range(6):
        piv = None
        for rr in range(r, 5):
            if rows[rr][c] != ZERO:
                piv = rr
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = INV[rows[r][c]]
        rows[r] = [MUL[inv][v] for v in rows[r]]
        for rr in range(5):
            if rr != r and rows[rr][c] != ZERO:
                f = MUL[6][rows[rr][c]]  # subtract: add (-1)*rows[rr][c]
                rows[rr] = [ADD[rows[rr][k]][MUL[f][rows[r][k]]] for k in range(6)]
        pivots.append(c)
        r += 1
        if r == 5:
            break
    free = [c for c in range(6) if c not in pivots]
    assert len(free) == 1, free
    fc = free[0]
    # set free variable = 1, back-substitute (rows are reduced)
    sol = [ZERO] * 6
    sol[fc] = ONE
    for rr, pc in enumerate(pivots):
        # row rr: x_pc + sum_{free} row[rr][f] x_f = 0
        val = ZERO
        for f in free:
            val = ADD[val][MUL[rows[rr][f]][sol[f]]]
        sol[pc] = MUL[6][val]  # -val, -1 = 6
    # canonicalize first non-zero coefficient to 1
    nz = next(i for i, v in enumerate(sol) if v != ZERO)
    inv = INV[sol[nz]]
    sol = tuple(MUL[inv][v] for v in sol)
    return sol


def enumerate_conics(board: Board, verbose: bool = True) -> dict:
    pts, standard_lines = standard_pg()
    monos = point_monomials(pts)
    forms = canonical_forms()
    assert len(forms) == (9 ** 6 - 1) // 8 == 66_430

    conic_masks: list[int] = []
    degenerate = 0
    bad_size = 0
    bad_det = 0
    for n, form in enumerate(forms):
        M = form_matrix(form)
        if det3(M) == ZERO:
            degenerate += 1
            continue
        mask = evaluate_form(form, monos)
        if mask.bit_count() != 10:
            bad_size += 1
            continue
        conic_masks.append(mask)
        if verbose and (n + 1) % 20000 == 0:
            print(f"  ... {n + 1}/{len(forms)} forms, {len(conic_masks)} conics")

    distinct = len(set(conic_masks))
    # every conic is a cap and is maximal
    bad_cap = sum(1 for m in conic_masks if not board.is_cap(m))
    bad_max = sum(1 for m in conic_masks if board.addable_mask(m) != 0)
    res = {
        "canonical_forms": len(forms),
        "nondegenerate_forms": len(conic_masks),
        "degenerate_forms": degenerate,
        "bad_size": bad_size,
        "bad_det": bad_det,
        "distinct_conic_point_sets": distinct,
        "conics_formula_9^5-9^2": 9 ** 5 - 9 ** 2,
        "all_conics_are_10caps": bad_cap == 0,
        "all_conics_maximal": bad_max == 0,
        "bad_cap": bad_cap,
        "bad_maximal": bad_max,
        "conic_masks": conic_masks,
    }
    if verbose:
        print(f"  canonical forms: {len(forms)}")
        print(f"  nondegenerate: {len(conic_masks)}, degenerate: {degenerate}, bad size: {bad_size}")
        print(f"  distinct point sets: {distinct}")
        print(f"  all 10-caps: {bad_cap == 0}, all maximal: {bad_max == 0}")
    return res


def subsets_of_mask(mask: int, k: int):
    ps = bits(mask)
    for sub in combinations(ps, k):
        m = 0
        for p in sub:
            m |= 1 << p
        yield m


if __name__ == "__main__":
    from pathlib import Path
    import json

    from common import load_board

    here = Path(__file__).resolve().parent
    board = load_board(here.parent / "output" / "board_pg2q9.txt")
    res = enumerate_conics(board)
    masks = res.pop("conic_masks")
    out = here / "out"
    out.mkdir(exist_ok=True)
    (out / "conics_summary.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    # sanity: the parent's advertised conic
    parent_conic = [0, 1, 10, 20, 31, 45, 51, 62, 75, 88]
    pm = sum(1 << p for p in parent_conic)
    print("parent conic found:", pm in set(masks))
    # sample conic 9/8 caps: addable set must be the missing conic point(s)
    for m in masks[:5]:
        for k in (9, 8):
            for sub in list(subsets_of_mask(m, k))[:3]:
                add = board.addable_mask(sub)
                rem = m & ~sub
                print("conic", m.bit_count(), "k", k, "addable", bits(add), "missing", bits(rem),
                      "match", add == rem)
    print("wrote", out / "conics_summary.json")
