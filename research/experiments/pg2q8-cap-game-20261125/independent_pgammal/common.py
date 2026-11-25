"""Independent verification of K1330: PG(2,8) caps under PGL(3,8) and PGammaL(3,8).

Only the Python standard library is used.  Everything here is built from
scratch from the definitions in the task statement:

  GF(8) = GF(2)[x]/(x^3+x+1), elements 0..7 with bit i = coefficient of x^i.
  Projective point = canonical nonzero vector (first nonzero coordinate 1).
  Point index = rank among sorted canonical vectors (lexicographic by the
  coordinate triple with coordinates compared as integers 0..7).

The board file is then checked against lines generated from the vector-space
definition (not against any other artefact).
"""
import os
import sys

N = 73  # number of projective points
Q = 8

# ---------------------------------------------------------------- GF(8) ----
def gf_add(a, b):
    return a ^ b


def gf_mul(a, b):
    """Multiply in GF(2)[x]/(x^3+x+1)."""
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if a & 8:          # x^3 -> x+1
            a ^= 0b1011
    return r


def gf_pow(a, e):
    r = 1
    while e:
        if e & 1:
            r = gf_mul(r, a)
        a = gf_mul(a, a)
        e >>= 1
    return r


GF_INV = [0] * 8
for _a in range(1, 8):
    GF_INV[_a] = gf_pow(_a, 6)   # a^7 = 1, so a^-1 = a^6
GF_SQUARE = [gf_mul(a, a) for a in range(8)]

assert all(gf_mul(a, GF_INV[a]) == 1 for a in range(1, 8))


# ------------------------------------------------------- projective points --
def canon(v):
    a, b, c = v
    if a:
        inv = GF_INV[a]
        return (1, gf_mul(b, inv), gf_mul(c, inv))
    if b:
        inv = GF_INV[b]
        return (0, 1, gf_mul(c, inv))
    return (0, 0, 1)


_CANON = []
for _a in range(8):
    for _b in range(8):
        for _c in range(8):
            if _a or _b or _c:
                _CANON.append(canon((_a, _b, _c)))
_CANON = sorted(set(_CANON))
assert len(_CANON) == N
IDX = {v: i for i, v in enumerate(_CANON)}
POINT = list(_CANON)


def point_index(v):
    return IDX[canon(v)]


def add_points(p, q):
    """Sum of two projective points (as representatives) -> point index."""
    v = tuple(gf_add(a, b) for a, b in zip(POINT[p], POINT[q]))
    return IDX[canon(v)]


def scalar_mul_point(t, p):
    v = tuple(gf_mul(t, a) for a in POINT[p])
    return IDX[canon(v)]


def line_through(p, q):
    """All points on the projective line through p != q, as a frozenset."""
    if p == q:
        raise ValueError("line needs two distinct points")
    a = POINT[p]
    b = POINT[q]
    pts = set()
    # {s*a + t*b : (s,t) != (0,0)}; this is the whole 2-D subspace.
    for s in range(8):
        for t in range(8):
            if s == 0 and t == 0:
                continue
            v = tuple(gf_add(gf_mul(s, x), gf_mul(t, y)) for x, y in zip(a, b))
            pts.add(IDX[canon(v)])
    assert len(pts) == Q + 1
    return frozenset(pts)


# all lines, obtained from all point pairs
LINES = set()
LINE_OF_PAIR = {}
for i in range(N):
    for j in range(i + 1, N):
        L = line_through(i, j)
        LINES.add(L)
        LINE_OF_PAIR[(i, j)] = L
LINES = sorted(LINES, key=lambda L: sorted(L))
assert len(LINES) == N
PAIR_LINE = {}
for L in LINES:
    Ls = sorted(L)
    for x in range(len(Ls)):
        for y in range(x + 1, len(Ls)):
            PAIR_LINE[(Ls[x], Ls[y])] = L
assert len(PAIR_LINE) == N * (N - 1) // 2


