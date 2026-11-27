"""Independent PG(2,9) board utilities (Python stdlib only).

Everything here is written from scratch for the independent verification of the
six-cap claims.  Point sets are Python ints used as 91-bit masks.

Board file format (as produced by the parent experiment):
    first line: "<n> <number_of_lines>"
    then, for every line: "<k> <p1> ... <pk>"  (0-based point labels)

The module provides
  * load_board / Plane.validate_plane  -- projective-plane axiom checks,
  * Plane.addable / is_cap / maximal    -- cap primitives,
  * build_std_pg29                      -- explicit model of PG(2,9) over GF(9),
  * is_isomorphic_to_pg29               -- constructive isomorphism test using a
                                           quadrangle frame closure (this both
                                           proves that the board is PG(2,9) and
                                           produces an explicit point bijection).
"""

from itertools import combinations

BOARD_REL = "../../pg2q9-cap-game-20261125/output/board_pg2q9.txt"


# --------------------------------------------------------------------------
# board loading
# --------------------------------------------------------------------------
def load_board(path):
    with open(path, "r", encoding="utf-8") as fh:
        tok = fh.read().split()
    it = iter(tok)
    n = int(next(it))
    nl = int(next(it))
    lines = []
    for _ in range(nl):
        k = int(next(it))
        pts = [int(next(it)) for _ in range(k)]
        lines.append(pts)
    return n, lines


class Plane:
    def __init__(self, n, lines):
        self.n = n
        self.lines = [list(ln) for ln in lines]
        self.line_pts = [frozenset(ln) for ln in lines]
        self.lmask = [sum(1 << p for p in ln) for ln in self.lines]
        self.lid = [[-1] * n for _ in range(n)]
        for li, ln in enumerate(self.lines):
            for a, b in combinations(ln, 2):
                if self.lid[a][b] != -1:
                    raise AssertionError(
                        "pair %d,%d on lines %d and %d" % (a, b, self.lid[a][b], li))
                self.lid[a][b] = self.lid[b][a] = li
        self.full = (1 << n) - 1
        self.pts = list(range(n))

    # -- incidence ---------------------------------------------------------
    def line_of(self, a, b):
        return self.lid[a][b]

    def validate_plane(self):
        """Return a dict of axiom checks (all must be True / expected values)."""
        n = self.n
        out = {}
        out["n_points"] = n
        out["n_lines"] = len(self.lines)
        out["line_sizes"] = sorted(set(len(ln) for ln in self.lines))
        out["distinct_lines"] = len(set(self.line_pts))
        out["point_degrees"] = sorted(set(
            sum(1 for ln in self.line_pts if p in ln) for p in range(n)))
        out["all_pairs_on_a_line"] = all(
            self.lid[a][b] != -1 for a in range(n) for b in range(a + 1, n))
        out["pair_line_unique"] = True  # enforced in __init__
        # every two lines meet in exactly one point
        mins = set()
        for i, j in combinations(range(len(self.lines)), 2):
            mins.add(len(self.line_pts[i] & self.line_pts[j]))
        out["pairwise_line_intersection_sizes"] = sorted(mins)
        out["line_sizes_all"] = set(len(ln) for ln in self.lines)
        return out

    # -- cap primitives ----------------------------------------------------
    def blocked(self, mask):
        """Union of all secant lines of the point set `mask`."""
        pts = [p for p in range(self.n) if (mask >> p) & 1]
        b = 0
        for a, bb in combinations(pts, 2):
            b |= self.lmask[self.lid[a][bb]]
        return b

    def addable(self, mask):
        """Points q (necessarily outside mask, for |mask| >= 2) with
        mask | (1<<q) still a cap."""
        return self.full & ~self.blocked(mask)

    def is_cap(self, mask):
        pts = [p for p in range(self.n) if (mask >> p) & 1]
        for a, b in combinations(pts, 2):
            if (self.lmask[self.lid[a][b]] & mask).bit_count() != 2:
                return False
        return True

    def maximal(self, mask):
        return self.addable(mask) == 0

    def mask_points(self, mask):
        return [p for p in range(self.n) if (mask >> p) & 1]


# --------------------------------------------------------------------------
# GF(9) = GF(3)[i]/(i^2+1).  Element a + b*i encoded as a + 3*b, a,b in {0,1,2}.
# --------------------------------------------------------------------------
GF_ADD = [[0] * 9 for _ in range(9)]
GF_MUL = [[0] * 9 for _ in range(9)]
for _a in range(3):
    for _b in range(3):
        x = _a + 3 * _b
        for _c in range(3):
            for _d in range(3):
                y = _c + 3 * _d
                GF_ADD[x][y] = ((_a + _c) % 3) + 3 * ((_b + _d) % 3)
                GF_MUL[x][y] = ((_a * _c - _b * _d) % 3) + 3 * ((_a * _d + _b * _c) % 3)
