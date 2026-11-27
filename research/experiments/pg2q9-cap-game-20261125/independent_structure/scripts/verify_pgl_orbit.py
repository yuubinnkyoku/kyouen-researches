"""PGL(3,9) structure of maximal 8-caps.

Builds explicit projectivities from 4-point frames and computes, for one
maximal 8-cap A:
  * the number of projectivities mapping A onto itself (stabilizer order)
  * the orbit size |PGL(3,9)| / |Stab(A)|, compared with census max-8 count
  * whether the stabilizer acts regularly on the 8 points of A
  * that a sample of other maximal 8-caps lies in the same orbit.
"""
import functools
import itertools
import random
import sys
from pathlib import Path

import pg

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "out"

INV = [None] * 9
for x in range(1, 9):
    for y in range(1, 9):
        if pg.MUL[x][y] == pg.ONE:
            INV[x] = y


def bits(mask):
    while mask:
        b = mask & -mask
        yield b.bit_length() - 1
        mask ^= b


def vec(p):
    """Board point index -> coordinate vector (field labels)."""
    if p == 0:
        return (0, 0, pg.ONE)
    if 1 <= p <= 9:
        return (0, pg.ONE, p - 1)
    q = p - 10
    y, z = divmod(q, 9)
    return (pg.ONE, y, z)


def canonical_index(v):
    v = tuple(v)
    if v == (0, 0, 0):
        raise ValueError("zero vector")
    i = next(k for k, x in enumerate(v) if x != 0)
    s = INV[v[i]]
    w = tuple(pg.MUL[x][s] for x in v)
    if w[0] != 0:
        assert w[0] == pg.ONE
        return 10 + 9 * w[1] + w[2]
    if w[1] != 0:
        assert w[1] == pg.ONE
        return 1 + w[2]
    assert w[2] == pg.ONE
    return 0


def matvec(M, v):
    out = []
    for row in M:
        s = 0
        for x, y in zip(row, v):
            s = pg.ADD[s][pg.MUL[x][y]]
        out.append(s)
    return tuple(out)


def matmul(A, B):
    n = len(A)
    m = len(B[0])
    k = len(B)
    return [[functools.reduce(lambda x, y: pg.ADD[x][y],
             (pg.MUL[A[i][t]][B[t][j]] for t in range(k)), 0)
             for j in range(m)] for i in range(n)]


