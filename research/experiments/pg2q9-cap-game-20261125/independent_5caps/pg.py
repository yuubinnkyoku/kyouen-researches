"""Core library: GF(9), the projective plane PG(2,9), and the board file.

Python standard library only.

Field encoding (as used by the claim under test):  the integer e = 3a + b
represents the field element  a + b*i  of  GF(9) = GF(3)[i]/(i^2 + 1).
Consequences that matter and are easy to get wrong:
    encoded 0  = field 0
    encoded 3  = field 1        (the multiplicative identity!)
    encoded 1  = field i
    encoded 6  = field -1 = 2
All arithmetic below goes through the tables; never use +,*,% on encoded
integers as if they were field elements.

Point coordinate map under test (claim):
    index 0            -> (0 : 0 : 1)
    index 1+j   (j=0..8)-> (0 : 1 : E[j])
    index 10+9p+j       -> (1 : E[p] : E[j])      (p,j = 0..8)
with E[k] = 3*(k//3) + (k%3) = k.
The literal "1" in the claim is the field element 1, i.e. encoded 3, so we
test that reading first ('field_one') and, for completeness, the alternative
reading in which "1" means the encoded integer 1 ('literal').
"""

from __future__ import annotations

import itertools
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP_DIR = HERE.parent
BOARD_PATH = EXP_DIR / "output" / "board_pg2q9.txt"

# ---------------------------------------------------------------- GF(9) tables


def _enc(a: int, b: int) -> int:
    return (3 * (a % 3) + (b % 3)) % 9


ZERO = 0
ONE = _enc(1, 0)      # == 3 : the field element 1
IELT = _enc(0, 1)     # == 1 : the field element i

