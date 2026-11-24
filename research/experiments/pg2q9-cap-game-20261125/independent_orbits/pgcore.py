"""pgcore.py -- self-contained GF(9) / PG(2,9) toolkit.

Independent verifier for the PG(2,9) maximal-cap orbit claims
(experiment pg2q9-cap-game-20261125).  Python standard library only.

Conventions
-----------
GF(9) = GF(3)[x]/(x^2+1).  Field elements are integers 0..8 with

    e = a + 3*b        meaning        a + b*i,     i^2 = -1,

and a, b in {0,1,2}.  So 0,1,2 are the prime field, 3 = i, 4 = 1+i,
5 = 2+i, 6 = 2i, 7 = 1+2i, 8 = 2+2i.

PG(2,9): points are the canonical nonzero vectors of GF(9)^3 (first
nonzero coordinate scaled to 1); lines are the kernels of the nonzero
covectors up to scalar.  Both are indexed 0..90 in a deterministic
(sorted-vector) order.

The board file is the experiment's output/board_pg2q9.txt: first line
"n nlines", then nlines lines each "k p0 ... p_{k-1}" (0-based labels).

Main entry points
-----------------
build_model()          -> Plane  (own PG(2,9) construction, vectors+lines)
read_board(path)       -> Plane  (incidence structure of the board file)
check_plane(P)         -> dict   (projective-plane axiom checks)
find_isomorphism(A,B)  -> list   (phi[a] = b, line-preserving bijection)
mat_perm(P, A)         -> tuple  (permutation of the 91 points of matrix A)
frame_caps(P, frame)   -> dict   (all caps containing a frame, by size)
stabilizer_elements(P, cap) -> list of (matrix, permutation) for Stab_PGL(cap)
"""

from __future__ import annotations

import itertools
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
DEFAULT_BOARD = EXP / "output" / "board_pg2q9.txt"
RESULTS = HERE / "results"

# ------------------------------------------------------------------ GF(9)
NEL = 9


def elt(a: int, b: int) -> int:
    """a + b*i as an integer 0..8."""
    return a + 3 * b


def dec(e: int):
    """integer 0..8 -> (a, b) with e = a + b*i."""
    return e % 3, e // 3


def _tables():
    add = [[0] * NEL for _ in range(NEL)]
    mul = [[0] * NEL for _ in range(NEL)]
    neg = [0] * NEL
    for x in range(NEL):
        ax, bx = dec(x)
        neg[x] = elt((-ax) % 3, (-bx) % 3)
        for y in range(NEL):
            ay, by = dec(y)
            add[x][y] = elt((ax + ay) % 3, (bx + by) % 3)
            mul[x][y] = elt((ax * ay - bx * by) % 3, (ax * by + bx * ay) % 3)
    inv = [None] * NEL
    for x in range(1, NEL):
        for y in range(1, NEL):
            if mul[x][y] == 1:
                inv[x] = y
    return add, mul, neg, inv


ADD, MUL, NEG, INV = _tables()


