"""Independent library for PG(2,8) conic / cap-game verification.

Python standard library only.  No code from the parent experiment is imported
or copied: the field, the plane, the board check, the conic search, the
PGL(2,8) construction and the cap-game DP are all built here from scratch.

GF(8) = GF(2)[x]/(x^3 + x + 1); elements encoded as ints 0..7 whose binary
digits are the polynomial coefficients (bit0 = 1, bit1 = x, bit2 = x^2).
Point of PG(2,8) = canonical non-zero vector (a,b,c) in GF(8)^3, i.e. the
first non-zero coordinate equals 1.
"""

from __future__ import annotations

import itertools

# --------------------------------------------------------------------------
# GF(8)
# --------------------------------------------------------------------------

_MOD = 0b1011  # x^3 + x + 1


def gf_mul(a: int, b: int) -> int:
    """Product in GF(8) = GF(2)[x]/(x^3+x+1)."""
    r = 0
    aa, bb = a, b
    while bb:
        if bb & 1:
            r ^= aa
        bb >>= 1
        aa <<= 1
    # aa has degree <= 4 here; reduce bits 5,4,3 (bit 5 cannot occur, kept for safety)
    for i in (5, 4, 3):
        if (r >> i) & 1:
            r ^= _MOD << (i - 3)
    return r & 7


def gf_add(a: int, b: int) -> int:
    return a ^ b


GF_MUL = [[gf_mul(a, b) for b in range(8)] for a in range(8)]
GF_ADD = [[a ^ b for b in range(8)] for a in range(8)]
GF_SQ = [GF_MUL[a][a] for a in range(8)]
GF_INV = [None] * 8
for _a in range(1, 8):
    for _b in range(1, 8):
        if GF_MUL[_a][_b] == 1:
            GF_INV[_a] = _b
assert all(GF_INV[a] is not None for a in range(1, 8))


def gf_neg(a: int) -> int:
    """Char 2: -a = a."""
    return a


def field_axiom_report():
    """Brute-force check of the field axioms and of x being primitive."""
    checks = {}
    checks["commutative_mul"] = all(
        GF_MUL[a][b] == GF_MUL[b][a] for a in range(8) for b in range(8)
    )
    checks["associative_mul"] = all(
        GF_MUL[GF_MUL[a][b]][c] == GF_MUL[a][GF_MUL[b][c]]
        for a in range(8)
        for b in range(8)
        for c in range(8)
    )
    checks["distributive"] = all(
        GF_MUL[a][b ^ c] == (GF_MUL[a][b] ^ GF_MUL[a][c])
        for a in range(8)
        for b in range(8)
        for c in range(8)
    )
    checks["inverse"] = all(GF_MUL[a][GF_INV[a]] == 1 for a in range(1, 8))
    checks["identity_1"] = all(GF_MUL[1][a] == a for a in range(8))
    checks["zero"] = all(GF_MUL[0][a] == 0 for a in range(8))
    # x = 2 is primitive (order 7)
    powers = []
    p = 1
    for _ in range(7):
        p = GF_MUL[p][2]
        powers.append(p)
    checks["x_primitive_order_7"] = (powers == [2, 4, 3, 6, 7, 5, 1])
    checks["x3_equals_x_plus_1"] = (GF_MUL[2][GF_MUL[2][2]] == 2 ^ 1)
    # Frobenius is a bijection
    checks["frobenius_bijective"] = sorted(set(GF_SQ)) == list(range(8))
    return checks


# --------------------------------------------------------------------------
# PG(2,8): points, lines
# --------------------------------------------------------------------------

def vcanon(v):
    """Normalise a non-zero GF(8)^3 vector so that its first entry is 1."""
    for c in v:
        if c:
            inv = GF_INV[c]
            return tuple(GF_MUL[inv][x] for x in v)
    return None


def vadd(u, v):
    return (u[0] ^ v[0], u[1] ^ v[1], u[2] ^ v[2])