ADD = tuple(
    tuple(_enc(e1 // 3 + e2 // 3, e1 % 3 + e2 % 3) for e2 in range(9))
    for e1 in range(9)
)
MUL = tuple(
    tuple(
        _enc(
            (e1 // 3) * (e2 // 3) - (e1 % 3) * (e2 % 3),
            (e1 // 3) * (e2 % 3) + (e1 % 3) * (e2 // 3),
        )
        for e2 in range(9)
    )
    for e1 in range(9)
)
NEG = tuple(_enc(-(e // 3), -(e % 3)) for e in range(9))
SUB = tuple(tuple(ADD[e1][NEG[e2]] for e2 in range(9)) for e1 in range(9))

INV: list[int | None] = [None] * 9
for _e in range(1, 9):
    for _f in range(1, 9):
        if MUL[_e][_f] == ONE:
            INV[_e] = _f
assert all(INV[e] is not None for e in range(1, 9))
assert MUL[IELT][IELT] == NEG[ONE] == 6, "i^2 must be -1"
# squares: 0, 1 = 1^2 = (-1)^2 encoded 3 (twice), i^2 = -1 encoded 6 (twice),
# 1+i and 1-i square to +-i encoded 2 (twice), (1+2i),(2+i) square to -+i encoded 1
assert sorted(MUL[e][e] for e in range(9)) == [0, 1, 1, 2, 2, 3, 3, 6, 6]
# x^2 + 1 is irreducible over GF(3): no root among encoded {0,1,2} = {0,3,6}
assert all(MUL[e][e] != NEG[ONE] for e in (ZERO, ONE, _enc(2, 0)))


def field_name(e: int) -> str:
    a, b = e // 3, e % 3
    if b == 0:
        return str(a)
    if a == 0:
        return "i" if b == 1 else "2i"
    return f"{a}+{'i' if b == 1 else '2i'}"


# --------------------------------------------------------------- 3-vectors


def vnorm(v: tuple[int, int, int]) -> tuple[int, int, int]:
    """Normalise a nonzero vector: first nonzero coordinate becomes 1."""
    for c in v:
        if c != ZERO:
            inv = INV[c]
            assert inv is not None
            return (MUL[inv][v[0]], MUL[inv][v[1]], MUL[inv][v[2]])
    raise ValueError("zero vector")


def vcross(u, v):
    return (
        SUB[MUL[u[1]][v[2]]][MUL[u[2]][v[1]]],
        SUB[MUL[u[2]][v[0]]][MUL[u[0]][v[2]]],
        SUB[MUL[u[0]][v[1]]][MUL[u[1]][v[0]]],
    )


def vdot(l, p):
    return ADD[ADD[MUL[l[0]][p[0]]][MUL[l[1]][p[1]]]][MUL[l[2]][p[2]]]


def vscale(c: int, v):
    return (MUL[c][v[0]], MUL[c][v[1]], MUL[c][v[2]])


def vindependent(vs) -> bool:
    """True iff the given vectors are linearly independent (row reduce)."""
    rows = [list(v) for v in vs]
    n = len(rows)
    r = 0
    for col in range(3):
        piv = None
        for i in range(r, n):
            if rows[i][col] != ZERO:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = INV[rows[r][col]]
        rows[r] = [MUL[inv][c] for c in rows[r]]
        for i in range(n):
            if i != r and rows[i][col] != ZERO:
                f = rows[i][col]
                rows[i] = [SUB[rows[i][k]][MUL[f][rows[r][k]]] for k in range(3)]
        r += 1
    return r == n


# --------------------------------------------------- points and the plane

def point_vectors(reading: str = "field_one") -> list[tuple[int, int, int]]:
    """The 91 point vectors of the claimed coordinate map."""
    if reading == "field_one":
        x = ONE
    elif reading == "literal":
        x = 1
    else:
        raise ValueError(reading)
    pts = [(ZERO, ZERO, ONE)]
    pts += [(ZERO, x, j) for j in range(9)]
    pts += [(x, p, j) for p in range(9) for j in range(9)]
    return pts


class Plane:
    """PG(2,9) rebuilt from a list of 91 point vectors."""

    def __init__(self, pts):
        assert len(pts) == 91
        self.vectors = list(pts)
        self.index = {vnorm(v): i for i, v in enumerate(pts)}
        assert len(self.index) == 91, "point vectors are not 91 distinct points"
        # all lines, as point-index bitmasks
        self.line_masks: list[int] = []
        self._line_id: dict[tuple[int, int, int], int] = {}
        for i in range(91):
            for j in range(i + 1, 91):
                l = vnorm(vcross(pts[i], pts[j]))
                if l in self._line_id:
                    continue
                m = 0
                for k in range(91):
                    if vdot(l, pts[k]) == ZERO:
                        m |= 1 << k
                self._line_id[l] = len(self.line_masks)
                self.line_masks.append(m)
        self.nlines = len(self.line_masks)
        # pairwise incidence helpers
        self.pair_line = [[-1] * 91 for _ in range(91)]
        for lid, m in enumerate(self.line_masks):
            members = bitlist(m)
            for a in members:
                for b in members:
                    self.pair_line[a][b] = lid
        self.point_lines: list[list[int]] = [[] for _ in range(91)]
        for lid, m in enumerate(self.line_masks):
            for p in bitlist(m):
                self.point_lines[p].append(lid)
        self.FULL = (1 << 91) - 1

    def line_mask(self, pts) -> int:
        """mask of the line through two points"""
        m = 0
        l = vnorm(vcross(self.vectors[pts[0]], self.vectors[pts[1]]))
        for k in range(91):
            if vdot(l, self.vectors[k]) == ZERO:
                m |= 1 << k
        return m

    def secant_mask(self, pts) -> int:
        """union of all secant lines of the given point set"""
        m = 0
        for a, b in itertools.combinations(pts, 2):
            m |= self.line_mask((a, b))
        return m

    def is_cap(self, pts) -> bool:
        pts = list(pts)
        if len(set(pts)) != len(pts):
            return False
        for t in itertools.combinations(pts, 3):
            if vdot(vnorm(vcross(self.vectors[t[0]], self.vectors[t[1]])),
                    self.vectors[t[2]]) == ZERO:
                return False
        return True

    def extensions(self, pts) -> list[int]:
        """points p (not in pts) such that pts+[p] is again a cap"""
        m = self.secant_mask(pts)
        mine = 0
        for p in pts:
            mine |= 1 << p
        return bitlist(self.FULL & ~m & ~mine)


def bitlist(m: int) -> list[int]:
    out = []
    while m:
        low = m & -m
        out.append(low.bit_length() - 1)
        m ^= low
    return out


# ------------------------------------------------------------- board file

def load_board(path: Path | None = None) -> list[frozenset[int]]:
    path = path or BOARD_PATH
    rows = [ln.split() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert rows[0] == ["91", "91"], f"bad header: {rows[0]}"
    lines = []
    for r in rows[1:]:
        assert r[0] == "10", f"bad line header: {r[0]}"
        assert len(r) == 11, f"bad line length: {len(r)}"
        lines.append(frozenset(int(t) for t in r[1:]))
    return lines


# ----------------------------------------------------- 3x3 matrices / PGL

Matrix = tuple[int, ...]  # row-major 9 entries


def mat(rows) -> Matrix:
    return tuple(int(c) for r in rows for c in r)


def mat_rows(m: Matrix):
    return [m[0:3], m[3:6], m[6:9]]


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    ar, br = mat_rows(a), mat_rows(b)
    out = []
    for i in range(3):
        for j in range(3):
            out.append(ADD[ADD[MUL[ar[i][0]][br[0][j]]][MUL[ar[i][1]][br[1][j]]]][
                MUL[ar[i][2]][br[2][j]]])
    return tuple(out)


def mat_vec(m: Matrix, v) -> tuple[int, int, int]:
    r = mat_rows(m)
    return tuple(
        ADD[ADD[MUL[r[i][0]][v[0]]][MUL[r[i][1]][v[1]]]][MUL[r[i][2]][v[2]]]
        for i in range(3)
    )  # type: ignore[return-value]


def mat_scalar(m: Matrix, c: int) -> Matrix:
    return tuple(MUL[c][x] for x in m)


def mat_canon(m: Matrix) -> Matrix:
    """Canonical representative of the projective class: first nonzero = 1."""
    for x in m:
        if x != ZERO:
            inv = INV[x]
            assert inv is not None
            return tuple(MUL[inv][c] for c in m)
    raise ValueError("zero matrix")


def mat_det(m: Matrix) -> int:
    r = mat_rows(m)
    t1 = MUL[r[0][0]][SUB[MUL[r[1][1]][r[2][2]]][MUL[r[1][2]][r[2][1]]]]
    t2 = MUL[r[0][1]][SUB[MUL[r[1][0]][r[2][2]]][MUL[r[1][2]][r[2][0]]]]
    t3 = MUL[r[0][2]][SUB[MUL[r[1][0]][r[2][1]]][MUL[r[1][1]][r[2][0]]]]
    return ADD[SUB[t1][t2]][t3]


def mat_inv(m: Matrix) -> Matrix:
    """Inverse by Gauss-Jordan over GF(9)."""
    a = [list(mat_rows(m)[i]) + [ONE if i == j else ZERO for j in range(3)] for i in range(3)]
    for col in range(3):
        piv = None
        for i in range(col, 3):
            if a[i][col] != ZERO:
                piv = i
                break
        assert piv is not None, "singular matrix"
        a[col], a[piv] = a[piv], a[col]
        inv = INV[a[col][col]]
        assert inv is not None
        a[col] = [MUL[inv][x] for x in a[col]]
        for i in range(3):
            if i != col and a[i][col] != ZERO:
                f = a[i][col]
                a[i] = [SUB[a[i][k]][MUL[f][a[col][k]]] for k in range(6)]
    return tuple(a[i][3 + j] for i in range(3) for j in range(3))


def cols_matrix(vecs) -> Matrix:
    """The 3x3 matrix whose j-th COLUMN is vecs[j] (row-major 9 entries)."""
    return tuple(vecs[j][i] for i in range(3) for j in range(3))


def solve3(cols, target):
    """Coefficients c with sum_i c_i * cols[i] = target (cols a basis)."""
    inv = mat_inv(cols_matrix(cols))
    # c = A^{-1} target, A = matrix with columns cols[i]
    return tuple(
        ADD[ADD[MUL[inv[3 * i + 0]][target[0]]][MUL[inv[3 * i + 1]][target[1]]]][
            MUL[inv[3 * i + 2]][target[2]]]
        for i in range(3)
    )


def projectivity_from_frames(src4, tgt4) -> Matrix:
    """The unique projectivity M with M src4[i] ~ tgt4[i] for i = 0..3.

    Both 4-tuples must be frames (no three collinear).  Derivation: write
    a4 = sum c_i a_i, b4 = sum d_i b_i in the bases (a1,a2,a3), (b1,b2,b3);
    M a_i = lam_i b_i and M a_4 = lam_4 b_4 force lam_i = lam_4 d_i / c_i.
    Normalise lam_4 = 1, then M = B diag(lam) A^{-1}.
    """
    a = list(src4)
    b = list(tgt4)
    assert vindependent(a[:3]) and vindependent(b[:3])
    c = solve3(a[:3], a[3])
    d = solve3(b[:3], b[3])
    assert all(x != ZERO for x in c) and all(x != ZERO for x in d), "not a frame"
    lam = [MUL[d[i]][INV[c[i]]] for i in range(3)]  # type: ignore[index]
    # M = B * diag(lam) * A^{-1}
    A = cols_matrix(a[:3])
    Ainv = mat_inv(A)
    B = cols_matrix(b[:3])
    Bd = tuple(MUL[B[3 * i + j]][lam[j]] for i in range(3) for j in range(3))
    M = mat_mul(Bd, Ainv)
    for i in range(4):  # self-check: M a_i is a nonzero multiple of b_i
        assert vnorm(mat_vec(M, a[i])) == vnorm(b[i]), "frame formula failed"
    return M


def apply_to_points(m: Matrix, plane: Plane, pts) -> frozenset[int]:
    return frozenset(plane.index[vnorm(mat_vec(m, plane.vectors[p]))] for p in pts)
