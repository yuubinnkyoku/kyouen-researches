"""Small GF(8) linear-algebra layer and conic utilities (built from scratch)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C


def nullspace(rows, ncols):
    """Basis of the nullspace of the matrix given by rows over GF(8)."""
    A = [list(r) for r in rows]
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
        inv = C.GF_INV[A[r][c]]
        A[r] = [C.gf_mul(x, inv) for x in A[r]]
        for i in range(m):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [C.gf_add(A[i][j], C.gf_mul(f, A[r][j]))
                        for j in range(ncols)]
        pivots.append(c)
        r += 1
        if r == m:
            break
    free_cols = [c for c in range(ncols) if c not in pivots]
    basis = []
    for fc in free_cols:
        v = [0] * ncols
        v[fc] = 1
        for i, pc in enumerate(pivots):
            v[pc] = A[i][fc]
        basis.append(v)
    return basis


def conic_row(p):
    x, y, z = C.POINT[p]
    return [C.gf_mul(x, x), C.gf_mul(y, y), C.gf_mul(z, z),
            C.gf_mul(x, y), C.gf_mul(x, z), C.gf_mul(y, z)]


def conic_through_five(pts):
    """Unique conic through 5 points in general position; returns coeffs."""
    rows = [conic_row(p) for p in pts]
    bas = nullspace(rows, 6)
    assert len(bas) == 1, ("nullspace dimension", len(bas))
    co = bas[0]
    assert any(co)
    # check all five points
    assert all(qeval(co, p) == 0 for p in pts)
    return tuple(co)


def qeval(co, p):
    row = conic_row(p)
    s = 0
    for a, t in zip(co, row):
        s = C.gf_add(s, C.gf_mul(a, t))
    return s


def conic_points(co):
    pts = [p for p in range(C.N) if qeval(co, p) == 0]
    return pts


def is_conic_set(pts):
    """True iff all points lie on one nondegenerate conic."""
    if len(pts) < 5:
        return True  # any <=5 points no 3 collinear lie on a conic
    co = conic_through_five(pts[:5])
    return all(qeval(co, p) == 0 for p in pts)


def conic_of_cap(pts):
    co = conic_through_five(pts[:5])
    allpts = conic_points(co)
    assert len(allpts) == 9, len(allpts)
    return co, allpts


if __name__ == "__main__":
    C6 = [2, 3, 10, 16, 18, 21]
    D6 = [1, 10, 12, 59, 62, 65]
    co, conic9 = conic_of_cap(C6)
    print("conic coeffs:", co)
    print("conic points:", conic9)
    print("C6 subset:", set(C6) <= set(conic9))
    print("D6 conic:", is_conic_set(D6))
    print("D6 first5 conic points contains rest:",
          all(qeval(conic_through_five(D6[:5]), p) == 0 for p in D6))
    # axiom: a conic has 9 points
    print("conic 9 points:", len(conic9) == 9)