def matinv(A):
    n = 3
    M = [list(A[i]) + [pg.ONE if i == j else 0 for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = next(r for r in range(col, n) if M[r][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        inv = INV[M[col][col]]
        M[col] = [pg.MUL[x][inv] for x in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = pg.NEG[M[r][col]]
                M[r] = [pg.ADD[M[r][j]][pg.MUL[f][M[col][j]]] for j in range(2 * n)]
    return [row[n:] for row in M]


def solve3(cols, rhs):
    """Solve x1*c1 + x2*c2 + x3*c3 = rhs for x (field labels)."""
    A = [[cols[0][i], cols[1][i], cols[2][i], rhs[i]] for i in range(3)]
    for col in range(3):
        piv = next(r for r in range(col, 3) if A[r][col] != 0)
        A[col], A[piv] = A[piv], A[col]
        inv = INV[A[col][col]]
        A[col] = [pg.MUL[x][inv] for x in A[col]]
        for r in range(3):
            if r != col and A[r][col] != 0:
                f = pg.NEG[A[r][col]]
                A[r] = [pg.ADD[A[r][j]][pg.MUL[f][A[col][j]]] for j in range(4)]
    return [A[i][3] for i in range(3)]


def projectivity_from_standard(frame):
    """Matrix of the projectivity sending the standard frame
    e1,e2,e3,(1,1,1) to the four points in `frame`."""
    P1, P2, P3, P4 = [vec(p) for p in frame]
    lam = solve3([P1, P2, P3], P4)
    cols = [tuple(pg.MUL[lam[i]][Pi[k]] for k in range(3))
            for i, Pi in enumerate((P1, P2, P3))]
    return [[cols[j][i] for j in range(3)] for i in range(3)]


def maps_frame(M0, M1):
    return matmul(M1, matinv(M0))


def apply_proj(M, p):
    return canonical_index(matvec(M, vec(p)))


def greedy_max_cap(rng):
    p = rng.randrange(91)
    cap = [p]
    add = pg.FULL & ~(1 << p)
    while add:
        q = rng.choice(list(bits(add)))
        cap.append(q)
        for a in cap[:-1]:
            add &= ~pg.line_mask(a, q)
        add &= ~(1 << q)
    return sorted(cap)


def main():
    conics = set(int(ln) for ln in (OUT / "conics.txt").read_text().splitlines())
    A = [11, 22, 29, 32, 41, 44, 61, 89]
    assert len(A) == 8 and pg.is_cap(A)
    m = 0
    for p in A:
        m |= 1 << p
    assert m not in conics
    print(f"maximal 8-cap A = {A}")
    print(f"  cap={pg.is_cap(A)} addable={pg.addable_mask(A)} "
          f"conic={m in conics}")

    F0 = A[:4]
    M0 = projectivity_from_standard(F0)
    print(f"  frame F0 = {F0}")

    # verify the construction maps the standard frame to F0
    # standard frame points in board coords: e1=(1,0,0)=10, e2=(0,1,0)=1,
    # e3=(0,0,1)=0, unit=(1,1,1)=40.  Coordinates here are field *labels*,
    # so field 1 is label pg.ONE = 3.
    assert vec(10) == (pg.ONE, 0, 0)
    assert vec(1) == (0, pg.ONE, 0)
    assert vec(0) == (0, 0, pg.ONE)
    assert vec(40) == (pg.ONE, pg.ONE, pg.ONE)
    assert [apply_proj(M0, p) for p in (10, 1, 0, 40)] == F0
    print("  frame construction verified")

    # stabilizer: enumerate ordered 4-frames inside A; each gives a unique
    # projectivity mapping A to A or not.
    stab = []
    stab_mats = []
    images_of_p0 = set()
    for F in itertools.permutations(A, 4):
        M1 = projectivity_from_standard(F)
        g = maps_frame(M0, M1)
        try:
            img = [apply_proj(g, p) for p in A]
        except AssertionError:
            print("FAIL F", F, "g", g)
            for p in A:
                print("  p", p, "vec", vec(p), "Mv", matvec(g, vec(p)))
            raise
        if sorted(img) == A:
            stab.append(tuple(F))
            stab_mats.append(g)
            images_of_p0.add(img[0])
    print(f"stabilizer order (projectivities fixing A setwise): {len(stab)}")
    print(f"images of first point under stabilizer: {sorted(images_of_p0)} "
          f"(#={len(images_of_p0)})")
    # orbits of the stabilizer on the points of A
    seen = set()
    orbits = []
    for p in A:
        if p in seen:
            continue
        orb = {apply_proj(g, p) for g in stab_mats}
        orbits.append(sorted(orb))
        seen |= orb
    print(f"stabilizer orbits on the 8 points of A: {orbits}")
    pgl = 9**3 * (9**3 - 1) * (9**2 - 1)
    orbit = pgl // len(stab)
    print(f"|PGL| / |Stab| = {orbit}")
    print(f"census maximal 8-cap count 5,307,120; equal: {orbit == 5307120}")
    print(f"8*max8 = {8 * 5307120} = |PGL|: {8 * 5307120 == pgl}")

    # test that other maximal 8-caps are in the same orbit: try all ordered
    # 4-frames of B as image of F0.
    rng = random.Random(777)
    tested = 0
    same = 0
    invM0 = matinv(M0)
    while tested < 20:
        B = greedy_max_cap(rng)
        if len(B) != 8:
            continue
        tested += 1
        found = False
        for F in itertools.permutations(B, 4):
            M1 = projectivity_from_standard(F)
            g = matmul(M1, invM0)
            if sorted(apply_proj(g, p) for p in A) == B:
                found = True
                break
        if found:
            same += 1
    print(f"random maximal 8-caps mapped from A to B: {same}/{tested}")


if __name__ == "__main__":
    main()
