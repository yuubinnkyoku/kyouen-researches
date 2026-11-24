"""Task 4: conics in PG(2,9) -- independent enumeration and identity checks.

* Enumerate all conics of PG(2,9) directly from GF(9) = GF(3)[x]/(x^2+1) as
  zero sets of nondegenerate quadratic forms: symmetric 3x3 matrices up to
  scalar.  Count must be 9^5 - 9^2 = 58,968.
* Verify every conic is a 10-cap, that its 10 points are distinct, that no two
  conics share a point set, and that the conic line structure is the classical
  one (10 tangents + 45 secants, 36 exterior lines).
* Map every conic to the published board labels through the Task-1 isomorphism
  and emit the 10-subsets, 10 x 9-subsets and 45 x 8-subsets as binary mask
  files, for set comparison against the census dumps.
"""

from __future__ import annotations

import json
import struct
import sys
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pgcore as pc

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"


def det3(F, a, b, c, d, e, f):
    """det of the symmetric matrix of Q = a x^2 + b y^2 + c z^2 + d xy + e xz + f yz.

    Matrix (char 3: 1/2 = 2):
        [ a      d/2    e/2 ]
        [ d/2    b      f/2 ]
        [ e/2    f/2    c   ]
    Use the equivalent doubled form det([[2a,d,e],[d,2b,f],[e,f,2c]]) which is
    a nonzero multiple of det(M) (8 = 2 in char 3), so nondegeneracy agrees.
    """
    M = F.MUL
    A = [[M[2][a], d, e], [d, M[2][b], f], [e, f, M[2][c]]]
    A = [[A[0][0], A[0][1], A[0][2]],
         [A[1][0], A[1][1], A[1][2]],
         [A[2][0], A[2][1], A[2][2]]]
    AD = F.ADD
    t1 = M[A[0][0]][M[A[1][1]][A[2][2]]]
    t2 = M[A[0][1]][M[A[1][2]][A[2][0]]]
    t3 = M[A[0][2]][M[A[1][0]][A[2][1]]]
    t4 = M[A[0][2]][M[A[1][1]][A[2][0]]]
    t5 = M[A[0][0]][M[A[1][2]][A[2][1]]]
    t6 = M[A[0][1]][M[A[1][0]][A[2][2]]]
    pos = AD[AD[t1][t2]][t3]
    neg = AD[AD[t4][t5]][t6]
    return AD[pos][F.NEG[neg]]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    F = pc.gf9()
    q = F.q
    pts = pc.pg_points(F)
    assert len(pts) == 91
    lines = pc.pg_lines_via_normals(F, pts)
    lid = [[-1] * len(pts) for _ in pts]
    lmask_model = []
    for li, L in enumerate(lines):
        m = 0
        for p in L:
            m |= 1 << p
        lmask_model.append(m)
        for i in range(len(L)):
            for j in range(i + 1, len(L)):
                lid[L[i]][L[j]] = li
                lid[L[j]][L[i]] = li

    # monomials of every point: (x^2, y^2, z^2, xy, xz, yz)
    M, AD = F.MUL, F.ADD
    monos = [(M[x][x], M[y][y], M[z][z], M[x][y], M[x][z], M[y][z])
             for (x, y, z) in pts]

    # canonical quadratic forms: first nonzero coefficient equals 1
    classes = []
    for lead in range(6):
        for pre in product(range(q), repeat=lead):
            if any(v != 0 for v in pre):
                continue
            for tail in product(range(q), repeat=5 - lead):
                classes.append(pre + (1,) + tail)
    assert len(classes) == (q ** 6 - 1) // (q - 1), len(classes)
    n_classes = len(classes)

    nondeg = []
    n_nonzero_pointsets = 0
    for coef in classes:
        a, b, c, d, e, f = coef
        if det3(F, a, b, c, d, e, f) == 0:
            continue
        nondeg.append(coef)
    n_nondeg = len(nondeg)

    # zero sets
    conic_sets = {}
    bad = 0
    mult4 = None
    for coef in nondeg:
        a, b, c, d, e, f = coef
        Ma, Mb, Mc, Md, Me, Mf = M[a], M[b], M[c], M[d], M[e], M[f]
        S = []
        for p in range(len(pts)):
            m0, m1, m2, m3, m4, m5 = monos[p]
            v = AD[AD[AD[Ma[m0]][Mb[m1]]][AD[Mc[m2]][Md[m3]]]][AD[Me[m4]][Mf[m5]]]
            if v == 0:
                S.append(p)
        if len(S) != q + 1:
            bad += 1
            continue
        ms = 0
        for p in S:
            ms |= 1 << p
        conic_sets[ms] = tuple(S)

    print(f"canonical form classes: {n_classes} (expect (9^6-1)/8 = 66430)")
    print(f"nondegenerate classes:  {n_nondeg} (expect 9^5-9^2 = {q**5 - q**2})")
    print(f"degenerate classes:     {n_classes - n_nondeg}")
    print(f"distinct conic point sets: {len(conic_sets)}")
    print(f"nondegenerate forms with != q+1 zeros: {bad}")

    # every conic must be a 10-cap in the model, with classical line structure
    cap_ok = 0
    line_stats = {"tangent": 0, "secant": 0, "external": 0}
    for ms, S in conic_sets.items():
        for li, m in enumerate(lmask_model):
            c = bin(m & ms).count("1")
            if c > 2:
                raise AssertionError(f"conic {S} has {c} points on line {li}")
            if c == 1:
                line_stats["tangent"] += 1
            elif c == 2:
                line_stats["secant"] += 1
        cap_ok += 1
    line_stats["external"] = 91 * len(conic_sets) - line_stats["tangent"] - line_stats["secant"]
    struct_per_conic = {"tangent": line_stats["tangent"] / len(conic_sets),
                        "secant": line_stats["secant"] / len(conic_sets),
                        "external": line_stats["external"] / len(conic_sets)}
    print(f"conics that are 10-caps: {cap_ok}; per-conic line structure {struct_per_conic}")

    # maximality of every conic: the union of its 45 secants must cover all 81
    # points outside it (then no point can be added).  Independent of the C census.
    cover_ok = 0
    maxmask = (1 << len(pts)) - 1
    for ms, S in conic_sets.items():
        cov = 0
        for m in lmask_model:
            if bin(m & ms).count("1") == 2:
                cov |= m
        if (cov & (maxmask ^ ms)) == (maxmask ^ ms):
            cover_ok += 1
    print(f"conics whose secants cover every outside point (=> maximal): {cover_ok}")
    assert cover_ok == len(conic_sets)

    # map to published board labels
    iso = json.loads((OUT / "iso_model_to_board.json").read_text(encoding="utf-8"))
    perm = {int(k): v for k, v in iso["perm_model_to_board"].items()}
    n_board, board_lines = pc.load_board(HERE.parent / "output" / "board_pg2q9.txt")
    blid = [[-1] * n_board for _ in range(n_board)]
    blmask = []
    for li, L in enumerate(board_lines):
        m = 0
        for p in L:
            m |= 1 << p
        blmask.append(m)
        for i in range(len(L)):
            for j in range(i + 1, len(L)):
                blid[L[i]][L[j]] = li
                blid[L[j]][L[i]] = li

    def board_mask(S):
        m = 0
        for p in S:
            m |= 1 << perm[p]
        return m

    conic_board = {board_mask(S): tuple(sorted(perm[p] for p in S))
                   for S in conic_sets.values()}
    assert len(conic_board) == len(conic_sets)
    # verify cap property in board labels as well
    for ms, S in conic_board.items():
        for li, m in enumerate(blmask):
            if bin(m & ms).count("1") > 2:
                raise AssertionError("mapped conic is not a cap")
    print(f"mapped conics that are 10-caps in board labels: {len(conic_board)}")

    def write_masks(path, masks):
        with open(path, "wb") as fh:
            fh.write(struct.pack("<Q", len(masks)))
            for m in masks:
                fh.write(m.to_bytes(16, "little"))

    c10 = sorted(conic_board)
    write_masks(OUT / "conic10_board.bin", c10)

    c9 = []
    c8 = []
    from itertools import combinations
    for m in c10:
        S = [p for p in range(n_board) if (m >> p) & 1]
        for sub in combinations(S, 9):
            mm = 0
            for p in sub:
                mm |= 1 << p
            c9.append(mm)
        for sub in combinations(S, 8):
            mm = 0
            for p in sub:
                mm |= 1 << p
            c8.append(mm)
    write_masks(OUT / "conic9_board.bin", c9)
    write_masks(OUT / "conic8_board.bin", c8)

    # each 9-subset must be a cap, each 8-subset too; report
    def is_cap_mask(m):
        for lm in blmask:
            if bin(lm & m).count("1") > 2:
                return False
        return True

    bad9 = sum(0 if is_cap_mask(m) else 1 for m in c9)
    bad8 = sum(0 if is_cap_mask(m) else 1 for m in c8)

    res = {
        "q": 9,
        "classes": n_classes,
        "expected_classes": (q ** 6 - 1) // (q - 1),
        "nondegenerate": n_nondeg,
        "expected_nondegenerate": q ** 5 - q ** 2,
        "degenerate": n_classes - n_nondeg,
        "distinct_conic_point_sets": len(conic_sets),
        "conics_are_10caps": cap_ok,
        "conics_maximal_secant_cover": cover_ok,
        "per_conic_line_structure": struct_per_conic,
        "conic10_masks": len(c10),
        "conic9_masks": len(c9),
        "conic8_masks": len(c8),
        "expected_9": len(c10) * 10,
        "expected_8": len(c10) * 45,
        "bad9_caps": bad9,
        "bad8_caps": bad8,
    }
    (OUT / "task4_conics.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
