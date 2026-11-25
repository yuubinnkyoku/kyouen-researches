"""Task 2: {10,16,29,47,48} is a 5-cap and lies on a unique conic C (9 points).

Run:  python task2_conic.py
"""

from __future__ import annotations

import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pg8

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.join(HERE, os.pardir, "output", "board_pg2q8.txt")

GLYPHS = "01234567"


def form_str(co):
    names = ["x^2", "y^2", "z^2", "xy", "xz", "yz"]
    terms = [f"{GLYPHS[c]}*{n}" for c, n in zip(co, names) if c]
    return " + ".join(terms) if terms else "0"


def main():
    print("=" * 78)
    print("TASK 2 - 5-cap and the unique conic through it")
    print("=" * 78)
    board = pg8.Board(BOARD)
    S = list(pg8.BASE_5CAP)
    print("5-cap (board indices):", S)
    for p in S:
        print(f"  point {p:2d} = {pg8.POINTS[p]}")

    # ---- 1. cap property -------------------------------------------------
    coll = []
    for t in itertools.combinations(S, 3):
        a, b, c = t
        if board.line_of_pair[a][b] == board.line_of_pair[a][c] == board.line_of_pair[b][c]:
            coll.append(t)
    print("\n-- cap property ---------------------------------------------")
    print("  collinear triples among the 5 points:", coll)
    print("  is 5-cap:", board.is_cap(S), " (no 3 collinear:", not coll, ")")

    # ---- 2. linear system for quadratic forms through the 5 points -------
    info = pg8.find_conic_through(S)
    print("\n-- quadratic forms through the 5 points ----------------------")
    print("  unknowns: (q00,q11,q22,q01,q02,q12)")
    print("  rank of the 5x6 incidence system :", info["rank"], "of 6 -> nullity",
          info["nullity"])
    can = info["canonical"]
    print("  canonical form                   :", can, " =", form_str(can))
    print("  scalar multiples (7) give the same zero set (checked below)")
    Z = info["zero_set"]
    print("  zero set size                    :", len(Z))
    print("  zero set (board indices)         :", Z)
    print("  zero set (canonical vectors)     :")
    for p in Z:
        print(f"      {p:2d}  {pg8.POINTS[p]}")
    print("  contains the 5-cap               :", set(S) <= set(Z))
    print("  9 points form a cap (no 3 coll.) :", board.is_cap(Z))

    # ---- 3. brute force: EVERY quadratic form through the 5 points -------
    print("\n-- brute force over all 8^6 = 262144 quadratic forms ----------")
    through = []
    for co in itertools.product(range(8), repeat=6):
        if co == (0, 0, 0, 0, 0, 0):
            continue
        if all(pg8.qeval(co, pg8.POINTS[p]) == 0 for p in S):
            through.append(co)
    print("  forms vanishing on all 5 points   :", len(through), "(expect 7 = 8-1 scalars)")
    zsets = {frozenset(pg8.zero_set_fast(co)) for co in through}
    print("  distinct zero sets among them     :", len(zsets))
    print("  that zero set == C                :", zsets == {frozenset(Z)})

    # ---- 4. census of all non-degenerate conics --------------------------
    print("\n-- census: all 8^6-1 forms modulo scalars (37449 canonical) ----")
    forms = pg8.all_canonical_forms()
    print("  canonical forms (one per scalar class):", len(forms))
    by_size = {}
    conic_zs = {}
    double_lines = 0
    for co in forms:
        zs = pg8.zero_set_fast(co)
        key = len(zs)
        by_size[key] = by_size.get(key, 0) + 1
        if key == 9:
            if board.is_cap(zs):
                conic_zs[frozenset(zs)] = co
            else:
                double_lines += 1
    print("  distribution of |zero set|        :", dict(sorted(by_size.items())))
    print("  |zero set| = 9 and a cap (conic)  :", by_size.get(9, 0) - double_lines)
    print("  |zero set| = 9 but a line (l^2)   :", double_lines)
    print("  DISTINCT conic point sets         :", len(conic_zs))
    print("  q^5-q^2 with q=8                  :", 8**5 - 8**2)
    injective = len(conic_zs) == by_size.get(9, 0) - double_lines
    print("  each conic has a unique quadratic form up to scalar:", injective)
    hits = [zs for zs in conic_zs if set(S) <= set(zs)]
    print("  conics containing the 5-cap       :", len(hits),
          "(unique)" if len(hits) == 1 else "")
    print("  unique conic == C                 :", hits == [frozenset(Z)])

    # ---- 5. char-2 structure: polar radical = nucleus, tangents ----------
    q00, q11, q22, q01, q02, q12 = can
    M = [[0, q01, q02], [q01, 0, q12], [q02, q12, 0]]
    rad = pg8.nullspace_basis(M, 3)
    print("\n-- characteristic-2 structure of C ---------------------------")
    print("  polar form matrix                :", M)
    print("  radical of polar form (dim)      :", len(rad), "(odd dimension => >=1)")
    nucleus = None
    if len(rad) == 1:
        nv = pg8.vcanon(tuple(rad[0]))
        nucleus = pg8.PIDX[nv]
        print("  nucleus point                    :", nucleus, nv)
    # every tangent passes through the nucleus: line(P,n) meets C only in P
    tang_ok = True
    if nucleus is not None:
        for p in Z:
            li = board.line_of_pair[p][nucleus]
            if (board.line_sets[li] & set(Z)) != {p}:
                tang_ok = False
        print("  all 9 tangents pass through nucleus:", tang_ok)
        hyper = sorted(set(Z) | {nucleus})
        print("  C + nucleus is a 10-cap          :",
              len(hyper) == 10 and board.is_cap(hyper))
        print("  nucleus on C                     :", nucleus in Z)

    ok = (
        not coll
        and info["rank"] == 5
        and info["nullity"] == 1
        and len(Z) == 9
        and set(S) <= set(Z)
        and board.is_cap(Z)
        and len(through) == 7
        and len(zsets) == 1
        and len(hits) == 1
        and hits == [frozenset(Z)]
        and len(conic_zs) == 32704
        and injective
        and len(rad) == 1
        and tang_ok
    )
    print("\nTASK 2:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
