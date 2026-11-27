"""Independent re-implementation of PG(2,8) and PGL(3,8), written from scratch
for the K1327 all-orbits verification.

Conventions (as stated in the task):
  * GF(8) = GF(2)[x]/(x^3 + x + 1); the field element a0 + a1*x + a2*x^2 is
    encoded as the integer a0 + 2*a1 + 4*a2  (so x == 2).
  * Points of PG(2,8) are the 1-dimensional subspaces of GF(8)^3, each
    represented by its *canonical* vector: the unique vector in the subspace
    whose first non-zero coordinate equals 1.
  * The board index of a point is its rank (0-based) among all canonical
    non-zero vectors sorted by integer value a*64 + b*8 + c, which is the same
    as lexicographic order on the coordinate triple.

Nothing here reads any file except the board itself (read-only).
"""

# --------------------------------------------------------------------------
# GF(8) arithmetic.  Modulus x^3 + x + 1, i.e. 0b1011 = 11.
# --------------------------------------------------------------------------
_POLY = 0b1011

# x is primitive: 2^0..2^6 = 1,2,4,3,6,7,5  (2^7 = 1)
EXP = [0] * 14
LOG = [0] * 8
_x = 1
for _i in range(7):
    EXP[_i] = _x
    LOG[_x] = _i
    _x = _x << 1
    if _x & 0b1000:
        _x ^= _POLY
EXP[7:14] = EXP[0:7]


def gf_mul(a, b):
    """Multiply two GF(8) elements (integers 0..7)."""
    if a == 0 or b == 0:
        return 0
    return EXP[(LOG[a] + LOG[b]) % 7]


def gf_inv(a):
    assert a != 0
    return EXP[(7 - LOG[a]) % 7]


def gf_div(a, b):
    if a == 0:
        return 0
    return EXP[(LOG[a] - LOG[b]) % 7]


def gf_sq(a):
    return gf_mul(a, a)


def gf_pow(a, n):
    if n == 0:
        return 1
    if a == 0:
        return 0
    return EXP[(LOG[a] * n) % 7]