def gf_axioms():
    """Self-check that (0..8, ADD, MUL) is the field GF(9)."""
    checks = {}
    checks["add_commutative"] = all(ADD[x][y] == ADD[y][x] for x in range(NEL) for y in range(NEL))
    checks["add_associative"] = all(
        ADD[ADD[x][y]][z] == ADD[x][ADD[y][z]] for x in range(NEL) for y in range(NEL) for z in range(NEL)
    )
    checks["mul_commutative"] = all(MUL[x][y] == MUL[y][x] for x in range(NEL) for y in range(NEL))
    checks["mul_associative"] = all(
        MUL[MUL[x][y]][z] == MUL[x][MUL[y][z]] for x in range(NEL) for y in range(NEL) for z in range(NEL)
    )
    checks["distributive"] = all(
        MUL[x][ADD[y][z]] == ADD[MUL[x][y]][MUL[x][z]]
        for x in range(NEL) for y in range(NEL) for z in range(NEL)
    )
    checks["zero_one"] = all(ADD[x][0] == x and MUL[x][1] == x for x in range(NEL))
    checks["all_nonzero_invertible"] = all(INV[x] is not None and MUL[x][INV[x]] == 1 for x in range(1, NEL))
    checks["no_zero_divisors"] = all(
        MUL[x][y] != 0 for x in range(1, NEL) for y in range(1, NEL)
    )
    checks["char_3"] = all(ADD[x][x] == NEG[x] and ADD[ADD[x][x]][x] == 0 for x in range(NEL))
    # i^2 = -1 and x^2+1 has no root in GF(3)
    checks["i_squared_is_minus_1"] = MUL[3][3] == 2
    checks["x2_plus_1_irreducible"] = all(ADD[MUL[a][a]][1] != 0 for a in (0, 1, 2))
    checks["additive_group_is_C3xC3"] = len({elt(a, b) for a in range(3) for b in range(3)}) == 9
    # GF(9)^* is cyclic of order 8: element orders must be 1,2,4,8 with
    # multiplicities phi(1),phi(2),phi(4),phi(8) = 1,1,2,4.
    order_hist = {}
    for x in range(1, NEL):
        o, y = 1, x
        while y != 1:
            y = MUL[y][x]
            o += 1
        order_hist[o] = order_hist.get(o, 0) + 1
    checks["multiplicative_orders"] = order_hist
    checks["multiplicative_group_cyclic_C8"] = order_hist == {1: 1, 2: 1, 4: 2, 8: 4}
    return checks


def _pow(x: int, k: int) -> int:
    r = 1
    for _ in range(k):
        r = MUL[r][x]
    return r


def canon_vec(v):
    """Canonical representative of a nonzero vector: first nonzero entry 1."""
    for x in v:
        if x:
            ix = INV[x]
            return tuple(MUL[ix][z] for z in v)
    return None


# ------------------------------------------------------------------ planes
class Plane:
    """A finite projective plane given by its line list (+ vectors for the model)."""

    __slots__ = (
        "n", "lines", "nlines", "line_sets", "line_index", "point_lines",
        "line_of_pair", "meet", "vectors", "idx",
    )

    def __init__(self, n, lines, vectors=None):
        self.n = n
        self.lines = [tuple(sorted(int(p) for p in L)) for L in lines]
        self.nlines = len(self.lines)
        self.line_sets = [frozenset(L) for L in self.lines]
        self.line_index = {}
        for i, L in enumerate(self.lines):
            self.line_index.setdefault(L, i)
        self.point_lines = [[] for _ in range(n)]
        for i, L in enumerate(self.lines):
            for p in L:
                self.point_lines[p].append(i)
        self.line_of_pair = {}
        for i, L in enumerate(self.lines):
            for a, b in itertools.combinations(L, 2):
                self.line_of_pair[(a, b)] = i
        self.meet = {}
        for i in range(self.nlines):
            si = self.line_sets[i]
            for j in range(i + 1, self.nlines):
                inter = si & self.line_sets[j]
                if len(inter) == 1:
                    (p,) = inter
                    self.meet[(i, j)] = p
                    self.meet[(j, i)] = p
        self.vectors = vectors
        self.idx = {v: i for i, v in enumerate(vectors)} if vectors is not None else None

    def line_through(self, a, b):
        return self.line_of_pair[(a, b) if a < b else (b, a)]


def _canon_covectors():
    out = []
    for first in range(3):
        for rest in itertools.product(range(NEL), repeat=2 - first):
            out.append((0,) * first + (1,) + tuple(rest))
    return sorted(set(out))


def _canon_vectors():
    out = []
    for first in range(3):
        for rest in itertools.product(range(NEL), repeat=2 - first):
            out.append((0,) * first + (1,) + tuple(rest))
    return sorted(set(out))


def build_model():
    """Own construction of PG(2,9) over GF(9) = GF(3)[x]/(x^2+1)."""
    vecs = _canon_vectors()
    assert len(vecs) == 91, len(vecs)
    idx = {v: i for i, v in enumerate(vecs)}
    lines = []
    for co in _canon_covectors():
        pts = []
        for v in vecs:
            s = 0
            for k in range(3):
                s = ADD[s][MUL[co[k]][v[k]]]
            if s == 0:
                pts.append(idx[v])
        assert len(pts) == 10, (co, len(pts))
        lines.append(tuple(sorted(pts)))
    assert len(set(lines)) == 91, len(set(lines))
    return Plane(91, lines, vectors=vecs)


