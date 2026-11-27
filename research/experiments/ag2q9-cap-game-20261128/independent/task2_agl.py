"""Task 2: verify that AGL(2,9) is (sharply) transitive on ordered triangles.

Method
------
Fix the ordered triangle T0 = ((0,0), (1,0), (0,1)).  For every ordered triangle
T = (a,b,c) there is at most one affine map phi_T with phi_T(T0) = T, namely

    phi_T(x) = a + x*(b-a) + y*(c-a)      (the two columns are b-a and c-a)

which is invertible exactly when T is non-collinear.  We enumerate all ordered
triangles, count them, verify injectivity of T -> phi_T, verify that every map
is an invertible affine map, and compare the number of ordered triangles with
|AGL(2,9)| = |GL(2,9)| * 81 (also computed independently).  Equality forces
{phi_T} = AGL(2,9), i.e. AGL(2,9) acts simply transitively on ordered triangles.

Run: python task2_agl.py
"""

import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from common import (  # noqa: E402
    E, enc, fadd, fsub, fmul, finv, fiszero, ONE, ZERO,
)

OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

POINTS = [(x, y) for x in E for y in E]
T0 = ((ZERO, ZERO), (ONE, ZERO), (ZERO, ONE))   # (0,0), (1,0), (0,1) as field pairs


def det(col1, col2):
    """det of the matrix whose columns are col1, col2 (vectors over GF(9))."""
    return fsub(fmul(col1[0], col2[1]), fmul(col2[0], col1[1]))


def vadd(u, v):
    return (fadd(u[0], v[0]), fadd(u[1], v[1]))


def vsub(u, v):
    return (fsub(u[0], v[0]), fsub(u[1], v[1]))


def vscale(s, v):
    return (fmul(s, v[0]), fmul(s, v[1]))


def lin_image(col1, col2, v):
    """v[0]*col1 + v[1]*col2  (columns of the matrix)."""
    return vadd(vscale(v[0], col1), vscale(v[1], col2))


def aff_image(mp, p):
    col1, col2, a = mp
    return vadd(a, lin_image(col1, col2, p))


def psub(a, b):
    return (fsub(a[0], b[0]), fsub(a[1], b[1]))


def lin_inverse(col1, col2, w):
    c10, c11 = col1
    c20, c21 = col2
    d = det(col1, col2)
    di = finv(d)
    x = fmul(fsub(fmul(c21, w[0]), fmul(c20, w[1])), di)
    y = fmul(fsub(fmul(c10, w[1]), fmul(c11, w[0])), di)
    return (x, y)


def code(mp):
    col1, col2, a = mp
    vals = (enc(col1[0]), enc(col1[1]), enc(col2[0]), enc(col2[1]), enc(a[0]), enc(a[1]))
    c = 0
    for v in vals:
        c = c * 9 + v
    return c