# Multiplication table, checked against a direct shift-and-xor implementation.
def _gf_mul_slow(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if a & 0b1000:
            a ^= _POLY
    return r


for _a in range(8):
    for _b in range(8):
        assert gf_mul(_a, _b) == _gf_mul_slow(_a, _b), (_a, _b)
        assert gf_mul(_a, _b) == gf_mul(_b, _a)
# associativity / distributivity spot checks (exhaustive)
for _a in range(8):
    for _b in range(8):
        for _c in range(8):
            assert gf_mul(gf_mul(_a, _b), _c) == gf_mul(_a, gf_mul(_b, _c))
            assert gf_mul(_a, _b ^ _c) == gf_mul(_a, _b) ^ gf_mul(_a, _c)
# field axioms: every non-zero element invertible, x^7 = 1, x has order 7
assert all(gf_mul(a, gf_inv(a)) == 1 for a in range(1, 8))
assert EXP[7] == 1 and len(set(EXP[:7])) == 7

# x^3 + x + 1 is irreducible over GF(2): it has no root in GF(2).
assert all((v ** 3) ^ v ^ 1 for v in (0, 1))


# --------------------------------------------------------------------------
# Vectors and matrices over GF(8)
# --------------------------------------------------------------------------
def vadd(u, v):
    return (u[0] ^ v[0], u[1] ^ v[1], u[2] ^ v[2])


def vscale(l, v):
    return (gf_mul(l, v[0]), gf_mul(l, v[1]), gf_mul(l, v[2]))


def vdot(u, v):
    return gf_mul(u[0], v[0]) ^ gf_mul(u[1], v[1]) ^ gf_mul(u[2], v[2])


def vcross(u, v):
    return (
        gf_mul(u[1], v[2]) ^ gf_mul(u[2], v[1]),
        gf_mul(u[2], v[0]) ^ gf_mul(u[0], v[2]),
        gf_mul(u[0], v[1]) ^ gf_mul(u[1], v[0]),
    )


def normalize(v):
    """Canonical representative of the 1-dim subspace spanned by v (v != 0)."""
    for c in v:
        if c:
            inv = gf_inv(c)
            return (gf_mul(inv, v[0]), gf_mul(inv, v[1]), gf_mul(inv, v[2]))
    raise ValueError("zero vector")


def mat_mul(A, B):
    C = []
    for i in range(3):
        row = []
        for j in range(3):
            s = 0
            for k in range(3):
                s ^= gf_mul(A[i][k], B[k][j])
            row.append(s)
        C.append(tuple(row))
    return tuple(C)


def mat_vec(A, v):
    return tuple(
        gf_mul(A[i][0], v[0]) ^ gf_mul(A[i][1], v[1]) ^ gf_mul(A[i][2], v[2])
        for i in range(3)
    )


def mat_det(A):
    return (
        gf_mul(A[0][0], gf_mul(A[1][1], A[2][2]) ^ gf_mul(A[1][2], A[2][1]))
        ^ gf_mul(A[0][1], gf_mul(A[1][0], A[2][2]) ^ gf_mul(A[1][2], A[2][0]))
        ^ gf_mul(A[0][2], gf_mul(A[1][0], A[2][1]) ^ gf_mul(A[1][1], A[2][0]))
    )


IDENT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


def mat_inv(A):
    d = mat_det(A)
    assert d != 0, "singular matrix"
    di = gf_inv(d)
    # adjugate
    C = [
        [
            gf_mul(A[(j + 1) % 3][(i + 1) % 3], A[(j + 2) % 3][(i + 2) % 3])
            ^ gf_mul(A[(j + 1) % 3][(i + 2) % 3], A[(j + 2) % 3][(i + 1) % 3])
            for j in range(3)
        ]
        for i in range(3)
    ]
    return tuple(tuple(gf_mul(di, C[i][j]) for j in range(3)) for i in range(3))


# --------------------------------------------------------------------------
# Points of PG(2,8) with the board labelling
# --------------------------------------------------------------------------
def _canonical_vectors():
    out = []
    for a in range(8):
        for b in range(8):
            for c in range(8):
                v = (a, b, c)
                if v == (0, 0, 0):
                    continue
                if normalize(v) == v:
                    out.append(v)
    out.sort(key=lambda v: (v[0] << 6) | (v[1] << 3) | v[2])
    return out


POINTS = _canonical_vectors()          # POINTS[rank] = canonical vector
assert len(POINTS) == 73, len(POINTS)
PIDX = {v: i for i, v in enumerate(POINTS)}
assert len(PIDX) == 73
assert POINTS[0] == (0, 0, 1)          # the unique vector with a = b = 0
assert POINTS[1] == (0, 1, 0) and POINTS[8] == (0, 1, 7)
assert POINTS[9] == (1, 0, 0) and POINTS[10] == (1, 0, 1)
assert POINTS[72] == (1, 7, 7)


def point_index(v):
    """board index of the projective point spanned by the non-zero vector v."""
    return PIDX[normalize(v)]


def rank_to_vec(r):
    return POINTS[r]


def canonical_lines():
    """The 73 lines of PG(2,8) in the board labelling, each as a frozenset."""
    lines = {}
    for i in range(73):
        for j in range(i + 1, 73):
            u, v = POINTS[i], POINTS[j]  # independent (distinct 1-spaces)
            w = vcross(u, v)
            assert w != (0, 0, 0)
            s = frozenset(k for k in range(73) if vdot(w, POINTS[k]) == 0)
            assert len(s) == 9
            lines.setdefault(s, None)
    return lines


# --------------------------------------------------------------------------
# The board (read-only)
# --------------------------------------------------------------------------
BOARD_PATH = (
    r"C:\Users\yuubi\ghq\github.com\yuubinnkyoku\kyouen-researches"
    r"\research\experiments\pg2q8-cap-game-20261125\output\board_pg2q8.txt"
)


def read_board(path=BOARD_PATH):
    with open(path, "r", encoding="utf-8") as fh:
        toks = fh.read().split()
    n, m = int(toks[0]), int(toks[1])
    pos = 2
    lines = []
    for _ in range(m):
        k = int(toks[pos]); pos += 1
        lines.append(tuple(int(toks[pos + t]) for t in range(k)))
        pos += k
    assert pos == len(toks), (pos, len(toks))
    return n, m, lines


# --------------------------------------------------------------------------
# Permutation induced on the 73 points by a 3x3 matrix
# --------------------------------------------------------------------------
def matrix_perm(A):
    """perm[p] = image of point p under v -> A v.  Requires det A != 0."""
    assert mat_det(A) != 0
    perm = [point_index(mat_vec(A, POINTS[p])) for p in range(73)]
    assert sorted(perm) == list(range(73))
    return tuple(perm)


def perm_act(perm, mask):
    """Act on a 73-bit point mask."""
    out = 0
    m = mask
    while m:
        b = m & -m
        out |= 1 << perm[b.bit_length() - 1]
        m ^= b
    return out


def perm_act_set(perm, s):
    return frozenset(perm[p] for p in s)


# --------------------------------------------------------------------------
# Caps
# --------------------------------------------------------------------------
def is_cap(s, lines=None):
    """True iff no three points of the set s are collinear."""
    s = list(s)
    for a in range(len(s)):
        for b in range(a + 1, len(s)):
            for c in range(b + 1, len(s)):
                if _collinear(s[a], s[b], s[c]):
                    return False
    return True


def _collinear(p, q, r):
    u, v, w = POINTS[p], POINTS[q], POINTS[r]
    return vdot(vcross(u, v), w) == 0


def line_through(p, q):
    w = vcross(POINTS[p], POINTS[q])
    return frozenset(k for k in range(73) if vdot(w, POINTS[k]) == 0)


# --------------------------------------------------------------------------
# PGL(3,8) generators (verified in task 2)
# --------------------------------------------------------------------------
# D : x0 -> x*x0            (diagonal)
# T : x0 -> x0 + x1         (transvection)
# S : swap x0,x1            (permutation)
# U : swap x1,x2            (permutation)
GEN_D = ((2, 0, 0), (0, 1, 0), (0, 0, 1))
GEN_T = ((1, 1, 0), (0, 1, 0), (0, 0, 1))
GEN_S = ((0, 1, 0), (1, 0, 0), (0, 0, 1))
GEN_U = ((1, 0, 0), (0, 0, 1), (0, 1, 0))
GENERATORS = (GEN_D, GEN_T, GEN_S, GEN_U)


def perm_inverse(perm):
    inv = [0] * len(perm)
    for i, p in enumerate(perm):
        inv[p] = i
    return tuple(inv)


def perm_compose(a, b):
    """(a o b)(i) = a[b[i]]"""
    return tuple(a[b[i]] for i in range(len(a)))


def gf8_name(a):
    if a == 0:
        return "0"
    names = {1: "1", 2: "x", 4: "x^2", 3: "x+1", 6: "x^2+x", 7: "x^2+x+1", 5: "x^2+1"}
    return names[a]


def mat_str(A):
    return "[" + "; ".join(", ".join(gf8_name(x) for x in row) for row in A) + "]"