def vscale(a, v):
    return (GF_MUL[a][v[0]], GF_MUL[a][v[1]], GF_MUL[a][v[2]])


def vdot(u, v):
    return GF_MUL[u[0]][v[0]] ^ GF_MUL[u[1]][v[1]] ^ GF_MUL[u[2]][v[2]]


POINTS = [
    v
    for v in itertools.product(range(8), repeat=3)
    if v != (0, 0, 0) and vcanon(v) == v
]
POINTS.sort()
assert len(POINTS) == 73, len(POINTS)
PIDX = {v: i for i, v in enumerate(POINTS)}


def span_line(u, v):
    """The (unique) projective line through two distinct model points."""
    pts = set()
    for a in range(8):
        for b in range(8):
            if a == 0 and b == 0:
                continue
            w = (
                GF_MUL[a][u[0]] ^ GF_MUL[b][v[0]],
                GF_MUL[a][u[1]] ^ GF_MUL[b][v[1]],
                GF_MUL[a][u[2]] ^ GF_MUL[b][v[2]],
            )
            pts.add(vcanon(w))
    return frozenset(pts)


MODEL_LINES = set()
for i in range(73):
    for j in range(i + 1, 73):
        MODEL_LINES.add(span_line(POINTS[i], POINTS[j]))
MODEL_LINES = sorted(MODEL_LINES, key=lambda s: tuple(sorted(PIDX[p] for p in s)))


def model_line_index_sets():
    """Model lines as frozensets of point indices, sorted lexicographically."""
    out = [frozenset(PIDX[p] for p in L) for L in MODEL_LINES]
    out.sort(key=lambda s: tuple(sorted(s)))
    return out


# --------------------------------------------------------------------------
# Board
# --------------------------------------------------------------------------

def load_board(path):
    with open(path, "r", encoding="utf-8") as fh:
        raw = [ln.split() for ln in fh if ln.strip()]
    header = [int(x) for x in raw[0]]
    lines = []
    for row in raw[1:]:
        n = int(row[0])
        pts = [int(x) for x in row[1:]]
        assert n == len(pts), (n, pts)
        lines.append(tuple(pts))
    return header, lines


class Board:
    """Parsed board together with derived incidence structures."""

    def __init__(self, path):
        self.path = str(path)
        header, lines = load_board(path)
        self.header = header
        self.npoints, self.nlines_declared = header
        self.lines = lines
        self.line_sets = [frozenset(L) for L in lines]
        # line masks (73-bit integers)
        self.line_masks = []
        for L in lines:
            m = 0
            for p in L:
                m |= 1 << p
            self.line_masks.append(m)
        self.FULL = (1 << self.npoints) - 1
        # incidence
        self.point_lines = [[] for _ in range(self.npoints)]
        for li, L in enumerate(lines):
            for p in L:
                self.point_lines[p].append(li)
        # line through a pair of points
        self.line_of_pair = [[None] * self.npoints for _ in range(self.npoints)]
        for li, L in enumerate(lines):
            for p in L:
                for q in L:
                    if p != q:
                        self.line_of_pair[p][q] = li
        self.line_mask_of_pair = [[0] * self.npoints for _ in range(self.npoints)]
        for p in range(self.npoints):
            for q in range(self.npoints):
                if p != q:
                    self.line_mask_of_pair[p][q] = self.line_masks[
                        self.line_of_pair[p][q]
                    ]

    def line_through(self, p, q):
        return self.line_of_pair[p][q]

    def third_points(self, S):
        """Points on a line spanned by a pair of points of S."""
        mask = 0
        S = list(S)
        for a, b in itertools.combinations(S, 2):
            mask |= self.line_mask_of_pair[a][b]
        return mask

    def is_cap(self, S):
        S = list(S)
        for a, b in itertools.combinations(S, 2):
            li = self.line_of_pair[a][b]
            if sum(1 for x in S if x in self.line_sets[li]) > 2:
                return False
        return True

    def maximal_extension_sizes(self, S, limit=None):
        """Sizes of all maximal caps containing S (brute force, small S only)."""
        S = frozenset(S)
        seen = {}
        out = set()

        def rec(cur):
            forb = self.third_points(cur)
            allowed = self.FULL & ~forb & ~sum(1 << p for p in cur)
            if allowed == 0:
                out.add(len(cur))
                return
            m = allowed
            while m:
                b = m & -m
                p = b.bit_length() - 1
                rec(cur | {p})
                m ^= b

        rec(S)
        return out