def read_board(path=DEFAULT_BOARD):
    """Parse the board file into a Plane."""
    toks = Path(path).read_text(encoding="utf-8").split()
    n, nl = int(toks[0]), int(toks[1])
    lines = []
    k = 2
    for _ in range(nl):
        sz = int(toks[k])
        k += 1
        lines.append(tuple(int(t) for t in toks[k:k + sz]))
        k += sz
    assert k == len(toks), (k, len(toks))
    return Plane(n, lines)


def check_plane(P, name="plane"):
    """Verify the incidence axioms of a projective plane of order 9."""
    n = P.n
    res = {"name": name, "n": n, "nlines": P.nlines}
    sizes = {len(L) for L in P.lines}
    res["all_lines_size_10"] = sizes == {10}
    res["line_sizes"] = sorted(sizes)
    deg = [len(v) for v in P.point_lines]
    res["point_degree_all_10"] = set(deg) == {10}
    pair_count = {}
    for L in P.lines:
        for a, b in itertools.combinations(L, 2):
            pair_count[(a, b)] = pair_count.get((a, b), 0) + 1
    res["n_pairs"] = len(pair_count)
    res["pair_lambda_1"] = set(pair_count.values()) == {1} and len(pair_count) == n * (n - 1) // 2
    # line-line: every two lines meet in exactly one point
    meet_ok = True
    for i in range(P.nlines):
        si = P.line_sets[i]
        for j in range(i + 1, P.nlines):
            if len(si & P.line_sets[j]) != 1:
                meet_ok = False
                break
        if not meet_ok:
            break
    res["any_two_lines_meet_once"] = meet_ok
    res["distinct_lines"] = len(set(P.lines)) == P.nlines
    res["all_ok"] = all(
        res[k] for k in ("all_lines_size_10", "point_degree_all_10", "pair_lambda_1",
                         "any_two_lines_meet_once", "distinct_lines")
    )
    return res


def pick_frame(P):
    """Four points of P with no three collinear (an ordered projective frame)."""
    n = P.n
    p0 = 0
    p1 = 1
    L01 = P.line_through(p0, p1)
    p2 = next(q for q in range(n) if q not in P.line_sets[L01])
    sides = {P.line_through(p0, p1), P.line_through(p0, p2), P.line_through(p1, p2)}
    p3 = next(q for q in range(n) if all(q not in P.line_sets[s] for s in sides))
    return (p0, p1, p2, p3)


def _propagate(src, dst, phi, inv, kline):
    """Close the partial map under 'line with 2 known points' / 'point on 2 known lines'."""
    n = src.n
    changed = True
    while changed:
        changed = False
        for lid in range(src.nlines):
            imgs = [phi[p] for p in src.lines[lid] if phi[p] >= 0]
            if len(imgs) >= 2:
                ml = dst.line_of_pair[(imgs[0], imgs[1]) if imgs[0] < imgs[1] else (imgs[1], imgs[0])]
                if kline[lid] >= 0:
                    if kline[lid] != ml:
                        return False
                else:
                    ms = dst.line_sets[ml]
                    for m in imgs:
                        if m not in ms:
                            return False
                    kline[lid] = ml
                    changed = True
        for p in range(n):
            if phi[p] >= 0:
                continue
            mls = [kline[l] for l in src.point_lines[p] if kline[l] >= 0]
            if len(mls) >= 2:
                mp = dst.meet.get((mls[0], mls[1]))
                if mp is None:
                    return False
                for ml in mls:
                    if mp not in dst.line_sets[ml]:
                        return False
                if inv[mp] >= 0 and inv[mp] != p:
                    return False
                phi[p] = mp
                inv[mp] = p
                changed = True
    return True