def main():
    rng = random.Random(20261128)
    result = {}

    # ---------------------------------------------------------- ordered triangles
    ordered = []
    for a in POINTS:
        for b in POINTS:
            if b == a:
                continue
            for c in POINTS:
                if c == a or c == b:
                    continue
                col1 = vsub(b, a)
                col2 = vsub(c, a)
                if not fiszero(det(col1, col2)):
                    ordered.append((a, b, c, (col1, col2, a)))
    n_ord = len(ordered)
    result["ordered_triangles"] = n_ord
    result["formula_81_80_72"] = 81 * 80 * 72

    # every triangle gives an invertible affine map and the map sends T0 to it
    maps = {}
    images_ok = True
    for a, b, c, mp in ordered:
        if fiszero(det(mp[0], mp[1])):
            images_ok = False
        if not (aff_image(mp, T0[0]) == a and aff_image(mp, T0[1]) == b and aff_image(mp, T0[2]) == c):
            images_ok = False
        maps[code(mp)] = (a, b, c)
    distinct = len(maps)
    result["distinct_maps"] = distinct
    result["maps_send_T0_to_the_triangle"] = images_ok
    result["injective"] = distinct == n_ord

    # ------------------------------------------------------------- |AGL(2,9)|
    nz = [p for p in POINTS if p != ZERO]                    # 80
    n_gl = 0
    for v1 in nz:
        for v2 in POINTS:
            if not fiszero(det(v1, v2)):
                n_gl += 1
    n_agL = n_gl * 81
    result["nonzero_vectors"] = len(nz)
    result["gl2_9_count"] = n_gl
    result["gl2_9_formula_80_72"] = 80 * 72
    result["agl2_9_count"] = n_agL
    result["ordered_triangles_equal_agl"] = n_ord == n_agL
    result["non_collinear_ordered_triples_all"] = 81 * 80 * 72

    # the three points of T0 are non-collinear
    result["T0_nondegenerate"] = not fiszero(det(vsub(T0[1], T0[0]), vsub(T0[2], T0[0])))

    # --------------------------------------------------- explicit transitivity
    # For random pairs of ordered triangles, build psi = phi_{T'} o phi_T^{-1}
    # and check that it is an invertible affine map sending T to T'.
    transitivity_fail = 0
    for _ in range(500):
        a, b, c, mp = ordered[rng.randrange(n_ord)]
        a2, b2, c2, mp2 = ordered[rng.randrange(n_ord)]
        c1, c2v, t1 = mp
        d1, d2v, t2 = mp2
        # psi(p) = t2 + L2( L1^{-1}(p - t1) )
        def psi(p):
            u = vsub(p, t1)
            v = lin_inverse(c1, c2v, u)
            return vadd(t2, lin_image(d1, d2v, v))
        if not (psi(a) == a2 and psi(b) == b2 and psi(c) == c2):
            transitivity_fail += 1
    result["random_pair_transitivity_failures"] = transitivity_fail

    # composition closure: for random pairs of the 466,560 maps, the composite
    # must again be one of the maps (i.e. the set really is the full affine group)
    keys = list(maps)
    closure_fail = 0
    for _ in range(2000):
        e1 = maps[keys[rng.randrange(len(keys))]]
        e2 = maps[keys[rng.randrange(len(keys))]]
        # rebuild the affine maps from the triangle data
        def mp_of(tri):
            aa, bb, cc = tri
            return (vsub(bb, aa), vsub(cc, aa), aa)
        m1 = mp_of(e1)
        m2 = mp_of(e2)
        # m2 o m1: linear part L2 L1, translation t2 + L2(t1)
        cols = (lin_image(m2[0], m2[1], m1[0]), lin_image(m2[0], m2[1], m1[1]))
        comp = (cols[0], cols[1], vadd(m2[2], lin_image(m2[0], m2[1], m1[2])))
        if fiszero(det(comp[0], comp[1])) or code(comp) not in maps:
            closure_fail += 1
    result["composition_closure_failures_out_of_2000"] = closure_fail

    # -------------------------------------------------- unordered triangle count
    # ordered triples of distinct non-collinear points / 6
    result["unordered_triangles"] = n_ord // 6
    # independent count: all 3-subsets minus the collinear ones
    from math import comb
    collinear_triples = 90 * comb(9, 3)
    result["collinear_triples_formula"] = collinear_triples
    result["noncollinear_triples_formula"] = comb(81, 3) - collinear_triples
    result["N3_claim"] = 77760
    result["N3_matches"] = (
        result["unordered_triangles"] == result["noncollinear_triples_formula"] == 77760
    )

    # ------------------------------------------- affine maps preserve the design
    # sample 300 maps: the image of every line must be a line of the board
    sys.path.insert(0, str(HERE))
    from common import build_board, line_masks
    _, lines = build_board("y")
    line_sets = {frozenset(L) for L in lines}
    pt_index = {p: i for i, p in enumerate(POINTS)}
    line_fail = 0
    for _ in range(300):
        a, b, c, mp = ordered[rng.randrange(n_ord)]
        for L in lines:
            img = []
            for i in L:
                q = aff_image(mp, POINTS[i])
                img.append(pt_index[q])
            if frozenset(img) not in line_sets:
                line_fail += 1
                break
    result["line_preservation_failures_out_of_300_maps"] = line_fail

    result["all_task2_checks_ok"] = all(
        [
            n_ord == 81 * 80 * 72 == 466560,
            result["maps_send_T0_to_the_triangle"],
            result["injective"],
            n_gl == 80 * 72 == 5760,
            n_agL == 466560,
            result["ordered_triangles_equal_agl"],
            result["T0_nondegenerate"],
            transitivity_fail == 0,
            closure_fail == 0,
            result["N3_matches"],
            line_fail == 0,
        ]
    )

    (OUT / "task2_agl.json").write_text(json.dumps(result, indent=1), encoding="utf-8")

    print("=" * 78)
    print("TASK 2  AGL(2,9) transitivity on triangles")
    print("=" * 78)
    print("ordered triangles             :", n_ord, "(81*80*72 =", 81 * 80 * 72, ")")
    print("distinct affine maps phi_T    :", distinct, "injective:", result["injective"])
    print("|GL(2,9)| (ordered bases)     :", n_gl, "(80*72 =", 80 * 72, ")")
    print("|AGL(2,9)| = |GL|*81          :", n_agL)
    print("ordered triangles == |AGL|    :", result["ordered_triangles_equal_agl"])
    print("phi_T sends T0 to T (all)     :", images_ok)
    print("random transitivity failures  :", transitivity_fail)
    print("composition-closure failures  :", closure_fail, "/2000")
    print("line-preservation failures    :", line_fail, "/300 maps")
    print("unordered triangles           :", result["unordered_triangles"],
          "= 77760:", result["N3_matches"])
    print("=> AGL(2,9) is simply transitive on ordered triangles,")
    print("   hence transitive on (unordered) triangles (77,760 of them).")
    print("all task-2 checks             :", result["all_task2_checks_ok"])
    print("wrote", OUT / "task2_agl.json")
    return result


if __name__ == "__main__":
    r = main()
    raise SystemExit(0 if r["all_task2_checks_ok"] else 1)