GF_ZERO = 0
GF_ONE = 1
GF_NEG = [0] * 9
for _x in range(9):
    for _y in range(9):
        if GF_ADD[_x][_y] == 0:
            GF_NEG[_x] = _y
            break
GF_INV = [None] * 9
for _x in range(1, 9):
    for _y in range(1, 9):
        if GF_MUL[_x][_y] == GF_ONE:
            GF_INV[_x] = _y
            break
GF_SUB = [[GF_ADD[x][GF_NEG[y]] for y in range(9)] for x in range(9)]


def gf_vec_canon(v):
    """Canonical representative of a nonzero 3-vector up to GF(9)^* scaling."""
    for c in v:
        if c != 0:
            inv = GF_INV[c]
            return tuple(GF_MUL[inv][x] for x in v)
    raise ValueError("zero vector")


def gf_cross(u, v):
    return (
        GF_SUB[GF_MUL[u[1]][v[2]]][GF_MUL[u[2]][v[1]]],
        GF_SUB[GF_MUL[u[2]][v[0]]][GF_MUL[u[0]][v[2]]],
        GF_SUB[GF_MUL[u[0]][v[1]]][GF_MUL[u[1]][v[0]]],
    )


def gf_dot(u, v):
    s = 0
    for i in range(3):
        s = GF_ADD[s][GF_MUL[u[i]][v[i]]]
    return s


class StdPG29:
    """The Desarguesian plane PG(2,9) with explicit GF(9) coordinates."""

    def __init__(self):
        pts = set()
        for x in range(9):
            for y in range(9):
                for z in range(9):
                    if x == 0 and y == 0 and z == 0:
                        continue
                    pts.add(gf_vec_canon((x, y, z)))
        self.points = sorted(pts)
        self.index = {p: i for i, p in enumerate(self.points)}
        assert len(self.points) == 91
        # lines: nonzero normals up to scalar; line = points p with n . p = 0
        normals = set()
        for x in range(9):
            for y in range(9):
                for z in range(9):
                    if x == 0 and y == 0 and z == 0:
                        continue
                    normals.add(gf_vec_canon((x, y, z)))
        self.normals = sorted(normals)
        assert len(self.normals) == 91
        self.lines = []
        for nrm in self.normals:
            pts_on = frozenset(self.index[p] for p in self.points if gf_dot(nrm, p) == 0)
            assert len(pts_on) == 10
            self.lines.append(pts_on)
        self.line_index = {ln: i for i, ln in enumerate(self.lines)}
        # pair -> line
        self.lid = [[-1] * 91 for _ in range(91)]
        for li, ln in enumerate(self.lines):
            for a, b in combinations(sorted(ln), 2):
                assert self.lid[a][b] == -1
                self.lid[a][b] = self.lid[b][a] = li
        self.full = (1 << 91) - 1

    def line_of(self, a, b):
        return self.lid[a][b]

    def check(self):
        return {
            "points": len(self.points),
            "lines": len(self.lines),
            "line_sizes": sorted(set(len(ln) for ln in self.lines)),
            "pairs_covered": all(self.lid[a][b] != -1
                                 for a in range(91) for b in range(a + 1, 91)),
        }


def build_std_pg29():
    return StdPG29()


def _std_points_on_line(std, a, b):
    return std.lines[std.lid[a][b]]


# --------------------------------------------------------------------------
# constructive isomorphism test via quadrangle frame closure
# --------------------------------------------------------------------------
def _find_quadrangle(plane):
    n = plane.n
    b1, b2 = 0, 1
    L = plane.line_pts[plane.lid[b1][b2]]
    b3 = next(p for p in range(n) if p not in L)
    bad = set(L) | set(plane.line_pts[plane.lid[b1][b3]]) | set(
        plane.line_pts[plane.lid[b2][b3]])
    b4 = next(p for p in range(n) if p not in bad)
    return [b1, b2, b3, b4]


def _close_frame(plane, std, pmap, lmap, max_rounds=100):
    """Propagate the forced point/line images to a fixed point.

    Returns (status, info) where status is "ok", "conflict" or "stall".
    """
    rounds = 0
    while rounds < max_rounds:
        rounds += 1
        changed = False
        # 1. lines through two mapped points are forced
        for a, b in combinations(list(pmap.keys()), 2):
            lb = plane.lid[a][b]
            ls = std.lid[pmap[a]][pmap[b]]
            if lb in lmap:
                if lmap[lb] != ls:
                    return "conflict", {"error": "line conflict", "round": rounds}
            else:
                lmap[lb] = ls
                changed = True
        # 2. points that are intersections of two mapped lines are forced
        for l1, l2 in combinations(list(lmap.keys()), 2):
            pb = plane.line_pts[l1] & plane.line_pts[l2]
            ps = std.lines[lmap[l1]] & std.lines[lmap[l2]]
            if len(pb) != 1 or len(ps) != 1:
                return "conflict", {"error": "degenerate intersection",
                                    "round": rounds}
            pb = next(iter(pb))
            ps = next(iter(ps))
            if pb in pmap:
                if pmap[pb] != ps:
                    return "conflict", {"error": "point conflict",
                                        "round": rounds}
            else:
                pmap[pb] = ps
                changed = True
        if not changed:
            return "stall", {"rounds": rounds,
                             "points_mapped": len(pmap),
                             "lines_mapped": len(lmap)}
    return "stall", {"rounds": rounds, "points_mapped": len(pmap),
                     "lines_mapped": len(lmap)}