def find_isomorphism(src, dst, verbose=False):
    """Find a line-preserving bijection phi: points(src) -> points(dst)."""
    assert src.n == dst.n and src.nlines == dst.nlines
    fs = pick_frame(src)
    fd = pick_frame(dst)
    phi = [-1] * src.n
    inv = [-1] * dst.n
    kline = [-1] * src.nlines
    for a, b in zip(fs, fd):
        phi[a] = b
        inv[b] = a
    if not _propagate(src, dst, phi, inv, kline):
        raise RuntimeError("frame assignment failed to propagate")
    n = src.n
    nodes = [0]

    def candidates(p):
        allowed = None
        for l in src.point_lines[p]:
            if kline[l] >= 0:
                s = dst.line_sets[kline[l]]
                allowed = set(s) if allowed is None else (allowed & s)
        if allowed is None:
            allowed = range(n)
        return [m for m in allowed if inv[m] < 0]

    def dfs():
        nodes[0] += 1
        best, bestc = -1, None
        for p in range(n):
            if phi[p] >= 0:
                continue
            c = candidates(p)
            if not c:
                return None
            if bestc is None or len(c) < len(bestc):
                best, bestc = p, c
                if len(c) == 1:
                    break
        if best < 0:
            return True
        for m in bestc:
            phi2 = phi[:]
            inv2 = inv[:]
            kline2 = kline[:]
            phi2[best] = m
            inv2[m] = best
            if _propagate(src, dst, phi2, inv2, kline2):
                phi[:] = phi2
                inv[:] = inv2
                kline[:] = kline2
                if dfs():
                    return True
                phi[:] = [-1] * n
                inv[:] = [-1] * dst.n
                kline[:] = [-1] * src.nlines
                # restore the closure of the parent assignment
                for a, b in zip(fs, fd):
                    phi[a] = b
                    inv[b] = a
                _propagate(src, dst, phi, inv, kline)
        return None

    ok = dfs()
    if not ok:
        raise RuntimeError("no isomorphism found")
    if not verify_isomorphism(src, dst, phi):
        raise RuntimeError("isomorphism verification failed")
    if verbose:
        print(f"  isomorphism search nodes: {nodes[0]}")
    return phi


def verify_isomorphism(src, dst, phi):
    n = src.n
    if sorted(phi) != list(range(n)):
        return False
    for L in src.lines:
        imgs = tuple(sorted(phi[p] for p in L))
        if imgs not in dst.line_index:
            return False
    return True


# ------------------------------------------------------- matrices / linear
def mat_mul(A, B):
    return [[ADD[ADD[MUL[A[i][0]][B[0][j]]][MUL[A[i][1]][B[1][j]]]][MUL[A[i][2]][B[2][j]]]
             for j in range(3)] for i in range(3)]


def det3(A):
    """Determinant over GF(9) via the Leibniz expansion."""
    tot = 0
    for perm, sign in (((0, 1, 2), 1), ((1, 2, 0), 1), ((2, 0, 1), 1),
                       ((0, 2, 1), -1), ((2, 1, 0), -1), ((1, 0, 2), -1)):
        term = 1
        for i in range(3):
            term = MUL[term][A[i][perm[i]]]
        if sign == 1:
            tot = ADD[tot][term]
        else:
            tot = ADD[tot][NEG[term]]
    return tot


def mat_perm(P, A):
    """Permutation of the 91 points of PG(2,9) induced by the matrix A."""
    perm = []
    for v in P.vectors:
        w = []
        for r in range(3):
            s = 0
            for c in range(3):
                s = ADD[s][MUL[A[r][c]][v[c]]]
            w.append(s)
        perm.append(P.idx[canon_vec(w)])
    return tuple(perm)


def nullspace(rows, ncols):
    """Basis of {x in GF(9)^ncols : rows . x = 0}."""
    mat = [list(r) for r in rows]
    nrows = len(mat)
    pivots = []
    r = 0
    for c in range(ncols):
        pr = None
        for i in range(r, nrows):
            if mat[i][c]:
                pr = i
                break
        if pr is None:
            continue
        mat[r], mat[pr] = mat[pr], mat[r]
        iv = INV[mat[r][c]]
        mat[r] = [MUL[iv][x] for x in mat[r]]
        for i in range(nrows):
            if i != r and mat[i][c]:
                f = mat[i][c]
                mat[i] = [ADD[mat[i][j]][NEG[MUL[f][mat[r][j]]]] for j in range(ncols)]
        pivots.append(c)
        r += 1
        if r == nrows:
            break
    freepos = [c for c in range(ncols) if c not in pivots]
    basis = []
    for f in freepos:
        v = [0] * ncols
        v[f] = 1
        for i, p in enumerate(pivots):
            v[p] = NEG[mat[i][f]]
        basis.append(v)
    return basis


