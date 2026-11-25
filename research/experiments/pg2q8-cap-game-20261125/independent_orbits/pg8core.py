"""Independent construction of PG(2,8) and of PGL(3,8) as permutations of its 73 points.

Written from scratch for an independent verification of claim K1324.
Python standard library only.

Conventions (as stated in the task):
  * GF(8) = GF(2)[x]/(x^3 + x + 1); field elements are the integers 0..7 whose
    3 bits are the coordinates in the basis (1, x, x^2).
  * PG(2,8) points are the 1-dimensional subspaces of GF(8)^3, represented by the
    unique vector whose first nonzero coordinate is 1.  Sorting those vectors
    lexicographically gives the board index of the point.
"""

from collections import deque
from functools import reduce

# ----------------------------------------------------------------------------
# GF(8) arithmetic:  x^3 = x + 1  ->  modulus polynomial 0b1011
# ----------------------------------------------------------------------------
_MOD = 0b1011


def gf_mul(a, b):
    r = 0
    for i in range(3):
        if (b >> i) & 1:
            r ^= a << i
    for i in (5, 4, 3):
        if (r >> i) & 1:
            r ^= _MOD << (i - 3)
    return r & 7


def gf_add(a, b):
    return a ^ b


def gf_pow(a, e):
    assert e >= 0
    r = 1
    for _ in range(e):
        r = gf_mul(r, a)
    return r


def gf_inv(a):
    assert a != 0
    return gf_pow(a, 6)  # a^7 = 1 for a != 0


def gf_neg(a):
    return a  # characteristic 2


def check_field():
    """Brute-force field axioms; returns list of failure strings (empty = OK)."""
    bad = []
    # commutativity / associativity / distributivity / inverses
    for a in range(8):
        for b in range(8):
            if gf_mul(a, b) != gf_mul(b, a):
                bad.append("mul not commutative %d %d" % (a, b))
            if gf_add(a, b) != gf_add(b, a):
                bad.append("add not commutative %d %d" % (a, b))
        if a != 0:
            if gf_mul(a, gf_inv(a)) != 1:
                bad.append("bad inverse %d" % a)
    for a in range(8):
        for b in range(8):
            for c in range(8):
                if gf_mul(a, gf_mul(b, c)) != gf_mul(gf_mul(a, b), c):
                    bad.append("mul not associative %d %d %d" % (a, b, c))
                if gf_add(a, gf_add(b, c)) != gf_add(gf_add(a, b), c):
                    bad.append("add not associative %d %d %d" % (a, b, c))
                if gf_mul(a, gf_add(b, c)) != gf_add(gf_mul(a, b), gf_mul(a, c)):
                    bad.append("not distributive %d %d %d" % (a, b, c))
    # x = 2 must generate the multiplicative group of order 7
    pw = []
    v = 1
    for _ in range(7):
        pw.append(v)
        v = gf_mul(v, 2)
    if v != 1 or sorted(pw) != list(range(1, 8)):
        bad.append("x=2 is not a primitive element: %r" % (pw,))
    # x^3 + x + 1 = 0 in the quotient
    if gf_mul(gf_mul(2, 2), 2) != gf_add(2, 1):
        bad.append("x^3 != x+1")
    # x^3+x+1 is irreducible over GF(2): it has no root in GF(2) (f(0)=f(1)=1),
    # and a cubic over a field is irreducible iff it has no linear factor.
    f0 = gf_add(gf_add(0, 0), 1)
    f1 = gf_add(gf_add(1, 1), 1)
    if f0 == 0 or f1 == 0:
        bad.append("x^3+x+1 has a root in GF(2): not irreducible")
    return bad


# ----------------------------------------------------------------------------
# Points and lines of PG(2,8)
# ----------------------------------------------------------------------------
def _canon(v):
    """Normalise a nonzero vector so that its first nonzero coordinate is 1."""
    for c in v:
        if c != 0:
            if c == 1:
                return v
            inv = gf_inv(c)
            return tuple(gf_mul(inv, x) for x in v)
    raise ValueError("zero vector")