def collinear(a, b, c):
    if a == b or a == c or b == c:
        return True
    return c in PAIR_LINE[(min(a, b), max(a, b))]


def is_cap(pts):
    if len(set(pts)) != len(pts):
        return False
    s = sorted(pts)
    for x in range(len(s)):
        for y in range(x + 1, len(s)):
            L = PAIR_LINE[(s[x], s[y])]
            for z in range(y + 1, len(s)):
                if s[z] in L:
                    return False
    return True


# ---------------------------------------------------------------- board ----
def load_board(path):
    with open(path, "r", encoding="utf-8") as f:
        toks = f.read().split()
    assert toks[0] == "73" and toks[1] == "73", toks[:2]
    rest = list(map(int, toks[2:]))
    assert len(rest) == 73 * 10, len(rest)
    lines = []
    k = 0
    for _ in range(73):
        n = rest[k]
        pts = tuple(rest[k + 1:k + 1 + n])
        k += 1 + n
        assert n == 9, n
        assert len(set(pts)) == 9
        lines.append(frozenset(pts))
    return lines


HERE = os.path.dirname(os.path.abspath(__file__))
BOARD_PATH = os.path.normpath(os.path.join(
    HERE, "..", "output", "board_pg2q8.txt"))


# ------------------------------------------------------------ Frobenius ----
def frob_point(p):
    v = POINT[p]
    return IDX[canon(tuple(GF_SQUARE[x] for x in v))]


PHI = tuple(frob_point(p) for p in range(N))
PHI2 = tuple(PHI[PHI[p]] for p in range(N))
PHI3 = tuple(PHI[PHI2[p]] for p in range(N))


# ------------------------------------------------------------ utilities ----
def compose(a, b):
    """Permutation a after b."""
    return tuple(a[b[i]] for i in range(N))


IDENT = tuple(range(N))


def inverse(p):
    r = [0] * N
    for i, x in enumerate(p):
        r[x] = i
    return tuple(r)


def perm_from_map(mapping):
    """mapping: dict point->point (must be a permutation)."""
    p = [None] * N
    for i, j in mapping.items():
        p[i] = j
    assert all(x is not None for x in p)
    assert len(set(p)) == N
    return tuple(p)


def mat_apply(M, v):
    """M is 3x3 tuple of GF(8) ints, v triple; return point index."""
    out = []
    for i in range(3):
        s = 0
        for j in range(3):
            s = gf_add(s, gf_mul(M[3 * i + j], v[j]))
        out.append(s)
    return IDX[canon(tuple(out))]


def perm_from_matrix(M):
    return tuple(mat_apply(M, POINT[p]) for p in range(N))


def mat_mul(A, B):
    C = [0] * 9
    for i in range(3):
        for j in range(3):
            s = 0
            for k in range(3):
                s = gf_add(s, gf_mul(A[3 * i + k], B[3 * k + j]))
            C[3 * i + j] = s
    return tuple(C)


def mat_id():
    return (1, 0, 0, 0, 1, 0, 0, 0, 1)


def mat_elementary(i, j, a):
    """Identity + a*E_ij (i != j), 0-based."""
    M = [0] * 9
    M[0] = M[4] = M[8] = 1
    M[3 * i + j] = a
    return tuple(M)


if __name__ == "__main__":
    board = load_board(BOARD_PATH)
    print("board lines:", len(board))
    print("generated lines:", len(LINES))
    print("board == generated:", sorted(board, key=sorted) == LINES)
    print("phi^3 == id:", PHI3 == IDENT)
    print("phi != id:", PHI != IDENT)
    print("phi^2 == phi^-1:", PHI2 == inverse(PHI))
    for name, pts in [("C6", [2, 3, 10, 16, 18, 21]),
                      ("phi(C6)", [2, 5, 10, 12, 18, 23]),
                      ("D6", [1, 10, 12, 59, 62, 65]),
                      ("phi(D6)", [1, 10, 14, 29, 32, 33])]:
        print(name, "cap:", is_cap(pts))