def is_isomorphic_to_pg29(plane, verbose=False):
    """Construct an explicit incidence isomorphism plane -> PG(2,9).

    A projective plane isomorphism is an incidence bijection.  PGL(3,9) is
    sharply 4-transitive on ordered quadrangles, so an isomorphism is
    determined by the image of one quadrangle, and both the image of a line
    through two mapped points and the image of the intersection of two mapped
    lines are forced.  Iterating this closure from a quadrangle yields the
    PG(2,3) subplane (13 points/13 lines).  To reach the full PG(2,9) we then
    guess the image of one further point outside that subplane (78 choices)
    and re-run the closure; for the (at most two) correct choices -- the
    identity and the Frobenius twist -- the closure covers all 91 points and
    91 lines, and the resulting bijection is checked against every incidence.
    An explicit isomorphism is a proof that the board is PG(2,9).
    """
    std = build_std_pg29()
    if std.check() != {"points": 91, "lines": 91, "line_sizes": [10],
                       "pairs_covered": True}:
        return False, {}, "standard model construction failed"

    s1 = std.index[(1, 0, 0)]
    s2 = std.index[(0, 1, 0)]
    s3 = std.index[(0, 0, 1)]
    s4 = std.index[(1, 1, 1)]
    sq = [s1, s2, s3, s4]

    bq = _find_quadrangle(plane)
    for i, j, k in combinations(range(4), 3):
        if plane.lid[bq[i]][bq[j]] == plane.lid[bq[i]][bq[k]] == plane.lid[bq[j]][bq[k]]:
            return False, {}, "board quadrangle degenerate"
        if (std.lid[sq[i]][sq[j]] == std.lid[sq[i]][sq[k]]
                == std.lid[sq[j]][sq[k]]):
            return False, {}, "standard quadrangle degenerate"

    base_pmap = {bq[i]: sq[i] for i in range(4)}
    base_lmap = {}
    for i, j in combinations(range(4), 2):
        base_lmap[plane.lid[bq[i]][bq[j]]] = std.lid[sq[i]][sq[j]]

    status, info = _close_frame(plane, std, dict(base_pmap), dict(base_lmap))
    info["subplane_closure"] = status
    if status == "conflict":
        return False, info, "inconsistent PG(2,3) subplane closure"
    if len(base_pmap) == 91 and len(base_lmap) == 91:
        # already complete (not expected, but then the frame alone suffices)
        candidates = []
    else:
        # the closure stabilised on the prime-field subplane; choose one more
        # point P outside it and try all possible images outside the image.
        pmap, lmap = dict(base_pmap), dict(base_lmap)
        # remember the full subplane closure (not just base_pmap)
        status, sub_info = _close_frame(plane, std, pmap, lmap)
        info["subplane_points"] = len(pmap)
        info["subplane_lines"] = len(lmap)
        if status != "stall":
            return False, info, "unexpected subplane closure status"
        P = next(p for p in range(91) if p not in pmap)
        used = set(pmap.values())
        candidates = [q for q in range(91) if q not in used]
        info["extra_point"] = P
        info["candidate_images"] = len(candidates)
        base_pmap, base_lmap = pmap, lmap

    attempts = 0
    for Q in candidates:
        attempts += 1
        pmap = dict(base_pmap)
        lmap = dict(base_lmap)
        if Q in pmap.values():
            continue
        pmap[P] = Q
        status, info2 = _close_frame(plane, std, pmap, lmap)
        if status != "stall":
            continue
        if len(pmap) != 91 or len(lmap) != 91:
            continue
        if len(set(pmap.values())) != 91:
            continue
        ok = True
        for lb, ls in lmap.items():
            if frozenset(pmap[p] for p in plane.line_pts[lb]) != std.lines[ls]:
                ok = False
                break
        if ok:
            info.update({
                "attempts": attempts,
                "extra_point": P,
                "extra_point_image": Q,
                "points_mapped": len(pmap),
                "lines_mapped": len(lmap),
                "isomorphism_ok": True,
            })
            return True, info, ""
    info["attempts"] = attempts
    return False, info, "no consistent completion found"
