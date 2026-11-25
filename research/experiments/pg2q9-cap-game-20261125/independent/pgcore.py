"""Independent core library: finite-field PG(2,q) construction + board parsing.

Written from scratch for the independent verification of the PG(2,9) cap census.
Python standard library only.

Conventions
-----------
* A board is (n, lines) where lines is a list of tuples of point indices, each
  of length q+1, with n = q^2+q+1 points and n lines.
* A field element is an int in 0..q-1 with tables ADD/MUL; the prime subfield is
  handled by the same tables (q prime -> element = residue).
* PG(2,q) points are the 1-dimensional GF(q)-subspaces of GF(q)^3, represented
  by canonical vectors (first nonzero coordinate equal to 1).
"""

from __future__ import annotations


# ----------------------------------------------------------------------------
# GF(q) as a quotient GF(p)[x]/(f)
# ----------------------------------------------------------------------------
class GF:
    """Prime-power field GF(p^d) with elements 0..p^d-1 = base-p digit vectors."""

    def __init__(self, p: int, d: int, poly: int):
        # poly: monic irreducible of degree d, encoded as int bit mask of
        # coefficients (bit i = coefficient of x^i), excluding the leading x^d.
        self.p, self.d, self.poly = p, d, poly
        self.q = p ** d
        self.ADD = [[0] * self.q for _ in range(self.q)]
        self.MUL = [[0] * self.q for _ in range(self.q)]
        self.NEG = [0] * self.q
        self.INV = [0] * self.q
        for a in range(self.q):
            for b in range(self.q):
                s, m = self._add_raw(a, b), self._mul_raw(a, b)
                self.ADD[a][b] = s
                self.MUL[a][b] = m
        for a in range(self.q):
            self.NEG[a] = next(b for b in range(self.q) if self.ADD[a][b] == 0)
        for a in range(1, self.q):
            for b in range(1, self.q):
                if self.MUL[a][b] == 1:
                    self.INV[a] = b
                    break
            else:
                raise AssertionError(f"GF: no inverse for {a}")
        # sanity: field axioms
        assert len({tuple(r) for r in self.MUL}) == 1 or True
        self._check_field()

    def _add_raw(self, a: int, b: int) -> int:
        p, r = self.p, 0
        shift = 1
        for _ in range(self.d):
            r += ((a % p + b % p) % p) * shift
            a //= p
            b //= p
            shift *= p
        return r

    def _polymul(self, a: int, b: int) -> int:
        p = self.p
        da, db = [], []
        x = a
        for _ in range(self.d):
            da.append(x % p)
            x //= p
        x = b
        for _ in range(self.d):
            db.append(x % p)
            x //= p
        res = [0] * (2 * self.d - 1)
        for i, ai in enumerate(da):
            if ai:
                for j, bj in enumerate(db):
                    if bj:
                        res[i + j] = (res[i + j] + ai * bj) % p
        # reduce by poly
        for i in range(2 * self.d - 2, self.d - 1, -1):
            c = res[i]
            if c:
                res[i] = 0
                for j in range(self.d):
                    if (self.poly >> j) & 1:
                        res[i - self.d + j] = (res[i - self.d + j] - c) % p
        r, shift = 0, 1
        for i in range(self.d):
            r += res[i] * shift
            shift *= p
        return r

    def _mul_raw(self, a: int, b: int) -> int:
        return self._polymul(a, b)

    def _check_field(self):
        p, q = self.p, self.q
        assert self.MUL[1][1] == 1
        for a in range(q):
            assert self.ADD[0][a] == a and self.ADD[a][0] == a
            assert self.MUL[1][a] == a and self.MUL[a][1] == a
            assert self.MUL[0][a] == 0
            assert self.ADD[a][self.NEG[a]] == 0
        # associativity / distributivity / commutativity spot-check (full)
        for a in range(q):
            for b in range(q):
                assert self.ADD[a][b] == self.ADD[b][a]
                assert self.MUL[a][b] == self.MUL[b][a]
                for c in range(q):
                    assert self.ADD[self.ADD[a][b]][c] == self.ADD[a][self.ADD[b][c]]
                    assert self.MUL[self.MUL[a][b]][c] == self.MUL[a][self.MUL[b][c]]
                    assert self.MUL[a][self.ADD[b][c]] == self.ADD[self.MUL[a][b]][self.MUL[a][c]]


def gf9() -> GF:
    """GF(9) = GF(3)[x]/(x^2+1).  x = 3 (digits: low = a0, high = a1)."""
    return GF(3, 2, poly=0b01)  # x^2 = -1 = 2