def verify_board(board):
    """Task 1 checks: is the board PG(2,8), and is the ordering the
    sorted-canonical-vector ordering?"""
    res = {}
    n = board.npoints
    res["header"] = board.header
    res["n_points_declared_73"] = (board.header == [73, 73])
    res["n_lines"] = len(board.lines)
    res["all_lines_size_9"] = all(len(L) == 9 for L in board.lines)
    res["all_points_in_range"] = all(
        0 <= p < 73 for L in board.lines for p in L
    )
    res["all_lines_distinct"] = len(set(board.line_sets)) == len(board.line_sets)

    # every pair on exactly one line
    pair_count = {}
    for li, L in enumerate(board.lines):
        for a, b in itertools.combinations(sorted(L), 2):
            key = (a, b)
            pair_count[key] = pair_count.get(key, 0) + 1
    expected_pairs = 73 * 72 // 2
    res["n_pairs_covered"] = len(pair_count)
    res["all_pairs_once"] = (
        len(pair_count) == expected_pairs and all(v == 1 for v in pair_count.values())
    )
    # point degree
    deg = [len(board.point_lines[p]) for p in range(73)]
    res["point_degrees"] = sorted(set(deg))
    res["all_degrees_9"] = all(d == 9 for d in deg)
    # line sizes distinct points
    res["lines_have_distinct_points"] = all(len(set(L)) == 9 for L in board.lines)

    # --- model comparison ---------------------------------------------------
    model_sets = model_line_index_sets()
    board_sorted = sorted(board.line_sets, key=lambda s: tuple(sorted(s)))
    res["model_n_lines"] = len(model_sets)
    res["model_equals_board_as_sets"] = (
        [frozenset(s) for s in model_sets] == [frozenset(s) for s in board_sorted]
    )
    res["model_equals_board_in_order"] = [
        frozenset(s) for s in model_sets
    ] == [frozenset(s) for s in board.line_sets]
    # point ordering: model point i must be the i-th sorted canonical vector
    pts_ok = all(board.line_sets[li] == frozenset(PIDX[p] for p in L)
                 for li, L in enumerate(MODEL_LINES))
    res["point_ordering_matches"] = pts_ok
    res["model_points_sample"] = [(i, POINTS[i]) for i in (0, 1, 9, 10, 16, 29, 47, 48, 72)]
    return res


# --------------------------------------------------------------------------
# Quadratic forms / conics over GF(8)
# --------------------------------------------------------------------------

def qeval(co, pt):
    """Evaluate q(x,y,z) = q00 x^2 + q11 y^2 + q22 z^2 + q01 xy + q02 xz + q12 yz.

    In characteristic 2 every cross term is counted ONCE; x*y is the same
    field element as y*x, so writing it twice would double-count (and vanish).
    """
    q00, q11, q22, q01, q02, q12 = co
    x, y, z = pt
    return (
        GF_MUL[q00][GF_SQ[x]]
        ^ GF_MUL[q11][GF_SQ[y]]
        ^ GF_MUL[q22][GF_SQ[z]]
        ^ GF_MUL[q01][GF_MUL[x][y]]
        ^ GF_MUL[q02][GF_MUL[x][z]]
        ^ GF_MUL[q12][GF_MUL[y][z]]
    )


def form_row(pt):
    """Row of the linear system 'q vanishes at pt' in unknowns
    (q00,q11,q22,q01,q02,q12)."""
    x, y, z = pt
    return [GF_SQ[x], GF_SQ[y], GF_SQ[z], GF_MUL[x][y], GF_MUL[x][z], GF_MUL[y][z]]