def frame_map_basis(f, d):
    """Solution space of A f_i = lam_i d_i (12 homogeneous equations, 13 unknowns)."""
    rows = []
    for i in range(4):
        for r in range(3):
            row = [0] * 13
            for c in range(3):
                row[3 * r + c] = f[i][c]
            row[9 + i] = NEG[d[i][r]]
            rows.append(row)
    return nullspace(rows, 13)


def _mat_from_vec(x):
    return [[x[3 * r + c] for c in range(3)] for r in range(3)]


def solve_frame_map(f, d, strict=True):
    """Matrix A (up to scale) with A f_i proportional to d_i for the 4-tuples f, d.

    Returns None when no invertible solution exists.  With strict=True a
    non-unique solution space is an error (it cannot happen when both 4-tuples
    are frames).
    """
    basis = frame_map_basis(f, d)
    if not basis:
        return None
    if len(basis) > 1:
        if strict:
            raise RuntimeError("frame map not unique")
        return None
    A = _mat_from_vec(basis[0])
    if det3(A) == 0:
        return None
    return A


def frame_map_has_invertible(f, d, maxdim=5):
    """Is there any invertible A with A f_i proportional to d_i?  (None if no solution.)"""
    basis = frame_map_basis(f, d)
    if not basis:
        return None
    if len(basis) > maxdim:
        raise RuntimeError("solution space too large")
    # enumerate all nonzero GF(9)-linear combinations of the basis
    for coeffs in itertools.product(range(NEL), repeat=len(basis)):
        if not any(coeffs):
            continue
        x = [0] * 13
        for k, c in enumerate(coeffs):
            if c:
                for j in range(13):
                    x[j] = ADD[x[j]][MUL[c][basis[k][j]]]
        if det3(_mat_from_vec(x)) != 0:
            return True
    return False


# ------------------------------------------------------------ quadratic forms
def quad_form_matrix(coefs):
    """Symmetric matrix A with q(x) = x^T A x for
    q = c0 x^2 + c1 y^2 + c2 z^2 + c3 xy + c4 xz + c5 yz  (char != 2)."""
    c0, c1, c2, c3, c4, c5 = coefs
    h = 2  # 1/2 in GF(3)
    return [[c0, MUL[h][c3], MUL[h][c4]],
            [MUL[h][c3], c1, MUL[h][c5]],
            [MUL[h][c4], MUL[h][c5], c2]]


def quad_form_value(A, v):
    x, y, z = v
    val = ADD[ADD[MUL[A[0][0]][MUL[x][x]]][MUL[A[1][1]][MUL[y][y]]]][MUL[A[2][2]][MUL[z][z]]]
    val = ADD[val][MUL[2][MUL[A[0][1]][MUL[x][y]]]]
    val = ADD[val][MUL[2][MUL[A[0][2]][MUL[x][z]]]]
    val = ADD[val][MUL[2][MUL[A[1][2]][MUL[y][z]]]]
    return val


def conic_point_set(P, A):
    """Point set of the conic x^T A x = 0 in the plane P."""
    return [i for i, v in enumerate(P.vectors) if quad_form_value(A, v) == 0]


# ---------------------------------------------------------------- generators
def e_ij(i, j, a):
    A = [[1 if r == c else 0 for c in range(3)] for r in range(3)]
    A[i][j] = a
    return A


def diag(d, e1, e2):
    return [[d, 0, 0], [0, e1, 0], [0, 0, e2]]


def perm_matrix(p):
    """3x3 permutation matrix mapping basis vector k -> basis vector p[k]."""
    A = [[0] * 3 for _ in range(3)]
    for k in range(3):
        A[p[k]][k] = 1
    return A