def build_points():
    pts = []
    for a in range(8):
        for b in range(8):
            for c in range(8):
                if a == 0 and b == 0 and c == 0:
                    continue
                if a != 0 and a != 1:
                    continue
                if a == 0 and b != 0 and b != 1:
                    continue
                if a == 0 and b == 0 and c != 1:
                    continue
                pts.append((a, b, c))
    return pts


PTS = build_points()
assert len(PTS) == 73
IDX = {v: i for i, v in enumerate(PTS)}
assert all(IDX[PTS[i]] == i for i in range(73))


def build_lines():
    """All lines of PG(2,8) as frozensets of point indices (independent of the board)."""
    lines = set()
    n = len(PTS)
    for i in range(n):
        for j in range(i + 1, n):
            s = set()
            p, q = PTS[i], PTS[j]
            for lam in range(8):
                for mu in range(8):
                    if lam == 0 and mu == 0:
                        continue
                    v = tuple(gf_add(gf_mul(lam, p[k]), gf_mul(mu, q[k])) for k in range(3))
                    s.add(IDX[_canon(v)])
            lines.add(frozenset(s))
    return lines


# ----------------------------------------------------------------------------
# Board file
# ----------------------------------------------------------------------------
def read_board(path):
    with open(path, "r") as f:
        raw = [ln.split() for ln in f if ln.strip()]
    n, b = int(raw[0][0]), int(raw[0][1])
    lines = []
    for row in raw[1:]:
        k = int(row[0])
        assert k == len(row) - 1
        lines.append(frozenset(int(x) for x in row[1:]))
    assert len(lines) == b, (len(lines), b)
    return n, b, lines


# ----------------------------------------------------------------------------
# Matrices over GF(8), acting on points
# ----------------------------------------------------------------------------
def mat_vec(M, v):
    out = []
    for i in range(3):
        s = 0
        for k in range(3):
            s = gf_add(s, gf_mul(M[i][k], v[k]))
        out.append(s)
    return tuple(out)


def mat_det(M):
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    t1 = gf_mul(a, gf_add(gf_mul(e, i), gf_mul(f, h)))
    t2 = gf_mul(b, gf_add(gf_mul(d, i), gf_mul(f, g)))
    t3 = gf_mul(c, gf_add(gf_mul(d, h), gf_mul(e, g)))
    return gf_add(gf_add(t1, t2), t3)


def mat_mul(A, B):
    return tuple(
        tuple(
            reduce(gf_add, (gf_mul(A[i][k], B[k][j]) for k in range(3)), 0)
            for j in range(3)
        )
        for i in range(3)
    )


def eye():
    return tuple(tuple(1 if i == j else 0 for j in range(3)) for i in range(3))


def transvection(i, j, c):
    assert i != j
    M = [[1 if a == b else 0 for b in range(3)] for a in range(3)]
    M[i][j] = c
    return tuple(tuple(r) for r in M)


def diagonal(d0, d1, d2):
    return ((d0, 0, 0), (0, d1, 0), (0, 0, d2))


def coord_swap():
    # permutation matrix swapping coordinates 0 and 1 (det = -1 = 1 in char 2)
    return ((0, 1, 0), (1, 0, 0), (0, 0, 1))


def perm_from_matrix(M):
    assert mat_det(M) != 0
    p = [0] * 73
    for i, v in enumerate(PTS):
        p[i] = IDX[_canon(mat_vec(M, v))]
    return tuple(p)


# ----------------------------------------------------------------------------
# Permutation utilities
# ----------------------------------------------------------------------------
def identity(n=73):
    return tuple(range(n))


def pcompose(a, b):
    """a after b."""
    return tuple(a[b[i]] for i in range(len(a)))


def pinv(a):
    r = [0] * len(a)
    for i, x in enumerate(a):
        r[x] = i
    return tuple(r)


def porder(a):
    n = len(a)
    k = 1
    x = a
    while x != tuple(range(n)):
        x = pcompose(a, x)
        k += 1
    return k


def permute_mask(pbits, mask):
    """Image of a point set (bitmask) under the permutation with bit table pbits."""
    res = 0
    m = mask
    while m:
        lb = m & -m
        res |= pbits[lb.bit_length() - 1]
        m ^= lb
    return res