def zero_points(co):
    return [i for i, p in enumerate(POINTS) if qeval(co, p) == 0]


def rref(rows, ncols):
    """Reduced row echelon form over GF(8).  Returns (rows, pivots)."""
    R = [list(r) for r in rows]
    piv = []
    r = 0
    for c in range(ncols):
        pr = None
        for i in range(r, len(R)):
            if R[i][c]:
                pr = i
                break
        if pr is None:
            continue
        R[r], R[pr] = R[pr], R[r]
        inv = GF_INV[R[r][c]]
        R[r] = [GF_MUL[inv][x] for x in R[r]]
        for i in range(len(R)):
            if i != r and R[i][c]:
                fct = R[i][c]
                R[i] = [x ^ GF_MUL[fct][y] for x, y in zip(R[i], R[r])]
        piv.append(c)
        r += 1
        if r == len(R):
            break
    return R[:r], piv


def rank(rows, ncols):
    _, piv = rref(rows, ncols)
    return len(piv)


def nullspace_basis(rows, ncols):
    R, piv = rref(rows, ncols)
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for f in free:
        vec = [0] * ncols
        vec[f] = 1
        for ri, c in enumerate(piv):
            vec[c] = R[ri][f]  # char 2: minus == plus
        basis.append(tuple(vec))
    return basis


def scalar_mult_form(a, co):
    return tuple(GF_MUL[a][c] for c in co)


def canonical_form(co):
    """Scale so the first non-zero coefficient (in the fixed order) is 1."""
    for c in co:
        if c:
            return scalar_mult_form(GF_INV[c], co)
    return None


def all_canonical_forms():
    """One representative per non-zero scalar class of quadratic forms."""
    out = []
    for co in itertools.product(range(8), repeat=6):
        if co == (0, 0, 0, 0, 0, 0):
            continue
        if canonical_form(co) == co:
            out.append(co)
    return out


def polar_matrix(co):
    """Matrix of the polar form B(u,v) = q(u+v)+q(u)+q(v) (char 2, alternating)."""
    q00, q11, q22, q01, q02, q12 = co
    return [[0, q01, q02], [q01, 0, q12], [q02, q12, 0]]


def polar_rank(co):
    """Rank of the alternating polar form (over GF(8))."""
    M = polar_matrix(co)
    R, piv = rref(M, 3)
    return len(piv)


_PT_TABLES = None


def point_tables():
    """Per-point precomputed monomial values (x^2,y^2,z^2,xy,xz,yz)."""
    global _PT_TABLES
    if _PT_TABLES is None:
        _PT_TABLES = [
            (GF_SQ[x], GF_SQ[y], GF_SQ[z], GF_MUL[x][y], GF_MUL[x][z], GF_MUL[y][z])
            for (x, y, z) in POINTS
        ]
    return _PT_TABLES


def zero_set_fast(co):
    """Point indices where q vanishes (same convention as qeval)."""
    q0, q1, q2, q3, q4, q5 = co
    M = GF_MUL
    out = []
    for i, t in enumerate(point_tables()):
        if (
            M[q0][t[0]]
            ^ M[q1][t[1]]
            ^ M[q2][t[2]]
            ^ M[q3][t[3]]
            ^ M[q4][t[4]]
            ^ M[q5][t[5]]
        ) == 0:
            out.append(i)
    return out


# --------------------------------------------------------------------------
# The 5-cap of claim K1323 and the conic through it
# --------------------------------------------------------------------------

BASE_5CAP = (10, 16, 29, 47, 48)


def find_conic_through(pidx):
    """Solve for all quadratic forms vanishing at the given point indices.

    Returns dict(rank, nullity, basis, canonical, zero_set).
    """
    rows = [form_row(POINTS[p]) for p in pidx]
    r = rank(rows, 6)
    basis = nullspace_basis(rows, 6)
    can = None
    zs = None
    if len(basis) == 1:
        can = canonical_form(basis[0])
        zs = zero_set_fast(can)
    return {"rank": r, "nullity": len(basis), "basis": basis,
            "canonical": can, "zero_set": zs}