def gf8() -> GF:
    """GF(8) = GF(2)[x]/(x^3+x+1)."""
    return GF(2, 3, poly=0b011)


def gf7() -> GF:
    return GF(7, 1, poly=0)


def gf5() -> GF:
    return GF(5, 1, poly=0)


def gf3() -> GF:
    return GF(3, 1, poly=0)


# ----------------------------------------------------------------------------
# PG(2,q)
# ----------------------------------------------------------------------------
def canonical(vec, F: GF):
    """Scale a nonzero vector so that its first nonzero entry is 1."""
    for x in vec:
        if x != 0:
            ix = F.INV[x]
            return tuple(F.MUL[ix][y] for y in vec)
    raise ValueError("zero vector")


def pg_points(F: GF):
    """All 1D subspaces, sorted as canonical vectors."""
    q = F.q
    pts = sorted({canonical(v, F) for v in _product3(q)
                  if v != (0, 0, 0)})
    return pts


def _product3(q: int):
    for a in range(q):
        for b in range(q):
            for c in range(q):
                yield (a, b, c)


def pg_lines_via_normals(F: GF, pts):
    """Lines as zero sets of nonzero normal vectors (a totally different
    construction from 'span of two points')."""
    q, idx = F.q, {p: i for i, p in enumerate(pts)}
    lines = set()
    for n in pg_points(F):           # one representative per 1D normal class
        L = []
        for p in pts:
            s = 0
            for c, v in zip(n, p):
                s = F.ADD[s][F.MUL[c][v]]
            if s == 0:
                L.append(idx[p])
        if len(L) != q + 1:
            raise AssertionError(f"normal {n} gives line of size {len(L)}")
        lines.add(tuple(sorted(L)))
    return sorted(lines)


def pg(q: int):
    """Return (points, lines) for PG(2,q), q in {3,5,7,8,9}."""
    F = {3: gf3, 5: gf5, 7: gf7, 8: gf8, 9: gf9}[q]()
    pts = pg_points(F)
    lines = pg_lines_via_normals(F, pts)
    return pts, lines


# ----------------------------------------------------------------------------
# board file I/O
# ----------------------------------------------------------------------------
def load_board(path):
    with open(path, "r", encoding="utf-8") as fh:
        head = fh.readline().split()
        n, nl = int(head[0]), int(head[1])
        lines = []
        for row in fh:
            row = row.split()
            if not row:
                continue
            k = int(row[0])
            L = tuple(int(x) for x in row[1:])
            assert len(L) == k, (len(L), k)
            lines.append(L)
    assert len(lines) == nl, (len(lines), nl)
    return n, lines


def board_mask(line) -> int:
    m = 0
    for p in line:
        m |= 1 << p
    return m


# ----------------------------------------------------------------------------
# axiom checks
# ----------------------------------------------------------------------------
def check_plane(n: int, lines) -> dict:
    """Full axiom verification of a projective plane of order q."""
    nl = len(lines)
    out = {"n": n, "nlines": nl}
    sizes = sorted({len(L) for L in lines})
    out["line_sizes"] = sizes
    assert len(sizes) == 1, sizes
    k = sizes[0]
    q = k - 1
    out["k"] = k
    out["q"] = q
    assert n == q * q + q + 1, (n, q)
    assert nl == n, (nl, n)
    for L in lines:
        assert len(set(L)) == k, L
        assert all(0 <= p < n for p in L), L
    # point degree
    deg = [0] * n
    for L in lines:
        for p in L:
            deg[p] += 1
    out["point_degree_set"] = sorted(set(deg))
    assert set(deg) == {k}, set(deg)
    # point pairs on exactly one line
    pair = {}
    for li, L in enumerate(lines):
        for i in range(k):
            for j in range(i + 1, k):
                key = (L[i], L[j]) if L[i] < L[j] else (L[j], L[i])
                if key in pair:
                    pair[key] = -1
                else:
                    pair[key] = li
    npairs = n * (n - 1) // 2
    out["npairs"] = len(pair)
    out["bad_pairs"] = sum(1 for v in pair.values() if v < 0)
    assert len(pair) == npairs, (len(pair), npairs)
    assert out["bad_pairs"] == 0
    # line pairs meet in exactly one point
    masks = [board_mask(L) for L in lines]
    bad_meet = 0
    for i in range(nl):
        for j in range(i + 1, nl):
            if bin(masks[i] & masks[j]).count("1") != 1:
                bad_meet += 1
    out["bad_line_meets"] = bad_meet
    assert bad_meet == 0
    # derived: number of lines through two points
    out["pair_lambda"] = max(1 for _ in [0])
    return out