# ----------------------------------------------------------------------------
# Schreier-Sims (deterministic; monotone growth + work-list fixpoint)
# ----------------------------------------------------------------------------
class BSGS:
    """Base and strong generating set for a permutation group on n points.

    Invariants maintained:
      * gens[i] is a set of permutations fixing base[0..i-1];
      * trans[i] is the complete orbit of base[i] under <gens[i]>, with
        trans[i][b] a group element mapping base[i] to b;
      * gens[0] contains every generator handed to add_generator().

    The chain is saturated until every Schreier generator of every level sifts
    to the identity; then order() = product of orbit lengths is |<gens>|.
    """

    def __init__(self, n=73):
        self.n = n
        self.base = []   # base points
        self.gens = []   # gens[i]: dict (ordered set) of level-i generators
        self.trans = []  # trans[i]: dict pos -> perm taking base[i] to pos
        self._id = tuple(range(n))

    # -- orbit / transversal -------------------------------------------------
    def _orbit(self, i):
        alpha = self.base[i]
        T = {alpha: self._id}
        stack = [alpha]
        gens = list(self.gens[i])
        while stack:
            b = stack.pop()
            Tb = T[b]
            for g in gens:
                c = g[b]
                if c not in T:
                    T[c] = pcompose(g, Tb)
                    stack.append(c)
        return T

    # -- sifting -------------------------------------------------------------
    def sift(self, g, start=0):
        i = start
        while i < len(self.base):
            img = g[self.base[i]]
            Ti = self.trans[i]
            if img not in Ti:
                return g, i
            g = pcompose(pinv(Ti[img]), g)
            i += 1
        return g, len(self.base)

    # -- construction --------------------------------------------------------
    def _new_level(self, h):
        pt = next(x for x in range(self.n) if h[x] != x)
        assert pt not in self.base
        self.base.append(pt)
        self.gens.append({h: None})
        self.trans.append(self._orbit(len(self.base) - 1))

    def add_generator(self, g):
        if g == self._id:
            return
        if not self.base:
            self._new_level(g)
        else:
            if g in self.gens[0]:
                return
            self.gens[0][g] = None
            self.trans[0] = self._orbit(0)
        self._saturate()

    def _saturate(self):
        """Close the chain: every level-i Schreier generator must lie in <gens[i+1]>.

        Residues are added to *all* stabiliser levels 1..j they belong to, so
        the level groups are nested: H_0 = G >= H_1 >= H_2 >= ... where
        H_i = <gens[i]> is the stabiliser of base[0..i-1].
        Correctness (why order() = |G|): the Schreier generators of level i
        generate Stab_{H_i}(base[i]); each of them is reduced to the identity by
        transversal elements of levels i+1.., and by nesting all those lie in
        H_{i+1}; conversely gens[i+1] fixes base[0..i].  Hence
        Stab_{H_i}(base[i]) = H_{i+1} and |H_i| = |orbit_i| * |H_{i+1}|.
        """
        todo = list(range(len(self.base) - 1, -1, -1))
        while todo:
            i = todo.pop()
            if i >= len(self.base):
                continue
            top = self._add_one_residue(i)
            if top is not None:
                todo = list(range(min(top, len(self.base) - 1), -1, -1))

    def _add_one_residue(self, i):
        """Install one missing stabiliser generator found at level i.

        Returns the deepest level whose transversal changed, or None.
        """
        Ti = self.trans[i]
        for b in list(Ti.keys()):
            Tb = Ti[b]
            for s in list(self.gens[i]):
                c = s[b]
                x = pcompose(pinv(Ti[c]), pcompose(s, Tb))
                if x == self._id:
                    continue
                y, j = self.sift(x, i + 1)
                if y == self._id:
                    continue
                return self._install(y, j)
        return None

    def _install(self, y, j):
        if j == len(self.base):
            self._new_level(y)
            top = j
        else:
            top = j
        for k in range(1, top + 1):
            if y in self.gens[k]:
                continue
            self.gens[k][y] = None
            self.trans[k] = self._orbit(k)
        return top

    def verify(self):
        """Check that (base, gens, trans) is a genuine BSGS; return count of failures."""
        fails = 0
        for i in range(len(self.base)):
            Ti = self.trans[i]
            for b in Ti:
                Tb = Ti[b]
                for s in self.gens[i]:
                    x = pcompose(pinv(Ti[s[b]]), pcompose(s, Tb))
                    if x == self._id:
                        continue
                    y, _ = self.sift(x, i + 1)
                    if y != self._id:
                        fails += 1
        return fails

    def order(self):
        n = 1
        for T in self.trans:
            n *= len(T)
        return n

    def report(self):
        return {
            "base": self.base,
            "orbit_sizes": [len(T) for T in self.trans],
            "num_level_gens": [len(g) for g in self.gens],
            "order": self.order(),
            "verify_failures": self.verify(),
        }