# --------------------------------------------------------------------------
# Linear-algebra helpers for 3x3 matrices over GF(8)
# --------------------------------------------------------------------------

def mat_mul_vec(M, v):
    return tuple(
        GF_MUL[M[i][0]][v[0]] ^ GF_MUL[M[i][1]][v[1]] ^ GF_MUL[M[i][2]][v[2]]
        for i in range(3)
    )


def mat_mul(A, B):
    return [
        [
            GF_MUL[A[i][0]][B[0][j]]
            ^ GF_MUL[A[i][1]][B[1][j]]
            ^ GF_MUL[A[i][2]][B[2][j]]
            for j in range(3)
        ]
        for i in range(3)
    ]


def mat_inv(A):
    """Inverse of a non-singular 3x3 matrix over GF(8)."""
    aug = [list(A[i]) + [1 if i == j else 0 for j in range(3)] for i in range(3)]
    for c in range(3):
        pr = None
        for i in range(c, 3):
            if aug[i][c]:
                pr = i
                break
        if pr is None:
            return None
        aug[c], aug[pr] = aug[pr], aug[c]
        inv = GF_INV[aug[c][c]]
        aug[c] = [GF_MUL[inv][x] for x in aug[c]]
        for i in range(3):
            if i != c and aug[i][c]:
                f = aug[i][c]
                aug[i] = [x ^ GF_MUL[f][y] for x, y in zip(aug[i], aug[c])]
    return [row[3:] for row in aug]


def solve_vec(A, b):
    """Solve A x = b over GF(8) for a 3x3 matrix A (or return None)."""
    aug = [list(A[i]) + [b[i]] for i in range(3)]
    for c in range(3):
        pr = None
        for i in range(c, 3):
            if aug[i][c]:
                pr = i
                break
        if pr is None:
            return None
        aug[c], aug[pr] = aug[pr], aug[c]
        inv = GF_INV[aug[c][c]]
        aug[c] = [GF_MUL[inv][x] for x in aug[c]]
        for i in range(3):
            if i != c and aug[i][c]:
                f = aug[i][c]
                aug[i] = [x ^ GF_MUL[f][y] for x, y in zip(aug[i], aug[c])]
    return tuple(row[3] for row in aug)


def projectivity_from_four(a, b):
    """Unique projectivity (3x3 matrix, up to scalar) with a[i] |-> b[i]
    for i=0..3, where each quadruple is in general position (no 3 collinear).

    a, b are lists of 4 canonical point triples.  Returns a matrix M with
    vcanon(M a_i) == b_i for all i, or None if the data are not in general
    position.
    """
    # columns are a0,a1,a2 / b0,b1,b2 : build as row-matrices A[i][j] = a_j[i]
    A = [[a[j][i] for j in range(3)] for i in range(3)]
    B = [[b[j][i] for j in range(3)] for i in range(3)]
    alpha = solve_vec(A, a[3])
    beta = solve_vec(B, b[3])
    if alpha is None or beta is None:
        return None
    if 0 in alpha or 0 in beta:
        return None
    Ainv = mat_inv(A)
    if Ainv is None:
        return None
    # M = B * diag(beta_i/alpha_i) * Ainv
    D = [[0] * 3 for _ in range(3)]
    for i in range(3):
        D[i][i] = GF_MUL[beta[i]][GF_INV[alpha[i]]]
    return mat_mul(mat_mul(B, D), Ainv)


def apply_projectivity_to_points(M, pidx_list):
    """Image of a list of point indices under a 3x3 matrix, or None if singular."""
    out = []
    for p in pidx_list:
        w = mat_mul_vec(M, POINTS[p])
        c = vcanon(w)
        if c is None:
            return None
        out.append(PIDX[c])
    return out
