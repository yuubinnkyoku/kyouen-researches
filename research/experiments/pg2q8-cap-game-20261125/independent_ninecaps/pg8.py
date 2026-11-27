"""Independent core for PG(2,8) verification.

GF(8) = GF(2)[x]/(x^3+x+1); projective points are canonical nonzero vectors
(first nonzero coordinate scaled to 1), sorted lexicographically; board indices
are ranks in that sorted list.

Nothing here reads any other verifier's code.  The board file is treated as the
object under test: it is validated both intrinsically (projective-plane axioms)
and by exact comparison with the coordinate plane built from the field.
"""
import os

BOARD = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "output", "board_pg2q8.txt")

# ---------------------------------------------------------------- GF(8) -----
MOD = 0b1011  # x^3 + x + 1


def gf_mul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if a & 8:
            a ^= MOD
    return r


MUL = tuple(tuple(gf_mul(a, b) for b in range(8)) for a in range(8))
INV = [0] * 8
for _a in range(1, 8):
    for _b in range(1, 8):
        if MUL[_a][_b] == 1:
            INV[_a] = _b


def gf_add(a, b):
    return a ^ b


def gf_neg(a):
    return a


def gf_inv(a):
    assert a != 0
    return INV[a]


def canon(v):
    """Canonical representative of a nonzero vector: first nonzero coord -> 1."""
    for x in v:
        if x:
            i = INV[x]
            return tuple(MUL[c][i] for c in v)
    return None


def _build_points():
    pts = set()
    for a in range(8):
        for b in range(8):
            for c in range(8):
                if a or b or c:
                    pts.add(canon((a, b, c)))
    return sorted(pts)


PTS = _build_points()
assert len(PTS) == 73
PTIDX = {v: i for i, v in enumerate(PTS)}

# The indexing convention claimed in the task: first nonzero coordinate 1,
# lexicographic sort.  Consequences (verified in check_board.py):
#   0            -> (0,0,1)
#   1..8         -> (0,1,c)
#   9+8*y+z      -> (1,y,z)
assert PTS[0] == (0, 0, 1)
for c in range(8):
    assert PTS[1 + c] == (0, 1, c)
for y in range(8):
    for z in range(8):
        assert PTS[9 + 8 * y + z] == (1, y, z)


def vadd(u, v):
    return tuple(a ^ b for a, b in zip(u, v))


def vscale(s, v):
    return tuple(MUL[s][x] for x in v)


def cross(u, v):
    return (MUL[u[1]][v[2]] ^ MUL[u[2]][v[1]],
            MUL[u[2]][v[0]] ^ MUL[u[0]][v[2]],
            MUL[u[0]][v[1]] ^ MUL[u[1]][v[0]])


def dot(u, v):
    return MUL[u[0]][v[0]] ^ MUL[u[1]][v[1]] ^ MUL[u[2]][v[2]]


# ------------------------------------------------------- plane from field --
def build_geo_lines():
    """All 73 lines of PG(2,8) as frozensets of board indices."""
    lines = set()
    for i in range(73):
        for j in range(i + 1, 73):
            n = cross(PTS[i], PTS[j])
            assert n != (0, 0, 0)
            L = frozenset(k for k in range(73) if dot(n, PTS[k]) == 0)
            assert len(L) == 9
            lines.add(L)
    assert len(lines) == 73
    return sorted(lines)


GEO_LINES = build_geo_lines()


# ------------------------------------------------------------- the board ---
def load_board(path=BOARD):
    with open(path, "r") as f:
        toks = f.read().split()
    npts, nlines = int(toks[0]), int(toks[1])
    pos = 2
    lines = []
    while pos < len(toks):
        n = int(toks[pos])
        pts = tuple(int(t) for t in toks[pos + 1:pos + 1 + n])
        pos += 1 + n
        lines.append(pts)
    return npts, nlines, lines


def board_checks(path=BOARD):
    """Intrinsic projective-plane checks plus exact coordinate-plane match."""
    npts, nlines, raw = load_board(path)
    res = {}
    res["header"] = [npts, nlines]
    res["n_lines"] = len(raw)
    res["all_lines_size_9"] = all(len(L) == 9 for L in raw)
    res["all_points_in_range"] = all(0 <= p < 73 for L in raw for p in L)
    res["all_lines_distinct_sets"] = len({frozenset(L) for L in raw}) == len(raw)
    res["all_lines_distinct_points"] = all(len(set(L)) == 9 for L in raw)

    # incidence: every pair of points on exactly one line
    pair_count = {}
    for L in raw:
        for a in range(9):
            for b in range(a + 1, 9):
                key = (min(L[a], L[b]), max(L[a], L[b]))
                pair_count[key] = pair_count.get(key, 0) + 1
    res["n_pairs_covered"] = len(pair_count)
    res["expected_pairs"] = 73 * 72 // 2
    res["every_pair_exactly_once"] = (len(pair_count) == 73 * 72 // 2
                                      and all(v == 1 for v in pair_count.values()))

    # every point on exactly 9 lines
    deg = [0] * 73
    for L in raw:
        for p in L:
            deg[p] += 1
    res["point_degrees"] = sorted(set(deg))
    res["each_point_on_9_lines"] = all(d == 9 for d in deg)

    # exact match with the coordinate plane built from GF(8)
    bset = {frozenset(L) for L in raw}
    gset = set(GEO_LINES)
    res["matches_coordinate_PG28"] = (bset == gset)
    res["lines_only_in_board"] = len(bset - gset)
    res["lines_only_in_geo"] = len(gset - bset)
    return res


class Incidence:
    """Line id / mask structure taken directly from the board file."""

    def __init__(self, path=BOARD):
        npts, nlines, raw = load_board(path)
        assert npts == 73 and len(raw) == 73
        self.board_lines = [frozenset(L) for L in raw]
        self.raw = raw
        self.lof = [[-1] * 73 for _ in range(73)]
        for lid, L in enumerate(self.board_lines):
            Ls = sorted(L)
            for a in range(9):
                for b in range(a + 1, 9):
                    p, q = Ls[a], Ls[b]
                    assert self.lof[p][q] in (-1, lid)
                    self.lof[p][q] = self.lof[q][p] = lid
        for p in range(73):
            for q in range(73):
                if p != q:
                    assert self.lof[p][q] >= 0
            self.lof[p][p] = -1
        self.line_masks = []
        for L in self.board_lines:
            m = 0
            for p in L:
                m |= 1 << p
            self.line_masks.append(m)
        self.ALL = (1 << 73) - 1

    def line_of(self, p, q):
        return self.lof[p][q]

    def cap_mask(self, pts):
        m = 0
        for p in pts:
            m |= 1 << p
        return m

    def is_cap(self, pts):
        """No three of pts collinear."""
        S = list(pts)
        n = len(S)
        for i in range(n):
            p = S[i]
            for j in range(i + 1, n):
                q = S[j]
                L = self.lof[p][q]
                for k in range(n):
                    if k != i and k != j:
                        if self.lof[p][S[k]] == L:
                            return False
        return True

    def blocked_mask(self, pts):
        """Union of all lines meeting pts in >= 2 points."""
        m = 0
        S = list(pts)
        for i in range(len(S)):
            for j in range(i + 1, len(S)):
                m |= self.line_masks[self.lof[S[i]][S[j]]]
        return m


INC = None


def inc():
    global INC
    if INC is None:
        INC = Incidence()
    return INC