def generator_matrices():
    """Elementary transvections E_ij(a), a in {1,i}; diag(i,1,1); 3-cycle."""
    gens = []
    labels = []
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            for a in (1, 3):  # 1 and i
                gens.append(e_ij(i, j, a))
                labels.append(f"E_{i}{j}({a})")
    gens.append(diag(3, 1, 1))
    labels.append("diag(i,1,1)")
    gens.append(perm_matrix((1, 2, 0)))
    labels.append("cycle(012)")
    return gens, labels


# ------------------------------------------------------------- orbit search
def perm_chunk_tables(perm, npts, bits=12):
    """8 chunk tables (bits=12 -> 8 chunks cover 96 >= 91 bits)."""
    nchunk = (npts + bits - 1) // bits
    tabs = []
    for c in range(nchunk):
        tbl = [0] * (1 << bits)
        base = c * bits
        for v in range(1, 1 << bits):
            low = v & -v
            i = low.bit_length() - 1
            k = base + i
            bit = (1 << perm[k]) if k < npts else 0
            tbl[v] = tbl[v ^ low] | bit
        tabs.append(tbl)
    return tabs


def apply_tables(tabs, mask):
    """Apply a permutation (given as chunk tables) to a 91-bit point mask."""
    t = tabs
    if len(t) == 8:
        return (t[0][mask & 0xFFF] | t[1][(mask >> 12) & 0xFFF]
                | t[2][(mask >> 24) & 0xFFF] | t[3][(mask >> 36) & 0xFFF]
                | t[4][(mask >> 48) & 0xFFF] | t[5][(mask >> 60) & 0xFFF]
                | t[6][(mask >> 72) & 0xFFF] | t[7][(mask >> 84) & 0xFFF])
    r = 0
    for c, tab in enumerate(t):
        r |= tab[(mask >> (12 * c)) & 0xFFF]
    return r


def mask_of(points):
    m = 0
    for p in points:
        m |= 1 << p
    return m


def points_of(mask):
    out = []
    i = 0
    while mask:
        if mask & 1:
            out.append(i)
        mask >>= 1
        i += 1
    return out


def orbit(start_mask, tabs_list, collect=True, progress=None):
    """BFS orbit of a point-set mask under a list of permutation tables."""
    seen = {start_mask}
    frontier = [start_mask]
    size = 1
    while frontier:
        nxt = []
        for mask in frontier:
            for tabs in tabs_list:
                m = apply_tables(tabs, mask)
                if m not in seen:
                    seen.add(m)
                    nxt.append(m)
        size += len(nxt)
        frontier = nxt
        if progress is not None:
            progress(size)
    return (seen if collect else None), size


# ------------------------------------------------- caps containing a frame
def frame_caps(P, frame, maxk=10):
    """All caps C with frame subset C subseteq points, |C| <= maxk.

    Returns dict size -> list of (frozenset(C), forbidden_size).
    A cap is maximal iff forbidden_size == P.n (every outside point lies on
    a line spanned by two of its points).
    """
    n = P.n
    frame = sorted(frame)
    forbidden = set(frame)
    for a, b in itertools.combinations(frame, 2):
        forbidden |= P.line_sets[P.line_through(a, b)]
    out = {k: [] for k in range(len(frame), maxk + 1)}
    out[len(frame)].append((frozenset(frame), len(forbidden)))

    def rec(chosen, forb):
        last = chosen[-1]
        if len(chosen) == maxk:
            return
        for q in range(last + 1, n):
            if q in forb:
                continue
            nf = set(forb)
            nf.add(q)
            for a in chosen:
                nf |= P.line_sets[P.line_through(a, q)]
            chosen.append(q)
            out[len(chosen)].append((frozenset(chosen), len(nf)))
            rec(chosen, nf)
            chosen.pop()

    rec(frame, forbidden)
    return out


# --------------------------------------------------------- stabilizer search
def ordered_frames(points, P):
    """Ordered 4-tuples of distinct points with no three collinear."""
    for quad in itertools.permutations(points, 4):
        lines = {P.line_through(quad[a], quad[b]) for a, b in itertools.combinations(range(4), 2)}
        if len(lines) == 6:  # no 3 collinear <=> all 6 joins distinct
            yield quad