def bsgs_order(gens, n=73):
    B = BSGS(n)
    for g in gens:
        B.add_generator(g)
    return B


def closure_order(gens, n=73, cap=200000):
    """Brute-force order of <gens> by BFS over permutations (small groups only)."""
    ident = tuple(range(n))
    seen = {ident}
    stack = [ident]
    while stack:
        x = stack.pop()
        for g in gens:
            y = pcompose(g, x)
            if y not in seen:
                seen.add(y)
                stack.append(y)
                if len(seen) > cap:
                    raise RuntimeError("closure too large")
    return len(seen)


# ----------------------------------------------------------------------------
# Caps
# ----------------------------------------------------------------------------
def mask_of(s):
    m = 0
    for x in s:
        m |= 1 << x
    return m


def popcount(m):
    return bin(m).count("1")


def set_of(m):
    return [i for i in range(m.bit_length()) if (m >> i) & 1]


class Geometry:
    def __init__(self, n, lines):
        self.n = n
        self.lines = [frozenset(L) for L in lines]
        self.line_set = set(self.lines)
        self.line_masks = [mask_of(L) for L in self.lines]
        # line through a pair of points
        self.pair_line = {}
        for L in self.lines:
            pts = sorted(L)
            for a in range(len(pts)):
                for b in range(a + 1, len(pts)):
                    self.pair_line[(pts[a], pts[b])] = L
        self.pairs = len(self.pair_line)
        self.point_lines = {p: [] for p in range(n)}
        for L in self.lines:
            for p in L:
                self.point_lines[p].append(L)

    def line_through(self, a, b):
        if a > b:
            a, b = b, a
        return self.pair_line[(a, b)]

    def is_cap(self, S):
        """True iff no three points of S are collinear."""
        S = sorted(S)
        for i in range(len(S)):
            for j in range(i + 1, len(S)):
                L = self.line_through(S[i], S[j])
                for k in range(j + 1, len(S)):
                    if S[k] in L:
                        return False
        return True

    def blocked(self, S):
        """Union of the lines spanned by pairs of S."""
        b = 0
        S = sorted(S)
        for i in range(len(S)):
            for j in range(i + 1, len(S)):
                b |= mask_of(self.line_through(S[i], S[j]))
        return b

    def addable(self, S):
        """Points not in S that can be added while keeping the cap property."""
        b = self.blocked(S)
        return [p for p in range(self.n) if not ((b >> p) & 1)]

    def is_maximal_cap(self, S):
        return self.is_cap(S) and len(self.addable(S)) == 0

    def line_ok(self, perm):
        """True iff perm maps every line onto a line (i.e. is a collineation)."""
        for L in self.lines:
            img = frozenset(perm[x] for x in L)
            if img not in self.line_set:
                return False, L
        return True, None


def apply_perm_to_set(perm, S):
    return frozenset(perm[x] for x in S)


# ----------------------------------------------------------------------------
# Orbit BFS on sets (bitmasks)
# ----------------------------------------------------------------------------
def orbit_of_mask(start_mask, perms, pbits=None, limit=None):
    if pbits is None:
        pbits = [[1 << p[i] for i in range(len(p))] for p in perms]
    seen = {start_mask}
    stack = [start_mask]
    while stack:
        m = stack.pop()
        for tb in pbits:
            r = permute_mask(tb, m)
            if r not in seen:
                seen.add(r)
                stack.append(r)
                if limit is not None and len(seen) > limit:
                    return seen
    return seen