def stabilizer_elements(P, cap):
    """All (matrix, permutation) of the PGL-stabilizer of the point set cap.

    Uses one fixed ordered frame f of the cap; every g in Stab gives a unique
    ordered frame d = g(f) inside the cap, so enumerating d and solving for the
    projectivity counts each g exactly once.
    """
    capset = frozenset(cap)
    pts = sorted(capset)
    f = next(ordered_frames(pts, P))
    fvec = [P.vectors[p] for p in f]
    out = []
    for d in ordered_frames(pts, P):
        dvec = [P.vectors[p] for p in d]
        A = solve_frame_map(fvec, dvec)
        if A is None:
            continue
        perm = mat_perm(P, A)
        if frozenset(perm[p] for p in pts) == capset:
            out.append((A, perm))
    return out


def perm_order(perm):
    n = len(perm)
    seen = [False] * n
    o = 1
    for i in range(n):
        if seen[i]:
            continue
        j, c = i, 0
        while not seen[j]:
            seen[j] = True
            j = perm[j]
            c += 1
        if c > 1:
            o = _lcm(o, c)
    return o


def _lcm(a, b):
    x, y = a, b
    while y:
        x, y = y, x % y
    return a // x * b


def cycle_type(perm):
    """Cycle type on the moved points, as a sorted tuple (descending)."""
    n = len(perm)
    seen = [False] * n
    out = []
    for i in range(n):
        if seen[i]:
            continue
        j, c = i, 0
        while not seen[j]:
            seen[j] = True
            j = perm[j]
            c += 1
        if c > 1:
            out.append(c)
    return tuple(sorted(out, reverse=True))


def orbits_of(perm, pts):
    """Cycles of perm restricted to the point set pts (as sorted tuples)."""
    S = set(pts)
    seen = set()
    out = []
    for p in pts:
        if p in seen:
            continue
        cyc = []
        q = p
        while q not in seen:
            seen.add(q)
            cyc.append(q)
            q = perm[q]
        out.append(tuple(cyc))
    return out


def cycle_type_restricted(perm, pts):
    """Cycle lengths of perm on an invariant point set pts."""
    seen = set()
    out = []
    for p in pts:
        if p in seen:
            continue
        q, c = p, 0
        while q not in seen:
            seen.add(q)
            q = perm[q]
            c += 1
        out.append(c)
    return sorted(out, reverse=True)


# ------------------------------------------------- permutation-group utilities
def compose(p, q):
    """p after q:  (p o q)[i] = p[q[i]]."""
    return tuple(p[q[i]] for i in range(len(p)))


def perm_inverse(p):
    inv = [0] * len(p)
    for i, x in enumerate(p):
        inv[x] = i
    return tuple(inv)


def identity_perm(n):
    return tuple(range(n))


def subgroup_generated(gens, n):
    """Closure of {identity} under multiplication by the given permutations."""
    idp = identity_perm(n)
    S = {idp}
    frontier = [idp]
    gens = [g for g in {tuple(g) for g in gens} if g != idp]
    while frontier:
        nf = []
        for g in frontier:
            for s in gens:
                h = compose(g, s)
                if h not in S:
                    S.add(h)
                    nf.append(h)
        frontier = nf
    return S


def small_generating_set(perms, n, order=None):
    """Greedy small generating set of a permutation group given as a list."""
    idp = identity_perm(n)
    gens = []
    S = {idp}
    for p in perms:
        if p in S:
            continue
        gens.append(p)
        S = subgroup_generated(gens, n)
        if order is not None and len(S) == order:
            break
    return gens, S


def derived_subgroup_order(gens, n):
    """Order of the commutator subgroup of <gens>."""
    comms = []
    for g in gens:
        gi = perm_inverse(g)
        for h in gens:
            hi = perm_inverse(h)
            c = compose(compose(g, h), compose(gi, hi))
            if c != identity_perm(n):
                comms.append(c)
    if not comms:
        return 1
    return len(subgroup_generated(comms, n))
